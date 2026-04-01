#!/usr/bin/env bash
# scripts/openclaude-setup.sh
# Configure OpenClaude pour utiliser l'Ollama local d'ARCEUS.
#
# Usage :
#   source scripts/openclaude-setup.sh              # modèle par défaut (qwen2.5-coder:14b)
#   source scripts/openclaude-setup.sh deepseek-coder-v2:16b
#
# Prérequis :
#   npm install -g @gitlawb/openclaude
#   docker compose up -d ollama
#   docker compose exec ollama ollama pull qwen2.5-coder:14b

set -e

MODEL="${1:-qwen2.5-coder:14b}"
OLLAMA_URL="${OLLAMA_URL:-http://localhost:11434}"

# Vérifier qu'Ollama répond
if ! curl -sf "${OLLAMA_URL}/api/tags" > /dev/null 2>&1; then
  echo "[openclaude-setup] ⚠  Ollama inaccessible sur ${OLLAMA_URL}"
  echo "                      Démarre la stack : docker compose up -d ollama"
  return 1 2>/dev/null || exit 1
fi

# Vérifier que le modèle est disponible localement
if ! curl -sf "${OLLAMA_URL}/api/tags" | grep -q "\"${MODEL}\""; then
  echo "[openclaude-setup] ℹ  Modèle '${MODEL}' non trouvé, pull en cours…"
  docker compose exec ollama ollama pull "${MODEL}"
fi

export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_API_BASE_URL="${OLLAMA_URL}/v1"
export OPENAI_API_KEY="ollama"
export OPENAI_MODEL="${MODEL}"

echo "[openclaude-setup] ✓ OpenClaude configuré"
echo "  URL    : ${OPENAI_API_BASE_URL}"
echo "  Modèle : ${OPENAI_MODEL}"
echo ""
echo "  Lance 'openclaude' pour démarrer."
