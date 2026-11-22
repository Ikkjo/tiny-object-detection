# Dataset selection

This is the final choice of the three datasets we use in the project (issue
#1): a reference benchmark, an aerial dataset and a ground-level dataset. For
each one we pick a nominee and a runner-up. The research for each choice is in
its own notes file, linked below.

**Status:** in progress. We have a nominee for the reference benchmark, and the
aerial and ground-level datasets are still being researched. We fill in the
rest of this file once all three are nominated and everyone working on the
issue agrees.

## Decision

| Kind | Chosen | Runner-up | Research notes |
|---|---|---|---|
| Reference benchmark | MS COCO 2017 *(nominated)* | LVIS v1.0 | [reference-benchmark.md](reference-benchmark.md) |
| Aerial images | *pending* | *pending* | [aerial-dataset.md](aerial-dataset.md) |
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

### Aerial images: *pending*

<!-- Nominee, why, runner-up, limitation. Summary of aerial-dataset.md section 4. -->

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
| Aerial | *pending* | *pending* | *pending* |
| Ground-level | *pending* | *pending* | *pending* |

## Agreement

- [ ] Reference benchmark agreed
- [ ] Aerial dataset agreed
- [ ] Ground-level dataset agreed
- [ ] Evaluation setup agreed
