"""LLM and embedding model configuration.

Single source of truth for the OpenAI models used across the pipeline.
Matches Appendix C7 of the WB MIP Social Listening report.
"""

OPENAI_MODEL = "gpt-5.1"          # thematic + sentiment + emotion classifier
LLM_TEMPERATURE = 0               # deterministic
EMBEDDING_MODEL = "text-embedding-3-large"  # 3072-dim, used for semantic rerank

# Used when serializing run manifests alongside outputs.
RUN_MANIFEST_FIELDS = (
    "model",
    "temperature",
    "taxonomy_version",
    "timestamp",
    "batch_size",
)
