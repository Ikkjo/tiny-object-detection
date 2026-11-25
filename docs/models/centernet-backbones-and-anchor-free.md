# CenterNet backbones and anchor-free detectors

This is the research for Track C of issue #2 (Select representative models for
initial dataset evaluation). Track C covers three things:

- **backbones for CenterNet** beyond the standard ones: a high-resolution CNN
  and transformer backbones,
- **anchor-free detectors** to compare CenterNet against, and
- **tiny-object label assignment** methods, which change which locations learn
  from which object.

CenterNet is a one-stage detector in every track [M2]. The tracks differ in
the backbone under CenterNet and in the detectors it is compared with.

**CenterNet backbones:** HRNet-W18 · runner-up: Swin-T · reference:
Hourglass-104, inference only

**Anchor-free detectors:** FCOS with ResNet-50 and FPN · runner-up: DINO with
ResNet-50

**Tiny-object label assignment:** RFLA on Faster R-CNN · runner-up: NWD-RKA on
Faster R-CNN

The reasons are in [section 6](#6-decision).

Every number has a source, listed in [section 8](#8-sources). **TBD** means we
haven't checked it against a primary source yet, and *(est.)* means we worked
the number out ourselves. The papers behind these choices are in our paper log [M42]. The
chosen models each have a folder in
[`models/`](../../models/) with details and how to run them. Our target GPU is
not decided yet, so for hardware we give the memory each model needs.
AI-TOD-v2 results use its test split and AI-TOD's size ranges: AP_vt (2–8 px),
AP_t (8–16 px), AP_s (16–32 px) and AP_m (32–64 px).

## 1. What these models are for

We want three things from this track:

1. **To find out whether the backbone helps CenterNet with tiny objects.**
   CenterNet predicts on a stride-4 grid, but most backbones lose detail long
   before that. A high-resolution CNN keeps a stride-4 branch the whole way,
   and a transformer backbone adds attention, which a survey of 60+ studies
   credits for transformers leading small-object detection on most datasets
   [M17]. Both keep CenterNet's head and loss unchanged, so any difference
   comes from the backbone.
2. **Anchor-free detectors as a baseline to compare with.** FCOS is the
   standard dense anchor-free detector, and DINO is the strongest anchor-free
   (query-based) detector we could train. Both have published AI-TOD-v2
   results [M23], [M31].
3. **Label-assignment methods as a reference for what fixing the training
   target is worth.** On AI-TOD-v2, RFLA and NWD-RKA lift Faster R-CNN from
   12.8 to 22.6 and 21.4 AP with the same backbone [M23], [M35]. Changing
   CenterNet's target is research direction 1, so these numbers tell us what
   to aim for.

From this we made these criteria. They cover everything issue #2 asks to
record for each candidate [M1], and match the Track B criteria.

| # | Criterion | Why it matters for us | Weight |
|---|---|---|---|
| C1 | **Published results on small objects**: COCO AP_S, and AI-TOD-v2 if available | We need numbers to check our runs against | High |
| C2 | **Code that runs today**: a maintained implementation, pretrained weights, works with a current PyTorch | Without it we spend our time fixing old code instead of running experiments | High |
| C3 | **Fits modest hardware**: training memory, speed | We don't have a large GPU | High |
| C4 | **Output stride**: how fine the grid is that objects are predicted on | Most AI-TOD-v2 objects are 8–16 px, so at stride 8 many cover only one or two cells [M41] | High |
| C5 | **Useful for our research directions**: does it test resolution, attention or the training target? | We want results that explain why detectors fail on tiny objects | Medium |
| C6 | **Effort to run on our datasets** (COCO, AI-TOD-v2) | Less setup work means more time for experiments | Medium |

## 2. CenterNet backbones

None of these combinations has published results; we build them ourselves.
MMDetection's CenterNet head takes exactly one feature map and works out the
output stride from its size [M10], so any backbone works if a neck turns its
outputs into one stride-4 map. MMDetection's HRFPN neck does exactly that: it
upsamples every level to the finest one (stride 4) and merges them [M10]. We
plan to use the same neck for every backbone here, so only the backbone
changes *(untried)*.

### 2.1 Nominee: CenterNet with HRNet-W18

HRNet runs several resolutions in parallel and keeps a branch at 1/4 of the
input size through the whole network [M7]. "W18" is the width of that branch.

All details, with sources, are in
[models/centernet-hrnet-w18/about.md](../../models/centernet-hrnet-w18/about.md),
and how to run it is in [its README](../../models/centernet-hrnet-w18/README.md).
In short:

- no published CenterNet-HRNet results. HRNetV2-W18 in FCOS on COCO: 35.2 AP,
  **AP_S 20.4** [M7]; in Faster R-CNN 36.9 AP with 6.6 GB training memory
  (MMDetection) [M8]
- output stride 4 [M7]
- parameters: **TBD** (Faster R-CNN with HRNetV2-W18 has 26.2 M [M46])
- ImageNet weights in MMDetection; no COCO-trained CenterNet-HRNet exists
  [M8]
- effort is **medium**: we write the config from MMDetection's CenterNet and
  HRNet configs, and train it on COCO and AI-TOD-v2 ourselves

**Strengths:** the cleanest test of "keep the detail": the network keeps a
branch at CenterNet's output resolution from start to end, instead of
recovering it by upsampling, with the same head and loss as the original. HRNet backbones are well tested in MMDetection, and it is used with
a CenterNet-style head in FairMOT [M45].

**Weaknesses:** it doesn't change the training target. At stride 4, 67% of
AI-TOD-v2 objects still get a one-pixel heatmap target [M41]. Without COCO
weights for this combination, our COCO number has nothing to be checked
against.

### 2.2 Runner-up: CenterNet with Swin-T

Swin is a hierarchical transformer: it computes attention inside local
windows and produces feature maps at strides 4, 8, 16 and 32, like a ResNet
[M11].

All details are in
[models/centernet-swin-t/about.md](../../models/centernet-swin-t/about.md),
and how to run it is in [its README](../../models/centernet-swin-t/README.md).
In short:

- no published CenterNet-Swin results on our datasets. Swin-T beats
  ResNet-50 by 3.4–4.2 box AP in four COCO detectors [M11]; Mask R-CNN with
  Swin-T: 42.7 box AP, 7.6 GB (MMDetection) [M12]
- output stride 4 with the HRFPN neck *(untried)*
- 28 M backbone parameters [M11]; full detector **TBD**
- ImageNet weights; COCO configs for RetinaNet and Mask R-CNN in MMDetection
  [M12]
- effort is **medium**: same config work as HRNet; the window size may need
  tuning for 8–16 px objects

**Strengths:** it tests whether attention helps CenterNet on tiny objects
(research direction 4). A CenterNet with a Swin neck for small birds found
that smaller windows (size 2) worked better on small objects [M19], which
gives us a first setting to try.

**Weaknesses:** the evidence for one-stage detectors is against it. On
SODA-A, Swin-T and ConvNeXt-T **lowered** one-stage detectors (Rotated
RetinaNet −3.5 AP) and helped two-stage ones by only 0.1–1.2 points [M18].
It also uses more memory than a ResNet.

**Why it is the runner-up:** HRNet answers the resolution question with less
risk, so it goes first. We suggest putting both on the final shortlist,
because Swin-T is how we test attention, and a negative result would be
useful too.

### 2.3 Reference: CenterNet with Hourglass-104, inference only

The most accurate backbone in the CenterNet paper: two stacked
hourglass modules that downsample and upsample, with stride-4 output [M2].

All details are in
[models/centernet-hourglass104/about.md](../../models/centernet-hourglass104/about.md),
and how to run it is in [its README](../../models/centernet-hourglass104/README.md).
In short:

- COCO val 2017: **40.3 AP** (no augmentation), 42.2 with flip, 45.1 with
  multi-scale [M3]
- output stride 4 [M2]
- 186.44 M parameters [M6]; trained 109 hours on 5 GPUs [M3]
- COCO weights in the official repo [M3]
- effort is **low** for inference: same code, environment and test command
  as CenterNet DLA-34 in Track B [M4]

**Why inference only:** it is too heavy for us to train (C3), but running the
published COCO model shows what CenterNet reaches with its strongest backbone,
and lets us measure its AP on COCO's tiniest objects with AI-TOD's size
ranges. Optionally, we can also run it on AI-TOD-v2 without training, because
COCO's car, bus, truck, boat, person and airplane cover AI-TOD's vehicle,
ship, person and airplane, 97.7% of AI-TOD-v2 objects [M41]. That would mostly
measure the gap between everyday photos and aerial images.

### 2.4 Other backbone options

#### PVTv2-B1

| Property | Value | Source |
|---|---|---|
| Paper / code | [PVT v2](https://arxiv.org/abs/2106.13797) (Wang et al., 2022); MMDetection | [M13], [M14] |
| C1 Results | RetinaNet on COCO: PVTv2-B0 37.1 AP, PVTv2-B1 41.2 AP (MMDetection). Among backbones of 28–35 M parameters, PVTv2 gave the highest AP [M20] | [M14], [M20] |
| C3 Hardware | RetinaNet: B0 7.4 GB, B1 9.5 GB per GPU | [M14] |
| C4 Stride | 4 to 32, like Swin | [M13] |

**Why not chosen:** a second transformer backbone answers the same question
as Swin-T. We keep it as the fallback if Swin-T doesn't fit our GPU, since B0
and B1 are smaller.

#### ConvNeXt-T

| Property | Value | Source |
|---|---|---|
| Paper / code | [A ConvNet for the 2020s](https://arxiv.org/abs/2201.03545) (Liu et al., CVPR 2022); MMDetection, needs MMPreTrain | [M15], [M16] |
| C1 Results | Mask R-CNN on COCO: 46.2 box AP (3x schedule), 7.3 GB | [M16] |

**Why not chosen now:** a modern CNN built with transformer-style design
choices. It is a useful control if Swin-T helps, to tell "attention helps"
apart from "a newer backbone helps". We add it only then.

#### Plain ViT and foundation-model backbones

**Why not chosen:** a plain ViT starts at stride 16, and the survey notes that
larger patches lose the detail small objects need [M17]. A satellite-pretrained
DINOv3 with 7 billion parameters reached only 27.4 AP on AI-TOD-v2, below
smaller specialised detectors [M38].

#### DLA-34 and ResNet-18

**Why not here:** they are Track B's and Track A's CenterNet backbones.

#### CenterNet2 and CenterNet++

**Why not here:** despite the names, they are different detectors from
Objects as Points. CenterNet2 is a two-stage detector that uses a CenterNet
as its first stage [M44], and CenterNet++ detects objects as keypoint
triplets (a centre and two corners), run with Hourglass, HRNet and Swin
backbones [M43].

## 3. Anchor-free detectors

### 3.1 Nominee: FCOS with ResNet-50 and FPN

Every location on the FPN levels predicts a class, the distances to the four
box sides, and a centre-ness score [M21].

All details are in
[models/fcos-r50-fpn/about.md](../../models/fcos-r50-fpn/about.md), and how
to run it is in [its README](../../models/fcos-r50-fpn/README.md). In short:

- COCO minival: 37.1 AP, **AP_S 21.3** (paper) [M21]; 36.6 AP in
  MMDetection [M22]
- AI-TOD-v2: **13.4 AP, AP_vt 2.5, AP_t 12.4**; with RFLA 15.6 AP,
  AP_vt 4.4 [M23]
- FPN levels with strides 8 to 128, so the finest is 8. RFLA's code also has
  a version with a stride-4 level (P2) [M21], [M23]
- 3.6 GB training memory (MMDetection) [M22]
- effort is **low**: AI-TOD-v2 configs exist with and without P2 and RFLA
  [M23]

**Strengths:** the standard anchor-free baseline, with published results on
AI-TOD-v2. With and without the stride-4 level, it isolates the effect of
output resolution: on AI-TOD (v1), adding P2 raises AP_vt from 2.3 to 6.0
[M23].

**Weaknesses:** weak on AI-TOD-v2 (13.4 AP). Its stride-4 version has no
published AI-TOD-v2 result, so we would measure it ourselves.

### 3.2 Runner-up: DINO with ResNet-50

A DETR-style detector: a transformer decoder turns 900 learned queries into
boxes, with no anchors and no non-maximum suppression [M29], [M30].

All details are in [models/dino-r50/about.md](../../models/dino-r50/about.md),
and how to run it is in [its README](../../models/dino-r50/README.md). In
short:

- COCO val 2017: 49.0 AP (4 scales, 12 epochs, MMDetection) [M30]
- AI-TOD-v2: **25.9 AP, AP_vt 12.7, AP_t 25.3**, re-implemented by the
  DQ-DETR authors. Better than any CNN detector in that table, including
  DetectoRS with RFLA (25.7) [M31]
- feature levels with strides 8 to 64, so the finest is 8 [M30]
- training memory **TBD**; DQ-DETR trained with batch 1 on RTX 3090 GPUs
  "due to memory constraints" [M31]
- effort is **medium**: COCO config and weights in MMDetection; AI-TOD-v2
  config is ours to write

**Strengths:** the strongest anchor-free detector we could train, and the
base of the best published detectors on AI-TOD-v2 (DQ-DETR 30.2 AP [M31],
Dome-DETR [M32]). It is our transformer reference point for the whole
detector, not just the backbone.

**Weaknesses:** heavy to train. It drops the stride-4 feature map to save
memory, which a recent paper shows hurts tiny objects: bringing it back adds
1.4 AP on AI-TOD-v2 [M33]. Its 900 queries cap the detections per image,
which leaves 1.2% of AI-TOD-v2 test objects out of reach [M47].

**Why it is the runner-up:** FCOS is cheaper and its stride-4 version tests
our resolution question directly, so it goes first. DINO shows how far a
CenterNet-based detector is from the state of the art; we suggest adding it
if the GPU allows.

### 3.3 Other anchor-free options

#### TTFNet

| Property | Value | Source |
|---|---|---|
| Paper / code | [TTFNet](https://arxiv.org/abs/1909.00700) (Liu et al., AAAI 2020); official repo on an early MMDetection (reported as v1.0rc0, **TBD** confirm) | [M25], [M26], [M27] |
| What it changes | CenterNet's training target: an elliptical Gaussian that scales with the box (α = 0.54), and box regression from every pixel in a Gaussian sub-area (β = 0.54) with a GIoU loss. Output stride 4 | [M25] |
| C1 Results | COCO: TTFNet-18 28.1 AP, AP_S 11.8, trained in 3.6 h vs 26.9 h for CenterNet-R18 at the same AP; TTFNet-53 35.1 AP, AP_S 17.0. No AI-TOD-v2 results | [M25] |
| C2 Code | MMDetection versions before 2.3 compiled their own CUDA operators, later moved to MMCV, so the code needs an old PyTorch and CUDA setup | [M28] |

**Why not chosen as a detector:** running it means porting its head, neck and
target code to our MMDetection version and reproducing its COCO result, a few
days of work *(est.)*. What matters for us is its training target, which is
our research direction 1. So we plan to add the elliptical Gaussian and the
Gaussian-area regression as an option in MMDetection's CenterNet head, and
compare it with the original target on the same backbone. That belongs to the
improvement phase, not the baselines.

#### CenterNet Update, RepPoints, FoveaBox, YOLO

**Why not here:** CenterNet Update is Track B's runner-up and YOLO is in
Track A. RepPoints and FoveaBox are in the NWD-RKA benchmark [M34] but add no
question that FCOS doesn't already answer.

## 4. Tiny-object label assignment

Both methods replace IoU when deciding which locations learn from which
object, since IoU drops to zero for tiny boxes that are only a few pixels off
[M24], [M34]. Neither has been applied to CenterNet's heatmap, which is one of
our candidate improvements.

### 4.1 Nominee: RFLA on Faster R-CNN (ResNet-50, FPN)

RFLA models each location's receptive field and each object as 2-D Gaussians,
and assigns locations to objects by the distance between them [M24].

All details are in
[models/faster-rcnn-r50-fpn-rfla/about.md](../../models/faster-rcnn-r50-fpn-rfla/about.md),
and how to run it is in [its README](../../models/faster-rcnn-r50-fpn-rfla/README.md).
In short:

- AI-TOD-v2: **22.6 AP, AP_vt 8.6, AP_t 21.7**, up from 12.8 AP without it
  [M23]. On DetectoRS: 25.7 AP [M23]
- FPN levels with strides 4 to 64, so the finest is 4 [M23]
- trained on one RTX 3090, batch 2, 12 epochs [M24]
- effort is **low**: official AI-TOD-v2 configs, in its own MMDetection 2.13.0
  [M23]

**Strengths:** the best published label assignment for our dataset at a size
we can train, and it plugs into FCOS as well (15.6 AP on AI-TOD-v2), so it
links our anchor-free and two-stage baselines [M23].

**Weaknesses:** its code is on an old MMDetection (2.13.0) that needs a
separate environment [M23]. Which pretrained models its download link holds
is **TBD**.

### 4.2 Runner-up: NWD-RKA on Faster R-CNN (ResNet-50, FPN)

NWD-RKA compares boxes as 2-D Gaussians with a normalised Wasserstein
distance and assigns positives by ranking instead of a fixed threshold [M34].

All details are in
[models/faster-rcnn-r50-fpn-nwdrka/about.md](../../models/faster-rcnn-r50-fpn-nwdrka/about.md),
and how to run it is in [its README](../../models/faster-rcnn-r50-fpn-nwdrka/README.md).
In short:

- AI-TOD-v2: **21.4 AP, AP_vt 7.7, AP_t 20.7** [M35]. On DetectoRS: 24.7 AP
  [M31]
- same FPN levels, 800×800 input, batch 2 and 12 epochs as RFLA [M35]
- effort is **low**: it uses mmdet-aitod, the same code and environment as
  Track B's Faster R-CNN on AI-TOD-v2 [M35]

**Strengths:** the paper that introduced AI-TOD-v2, with its training log
inside the config file, so we know exactly what to expect [M35].

**Weaknesses:** on Faster R-CNN, a little below RFLA in every size range
(21.4 vs 22.6 AP overall).

**Why it is the runner-up:** RFLA scores higher and also works on FCOS. If
RFLA's environment won't install, NWD-RKA runs in the environment Track B
already needs.

### 4.3 Other label-assignment options

#### DotD

**Why not chosen:** included in mmdet-aitod, but below both RFLA and NWD-RKA
on AI-TOD-v2 (20.4 AP) [M31].

#### SimD and M-CenterNet

**Why not chosen:** SimD reports results on AI-TOD (v1) only, as far as we
checked, and M-CenterNet (the multi-centre CenterNet from the AI-TOD paper,
14.5 AP on AI-TOD) has no code we could find [M37].

## 5. Comparison

✅ = meets the criterion, ⚠️ = partly, ❌ = does not, ❓ = unknown.

**CenterNet backbones**

| Criterion | **HRNet-W18** (nominee) | **Swin-T** (runner-up) | PVTv2-B1 | **Hourglass-104** (reference) |
|---|---|---|---|---|
| C1 Published small-object results | ⚠️ FCOS-HRNet AP_S 20.4; none with CenterNet | ❌ None with CenterNet | ❌ None with CenterNet | ⚠️ COCO AP only |
| C2 Code that runs today | ✅ Parts in MMDetection 3.x | ✅ Parts in MMDetection 3.x | ✅ Parts in MMDetection 3.x | ❌ PyTorch 0.4.1 + DCNv2 |
| C3 Fits modest hardware | ❓ Memory TBD | ❓ Memory TBD | ❓ Memory TBD | ✅ Inference only |
| C4 Output stride | ✅ 4 | ✅ 4 (with HRFPN) | ✅ 4 (with HRFPN) | ✅ 4 |
| C5 Research directions | ✅ Resolution | ✅ Attention | ⚠️ Same as Swin-T | ⚠️ Upper reference |
| C6 Effort on our datasets | ⚠️ Medium, our config | ⚠️ Medium, our config | ⚠️ Medium | ✅ Low (COCO) |

**Comparison detectors**

| Criterion | **FCOS R50-FPN** (nominee) | **DINO R50** (runner-up) | **Faster R-CNN + RFLA** (nominee) | **Faster R-CNN + NWD-RKA** (runner-up) |
|---|---|---|---|---|
| C1 Published small-object results | ✅ COCO AP_S; AI-TOD-v2 13.4 | ✅ AI-TOD-v2 25.9 (re-implemented) | ✅ AI-TOD-v2 22.6 | ✅ AI-TOD-v2 21.4 |
| C2 Code that runs today | ✅ MMDetection 3.x; mmdet-rfla | ✅ MMDetection 3.x | ⚠️ MMDetection 2.13.0 | ⚠️ MMDetection 2.24.1 |
| C3 Fits modest hardware | ✅ 3.6 GB | ❓ TBD, heavy | ✅ One RTX 3090 | ✅ One RTX 3090 |
| C4 Output stride | ⚠️ 8 (4 with P2) | ⚠️ 8 | ✅ FPN from 4 | ✅ FPN from 4 |
| C5 Research directions | ✅ Resolution (± P2) | ✅ Transformer reference | ✅ Training target | ✅ Training target |
| C6 Effort on our datasets | ✅ Low, configs exist | ⚠️ Medium | ✅ Low, configs exist | ✅ Low, configs exist |

## 6. Decision

**CenterNet backbone: HRNet-W18.**

1. **It keeps a stride-4 branch through the whole network**, the same
   resolution as CenterNet's output, so it tests whether keeping the detail
   helps (research direction 2).
2. **It changes only the backbone.** The head and loss stay as in the paper,
   so the result is comparable with Track B's DLA-34.
3. **All parts exist in MMDetection 3.x**, with ImageNet weights.

The main risk is that the combination is ours: no one has published it, so
our first COCO run has nothing to be checked against. We check our
MMDetection CenterNet setup first with its ResNet-18 config, which has a
published result (29.5 AP [M9]).

**CenterNet runner-up: Swin-T.** It tests attention instead of resolution.
SODA-A shows Swin-T hurting one-stage detectors, so we expect it may not help;
either result answers research direction 4. We suggest putting both
backbones on the final shortlist.

**Reference: Hourglass-104, inference only.** The published COCO model, as an
upper reference for CenterNet.

**Anchor-free detector: FCOS with ResNet-50 and FPN**, with and without the
stride-4 level. Published AI-TOD-v2 results, low memory, and the stride-4
version tests resolution in a second detector family.

**Anchor-free runner-up: DINO with ResNet-50.** The strongest anchor-free
detector at a size we could train, and the base of the best published
AI-TOD-v2 detectors. Its memory needs checking first.

**Label assignment: RFLA on Faster R-CNN**, runner-up **NWD-RKA**. Their
published AI-TOD-v2 numbers are the first thing we reproduce: if our
Faster R-CNN with RFLA reaches 22.6 AP, our AI-TOD-v2 data, training and
evaluation are set up correctly.

**Framework:** MMDetection 3.x (3.3.0 is its latest release, from January
2024 [M39]) for the CenterNet backbones, FCOS and DINO, in the `openmmlab`
environment Track B already uses. RFLA keeps its own
MMDetection 2.13.0 (a new `rfla` environment) and NWD-RKA uses mmdet-aitod
(Track B's `aitod` environment), so we can reproduce their published numbers
exactly. Every model writes its AI-TOD-v2 predictions in COCO format (MMDetection 3.x
can save them with its `format_only` option [M40]), and we score all of them with the same AI-TOD evaluation (cocoapi-aitod [M36]), so
the framework doesn't affect the numbers.

**One setting to change for every model on AI-TOD-v2:** the number of
detections kept per image. MMDetection's CenterNet keeps 100 [M9], but 6.7%
of AI-TOD-v2 test images have more than 100 objects, which puts 26.1% of all
test objects out of reach [M47]. The AI-TOD evaluation counts up to 1,500
detections per image [M35], and RFLA keeps up to 3,000 [M23]. We set every
model to at least 1,500. This also applies to the official CenterNet code
(Track B's DLA-34 and our Hourglass-104): it keeps 100 detections, set both
by the `--K` option and in the detector code, and for training it uses only
the first 128 objects of each image, which leaves out 20.1% of AI-TOD-v2 trainval objects at full image
size [M5], [M47].

We would change the decision if:
- the HRNet or Swin config doesn't train well in MMDetection's CenterNet
  (then we use CenterNet's own deconvolution neck on the backbone's last
  level, as MMDetection does for ResNet-18 [M9])
- DINO doesn't fit our GPU (then we drop it and keep FCOS only)
- RFLA's environment won't install (then NWD-RKA only)

## 7. Open items

- [ ] Write and test the CenterNet-HRNet-W18 and CenterNet-Swin-T configs
      (HRFPN neck, one stride-4 output). Measure parameters, FLOPs and
      training memory.
- [ ] Reproduce MMDetection's CenterNet ResNet-18 result (29.5 AP) to check
      the setup before the new backbones.
- [ ] Write an AI-TOD-v2 dataset config for MMDetection 3.x and a script that
      scores its COCO-format predictions with cocoapi-aitod (shared with
      Track B).
- [ ] Find DINO's training memory, and check whether its feature levels can
      start at stride 4.
- [ ] Find which pretrained models RFLA's download link holds.
- [ ] Check which test option gives the 40.3 AP for Hourglass-104
      (`--fix_res` in the getting-started guide, `--keep_res` in the
      training script).
- [ ] Confirm the early MMDetection version TTFNet is built on.
- [ ] Read the SODA paper's backbone section in full.

## 8. Sources

- [M1] Issue #2, *Select representative models for initial dataset evaluation* — <https://github.com/Ikkjo/tiny-object-detection/issues/2>
- [M2] Zhou et al., *Objects as Points* (CenterNet) — <https://arxiv.org/abs/1904.07850>
- [M3] CenterNet model zoo — <https://github.com/xingyizhou/CenterNet/blob/master/readme/MODEL_ZOO.md>
- [M4] CenterNet getting started guide — <https://github.com/xingyizhou/CenterNet/blob/master/readme/GETTING_STARTED.md>
- [M5] CenterNet code: test options (`--K`, default 100), detector (`max_per_image = 100`) and COCO dataset class (`max_objs = 128`) — <https://github.com/xingyizhou/CenterNet/blob/master/src/lib/opts.py>, <https://github.com/xingyizhou/CenterNet/blob/master/src/lib/detectors/base_detector.py>, <https://github.com/xingyizhou/CenterNet/blob/master/src/lib/datasets/dataset/coco.py>
- [M6] *Corner2Net: Detecting Objects as Cascade Corners* (comparison table with parameter counts) — <https://arxiv.org/abs/2411.15772>
- [M7] Wang et al., *Deep High-Resolution Representation Learning for Visual Recognition* (HRNet; FCOS results run with MMDetection) — <https://arxiv.org/abs/1908.07919>
- [M8] MMDetection HRNet configs and results — <https://github.com/open-mmlab/mmdetection/tree/main/configs/hrnet>
- [M9] MMDetection CenterNet configs and results — <https://github.com/open-mmlab/mmdetection/tree/main/configs/centernet>
- [M10] MMDetection code: HRFPN neck and CenterNet head — <https://github.com/open-mmlab/mmdetection/blob/main/mmdet/models/necks/hrfpn.py>, <https://github.com/open-mmlab/mmdetection/blob/main/mmdet/models/dense_heads/centernet_head.py>
- [M11] Liu et al., *Swin Transformer: Hierarchical Vision Transformer using Shifted Windows* — <https://arxiv.org/abs/2103.14030>
- [M12] MMDetection Swin configs and results — <https://github.com/open-mmlab/mmdetection/tree/main/configs/swin>
- [M13] Wang et al., *Pyramid Vision Transformer* (ICCV 2021) — <https://openaccess.thecvf.com/content/ICCV2021/papers/Wang_Pyramid_Vision_Transformer_A_Versatile_Backbone_for_Dense_Prediction_Without_ICCV_2021_paper.pdf>; *PVT v2* — <https://arxiv.org/abs/2106.13797>
- [M14] MMDetection PVT configs and results — <https://github.com/open-mmlab/mmdetection/tree/main/configs/pvt>
- [M15] Liu et al., *A ConvNet for the 2020s* (ConvNeXt) — <https://arxiv.org/abs/2201.03545>
- [M16] MMDetection ConvNeXt configs and results — <https://github.com/open-mmlab/mmdetection/tree/main/configs/convnext>
- [M17] Rekavandi et al., *Transformers in Small Object Detection: A Benchmark and Survey of State-of-the-Art* (ACM Computing Surveys 2025) — <https://arxiv.org/abs/2309.04902>
- [M18] Cheng et al., *Towards Large-Scale Small Object Detection: Survey and Benchmarks* (SODA; backbone comparison on SODA-A) — <https://arxiv.org/abs/2207.14096>
- [M19] Huo et al., *Small Object Detection for Birds with Swin Transformer* (CenterNet with a Swin backbone and neck) — <https://arxiv.org/abs/2511.22310>
- [M20] Song et al., *An Extendable, Efficient and Effective Transformer-based Object Detector* (ViDT+; Swin vs PVTv2 backbones) — <https://arxiv.org/abs/2204.07962>
- [M21] Tian et al., *FCOS: Fully Convolutional One-Stage Object Detection* — <https://arxiv.org/abs/1904.01355>
- [M22] MMDetection FCOS configs and results — <https://github.com/open-mmlab/mmdetection/tree/main/configs/fcos>
- [M23] mmdet-rfla repository (results tables, AI-TOD-v2 configs, MMDetection 2.13.0) — <https://github.com/Chasel-Tsui/mmdet-rfla>
- [M24] Xu et al., *RFLA: Gaussian Receptive Field based Label Assignment for Tiny Object Detection* — <https://arxiv.org/abs/2208.08738>
- [M25] Liu et al., *Training-Time-Friendly Network for Real-Time Object Detection* (TTFNet) — <https://arxiv.org/abs/1909.00700>
- [M26] TTFNet repository — <https://github.com/ZJULearning/ttfnet>
- [M27] TTFNet project summary listing version v1.0rc0 (secondary) — <https://kandi.openweaver.com/python/ZJULearning/ttfnet>
- [M28] MMDetection 2.x changelog: v2.3 moved the CUDA operators to MMCV (as reproduced by Safety DB) — <https://data.safetycli.com/packages/pypi/mmdet/changelog?page=9>
- [M29] Zhang et al., *DINO: DETR with Improved DeNoising Anchor Boxes for End-to-End Object Detection* — <https://arxiv.org/abs/2203.03605>
- [M30] MMDetection DINO configs and results — <https://github.com/open-mmlab/mmdetection/tree/main/configs/dino>
- [M31] Huang et al., *DQ-DETR: DETR with Dynamic Query for Tiny Object Detection* (AI-TOD-v2 table with DINO, DotD, NWD-RKA, RFLA) — <https://arxiv.org/abs/2404.03507>
- [M32] Hu et al., *Dome-DETR* — <https://arxiv.org/abs/2505.05741>
- [M33] Wang et al., *Reviving the Discarded High-Resolution Feature for Transformer-Based Tiny Object Detection* (ReDHF) — <https://arxiv.org/abs/2611.07994>
- [M34] Xu et al., *Detecting tiny objects in aerial images: A normalized Wasserstein distance and a new benchmark* (NWD-RKA, AI-TOD-v2) — <https://arxiv.org/abs/2206.13996>
- [M35] mmdet-aitod repository (MMDetection 2.24.1): NWD-RKA config with its training log, and the AI-TOD-v2 evaluation (up to 1,500 detections per image) — <https://github.com/Chasel-Tsui/mmdet-aitod/blob/main/mmdet-nwdrka/configs_nwdrka/nwd_rka/aitodv2_faster_r50_nwdrka_1x.py>, <https://github.com/Chasel-Tsui/mmdet-aitod/blob/main/mmdet-nwdrka/mmdet/datasets/aitodv2.py>
- [M36] cocoapi-aitod (AI-TOD evaluation) — <https://github.com/jwwangchn/cocoapi-aitod>
- [M37] Shi et al., *Similarity Distance-Based Label Assignment for Tiny Object Detection* (SimD; M-CenterNet on AI-TOD) — <https://arxiv.org/abs/2407.02394>
- [M38] Zhao et al., *Bridging the Scale Gap* (ScaleBridge-Det; AI-TOD-v2 comparison table) — <https://arxiv.org/abs/2512.01665>
- [M39] MMDetection releases (3.3.0, 5 January 2024) — <https://pypi.org/project/mmdet/>
- [M40] MMDetection config guide (saving test results as COCO JSON with `format_only` and `outfile_prefix`) — <https://github.com/open-mmlab/mmdetection/blob/main/docs/en/user_guides/config.md>
- [M41] Our aerial dataset notes (AI-TOD-v2 measurements) — [docs/datasets/aerial-dataset.md](../datasets/aerial-dataset.md)
- [M42] Our paper log — [docs/literature/paper-log.md](../literature/paper-log.md)
- [M43] Duan et al., *CenterNet++ for Object Detection* — <https://arxiv.org/abs/2204.08394>
- [M44] Zhou et al., *Probabilistic two-stage detection* (CenterNet2) — <https://arxiv.org/abs/2103.07461>
- [M45] FairMOT repository (HRNet-W18 option with a CenterNet-style head) — <https://github.com/ifzhang/FairMOT>
- [M46] HRNet object detection repository (Faster R-CNN with HRNetV2-W18) — <https://github.com/HRNet/HRNet-Object-Detection>
- [M47] Our script [`scripts/detection_cap_stats.py`](../../scripts/detection_cap_stats.py), run on the AI-TOD-v2 test annotations
