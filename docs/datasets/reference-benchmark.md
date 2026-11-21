# Reference benchmark dataset

Research for choosing the project's **reference benchmark**: the dataset we
use to compare our results with published work. It is one of the three
datasets we use, next to the [aerial dataset](aerial-dataset.md) and the
[ground-level dataset](ground-level-dataset.md). Part of issue #1 (Select
datasets for tiny object detection).

**Nominee: MS COCO 2017** · **Runner-up: LVIS v1.0**. The reasoning is in
[section 4](#4-decision).

Conventions: every number has a source in [section 7](#7-sources). Fields
marked **TBD** have not been checked against a primary source yet, and numbers
marked *(est.)* are derived by us, not reported. "Measured" means we computed
it ourselves from the official annotation files with
[`scripts/coco_size_stats.py`](../../scripts/coco_size_stats.py) [S27].

## Short answer: is there a standard dataset for tiny object detection?

**Not a single one.** The literature uses two references:

- **COCO** is the general reference. Every detector reports on it, and its
  AP_S metric (objects under 32×32 px) is the usual way to report small-object
  performance. It is not a tiny-object dataset, though: only 12.6% of its
  objects are under 16 px (measured).
- **AI-TOD / AI-TOD-v2** (aerial, under 16 px) and **SODA-D / SODA-A**
  (driving and aerial) are the dedicated tiny-object benchmarks recent papers
  report on most [S24], [S25]. All of them are domain-specific, so they belong
  to the aerial and ground-level dataset choices.

No survey we read names a general-purpose benchmark built for tiny objects.

## 1. What the reference benchmark is for

The aerial and ground-level datasets are where tiny objects actually appear.
The reference benchmark has a different job:

1. **Anchor our baselines to published numbers.** If our CenterNet run on the
   reference benchmark matches the paper's reported score, our pipeline is
   correct, and our results on the other two datasets can be trusted.
2. **Show the general small-object gap.** Every detector does worse on small
   objects. A benchmark that reports this separately lets us measure it the same
   way the literature does.
3. **Provide pretrained weights.** We fine-tune rather than train from
   scratch, so the weights we start from should match this dataset.

These roles give the criteria used to compare the contenders. They cover all
five selection criteria in issue #1, plus C3.

| # | Criterion | Why it matters for us | Weight |
|---|---|---|---|
| C1 | **Published results**, including CenterNet's | Role 1: without published numbers there is nothing to anchor to | High |
| C2 | **Small objects and a small-object metric** | Role 2: we need a separate score for small objects | High |
| C3 | **Clean, exhaustive evaluation** | If unlabelled objects are excluded from scoring, small-object errors are hard to interpret | High |
| C4 | **Fits modest hardware** (download size, image count) | We have limited GPU and disk | Medium |
| C5 | **Tooling and format** (COCO JSON, MMDetection support, evaluation code) | Less conversion work, comparable numbers | Medium |
| C6 | **Licence and access** allow academic use without hurdles | Must be usable for research without extra agreements | Medium |

## 2. Contenders

Five datasets are commonly used as general-purpose detection benchmarks: COCO,
LVIS, Objects365, Open Images and PASCAL VOC. I found no general-purpose
benchmark built specifically for tiny objects (see the short answer above).

### 2.1 Nominee: MS COCO 2017

The standard detection benchmark: everyday scenes, 80 object categories.

| Property | Value | Source |
|---|---|---|
| Domain, year | General everyday scenes; paper 2014, current 2017 splits | [S5], [S1] |
| Paper / download | [arXiv 1405.0312](https://arxiv.org/abs/1405.0312) / [cocodataset.org/#download](https://cocodataset.org/#download) | [S5], [S1] |
| Images | 118,287 train, 5,000 val (measured); 41K test, labels hidden | [S27], [S1] |
| Instances | 849,949 train + 36,335 val, not counting crowd regions (measured) | [S27] |
| Classes | 80 | [S3] |
| Instances per image | 7.7 on average (PASCAL VOC: 2.3) | [S5] |
| Share under 16 px / under 32 px | By box size √(w·h): **12.6% / 31.5%** (train and val alike). By mask area, COCO's official measure: 19.3% / 42.0% (val). See the size table below | [S27] |
| Image resolution | Longest side at most 640 px; 82–83% of images are exactly 640 px on the longest side (measured) | [S27] |
| Size on disk | Images: 18 GB train, 1 GB val, 6 GB test. Annotations: 241 MB | [S1] |
| Annotation format | COCO JSON | [S1] |
| Licence and access | Annotations CC BY 4.0; images under Flickr Terms of Use. Direct download, no registration | [S4], [S1] |
| Metric | AP averaged over IoU 0.50:0.05:0.95, AP50, AP75, **AP_S / AP_M / AP_L**, AR. At most 100 detections per image | [S2] |
| Published baselines | CenterNet on val 2017 (no test-time augmentation): ResNet-18 with deformable convs 28.1 AP, DLA-34 37.4 AP, Hourglass-104 40.3 AP | [S6] |
| How often used | Named as the general small-object reference in the surveys we read [S24], [S26]; the default benchmark in every detector repo we checked [S6], [S10] | — |
| Tooling | Official evaluation code (`pycocotools`); the default format for MMDetection, Detectron2 and Ultralytics | [S2] |

**Object sizes in detail** (measured on val 2017, 36,335 instances; train 2017
matches to within 0.2 points):

| AI-TOD bin, box size √(w·h) | Share | | COCO bin, mask area | Share |
|---|---|---|---|---|
| under 2 px | 0.0% | | under 8² px | 5.4% |
| 2–8 px (very tiny) | 3.0% | | under 16² px | 19.3% |
| 8–16 px (tiny) | 9.6% | | under 32² px (small) | 42.0% |
| 16–32 px (small) | 18.9% | | 32²–96² px (medium) | 34.1% |
| 32–64 px (medium) | 22.4% | | 96² px and up (large) | 23.9% |
| over 64 px | 46.1% | | | |

Median box size is 56 px. Our mask-area split (42 / 34 / 24%) matches COCO's
published 41 / 34 / 24% [S2], which confirms the script. Mask area is smaller
than box area, which is why the mask-based shares are higher than the box-based
ones.

**Strengths:** everything we compare against reports on it, CenterNet
included. It has a dedicated small-object metric with an official definition,
exhaustive labels and public val labels. Val 2017 alone is only 1 GB.

**Weaknesses:** "small" means under 32×32 px, which is larger than the
under-16 px "tiny" in the tiny-object literature, and only 12.6% of objects
are under 16 px. Full training (118K images) is heavy for modest hardware.

### 2.2 Runner-up: LVIS v1.0

Re-annotation of the COCO 2017 images with a large, long-tailed vocabulary.

| Property | Value | Source |
|---|---|---|
| Domain, year | General everyday scenes (COCO images); paper 2019, v1.0 released for the 2020 challenge | [S8], [S7] |
| Paper / download | [arXiv 1908.03195](https://arxiv.org/abs/1908.03195) / [lvisdataset.org/dataset](https://www.lvisdataset.org/dataset) | [S8], [S28] |
| Images | 100,170 train, 19,809 val, 19,822 test-dev, 19,822 test-challenge. All are COCO 2017 images; **LVIS val includes images from COCO train 2017** | [S28] |
| Instances | 1,270,141 train, 244,707 val | [S28] |
| Classes | 1,203, split into rare, common and frequent by how many training images they appear in | [S28], [S9] |
| Share under 16 px / under 32 px | **TBD**. The paper says LVIS objects tend to be smaller than COCO's, with very large objects ~10× rarer (v0.5, 5K val images). Measuring it needs the 192 MB val annotation file; our script works on it unchanged | [S8] |
| Image resolution | Same as COCO: longest side at most 640 px | [S28], [S27] |
| Size on disk | Same images as COCO (18 GB train, 1 GB val). Annotations: 1 GB train, 192 MB val | [S28] |
| Annotation format | COCO-like JSON with extra fields (`not_exhaustive_category_ids`, `neg_category_ids`); always polygons | [S28] |
| Licence and access | Annotations CC BY 4.0; images under COCO's terms. Direct download | [S28] |
| Metric | AP over IoU 0.50:0.95 and AP_S / AP_M / AP_L with COCO's thresholds, plus AP_r / AP_c / AP_f. At most 300 detections per image | [S9] |
| Annotation design | **Federated:** each category is exhaustively labelled only on a subset of images. Detections are scored only where the category is known to be present or absent | [S8], [S28] |
| Published baselines | MMDetection Mask R-CNN models on v1.0; no CenterNet results found | [S10], [S6] |
| How often used | Not named in the surveys we read (their full dataset lists were not checked) | — |
| Tooling | `lvis-api` (a COCO-API rewrite); MMDetection configs | [S7], [S10] |

**Strengths:** the same images and size thresholds as COCO, but smaller
objects. Switching from COCO costs only a 1.2 GB annotation download.

**Weaknesses:** the federated labels mean an unlabelled small object is not
necessarily background, which makes small-object errors harder to interpret.
The long tail mixes a second difficulty (rare classes) into every result.
There are no CenterNet numbers to anchor to. **Its val set contains COCO train
images**, so a COCO-pretrained model has already seen part of it. Evaluating
COCO-pretrained weights on LVIS val would overstate performance.

**Why it is the runner-up:** it is the only other contender that meets C2 and
C5 fully, and it is the cheapest switch if COCO falls through. Its failure on
C1 and C3 is why it is second, not first.

### 2.3 Other contenders

#### Objects365

| Property | Value | Source |
|---|---|---|
| Domain, year, paper | General scenes; ICCV 2019 ([objects365.org](https://www.objects365.org/overview.html)) | [S11] |
| Images / classes | ~2 million images (1,742,289 train + 80,000 val per Ultralytics) / 365 classes; 30 million boxes | [S11], [S13] |
| C1 Published results | Mostly used for pretraining; no CenterNet results found | [S13], [S6] |
| C2 Small objects | **TBD** (paper not readable). Does not change the outcome: C4 rules it out regardless | — |
| C3 Exhaustive labels | **TBD**. Does not change the outcome, for the same reason | — |
| C4 Hardware | ~345 GB of zips, ~712 GB extracted | [S13] |
| C5 Format | COCO-style JSON; MMDetection configs | [S13], [S10] |
| C6 Licence | Academic use only; annotations CC BY 4.0; images under Flickr terms; registration required | [S12] |

**Why not chosen:** far too large for our hardware (C4), and few papers report
results on it as a benchmark, CenterNet included (C1).

#### Open Images V7 (detection)

| Property | Value | Source |
|---|---|---|
| Domain, year, paper | General scenes; V7 ([facts and figures](https://storage.googleapis.com/openimages/web/factsfigures_v7.html)) | [S14] |
| Images / classes | 1,743,042 train, 41,620 val, 125,436 test images with boxes / 600 classes | [S14] |
| C1 Published results | No CenterNet results found | [S6] |
| C2 Small objects | Size distribution "in a similar ballpark to the COCO dataset" (no numbers); no small-object AP | [S14], [S16] |
| C3 Exhaustive labels | No: classes not verified on an image are excluded from evaluation; "group-of" boxes | [S16] |
| C4 Hardware | ~1.9M images with boxes | [S14] |
| C5 Format | CSV with normalised coordinates; its own AP@0.5 metric with class hierarchy | [S15], [S16] |
| C6 Licence | Annotations CC BY 4.0; images listed as CC BY 2.0 | [S14] |

**Why not chosen:** it has no small-object metric and its own scoring rules, so
results are not comparable with most papers (C1, C2). Its labels are not
exhaustive (C3), and it is too large (C4).

#### PASCAL VOC 2007 + 2012

| Property | Value | Source |
|---|---|---|
| Domain, year, paper | General scenes; 2007 and 2012 challenges ([mirror](https://pjreddie.com/projects/pascal-voc-dataset-mirror/)) | [S17], [S18] |
| Images / classes | 2007: 9,963 images, 24,640 objects. 2012: 11,540 trainval images, 27,450 objects / 20 classes | [S17] |
| C1 Published results | CenterNet: 72.6–80.7 mAP on VOC 2007 test (trained on 07+12) | [S6] |
| C2 Small objects | Fewer small objects than COCO (2.3 instances per image vs 7.7); no small-object metric | [S5] |
| C3 Exhaustive labels | Yes, for its 20 classes | [S17] |
| C4 Hardware | Under 3 GB in total | [S18] |
| C5 Format | XML; widely supported | [S19] |
| C6 Licence | **TBD** (official site unreachable). Does not change the outcome: C2 rules it out regardless | — |

**Why not chosen:** too few small objects and no small-object metric (C2), so
it cannot measure the small-object gap, which is half of this dataset's job.

## 3. Comparison

✅ = meets the criterion, ⚠️ = partly, ❌ = does not, ❓ = unknown.

| Criterion | **COCO 2017** (nominee) | **LVIS v1** (runner-up) | Objects365 | Open Images V7 | PASCAL VOC |
|---|---|---|---|---|---|
| C1 Published results, incl. CenterNet | ✅ Universal; CenterNet yes | ⚠️ Common; no CenterNet | ❌ Mostly pretraining; no CenterNet | ⚠️ Some; no CenterNet | ⚠️ Older papers; CenterNet yes |
| C2 Small objects + small-object metric | ✅ 31.5% under 32 px, 12.6% under 16 px; AP_S | ✅ Smaller than COCO; AP_S | ❓ Not published | ⚠️ Similar to COCO; no AP_S | ❌ Few small; no AP_S |
| C3 Clean, exhaustive evaluation | ✅ Exhaustive | ❌ Federated | ❓ TBD | ❌ Non-exhaustive, group-of | ✅ Exhaustive |
| C4 Fits modest hardware | ⚠️ 19 GB; val only 1 GB | ⚠️ Same images as COCO | ❌ ~345 GB of zips | ❌ ~1.9M images | ✅ Under 3 GB |
| C5 Tooling and format | ✅ The default | ✅ COCO-like, own API | ⚠️ COCO-style JSON | ❌ CSV, own metric | ✅ Widely supported |
| C6 Licence and access | ✅ CC BY 4.0 + Flickr | ✅ CC BY 4.0 + COCO terms | ⚠️ Academic only, registration | ✅ CC BY 4.0 / CC BY 2.0 | ❓ TBD |

## 4. Decision

**Nominee: MS COCO 2017**, with val 2017 (5K images, public labels) as our
evaluation split and AP_S as the headline small-object metric.

Why it wins:

1. **It is the only contender that meets all three high-weight criteria.** It
   has published results for every detector we might try, CenterNet included
   (C1). It has a small-object metric with an official definition (C2). Its
   labels are exhaustive (C3).
2. **We can check our pipeline against the paper.** CenterNet's published val
   2017 scores [S6] give us a target to reproduce before we trust any other
   number.
3. **The hardware concern is manageable.** We can evaluate pretrained models on
   val 2017 (1 GB) without training. Where we do train, we can use a subset of
   train 2017.

**Runner-up: LVIS v1.0.** It is the only other contender with both a
small-object metric and smaller objects than COCO (C2), on the same images and
tooling (C5). It loses on C1 (no CenterNet numbers) and C3 (federated labels).

Why not the others:

- **Objects365** is too large for our hardware (C4), and few papers report on it
  as a benchmark (C1).
- **Open Images** has no small-object metric and its own scoring rules (C1, C2),
  non-exhaustive labels (C3), and is too large (C4).
- **PASCAL VOC** is cheap and has CenterNet results, but too few small objects
  and no small-object metric (C2).

Known limitation and how we handle it: COCO's "small" (under 32 px) is not
"tiny" (under 16 px), and only 12.6% of COCO objects are under 16 px. The
aerial and ground-level datasets cover truly tiny objects. On COCO we will also
report AP in AI-TOD's finer size bins, which `pycocotools` supports through
custom area ranges [S2]. At 12.6% of 36,335 val instances, that is about 4,600
tiny objects, enough for a stable score.

What would change the decision:
- a specific benchmark is required for comparison with related work
- a general-purpose tiny-object benchmark with published results turns up

## 5. Ruled out early

These were looked at while searching for a general-purpose tiny-object
benchmark, but were not shortlisted.

| Dataset | Domain | Link | Why dropped |
|---|---|---|---|
| SOD4SB (MVA2023) | Birds | [S20] | Single class; few published results and no CenterNet results; public-test labels hidden; ~62 GB for the full training set |
| NUAA-SIRST, NUDT-SIRST, IRSTD-1k | Infrared | [S21] | Segmentation masks and Pd/Fa metrics instead of boxes and AP; one class |
| DeepPCB, PKU-Market-PCB | Industrial defects | [S22] | Niche; little published work to compare against |
| DeepLesion, LUNA16 | Medical | [S23] | 3D data, FROC metrics, restricted access; out of scope for this project |
| AI-TOD, SODA-A / SODA-D, TinyPerson | Aerial / ground-level | [S24] | Real tiny-object benchmarks, but domain-specific; they belong to the aerial and ground-level choices |

### Domains not covered by the aerial and ground-level datasets

- **Reviewed above:** infrared small targets, wildlife and birds, industrial
  defects, medical imaging.
- **Not reviewed yet:** agriculture (wheat heads, insects and pests), maritime
  (small boats), sports (ball tracking), microscopy (cells), astronomy and
  space debris.

### Papers found, by domain

| Domain | Paper | Venue | Datasets it uses or names |
|---|---|---|---|
| General (survey) | Cheng et al., *Towards Large-Scale Small Object Detection: Survey and Benchmarks* [S24] | TPAMI 2023 | COCO, WIDER FACE, xView, TinyPerson, AI-TOD; introduces SODA-D and SODA-A |
| General (survey) | Kos & Belter, *Deep Learning for Small and Tiny Object Detection: A Survey* [S25] | PAR 2023 | 10 datasets; compares size bands of WIDER FACE, TinyPerson, AI-TOD and SODA |
| General (survey) | Tong & Wu, *Deep learning-based detection from the perspective of small or tiny objects: A survey* (doi:10.1016/j.imavis.2022.104471) | IVC 2022 | Reviews 30 datasets, analyses 12 popular ones (list **TBD**) |
| General (survey) | *Small Object Detection: A Comprehensive Survey…* [S26] | arXiv 2025 | COCO as the reference for "small" |
| Birds | Kondo et al., *MVA2023 Small Object Detection Challenge for Spotting Birds* [S20] | MVA 2023 | SOD4SB |
| Infrared | *Deep learning based infrared small object segmentation: Challenges and future directions* [S21] | arXiv 2025 | NUAA-SIRST, NUDT-SIRST, IRSTD-1k |
| Medical | *From single to universal: tiny lesion detection in medical imaging* [S23] | AI Review 2024 | DeepLesion, LUNA16 |

## 6. Open items

- [ ] Measure LVIS v1 val object sizes (192 MB annotation file; same script).
- [ ] Get the list of 12 "popular" datasets from Tong & Wu (full text).
- [ ] Confirm that no specific reference benchmark is required.

## 7. Sources

- [S1] COCO download page — <https://cocodataset.org/#download> (read from its source, [cocodataset.github.io](https://github.com/cocodataset/cocodataset.github.io/blob/master/dataset/download.htm))
- [S2] COCO detection evaluation — <https://cocodataset.org/#detection-eval>
- [S3] COCO 2017 detection task — <https://cocodataset.org/#detection-2017>
- [S4] COCO terms of use — <https://cocodataset.org/#termsofuse>
- [S5] Lin et al., *Microsoft COCO: Common Objects in Context* — <https://arxiv.org/abs/1405.0312>
- [S6] CenterNet model zoo — <https://github.com/xingyizhou/CenterNet/blob/master/readme/MODEL_ZOO.md>
- [S7] LVIS API README — <https://github.com/lvis-dataset/lvis-api>
- [S8] Gupta et al., *LVIS: A Dataset for Large Vocabulary Instance Segmentation* — <https://arxiv.org/abs/1908.03195>
- [S9] LVIS evaluation code — <https://github.com/lvis-dataset/lvis-api/blob/master/lvis/eval.py>
- [S10] MMDetection configs (lvis, objects365, openimages) — <https://github.com/open-mmlab/mmdetection/tree/main/configs>
- [S11] Objects365 overview — <https://www.objects365.org/overview.html>
- [S12] Objects365 download and terms — <https://www.objects365.org/download.html>
- [S13] Ultralytics Objects365 docs (secondary) — <https://docs.ultralytics.com/datasets/detect/objects365/>
- [S14] Open Images V7 facts and figures — <https://storage.googleapis.com/openimages/web/factsfigures_v7.html>
- [S15] Open Images V7 download — <https://storage.googleapis.com/openimages/web/download_v7.html>
- [S16] Open Images evaluation — <https://storage.googleapis.com/openimages/web/evaluation.html>
- [S17] TensorFlow Datasets, VOC — <https://www.tensorflow.org/datasets/catalog/voc>
- [S18] PASCAL VOC mirror — <https://pjreddie.com/projects/pascal-voc-dataset-mirror/>
- [S19] torchvision VOCDetection — <https://docs.pytorch.org/vision/stable/generated/torchvision.datasets.VOCDetection.html>
- [S20] SOD4SB baseline repo — <https://github.com/IIM-TTIJ/MVA2023SmallObjectDetection4SpottingBirds>; Kondo et al. — <https://arxiv.org/abs/2307.09143>
- [S21] Infrared small object segmentation review — <https://arxiv.org/abs/2502.14168>
- [S22] DeepPCB — <https://github.com/tangsanli5201/DeepPCB>
- [S23] Tiny lesion detection review — <https://link.springer.com/article/10.1007/s10462-024-10762-x>
- [S24] Cheng et al. — <https://arxiv.org/abs/2207.14096>
- [S25] Kos & Belter — <https://yadda.icm.edu.pl/baztech/element/bwmeta1.element.baztech-0914b536-d052-40f7-b712-0487146494e0/c/Kos_Deep_PAR_3_2023.pdf>
- [S26] <https://arxiv.org/abs/2503.20516>
- [S27] Our measurement: [`scripts/coco_size_stats.py`](../../scripts/coco_size_stats.py) run on the official `annotations_trainval2017.zip` (downloaded 21 Nov 2026)
- [S28] LVIS dataset page — <https://www.lvisdataset.org/dataset>
