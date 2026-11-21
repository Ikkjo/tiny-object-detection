# Aerial dataset

Research for choosing the project's **aerial dataset**: drone or satellite imagery with tiny objects. It is one of the three
datasets we use, next to the [reference benchmark](reference-benchmark.md) and the [ground-level dataset](ground-level-dataset.md). Part of issue #1 (Select
datasets for tiny object detection).

**Nominee:** <!-- dataset name, once decided --> · **Runner-up:** <!-- dataset name -->

Status: not started. Use [reference-benchmark.md](reference-benchmark.md) as a
filled-in example.

Conventions: every number has a source in section 7. Mark anything not checked
against a primary source as **TBD**, and numbers you worked out yourself as
*(est.)*. State which definition of "tiny" a number uses (COCO small is under
32×32 px, AI-TOD tiny is under 16×16 px).

How much detail each dataset needs (from issue #1):

- **Nominee and runner-up:** every field in the full table below. The runner-up
  must be complete enough to switch to without new research.
- **Other contenders (3–5 shortlisted in total):** identity, size, a sourced
  value for each criterion, and why it was not chosen.
- **Ruled out early:** one line each.

Any criterion given as a reason for rejecting a dataset must be backed by a
sourced fact.

## 1. What this dataset is for

<!-- What job does this dataset do in the project? Turn that into the criteria
used to compare contenders, and say why each one matters. Start from the
selection criteria in issue #1. -->

| # | Criterion | Why it matters for us | Weight |
|---|---|---|---|
| C1 |  |  |  |

## 2. Contenders

<!-- Starting points: AI-TOD / AI-TOD-v2, VisDrone (the mentor's suggestion), DOTA, xView, SODA-A, the mentor's satellite-video dataset -->

### 2.1 Nominee: <!-- dataset name -->

<!-- One sentence: what it is. -->

| Property | Value | Source |
|---|---|---|
| Domain, year |  |  |
| Paper / download link |  |  |
| Images (per split) |  |  |
| Instances |  |  |
| Classes |  |  |
| Share of objects under 16 px / under 32 px |  |  |
| Image resolution / size on disk |  |  |
| Annotation format |  |  |
| Licence and access |  |  |
| Evaluation metric |  |  |
| Published baselines (CenterNet?) |  |  |
| How often used in the papers found |  |  |

**Strengths:**

**Weaknesses:**

### 2.2 Runner-up: <!-- dataset name -->

<!-- Same full table as the nominee. -->

### 2.3 Other contenders

<!-- One block per dataset. -->

#### <!-- Dataset name -->

| Property | Value | Source |
|---|---|---|
| Domain, year, paper link |  |  |
| Images / classes |  |  |
| <!-- one row per criterion from section 1 --> |  |  |

**Why not chosen:** <!-- 1–2 sentences naming the criteria it fails -->

## 3. Comparison

✅ = meets the criterion, ⚠️ = partly, ❌ = does not, ❓ = unknown.

| Criterion | Nominee | Runner-up | Contender 3 |
|---|---|---|---|
| C1 |  |  |  |

## 4. Decision

<!-- Why the nominee wins (tied to the criteria), why the runner-up is second,
why not each of the others, known limitations and how we handle them, and what
would change the decision. -->

## 5. Ruled out early

| Dataset | Domain | Link | Why dropped |
|---|---|---|---|
|  |  |  |  |

## 6. Open items

- [ ] <!-- Facts still to check -->

## 7. Sources

- [S1] <!-- Title — link -->
