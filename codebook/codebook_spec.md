# Human-coding instrument

This is the WB instrument used to code social-media comments by hand. It is
the ground-truth schema that LLM coding is benchmarked against. Two versions
exist in the data — list both for traceability.

## v2 (current — used for BBNaija, RHONairobi, India v2)

For each comment, code the following fields. Numeric scales are listed.

### Identification
- `Comment ID`
- `Comment Text`

### Top-level labels
- `Themes` — free-text or list (e.g. `["Marriage/Husband-Wife", "Money/Prize/Votes"]`)
- `Sentiment` — Positive / Neutral / Negative / Mixed / Unclear
- `Emotion Detection` — primary emotion(s)
- `Tone` — descriptor

### Media reference
- Mentions specific media content? `0=No, 1=Yes`
  - If Y: what content?
  - If Y: attitude toward media content? `1=Pos / 2=Neu / 3=Neg / 4=Mixed / 5=Unclear`
    - If positive: what does the author like?
    - If negative: what does the author dislike?

### Gender
- Mentions gender or gender roles? `0/1`
  - If Y: characterize the gender role(s):
    - `1` Women do domestic/care work
    - `2` Women have limited economic freedom
    - `3` Women have limited leadership
    - `4` Women are in subservient roles
    - `5` Women do not discuss sex / reproductive health
    - `5` Men are sexual aggressors *(note: original codebook has duplicate `5`)*
    - `6` Men are leaders
    - `7` Men are violent
    - `8` Men are primary breadwinners
  - If Y: free-text — other gender themes
  - If Y: attitude toward gender norms `1–5`
  - If Y: attitude toward women `1–5`
  - If Y: framing — `1=Collective, 2=Individual, 3=Can't tell/N/A`
  - If Y: contests or reproduces stereotypes? `0=Contest, 1=Reproduce, 3=Unclear`

### Race / ethnicity / caste / tribe / language
- Mentions race/ethnicity/nationality/tribe/caste/language re: media? `0/1`
  - If Y: which?
  - If Y: attitude `1–5`

### Sexism
- Includes sexist or derogatory language? `0/1`
  - If Y: provide a quote

### Emotions (Ekman+)
- Comment-level emotions: `1=Contempt, 2=Anger, 3=Disgust, 4=Sadness, 5=Shame, 6=Embarrassment, 7=Guilt, 8=Compassion, 9=Pride, 10=No emotion`
- Author's emotions toward media content: same scale

### Knowledge effects
- Indicates new knowledge acquired? `0/1` — if Y, what?
- Indicates existing knowledge reinforced? `0/1` — if Y, what?

### LLM ground-truth comparison
- LLM emotion output (string)
- LLM emotion confidence (float)
- "How accurate is this output?" `0=Inaccurate, 1=Accurate`
  - If inaccurate: which emotions are accurate / inaccurate / missing

---

## v1 (legacy — used for older MIH_S2 and RHON YT&X human-coding files in `archive/`)

Same questions, with these differences:
- No collective/individual framing field
- No contest/reproduce stereotypes field
- No tribe / caste in the ethnicity question (Kenya/India only)
- Column headers contain newlines and tabs (e.g. `'\n         \nDoes the comment include any sexist or derogatory language?'`) — strip when loading
- Some duplicate-question columns appear with `.1` suffixes after `pd.read_excel`

When working with archive files, normalize columns first:
```python
df.columns = (
    df.columns.astype(str)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)
```
