# Dataset selection

This is the final choice of the three datasets we use in the project (issue
#1): a reference benchmark, an aerial dataset and a ground-level dataset. For
each one we pick a nominee and a runner-up. The research for each choice is in
its own notes file, linked below.

**Status:** in progress. We have nominees for the reference benchmark and the
aerial dataset, and the ground-level dataset is still being researched. We fill in the
rest of this file once all three are nominated and everyone working on the
issue agrees.

## Decision

| Kind | Chosen | Runner-up | Research notes |
|---|---|---|---|
| Reference benchmark | MS COCO 2017 *(nominated)* | LVIS v1.0 | [reference-benchmark.md](reference-benchmark.md) |
| Aerial images | AI-TOD-v2 *(nominated)* | VisDrone2019-DET | [aerial-dataset.md](aerial-dataset.md) |
| Ground-level images | *pending* | *pending* | [ground-level-dataset.md](ground-level-dataset.md) |

## Why each was chosen

Each entry is a short summary based on the selection criteria in issue #1.
The full comparison is in the notes file.

### Reference benchmark: MS COCO 2017

- **What we use it for:** to compare our baselines with published results, and
  to measure how much worse detectors do on small objects. We test tiny objects
  mostly on the other two datasets.
- **Why:** it is the only dataset with published results for every detector we
  might use (including CenterNet), an official small-object metric (AP_S), and
  every object labelled.
- **Runner-up, LVIS v1.0:** the same images, but smaller objects. It came second
  because there are no CenterNet results for it and not every object is
  labelled.
- **Limitation:** only 12.6% of COCO objects are under 16 px (measured), so we
  need the aerial and ground-level datasets for tiny objects.

### Aerial images: AI-TOD-v2

- **What we use it for:** to test detectors on tiny objects. It is our main
  tiny-object dataset.
- **Why:** of the six aerial datasets we measured, it is the only one where
  almost all objects are tiny: 85.9% are under 16 px (measured), against
  26–48% for the others. Recent tiny-object methods report results on it, and
  its labels were cleaned to add missed objects. Its images are 800×800, so
  they don't need to be cut into tiles. It is large enough on its own (28,036
  images, 752,746 objects), so we use one aerial dataset, not two.
- **Runner-up, VisDrone2019-DET:** the aerial dataset used most often, and
  the easiest to get and train on. It came second because only 26–36% of its
  objects are under 16 px.
- **Limitation:** only the labels are published. The images have to be cut
  out of the xView training images with the AI-TOD tool, or taken from a full
  copy on Kaggle. 88% of the objects are vehicles, and there are no published
  CenterNet results, so we produce the first CenterNet baseline ourselves.

### Ground-level images: *pending*

<!-- Nominee, why, runner-up, limitation. Summary of ground-level-dataset.md section 4. -->

## How the three fit together

<!-- Fill in once all three are chosen. Check that together they cover:
- at least one dataset where a large share of objects is under 16 px
- the same metrics everywhere where possible (AP, AP_S, and AI-TOD size bins),
  so results can be compared across datasets
- what fits our hardware: which splits we evaluate on, and whether we train on
  full sets or subsets -->

## Evaluation setup

This is how we will use each dataset. We need to agree on it before running
any baselines.

| Dataset | Evaluation split | Training data | Metrics |
|---|---|---|---|
| MS COCO 2017 | val 2017 (5K images, public labels) | Pretrained weights; subsets of train 2017 where we train | AP, AP50, AP75, AP_S/M/L, plus AP in AI-TOD size bins |
| AI-TOD-v2 | test (14,018 images, public labels) | trainval (14,018 images), or a subset of it if our hardware needs that | AP, AP50, AP75, plus AP_vt / AP_t / AP_s / AP_m for AI-TOD's size ranges (`cocoapi-aitod`) |
| Ground-level | *pending* | *pending* | *pending* |

## Agreement

- [ ] Reference benchmark agreed
- [ ] Aerial dataset agreed
- [ ] Ground-level dataset agreed
- [ ] Evaluation setup agreed
