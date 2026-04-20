"""
OcrService — OCR fallback via GLM-4V (Zhipu AI) ou endpoint compatible OpenAI vision.

Déclenché par RagService.ingest() quand le texte natif extrait est trop court
(< settings.GLM_OCR_MIN_CHARS). Accepte PDF ou image, retourne texte + métadonnées.

Protocole endpoint (OpenAI-compatible /chat/completions) :
  Requête : JSON chat completions avec image base64 (content type image_url)
  Réponse : texte extrait dans choices[0].message.content

Pour PDF multi-pages : rendu via PyMuPDF (fitz) page par page → concaténation.
Fallback silencieux si fitz non disponible → tentative image directe.
"""

import base64
import io
from pathlib import Path
from typing import Optional

import httpx

from core.logging import get_logger
from core.settings import settings

log = get_logger("ocr_service")

_OCR_PROMPT = (
    "Extrais intégralement le texte de cette image en préservant la mise en page "
    "(colonnes, tableaux, listes). Retourne uniquement le texte brut sans commentaire, "
    "sans balise Markdown."
)

_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp", ".webp"}


def _is_image(filename: str) -> bool:
    return Path(filename).suffix.lower() in _IMAGE_SUFFIXES


def _is_pdf(filename: str) -> bool:
    return Path(filename).suffix.lower() == ".pdf"


def _pdf_to_images(file_bytes: bytes, dpi: int = 150) -> list[bytes]:
    """Convertit un PDF en liste d'images JPEG via PyMuPDF. Retourne [] si indisponible."""
    try:
        import fitz  # PyMuPDF

        doc = fitz.open(stream=file_bytes, filetype="pdf")
        images = []
        for page in doc:
            mat = fitz.Matrix(dpi / 72, dpi / 72)
            pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
            images.append(pix.tobytes("jpeg"))
        doc.close()
        return images
    except ImportError:
        log.debug("ocr.fitz_unavailable")
        return []
    except Exception as exc:
        log.warning("ocr.pdf_render_failed", error=str(exc))
        return []


def _image_to_b64(image_bytes: bytes, mime: str = "image/jpeg") -> str:
    b64 = base64.b64encode(image_bytes).decode()
    return f"data:{mime};base64,{b64}"


def _mime_from_filename(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    return {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".tiff": "image/tiff",
        ".tif": "image/tiff",
        ".bmp": "image/bmp",
        ".webp": "image/webp",
    }.get(suffix, "image/jpeg")


async def _call_vision(image_data_url: str, client: httpx.AsyncClient, endpoint: str) -> str:
    """Un appel vision → texte extrait."""
    headers = {"Content-Type": "application/json"}
    if settings.GLM_OCR_API_KEY:
        headers["Authorization"] = f"Bearer {settings.GLM_OCR_API_KEY}"

    payload = {
        "model": settings.GLM_OCR_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_data_url}},
                    {"type": "text", "text": _OCR_PROMPT},
                ],
            }
        ],
        "temperature": 0.0,
        "max_tokens": 4096,
    }
    resp = await client.post(
        f"{endpoint.rstrip('/')}/chat/completions",
        json=payload,
        headers=headers,
        timeout=60.0,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"] or ""


class OcrService:
    """OCR fallback via GLM-4V ou tout endpoint OpenAI-compatible vision."""

    @staticmethod
    async def extract_text(
        file_bytes: bytes,
        filename: str,
        mime_type: Optional[str] = None,
    ) -> dict:
        """
        Extrait le texte d'un fichier via OCR.

        Retourne :
          {
            "text": str,
            "confidence": float,      # 1.0 si succès (GLM ne retourne pas de score)
            "layout_blocks_count": int,
            "extraction_mode": "ocr",
            "ocr_provider": "glm-4v" | "glm-4v-flash" | ...,
          }
        Lève RuntimeError si l'endpoint n'est pas configuré.
        Lève httpx.HTTPError en cas d'échec réseau/HTTP.
        """
        endpoint = settings.GLM_OCR_ENDPOINT
        if not endpoint:
            raise RuntimeError("GLM_OCR_ENDPOINT non configuré")

        pages_text: list[str] = []

        async with httpx.AsyncClient() as client:
            if _is_pdf(filename):
                images = _pdf_to_images(file_bytes)
                if images:
                    for img_bytes in images:
                        data_url = _image_to_b64(img_bytes, "image/jpeg")
                        page_text = await _call_vision(data_url, client, endpoint)
                        pages_text.append(page_text)
                else:
                    # fitz non dispo : tenter envoi PDF direct si endpoint le supporte
                    b64 = base64.b64encode(file_bytes).decode()
                    data_url = f"data:application/pdf;base64,{b64}"
                    pages_text.append(await _call_vision(data_url, client, endpoint))
            else:
                mime = mime_type or _mime_from_filename(filename)
                data_url = _image_to_b64(file_bytes, mime)
                pages_text.append(await _call_vision(data_url, client, endpoint))

        full_text = "\n\n".join(p for p in pages_text if p.strip())
        # Heuristique sur les blocs : nombre de paragraphes non vides
        layout_blocks = sum(1 for line in full_text.splitlines() if line.strip())

        log.info(
            "ocr.extracted",
            filename=filename,
            pages=len(pages_text),
            chars=len(full_text),
            layout_blocks=layout_blocks,
        )
        return {
            "text": full_text,
            "confidence": 1.0,
            "layout_blocks_count": layout_blocks,
            "extraction_mode": "ocr",
            "ocr_provider": settings.GLM_OCR_MODEL,
        }
