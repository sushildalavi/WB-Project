"""LLM and embedding model configuration.

Two tiers, matching the report's documented setup (Appendix C7) and the
actual notebook implementation:

  * `OPENAI_MODEL` (gpt-5.1) — the production labeling model. Used for the
    substantive classification tasks the report attributes to gpt-5.1:
    theme tagging, 3-class sentiment, emotion detection, and sexism flags.

  * `OPENAI_MODEL_LIGHT` (gpt-4o-mini) — used for cheap auxiliary tasks
    that do not appear as primary outputs in the report:
    language tagging (English / Hindi / Hinglish / Swahili / Sheng),
    API health checks, and coarse pre-filtering before semantic rerank.
"""

OPENAI_MODEL = "gpt-5.1"                  # production labeling
OPENAI_MODEL_LIGHT = "gpt-4o-mini"        # auxiliary lightweight tasks
LLM_TEMPERATURE = 0                       # deterministic
EMBEDDING_MODEL = "text-embedding-3-large"  # 3072-dim, semantic rerank

# Used when serializing run manifests alongside outputs.
RUN_MANIFEST_FIELDS = (
    "model",
    "temperature",
    "taxonomy_version",
    "timestamp",
    "batch_size",
)
