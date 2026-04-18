"""
Tests RAG avancé — reranking, contextual retrieval, FTS tsv.
Fonctions utilitaires testées unitairement, services mockés.
"""

import pytest
from unittest.mock import MagicMock, patch


class TestRRFFusion:
    def test_basic_fusion(self):
        from core.services.rag_service import _rrf_fusion

        semantic = [
            {"chunk_id": "A", "document_id": "d1", "contenu": "texte A", "meta": {}, "score": 0.9},
            {"chunk_id": "B", "document_id": "d1", "contenu": "texte B", "meta": {}, "score": 0.8},
        ]
        fts = [
            {"chunk_id": "B", "document_id": "d1", "contenu": "texte B", "meta": {}, "score": 0.5},
            {"chunk_id": "C", "document_id": "d1", "contenu": "texte C", "meta": {}, "score": 0.3},
        ]

        results = _rrf_fusion(semantic, fts, top_k=3)
        assert len(results) == 3
        # B apparaît dans les deux -> score RRF le plus élevé
        assert results[0]["chunk_id"] == "B"
        assert results[0]["score_type"] == "rrf"

    def test_empty_inputs(self):
        from core.services.rag_service import _rrf_fusion

        results = _rrf_fusion([], [], top_k=5)
        assert results == []

    def test_top_k_limits(self):
        from core.services.rag_service import _rrf_fusion

        hits = [
            {"chunk_id": f"C{i}", "document_id": "d1", "contenu": f"texte {i}", "meta": {}, "score": 0.5}
            for i in range(10)
        ]
        results = _rrf_fusion(hits, [], top_k=3)
        assert len(results) == 3


class TestRerank:
    def test_rerank_disabled_returns_unchanged(self):
        from core.services.rag_service import _rerank

        hits = [
            {"chunk_id": "A", "contenu": "premier", "score": 0.5},
            {"chunk_id": "B", "contenu": "second", "score": 0.3},
        ]
        with patch("core.services.rag_service.settings") as mock_settings:
            mock_settings.RERANK_ENABLED = False
            result = _rerank("query", hits, top_k=2)
        assert result == hits

    def test_rerank_empty_hits(self):
        from core.services.rag_service import _rerank

        with patch("core.services.rag_service.settings") as mock_settings:
            mock_settings.RERANK_ENABLED = True
            result = _rerank("query", [], top_k=5)
        assert result == []

    def test_rerank_single_hit(self):
        from core.services.rag_service import _rerank

        hits = [{"chunk_id": "A", "contenu": "seul", "score": 0.5}]
        with patch("core.services.rag_service.settings") as mock_settings:
            mock_settings.RERANK_ENABLED = True
            result = _rerank("query", hits, top_k=5)
        assert result == hits

    def test_rerank_graceful_import_error(self):
        """Si sentence-transformers n'est pas installé, fallback sans crash."""
        from core.services.rag_service import _rerank

        hits = [
            {"chunk_id": "A", "contenu": "premier", "score": 0.5},
            {"chunk_id": "B", "contenu": "second", "score": 0.3},
        ]
        with patch("core.services.rag_service.settings") as mock_settings:
            mock_settings.RERANK_ENABLED = True
            # Force ImportError sur sentence_transformers
            with patch.dict("sys.modules", {"sentence_transformers": None}):
                import importlib

                # _rerank devrait attraper ImportError et retourner les hits
                result = _rerank("test query", hits, top_k=2)
        assert len(result) == 2


class TestFTSSanitization:
    def test_sanitize_special_chars(self):
        """Les caractères spéciaux sont nettoyés pour plainto_tsquery."""
        import re

        query = "béton @armé! article:12.3 (DTU)"
        sanitized = re.sub(r"[^\w\s\-àâäéèêëïîôùûüÿçœæ]", " ", query)
        sanitized = " ".join(sanitized.split())
        assert "@" not in sanitized
        assert "!" not in sanitized
        assert ":" not in sanitized
        assert "béton" in sanitized
        assert "armé" in sanitized
        assert "DTU" in sanitized

    def test_sanitize_empty_returns_clean(self):
        import re

        query = "@!#$%"
        sanitized = re.sub(r"[^\w\s\-àâäéèêëïîôùûüÿçœæ]", " ", query)
        sanitized = " ".join(sanitized.split())
        assert sanitized.strip() == ""


class TestChunkConfig:
    def test_cctp_uses_window_parser(self):
        from core.services.rag_service import _WINDOW_TYPES, CHUNK_CONFIG

        assert "cctp" in _WINDOW_TYPES
        assert CHUNK_CONFIG["cctp"]["chunk_size"] == 512

    def test_email_has_small_chunks(self):
        from core.services.rag_service import CHUNK_CONFIG

        assert CHUNK_CONFIG["email"]["chunk_size"] == 128

    def test_default_chunk_config(self):
        from core.services.rag_service import DEFAULT_CHUNK

        assert DEFAULT_CHUNK["chunk_size"] == 256
        assert DEFAULT_CHUNK["chunk_overlap"] == 32
