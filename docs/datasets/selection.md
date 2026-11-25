# Dataset selection

This is the final choice of the three datasets we use in the project (issue
#1): a reference benchmark, an aerial dataset and a ground-level dataset. For
each one we pick a nominee and a runner-up. The research for each choice is in
its own notes file, linked below.

All three datasets have nominees and runners-up. Team agreement on the choices and evaluation setup is pending.

## Decision

| Kind | Chosen | Runner-up | Research notes |
|---|---|---|---|
| Reference benchmark | MS COCO 2017 *(nominated)* | LVIS v1.0 | [reference-benchmark.md](reference-benchmark.md) |
| Aerial images | AI-TOD-v2 *(nominated)* | VisDrone2019-DET | [aerial-dataset.md](aerial-dataset.md) |
| Ground-level images | SODA-D *(nominated)* | TinyPerson | [ground-level-dataset.md](ground-level-dataset.md) |

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

### Ground-level images: SODA-D

SODA-D tests tiny objects across nine street and driving classes. In the native annotations, 21.0% of foreground boxes are under 16 px and 71.4% are under 32 px. The SODA paper reports CenterNet at 21.5 AP and 5.1 AP_eS and CornerNet at 24.6 AP. Native images average 3407x2470 px and the image archive is 24.92 GiB. We propose 800x800 patch inputs pending team agreement and a hardware check. [SODA-D research notes](ground-level-dataset.md#21-nominee-soda-d)

TinyPerson is the runner-up. Among its normal detection boxes, 58.0% are under 16 px. It evaluates one person class in coastal scenes and reports AP and log-average miss rate using IoU for normal boxes and intersection over detection area (IOD) for ignore regions. The image archive sizes and dataset licence are **TBD**. [TinyPerson research notes](ground-level-dataset.md#22-runner-up-tinyperson)

## How the three fit together

The nominees form a progression in native box size. The share under 16 px rises from 12.6% on COCO to 21.0% on SODA-D and 85.9% on AI-TOD-v2. At native resolution and stride 4, 12.9% of SODA-D boxes and 67% of AI-TOD-v2 boxes produce a radius-0 CenterNet Gaussian that covers just the centre cell. [COCO notes](reference-benchmark.md), [SODA-D notes](ground-level-dataset.md), [AI-TOD-v2 notes](aerial-dataset.md)

All three have COCO-style box labels and public evaluation annotations. Each benchmark uses its own AP protocol. In particular, SODA-D reports headline AP over its Small band, with box area up to and including 1024 px^2. [SODA-D evaluation](ground-level-dataset.md#soda-d-evaluation)

## Evaluation setup

| Dataset | Evaluation split | Training data | Metrics |
|---|---|---|---|
| MS COCO 2017 | val 2017 (5K images, public labels) | Pretrained weights; subsets of train 2017 where we train | AP, AP50, AP75, AP_S/M/L, plus AP in AI-TOD size bins |
| AI-TOD-v2 | test (14,018 images, public labels) | trainval (14,018 images), or a subset of it if our hardware needs that | AP, AP50, AP75, plus AP_vt / AP_t / AP_s / AP_m for AI-TOD's size ranges (`cocoapi-aitod`) |
| SODA-D | Full test, 7,428 images and 88,082 foreground boxes. Merge patch predictions in original image coordinates | Train, 12,383 images and 134,301 foreground boxes, or a fixed subset if needed. Proposed input for both splits is 800x800 patches at stride 650. The paper resizes to 1200x1200 | `SODADeval` on category IDs 1 through 9, with AP at 100 detections per class per image. Report AP, AP50, and AP75 on SODA Small, and AP_eS, AP_rS, AP_gS, and AP_N |

For supplemental AI-TOD size-bin scores on SODA-D, adapt a copy of the foreground annotations for `cocoapi-aitod` and use the same merged predictions. The [SODA-D evaluation protocol](ground-level-dataset.md#soda-d-evaluation) gives the annotation fields, detection cap, and NMS settings.

## Agreement

- [ ] Reference benchmark agreed
- [ ] Aerial dataset agreed
- [ ] Ground-level dataset agreed
- [ ] Evaluation setup agreed
