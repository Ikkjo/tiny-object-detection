# CLAUDE.md – Tiny Object Detection

Shared context for everyone working in this repo, and for Claude. Keep it up
to date when decisions change.

## What the project is

A research project on **tiny / small object detection**: how well existing
object detectors handle objects only a few pixels across, and how to improve
them.

The research so far has focused on point-based detectors (CornerNet,
CenterNet) as a starting point. The project is
**not limited to them**: any type of detector can be researched, benchmarked or
improved, including two-stage, one-stage, anchor-free and transformer-based ones.

We approach it like a research paper, methodically:

1. **Understand.** Know how detection evolved (sliding window → two-stage →
   single-stage → point-based). Know CornerNet and CenterNet in depth,
   especially their loss functions.
2. **Benchmark.** Run existing detectors of different types as baselines, on
   all three datasets (see Datasets).
3. **Improve existing detectors.** Change the formulation without retraining
   from scratch: loss, label assignment, output-resolution mapping, multi-scale,
   backbone.
4. **Train partially.** Fine-tune by unfreezing part of a pretrained detector,
   or add a new module or network on top of an existing one.
5. **Train a new model.** This is the last resort, only if the earlier steps show
   a clear reason it would help.

The final result is one of two outcomes, still to be decided:

- **A. Survey and benchmark.** Evaluate and analyse a set of models, then
  recommend the best ones for different tiny-object tasks.
- **B. Survey plus a new method.** Do A, then propose an improvement to an
  existing detector or a new architecture.

## Guiding principle

For every design choice in a paper, ask **why it was done that way** and
**whether it still makes sense for tiny objects**. The loss function, meaning
what each term does and why it exists, matters more than the code.

Reading checklist for each core paper:

- What does the network output (heatmaps, offsets, sizes, embeddings), and at
  what resolution?
- What is the full loss: every term, its weight, and the error it penalises?
- Why is each term needed, and what would break without it?
- What happens to that term when the object is only a few pixels wide?
- How are predictions mapped from the low-res output back to image pixels?

## Research directions under consideration

These are framed around CenterNet, but most apply to other detectors too:

1. **Loss and label assignment.** CenterNet has a single positive pixel per
   object, so the negative term dominates. Can the target be relaxed for tiny
   objects, for example with a different Gaussian radius, "anywhere inside the
   box", or receptive-field-based assignment like RFLA?
2. **Low-res grid → pixels.** CenterNet predicts on a downsampled grid (output
   stride 4) and corrects with an offset term. Is that mapping the bottleneck
   when an object is smaller than one grid cell?
3. **Multi-scale prediction.** Detect at several resolutions in parallel and
   merge the results.
4. **Backbone.** Are there structural reasons the point formulation suits CNNs
   better than transformers? Has anyone bridged the two?
5. **Weak supervision.** Can a less prescriptive training signal generalise
   better on tiny objects?

## Key papers

**Core:**
- Focal Loss (Lin et al., 2017)
- CornerNet (Law & Deng, 2018)
- Objects as Points / CenterNet (Zhou et al., 2019)

**Should read:**
- R-CNN, Fast R-CNN, Faster R-CNN
- YOLO
- RFLA (Xu et al., 2022)
- A CenterNet-based satellite-video vehicle detection paper (title still to be
  confirmed). Its loss is changed so the predicted point only has to fall
  inside the box.

**Skim:** HOG, SSD, FPN, Mask R-CNN, and DETR later on.

## Datasets

The dataset choice is tracked in issue #1. We use **three datasets, one of each
kind**:

1. **Reference benchmark**, like COCO: the general reference every detector
   reports on.
2. **Aerial images**: drone or satellite imagery.
3. **Ground-level images**: photos taken from the ground, such as street, driving or everyday
   scenes.

For the reference benchmark, the options are COCO or a standard benchmark more
specific to tiny objects.

Each dataset has its own research notes in `docs/datasets/`:
`reference-benchmark.md`, `aerial-dataset.md` and `ground-level-dataset.md`.

Each choice has a nominee and a runner-up, both documented with every field
from issue #1. Other shortlisted datasets need only enough to explain why they
were not chosen, and every reason for rejecting one must be backed by a sourced
fact.

Candidates so far:

- COCO, the general reference; CenterNet reports its results on it
- VisDrone, drone imagery with many small objects
- A satellite-video dataset (details still to be confirmed)
- AI-TOD / AI-TOD-v2, the closest thing to a standard tiny-object benchmark
- SODA-D and SODA-A
- TinyPerson
- SOD4SB
- Others; see `docs/datasets/`

Definitions of "tiny" differ between papers: COCO "small" is under 32×32 px, and
AI-TOD "tiny" is under 16×16 px. Always state which definition a number uses.

## How we work

- **Tasks** are GitHub issues in this repository. Work within an
  issue may be split between people; the split can change from issue to issue.
- **Research notes** go in `docs/`:
  - research notes, one file per topic, named after what they cover rather than
    after a person or track, e.g.
    `docs/datasets/reference-benchmark.md`
  - the paper log, `docs/literature/paper-log.md`: every paper we read, with
    the datasets and models it uses (input for issues #1 and #2)
  - final decisions in `docs/datasets/selection.md` and `docs/model-selection.md`
- **Scripts** (data analysis, evaluation helpers) go in `scripts/`, each with a
  docstring saying what it does and how to run it. Any number in the notes that
  we computed ourselves should come from a script in the repo, so it can be
  reproduced.
- **Framework:** PyTorch where possible, so results are comparable. CenterNet
  code is the official implementation or MMDetection.
- **Hardware:** modest. Target GPU and VRAM: **TODO**.

### Git workflow

- `main` holds reviewed work only. Nobody commits to it directly.
- One branch per piece of work, named `<type>/<short-topic>`, e.g.
  `docs/reference-benchmark-dataset` or `feat/centernet-baseline`. Types:
  `docs`, `feat`, `fix`, `exp` (experiments).
- Open a pull request into `main`. Another contributor reviews it before it is merged.
- Reference the issue in commit messages and PR descriptions with `refs #N`
  (or `closes #N` when the PR finishes the issue).
- **Never commit datasets, annotation files, model weights or experiment
  outputs.** Keep them in `data/`, `checkpoints/` and `outputs/`, which are
  ignored by git (see `.gitignore`). Write down in the notes where each file
  came from instead.

## Instructions for Claude

- Every factual claim about a paper or dataset (sizes, counts, licences,
  results) needs a source link. If something isn't verified, mark it **TBD**,
  and mark derived numbers *(est.)*. Never fill a gap with a guess.
- Read the actual paper or repository rather than relying on search snippets
  wherever possible.
- When discussing a method, follow the guiding principle: explain why each
  design choice exists and whether it holds for tiny objects.
- Show changes for review before committing. Never commit, push, or comment on
  GitHub issues without the author's explicit go-ahead.
- Keep this file current when a decision is made. Record the decision
  and the reason for it.
- Ask before downloading anything. Downloads go in `data/` or outside the repo,
  never into tracked folders.
- Follow the git workflow above: work on a branch, never on `main`.

## Open questions

- Outcome A or B (see above)
- Target GPU and VRAM
- Real-time speed or offline accuracy?
- Title of the satellite-video CenterNet paper
