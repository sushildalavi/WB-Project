# Coding instrument

This document mirrors **Appendix B (theme taxonomies)** and **Appendix F
(sentiment and emotion definitions)** of the WB MIP Social Listening Report.
Every comment in the focused-coded subsets receives multi-label theme tags,
a 3-class sentiment label, and an emotion tag.

Theme taxonomies are **closed-set** and **per-country** — Nigeria, India, and
Kenya each have their own list because the discourse genres differ. A
comment may receive multiple theme labels.

## Theme taxonomy — Nigeria (BBNaija S9, Nairaland)

| # | Theme | Definition |
|---|-------|------------|
| 1 | Participation, Competition, and Influence | Voting strength, fan bases, influence in the house, strategy, evictions, alliances. |
| 2 | Marriage, Relationships, and Loyalty Norms | Romantic pairings, loyalty, "ship" dynamics, marriage expectations, jealousy, fidelity. |
| 3 | Sexuality and Respectability Policing | Policing of women's sexual behavior, dress, perceived promiscuity, decency, sexual double standards. |
| 4 | Sexist or Derogatory Language | Gendered insults, slurs, sexualized name-calling, humiliation. |
| 5 | Conflict, Insults, and Humiliation Dynamics | Audience reactions to fights, insults, bullying, dragging, public embarrassment. |
| 6 | Moral Judgment and Character Evaluation | Character labeling ("liar", "wicked"), deservingness framing, real-world moral consequence talk. |
| 7 | Gender Norms and Gender Double Standards | Explicit or implicit references to gendered expectations and double standards, including stereotyping. |
| 8 | Emotional Expression | Strong affect (anger, contempt, ridicule, disgust, mockery, sympathy) shaping evaluation. |
| 9 | Behavioral Responses and Engagement | Calls to action and participation behaviors (urging others to vote, evict, support). |

## Theme taxonomy — India (Made in Heaven S2, YouTube)

| # | Theme | Definition |
|---|-------|------------|
| 1 | India Local Culture | Culture-specific framing of norms and identity ("society" talk, tradition vs modernity, language). |
| 2 | Gender Norms & Dynamics | General gender roles and expectations, patriarchy, marriage-role expectations, double standards. |
| 3 | Gender-Based Violence | Discussion of coercion, emotional abuse, physical abuse, threats, harm. |
| 4 | Economic Empowerment | Women's financial independence, work, career, "gold digger" framing. |
| 5 | Caste / Intersectionality | Caste, caste-coded respectability, privilege/exclusion, identity-based hierarchy. |
| 6 | Body & Beauty Standards | Body policing, colorism, attractiveness, appearance-based judgment. |

## Theme taxonomy — Kenya (RHONairobi, X/Twitter)

| # | Theme | Definition |
|---|-------|------------|
| 1 | Respectability, Morality, and Social Status | Class and status performance, "classy" vs "vulgar", legitimacy in elite space, taste, etiquette. |
| 2 | Conflict, Insults, and Social Sanctioning | Episode-driven conflict framing, name-calling, social punishment, audience-as-arbiter dynamics. |
| 3 | Sexuality, Body Politics, and Respectability Policing | Sexualized evaluation, body-focused commentary as legitimacy test, dress policing. |
| 4 | Sexist or Derogatory Language | Explicit misogynistic or gendered slurs, degrading labels (distinct from general insults). |
| 5 | Marriage, Relationships, and Intimate Power | Husbands, marriages, relationship power, dependency, loyalty. |
| 6 | Gender Norms, Femininity, and Masculinity Ideals | Explicit talk about womanhood, "pro-women" identity claims, femininity/masculinity expectations. |
| 7 | Cultural, Religious, and Ethnic Framing | Identity cues and cultural markers (language, tribe/ethnicity, religion). |
| 8 | Emotional Expression | Strong affect (love, hate, disgust, anger, praise, mockery) framing evaluation. |
| 9 | Behavioral Responses and Discursive Positioning | Direct prescriptions (remove cast, cancel) plus stance-taking. |

## Sentiment categories

3-class scheme applied uniformly across countries.

- **Positive** — approval, support, admiration, endorsement. Includes praise of a character, validation of a gender stance, or affirmation of empowerment, resilience, or fairness. May still include critique, but the dominant tone is supportive.
- **Neutral** — descriptive, interpretive, or observational. Summaries, motivation explanations, clarifying questions, or ambivalence without endorsing or condemning.
- **Negative** — disapproval, condemnation, ridicule, anger, disgust, moral sanctioning. May include shaming, insults, punitive judgment, or strong rejection of a behavior, character, or norm.

> Negative sentiment does *not* automatically indicate opposition to gender
> equality — in several Indian comments, negativity was directed at *harmful
> norms themselves* rather than at women.

## Emotion categories

Used to capture affective intensity beyond sentiment alone. Coded for the
dominant emotion expressed in each comment.

| Emotion | Definition |
|---------|------------|
| Anger | Irritation, outrage, hostility, moral fury. Often accompanies punitive judgment; escalatory. |
| Contempt / Disgust | Scorn, derision, revulsion. Signals moral superiority or social distancing; closely tied to reputational sanctioning. |
| Shame / Embarrassment | Discomfort, awkwardness, second-hand embarrassment — at characters or at the norms portrayed. |
| Sadness / Distress | Sorrow, empathy, emotional heaviness in response to harm, loss, injustice. Most often directed at conditions or structures, not individuals. |
| Encouragement / Support | Hope, pride, admiration, reassurance — toward a character or gender-progressive behavior. Typically co-occurs with positive sentiment. |

## How sentiment + emotion + theme combine

The analytic move is to look at **theme × sentiment** distributions to find
"rejection zones" — themes consistently negative-skewed mark portrayals the
audience finds *less acceptable*. Themes with neutral/positive sentiment
mark portrayals that are *relatively more acceptable*.

This is what the heatmaps in the report's Appendix G visualize.

## Codebook versions in this repo

| File | Codebook | Notes |
|------|----------|-------|
| [`data/human_coded/india/MIH_S2_human_coding_dataset.xlsx`](../data/human_coded/india/MIH_S2_human_coding_dataset.xlsx) | v2 (current) | 114 rows, gold pilot |
| [`data/human_coded/kenya/RHONairobi_human_coding_dataset.csv`](../data/human_coded/kenya/RHONairobi_human_coding_dataset.csv) | v2 (current) | 115 rows, gold pilot |
| [`data/human_coded/nigeria/BBNaija_human_coding_dataset.xlsx`](../data/human_coded/nigeria/BBNaija_human_coding_dataset.xlsx) | v2 (current) | 100 rows |
| [`data/human_coded/india/MIH_S2_human_coding_extended.xlsx`](../data/human_coded/india/MIH_S2_human_coding_extended.xlsx) | v1 (legacy) | 951 rows, working extension; not part of pilot |

Differences between v1 and v2:
- v2 adds: collective/individual framing, contest/reproduce stereotypes, tribe/caste in the ethnicity question.
- v1 has whitespace/newline noise in some column headers (loaders strip these at load time).
