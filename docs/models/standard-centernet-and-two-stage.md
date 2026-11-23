# Standard CenterNet and two-stage detectors

This is the research for Track B of issue #2 (Select representative models for
initial dataset evaluation). Track B covers two things:

- the **standard CenterNet** candidate, the backbone the CenterNet paper
  treats as its main model, and
- **two-stage detectors** to compare CenterNet against.

**CenterNet candidate:** CenterNet with DLA-34 · runner-up: CenterNet with
ResNet-50 and FPN ("CenterNet Update")

**Two-stage detectors:** Faster R-CNN with ResNet-50 and FPN · runner-up:
Cascade R-CNN with ResNet-50 and FPN

The reasons are in [section 5](#5-decision).

Every number has a source, listed in [section 7](#7-sources). **TBD** means we
haven't checked it against a primary source yet, and *(est.)* means we worked
the number out ourselves. The chosen models each have a folder in
[`models/`](../../models/) with details and how to run them. Our target GPU is
not decided yet (issue #2 still has it as TODO), so for hardware we give the
memory each model needs and leave the final check for when we know the GPU.

## 1. What these models are for

We want two things from this track:

1. **A CenterNet we can compare with the paper.** CenterNet with DLA-34 is the
   model the paper reports most results for. If we run it on COCO and get the
   paper's score, we know our setup works (this is the first reason we chose
   COCO as the reference benchmark). After that, it is the main model we try to
   improve for tiny objects.
2. **Two-stage detectors as a baseline to compare with.** Most tiny-object
   papers build their methods on Faster R-CNN or Cascade R-CNN (NWD-RKA, RFLA,
   SimD, CFINet, see the [paper log](../literature/paper-log.md) and its
   [archive](../literature/paper-log-archive.md)). So they give
   us published results on AI-TOD-v2 to compare against, and a well-known point
   of comparison for CenterNet.

From this we made these criteria. They cover everything issue #2 asks to
record for each candidate.

| # | Criterion | Why it matters for us | Weight |
|---|---|---|---|
| C1 | **Published results on small objects**: COCO AP_S, and AI-TOD-v2 if available | We need numbers to check our runs against | High |
| C2 | **Code that runs today**: a maintained implementation, pretrained weights, works with a current PyTorch | Without it we spend our time fixing old code instead of running experiments | High |
| C3 | **Fits modest hardware**: training memory, speed | We don't have a large GPU | High |
| C4 | **Output stride**: how fine the grid is that objects are predicted on | A tiny object can fall between grid cells on a coarse grid | Medium |
| C5 | **Useful for our research directions**: is it the model tiny-object methods are built on, or the CenterNet formulation we want to study? | We want baselines we can later improve | Medium |
| C6 | **Effort to run on our datasets** (COCO, AI-TOD-v2) | Less setup work means more time for experiments | Medium |

## 2. CenterNet candidates

### 2.1 Nominee: CenterNet with DLA-34

CenterNet predicts each object as its centre point on a heatmap, plus the box
size and a small offset. DLA-34 is the backbone the paper uses for its main
speed and accuracy results.

All details, with sources, are in
[models/centernet-dla34/about.md](../../models/centernet-dla34/about.md), and
how to run it is in [its README](../../models/centernet-dla34/README.md). In
short:

- COCO val 2017: 37.4 AP; COCO test-dev with flip: **AP_S 19.9** [M1], [M2]
- output stride 4 [M1]
- no published plain CenterNet results on AI-TOD-v2
- training memory: **TBD**
- effort is **high**: the official code was tested with PyTorch 0.4.1 and
  needs DCNv2 compiled. The Detectron2 re-implementation runs on current
  PyTorch but changes the loss [M3], [M5]

**Strengths:** it is the paper's main model, with published COCO results
including AP_S, so we can check our setup against it. Its output stride of 4
is the finest of the CenterNet options. Its loss is the one our research directions
are about (one positive pixel per object, the offset term).

**Weaknesses:** the official code is old and will take work to run on a
current setup. The modern re-implementation changes exactly the parts we want
to study (the loss and how positives are chosen), so it can't replace the
original for our research. Nobody has published plain CenterNet results on
AI-TOD-v2, so we would be the first to measure it.

### 2.2 Runner-up: CenterNet with ResNet-50 and FPN ("CenterNet Update")

An updated CenterNet by the same author, with an FPN so it predicts on several
resolutions.

All details are in
[models/centernet-update-r50-fpn/about.md](../../models/centernet-update-r50-fpn/about.md),
and how to run it is in [its README](../../models/centernet-update-r50-fpn/README.md).
In short:

- COCO val 2017: 40.2 AP; AP_S **TBD** [M4]
- FPN levels with strides 8 to 128, so the finest is 8 [M4]
- 3.3 GB training memory in MMDetection [M4]
- changes from the original: GIoU loss, more positive pixels, FPN levels by
  object size, standard NMS [M4], [M5]
- effort is **low**: it works in current MMDetection, but sometimes doesn't
  converge [M4]

**Strengths:** easy to run in a current framework, uses little memory, and
predicts on several resolutions, which is one of our research directions.

**Weaknesses:** it changes the original CenterNet loss and label assignment,
so it is a different model from the one in the paper. There are no published
tiny-object results.

**Why it is the runner-up:** if we can't get the original DLA-34 code running,
this is the closest CenterNet that works out of the box. We put it second
because it isn't the original formulation (C5) and has no published AP_S (C1).

### 2.3 Other CenterNet options

#### CenterNet with ResNet-101 (official)

| Property | Value | Source |
|---|---|---|
| Paper / code | Same as DLA-34: [M1], official repo | [M1], [M2] |
| C1 Results | COCO val 2017: 34.6 AP (36.2 with flip). No AP_S in the paper's test-dev table | [M1] |
| C2 Code | Same old setup as DLA-34 (PyTorch 0.4.1, DCNv2) | [M3] |
| C3 Hardware | Same training recipe as DLA-34 in the paper; memory **TBD** | [M1] |

**Why not chosen:** it has the same setup problem as DLA-34 but scores lower
(34.6 vs 37.4 AP) and has no published AP_S (C1, C2).

#### CenterNet with ResNet-18 (MMDetection)

**Why not here:** it is the lightweight CenterNet, which belongs to Track A.
MMDetection reports 29.5 AP on COCO (with deformable convolutions) using
3.47 GB per GPU [M4].

## 3. Two-stage detectors

### 3.1 Nominee: Faster R-CNN with ResNet-50 and FPN

The standard two-stage detector: a region proposal network suggests boxes,
then a second stage classifies them and refines the box. FPN adds predictions
from several resolutions.

All details are in
[models/faster-rcnn-r50-fpn/about.md](../../models/faster-rcnn-r50-fpn/about.md),
and how to run it is in [its README](../../models/faster-rcnn-r50-fpn/README.md).
In short:

- COCO val 2017: 37.4 AP (MMDetection); COCO minival: **AP_S 17.8** (FPN
  paper) [M8], [M10]
- AI-TOD-v2: 12.8 AP, **AP_vt 0.0, AP_t 9.2**. With RFLA: 22.6 AP; with
  NWD-RKA: 21.4 AP [M14], [M13]
- FPN levels with strides 4 to 64, so the finest is 4 [M8]
- 4.0 GB training memory; 41.8M parameters [M8], [M9]
- effort is **low**: configs exist for COCO and AI-TOD-v2 [M8], [M15]

**Strengths:** the model most tiny-object methods are built on, with published
results on AI-TOD-v2 both with and without those methods. Runs in every major
framework with pretrained weights, and fits a modest GPU.

**Weaknesses:** on AI-TOD-v2 it finds almost none of the very tiny objects
(AP_vt 0.0). This is exactly the weakness tiny-object methods try to fix, so it
is useful for comparison, but it is a weak baseline on its own.

### 3.2 Runner-up: Cascade R-CNN with ResNet-50 and FPN

Faster R-CNN with three box-refinement stages in a row, each trained with a
stricter IoU threshold.

All details are in
[models/cascade-rcnn-r50-fpn/about.md](../../models/cascade-rcnn-r50-fpn/about.md),
and how to run it is in [its README](../../models/cascade-rcnn-r50-fpn/README.md).
In short:

- COCO val 2017: 40.3 AP (MMDetection); paper AP_S 22.6 *(check)* [M11], [M12]
- AI-TOD-v2: 15.1 AP, AP_vt 0.1 *(check)* [M13]
- same FPN levels as Faster R-CNN [M12]
- 4.4 GB training memory [M11]
- effort is **low**: same setup as Faster R-CNN [M11], [M15]

**Strengths:** better than Faster R-CNN on both COCO and AI-TOD-v2 for little
extra memory (4.4 vs 4.0 GB).

**Weaknesses:** the extra stages help with box accuracy but not with finding
very tiny objects (AP_vt 0.1). It is slower, and some of its numbers still need
checking against the paper.

**Why it is the runner-up:** it is the next model up from Faster R-CNN, with
the same tools and only a little more memory. We put Faster R-CNN first because
more tiny-object methods are built on it and its AI-TOD-v2 results are
confirmed in two sources (C1, C5).

### 3.3 Other two-stage options

#### DetectoRS (Cascade R-CNN with ResNet-50)

| Property | Value | Source |
|---|---|---|
| Paper / code | [DetectoRS](https://arxiv.org/abs/2006.02334) (2021); MMDetection | [M16] |
| C1 Results | COCO 47.4 AP (MMDetection). AI-TOD-v2: 16.1 AP, AP_vt 0.1; with NWD-RKA 24.7 AP, with RFLA 25.7 AP, the best results in those papers | [M16], [M14], [M13] |
| C2 Code | MMDetection, pretrained COCO weights | [M16] |
| C3 Hardware | **9.9 GB per GPU** for training (MMDetection) | [M16] |

**Why not chosen:** it needs more than twice the memory of Faster R-CNN (C3).
It is worth keeping in mind as the strongest published host for tiny-object
methods if we end up with a bigger GPU.

#### Faster R-CNN with HRNet-w32

| Property | Value | Source |
|---|---|---|
| C1 Results | AI-TOD-v2: 14.5 AP, AP_vt 0.1 *(from a summary of the paper's table; check)* | [M13] |

**Why not here:** a high-resolution backbone, which is Track C's topic.

## 4. Comparison

✅ = meets the criterion, ⚠️ = partly, ❌ = does not, ❓ = unknown.

| Criterion | **CenterNet DLA-34** (nominee) | **CenterNet Update R50-FPN** (runner-up) | CenterNet R-101 | **Faster R-CNN R50-FPN** (nominee) | **Cascade R-CNN R50-FPN** (runner-up) | DetectoRS |
|---|---|---|---|---|---|---|
| C1 Published small-object results | ⚠️ COCO AP_S 19.9; no AI-TOD-v2 | ❌ No AP_S found | ❌ No AP_S | ✅ COCO AP_S; AI-TOD-v2 | ✅ COCO AP_S; AI-TOD-v2 *(check)* | ✅ AI-TOD-v2, best host |
| C2 Code that runs today | ❌ PyTorch 0.4.1 + DCNv2 (official) | ✅ MMDetection 3.x | ❌ Same as DLA-34 | ✅ Everywhere | ✅ MMDetection | ✅ MMDetection |
| C3 Fits modest hardware | ❓ Memory TBD | ✅ 3.3 GB | ❓ TBD | ✅ 4.0 GB | ✅ 4.4 GB | ❌ 9.9 GB |
| C4 Output stride | ✅ 4 | ⚠️ FPN, finest 8 | ✅ 4 | ✅ FPN from stride 4 | ✅ FPN from stride 4 | ✅ FPN |
| C5 Research directions | ✅ The original loss we study | ⚠️ Changed loss | ✅ Original loss | ✅ Host for NWD-RKA, RFLA | ✅ Host for NWD-RKA | ✅ Best host |
| C6 Effort on our datasets | ❌ High | ✅ Low | ❌ High | ✅ Low, AI-TOD-v2 configs exist | ✅ Low | ⚠️ Low setup, heavy runs |

## 5. Decision

**CenterNet candidate: CenterNet with DLA-34.**

1. **It is the model the paper reports most results for.** We can check our
   setup against its COCO score (37.4 AP on val 2017) and its AP_S (19.9 on
   test-dev with flip).
2. **It has the original loss.** Our research directions are about this loss
   (one positive pixel per object, the offset term), so we need the original
   formulation, not a re-implementation that already changes it.
3. **Its output stride of 4** is the finest of the CenterNet options.

The main risk is the old code (C2). Before the baselines start, we need to
check whether the official repo runs with a current PyTorch and a newer build
of DCNv2, or whether we need to port DLA-34 into MMDetection's CenterNet. If
neither works in reasonable time, we switch to the runner-up.

**CenterNet runner-up: CenterNet Update (ResNet-50, FPN).** It runs in current
MMDetection with 3.3 GB, and it predicts on several resolutions. It came second
because it changes the original loss and has no published AP_S.

**Two-stage detector: Faster R-CNN with ResNet-50 and FPN.**

1. **Most tiny-object methods are built on it** (NWD-RKA, RFLA, SimD, CFINet),
   so there are published AI-TOD-v2 results both for the plain model and with
   these methods.
2. **It runs everywhere** with pretrained weights, and fits a modest GPU
   (4.0 GB).
3. **Its weakness is useful to us.** It scores 0.0 AP on AI-TOD-v2's very tiny
   objects, which shows clearly what a two-stage detector misses and gives
   CenterNet something concrete to beat.

**Two-stage runner-up: Cascade R-CNN with ResNet-50 and FPN.** Slightly better
everywhere for little extra memory. If our GPU allows both, we suggest putting
both on the final shortlist, since issue #2 asks for 2 or 3 comparison
detectors.

We would change the decision if:
- the official CenterNet code can't be made to run (switch to the runner-up)
- our GPU turns out to be larger than expected (add DetectoRS as the
  strongest published host for tiny-object methods)

## 6. Open items

- [ ] Try to run the official CenterNet DLA-34 code on a current PyTorch, or
  find a working DCNv2 build. This decides between the nominee and the
  runner-up.
- [ ] Find CenterNet DLA-34's training memory and full parameter count.
- [ ] Check the Cascade R-CNN and HRNet rows of the AI-TOD-v2 table in the
  NWD-RKA paper PDF (we only have them from a summary).
- [ ] Check Cascade R-CNN's COCO AP_S in its paper (Table 6).
- [ ] Fix the mmdet-aitod Faster R-CNN baseline config, which loads the
  AI-TOD v1 dataset file (see
  [its README](../../models/faster-rcnn-r50-fpn/README.md#3-config)).
- [ ] Fill in the target GPU, then check every model against it.

## 7. Sources

- [M1] Zhou et al., *Objects as Points* — <https://arxiv.org/abs/1904.07850> (Tables 1 and 2, sections 3 and 5)
- [M2] CenterNet official repo, README and model zoo — <https://github.com/xingyizhou/CenterNet/blob/master/readme/MODEL_ZOO.md>
- [M3] CenterNet install guide — <https://github.com/xingyizhou/CenterNet/blob/master/readme/INSTALL.md>
- [M4] MMDetection CenterNet configs and results — <https://github.com/open-mmlab/mmdetection/tree/main/configs/centernet>
- [M5] CenterNet2 model zoo — <https://github.com/xingyizhou/CenterNet2/blob/master/docs/MODEL_ZOO.md>
- [M6] timm DLA-34 model card — <https://huggingface.co/timm/dla34.in1k>
- [M7] Yu et al., *Deep Layer Aggregation* — <https://arxiv.org/abs/1707.06484>
- [M8] MMDetection Faster R-CNN configs and results — <https://github.com/open-mmlab/mmdetection/tree/main/configs/faster_rcnn>
- [M9] torchvision `fasterrcnn_resnet50_fpn` — <https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.detection.fasterrcnn_resnet50_fpn.html>
- [M10] Lin et al., *Feature Pyramid Networks for Object Detection* — <https://arxiv.org/abs/1612.03144> (Table 3c)
- [M11] MMDetection Cascade R-CNN configs and results — <https://github.com/open-mmlab/mmdetection/tree/main/configs/cascade_rcnn>
- [M12] Cai & Vasconcelos, *Cascade R-CNN* — <https://arxiv.org/abs/1712.00726>
- [M13] Xu et al., *Detecting tiny objects in aerial images: A normalized Wasserstein distance and a new benchmark* (NWD-RKA, AI-TOD-v2) — <https://arxiv.org/abs/2206.13996>
- [M14] RFLA code and results — <https://github.com/Chasel-Tsui/mmdet-rfla>
- [M15] AI-TOD code (mmdet-aitod) — <https://github.com/Chasel-Tsui/mmdet-aitod>
- [M16] MMDetection DetectoRS configs and results — <https://github.com/open-mmlab/mmdetection/tree/main/configs/detectors>
- [M17] Our paper log — [docs/literature/paper-log.md](../literature/paper-log.md)
