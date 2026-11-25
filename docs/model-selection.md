# Model selection

This is the shortlist of models we benchmark first (issue #2). It needs at
least three CenterNet variants and two or three comparison detectors, all
runnable on modest hardware, each with a named owner. The research for each
track is in its own notes file in [`models/`](models/), and each chosen model
has a folder in [`../models/`](../models/) with its details and how to run it.

CenterNet is a one-stage detector in every track. A track's name says which
backbone goes under CenterNet and which family of detectors we compare it
with.

**Status:** in progress. Tracks B and C have proposals; Track A is still being
researched. We fill in the rest of this file once all tracks are proposed and
everyone working on the issue agrees.

## Shortlist

| Track | CenterNet variant | Comparison detectors | Owner | Research notes |
|---|---|---|---|---|
| A. Lightweight | *pending* (ResNet-18 or MobileNet) | *pending* (one-stage: YOLO nano/small, SSD-Lite, RetinaNet) | *pending* | *pending* |
| B. Standard | DLA-34 · runner-up: CenterNet Update (ResNet-50, FPN) *(proposed)* | Two-stage: Faster R-CNN R50-FPN · runner-up: Cascade R-CNN R50-FPN *(proposed)* | Una | [standard-centernet-and-two-stage.md](models/standard-centernet-and-two-stage.md) |
| C. Backbones and anchor-free | HRNet-W18 · runner-up: Swin-T; Hourglass-104 for inference only *(proposed)* | Anchor-free: FCOS R50-FPN · runner-up: DINO R50. Label assignment: Faster R-CNN with RFLA · runner-up: with NWD-RKA *(proposed)* | Marko | [centernet-backbones-and-anchor-free.md](models/centernet-backbones-and-anchor-free.md) |

## Why each was chosen

Each entry is a short summary. The full comparison is in the notes file.

### Track A. Lightweight: *pending*

<!-- CenterNet variant, comparisons, why, limitation. -->

### Track B. Standard

See [section 5 of the Track B notes](models/standard-centernet-and-two-stage.md#5-decision).

### Track C. Backbones and anchor-free

- **CenterNet with HRNet-W18:** HRNet keeps a stride-4 branch through the
  whole network, the same resolution as CenterNet's output. It tests whether
  keeping the detail helps. No published model exists, so we build it from
  MMDetection's CenterNet head and HRNet backbone.
- **CenterNet with Swin-T (runner-up):** a transformer backbone with a
  stride-4 stage. Transformers lead small-object detection on most datasets,
  but on SODA-A Swin-T made one-stage detectors worse, so whether it helps
  CenterNet on tiny objects is an open question we test.
- **CenterNet with Hourglass-104, inference only:** CenterNet's most accurate
  published backbone (40.3 AP on COCO val), as an upper reference. Too heavy
  to train.
- **FCOS:** the standard anchor-free baseline, with and without a stride-4
  level, with published AI-TOD-v2 results (13.4 AP).
- **DINO (runner-up):** the strongest anchor-free detector we could train
  (25.9 AP on AI-TOD-v2), and the base of the best published AI-TOD-v2
  detectors. Its memory needs checking first.
- **Faster R-CNN with RFLA or NWD-RKA:** tiny-object label assignment with
  published AI-TOD-v2 results (12.8 → 22.6 / 21.4 AP). Reproducing them is
  our first check of the AI-TOD-v2 setup.
- **TTFNet:** not run as a separate detector. Its training target (elliptical
  Gaussian, box regression from the whole Gaussian area) becomes an option
  in CenterNet's head when we work on improvements.

## Framework and hardware

<!-- Agree once all tracks are proposed. -->

| Item | Decision |
|---|---|
| Framework | *pending*. Proposed by Tracks B and C: MMDetection 3.x where possible; the official CenterNet code for DLA-34 and Hourglass-104; mmdet-aitod (MMDetection 2.24.1) and mmdet-rfla (MMDetection 2.13.0) to reproduce published AI-TOD-v2 numbers. One environment per codebase, listed in [`models/README.md`](../models/README.md#code-environments) |
| Evaluation | *pending*. Proposed: every model saves COCO-format predictions, scored with the same AI-TOD evaluation (`cocoapi-aitod`) |
| Detections per image on AI-TOD-v2 | *pending*. Proposed: at least 1,500 for every model (the AI-TOD evaluation's limit; the default of 100 puts 26.1% of test objects out of reach, see the [Track C notes](models/centernet-backbones-and-anchor-free.md#6-decision)) |
| GPU | *pending* (proposed: one rented 24 GB GPU) |
| Input size on AI-TOD-v2 | *pending* |

## Agreement

- [ ] Track A agreed
- [ ] Track B agreed
- [ ] Track C agreed
- [ ] Framework and hardware agreed
