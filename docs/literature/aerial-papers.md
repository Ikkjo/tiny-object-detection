# Aerial tiny-object detection: paper review

These are our notes on papers about tiny objects in drone, aerial and
satellite images, and how each paper connects to the research directions in
[CLAUDE.md](../../CLAUDE.md). This is part of issue #1. The facts about each
dataset and our choice of dataset are in
[`aerial-dataset.md`](../datasets/aerial-dataset.md), and the datasets and
models each paper uses are listed in [`paper-log.md`](paper-log.md).

Every number has a source, listed in [section 6](#6-sources). **TBD** means
we haven't checked it against a primary source yet, and *(est.)* means we
derived the number ourselves. "Tiny" means under 16 px (the AI-TOD
definition) unless a row says otherwise, and COCO's "small" means under
32×32 px.

## Short answer

- **The aerial tiny-object literature is dominated by one group and one
  benchmark.** Wuhan University (Xia, Yang, Xu, Wang) built AI-TOD and
  AI-TOD-v2 and proposed DotD, NWD-RKA and RFLA on them [S4], [S5], [S6],
  [S7]. Most recent tiny-object methods report on AI-TOD-v2 (NWD-RKA,
  DQ-DETR, Dome-DETR, Point Teacher, ScaleBridge-Det), often alongside
  VisDrone [S5], [S15], [S16], [S21], [S25].
- **Their central claim matches research direction D1.** IoU-based label assignment
  gives tiny objects few or no positive samples, so the training signal for
  them is weak. DotD, NWD and RFLA all replace IoU with a softer,
  distance-based or Gaussian similarity [S4], [S5], [S6]. RFLA is one of the key papers listed in CLAUDE.md.
- **CenterNet has been tried on aerial data, but rarely as a modern
  baseline.** M-CenterNet (a multi-centre CenterNet from the AI-TOD paper)
  scores 14.5 AP on AI-TOD [S3], [S8]. CenterNet and CornerNet trail
  anchor-based detectors on SODA-D, especially on the smallest objects [S11].
  YOLC builds on CenterNet for VisDrone [S10]. Satellite-video detectors
  (DSFNet, HiEUM) reuse the CenterNet code or head [S13], [S14].
- **Our own check of the CenterNet code shows why it struggles.** With the
  default output stride of 4, a square object of 12 px or less (and an
  8×16 px vehicle) gets a heatmap Gaussian of radius 0: one positive pixel and
  no soft neighbourhood
  ([section 4](#4-our-analysis-centernet-targets-for-tiny-objects)). This is the "positive signal never arrives" problem behind D1. On AI-TOD-v2 it
  affects 67% of objects (measured; see
  [`aerial-dataset.md`](../datasets/aerial-dataset.md)).
- **Dataset choice:** we chose AI-TOD-v2, with VisDrone as the runner-up. The
  comparison is in [`aerial-dataset.md`](../datasets/aerial-dataset.md).

## 1. Research directions

The project starts from point-based detectors (CornerNet, CenterNet) and asks
which of their design choices break for tiny objects. The research directions
are listed in [CLAUDE.md](../../CLAUDE.md). Each paper below is tagged with
the ones it touches:

| Tag | Direction | Question |
|---|---|---|
| **D1** | Loss and label assignment | CenterNet has one positive pixel per object, so the negative term dominates. Can the target be relaxed for tiny objects (wider Gaussian, "anywhere inside the box", receptive-field-based assignment as in RFLA)? |
| **D2** | Low-res grid → pixels | Centres are found on a downsampled grid and corrected with an offset. Is this the bottleneck for tiny objects? |
| **D3** | Multi-scale | Detect at several resolutions in parallel and merge. |
| **D4** | Backbone | Is the point formulation tied to CNN receptive fields? Can transformers fit it? |
| **D5** | Weak supervision | Can a less prescriptive training signal generalise better on tiny objects? |

Two leads are still open (see CLAUDE.md): a CenterNet-based satellite-video
paper whose loss lets the predicted point fall anywhere inside the box (title
to be confirmed), and a satellite-video dataset (details to be confirmed).

## 2. Datasets

The datasets these papers use are compared, with measured statistics, in
[`aerial-dataset.md`](../datasets/aerial-dataset.md). Two facts from the papers
matter for reading the results below:

- **AI-TOD is not independent of the others.** It is built from DOTA, xView,
  VisDrone, Airbus-Ship and DIOR [S5], and more than 88% of its instances
  are vehicles [S11].
- **AI-TOD-v2 fixes missing labels.** The authors added over 50,000 missed
  objects found by inspecting their detector's false positives [S5]. For a
  loss-function study this matters: on AI-TOD v1, a "false positive" may be a
  real but unlabelled vehicle.

## 3. Method papers, grouped by direction

### 3.1 Loss and label assignment for tiny objects (D1)

| Paper | Idea | Datasets | Why it matters to us |
|---|---|---|---|
| **DotD** — Dot Distance, CVPRW 2021 [S4] | Replace IoU with a normalised Euclidean distance between box centres for assignment and NMS | AI-TOD | The simplest "match by centre distance" idea; close to what a point-based detector does anyway |
| **NWD-RKA** — Normalized Wasserstein Distance, ISPRS J. 2022 [S5] | Model each box as a 2-D Gaussian (mean = centre, covariance from w, h) and compare boxes with a normalised Wasserstein distance. RKA then takes the top-k anchors (k = 2) per object as positives, with no IoU threshold | AI-TOD, AI-TOD-v2, VisDrone2019, DOTA-v2.0 | Explains why IoU fails: it is very sensitive to small shifts for tiny boxes and is 0 for non-overlapping boxes, so tiny objects get too few positives. Introduces AI-TOD-v2. DetectoRS + NWD-RKA: 24.7 AP on AI-TOD-v2 |
| **RFLA** — Gaussian receptive-field label assignment, ECCV 2022 [S6] | Model each feature point's effective receptive field as a Gaussian, measure its distance to the box Gaussian (KL or Wasserstein), assign the top-k, then a second pass with a smaller radius for objects still short of positives | AI-TOD, TinyPerson, VisDrone2019, DOTA-v2.0 | **Listed as a key paper in CLAUDE.md.** Directly about the receptive field and the "outlier" tiny objects that get no positive location. Ablation on AI-TOD: baseline 11.1 AP → 21.1 AP with RFD + HLA. Trained on **one RTX 3090**, MMDetection, 12 epochs, batch 2 |
| **SimD** — Similarity Distance, 2024 [S8] | Another similarity metric for assignment, normalised by object size | AI-TOD (others **TBD**) | Recent follow-up; its AI-TOD table is the clearest place to see M-CenterNet's numbers |

**Open question for D1:** all four target anchor-based or FCOS-style
detectors, where assignment decides which anchors or locations are positive.
In CenterNet the equivalent knob is the heatmap target itself (Gaussian radius
and the focal-loss penalty reduction). Nobody in this list applies a
Gaussian-distance assignment to CenterNet's heatmap. That gap is a possible
contribution (**TBD**: a deeper search is needed to confirm).

### 3.2 CenterNet and point-based detectors on aerial data (D1, D2)

| Paper | What it reports | Source |
|---|---|---|
| **M-CenterNet** (in the AI-TOD paper, ICPR 2020) | "Multiple center points based learning network" to improve localisation of tiny objects. On AI-TOD: 14.5 AP, 40.7 AP50, 6.1 AP very-tiny, 15.0 AP tiny (DLA-34). How the multiple centres work: **TBD** (paper is behind IEEE access) | [S3], [S8] |
| **SODA benchmark** (TPAMI 2023) | On SODA-D, CenterNet 21.5 AP (5.1 AP extremely small) and CornerNet 24.6 AP (6.5), below RepPoints 28.0 and anchor-based methods; the authors note the gap is largest on the smallest objects. No CenterNet on SODA-A | [S11] |
| **VisDrone challenge paper** | CornerNet (Hourglass-104): 23.43 AP on test-dev. CenterNet variants appear among challenge entries: RRNet 29.13 AP (2019), MSC-CenterNet 31.13 AP (2020). Best 2020 entry: 34.57 AP (Cascade R-CNN based) | [S9] |
| **CenterNet on VisDrone** (arXiv 2019) | Applies CenterNet to VisDrone2019 with several backbones and training/test resolutions; a direct starting point for our baseline. Numbers **TBD** | [S17] |
| **YOLC** (IEEE T-ITS 2024) | CenterNet-based. Adds a module that finds dense clusters and zooms into them (D3), changes the box regression loss to a Gaussian Wasserstein distance (D1), adds deformable conv to the head. VisDrone2019 and UAVDT. Code available | [S10] |

**Takeaway:** CenterNet works on drone imagery once someone changes the
target, the regression loss or the input scale. On the dedicated tiny
benchmarks, plain CenterNet is rarely reported, so our own CenterNet baseline
on AI-TOD-v2 would itself be a useful data point.

### 3.3 Satellite video (D1, D5)

| Paper | Relevance | Source |
|---|---|---|
| **VISO** benchmark (TGRS 2021) | Dataset plus a non-learning motion baseline (multi-frame differencing and matrix completion) | [S12] |
| **DSFNet** (IEEE GRSL 2022) | Two-stream network (2-D static + 3-D motion backbone); the code is "highly borrowed from CenterNet"; data is part of VISO | [S13], [S28] |
| **HiEUM** (arXiv 2024) | **Unsupervised:** pseudo-labels from a traditional method, updated during training; a sparse head inspired by CenterNet predicts centres, sizes and offsets; 98.8 fps at 1024×1024. Reported F1: DSFNet 74.4%, HiEUM's supervised variant 82.1% (unsupervised score **TBD**) | [S14] |
| **Frame difference + CenterNet** (Sensors 2025) | CenterNet baseline plus frame-difference input and a self-reconstruction branch for tiny objects; notes that small centre offsets wreck IoU for these targets | [S18] |
| **Deep Vehicle Detection in Satellite Video** (arXiv 2022) | Vehicles are 4–10 px; argues single frames are not enough and uses motion; outputs a heatmap | [S19] |

HiEUM is the closest public match to the satellite-video lead in CLAUDE.md
(training labels produced by another method, CenterNet-style head), but it is
not that paper; its title is still to be confirmed.

### 3.4 Weak and point supervision (D5)

| Paper | Idea | Source |
|---|---|---|
| **P2BNet** (ECCV 2022) | Train a detector from one point per object: generate box proposals around each point, refine them with multiple-instance learning | [S20] |
| **Point Teacher** (arXiv 2024) | Point-supervised detection built for tiny aerial objects: a teacher turns noisy points into pseudo-boxes, then multiple-instance learning picks the best. Tested on AI-TOD-v2, SODA-A, TinyPerson. Claims performance comparable to box supervision and robustness to shifted points; reports that P2BNet does very poorly on AI-TOD-v2 | [S21] |
| **PointOBB** (CVPR 2024) | Point supervision for oriented boxes (DIOR-R, DOTA-v1.0) | [S22] |

This is the cleanest bridge between the weak-supervision direction (D5) and
point-based detection: for tiny objects a box is barely more informative than
a point.

### 3.5 Large images, slicing and efficiency (D3)

- **SAHI** (ICIP 2022): slice large images into overlapping tiles for
  inference and fine-tuning, then merge. On VisDrone and xView, sliced
  inference adds 6.8 / 5.1 / 5.3 AP to FCOS / VFNet / TOOD, and 12.7 / 13.4 /
  14.5 AP with sliced fine-tuning. Works with MMDetection and YOLO [S23].
  Almost certainly needed for SODA-A, xView and VISO frame sizes.
- **CEASC** (CVPR 2023): sparse convolution in the detection head so compute
  goes to foreground; plugs into RetinaNet and GFL on VisDrone and UAVDT;
  MMDetection code [S24].

### 3.6 Transformers and foundation models (D4)

- **DQ-DETR** (ECCV 2024): DETR with a counting module that sets the number
  and position of queries per image; 30.2 AP on AI-TOD-v2. Motivation: some
  AI-TOD-v2 images have over 1,500 objects, others under 10, so a fixed query
  count fails [S15].
- **Dome-DETR** (ACM MM 2025): density-guided query and feature
  manipulation; claims state of the art with +3.3 AP on AI-TOD-v2 and +2.5
  AP on VisDrone [S16].
- **ScaleBridge-Det** (arXiv 2025): a 2–3 B parameter detector; 35.7 AP on
  AI-TOD-v2. Its comparison table shows YOLOv11-M at 30.5 AP and a
  satellite-pretrained DINOv3 ViT-7B at 27.4 AP, with only its last two
  blocks trainable [S25]. Read as: a generic modern detector is competitive
  with specialised tiny-object methods, and a mostly frozen self-supervised
  foundation model does not solve tiny objects by itself.

### 3.7 Surveys

- **Towards Large-Scale Small Object Detection** (SODA, TPAMI 2023): survey
  plus SODA-D/SODA-A benchmarks. Groups methods into six families:
  sample-oriented (augmentation, label assignment), scale-aware, attention,
  feature imitation (similarity learning, super-resolution), context
  modelling, and focus-and-detect [S11]. Good structure for our own
  related-work section.
- **Remote Sensing Object Detection Meets Deep Learning** (meta-review, 2023):
  treats tiny objects as one of five remote-sensing challenges [S26].

### 3.8 Benchmark comparisons on satellite imagery

| Paper | What it does | Datasets | Models compared | Notes |
|---|---|---|---|---|
| **Analysis of Object Detection Models for Tiny Object in Satellite Imagery** (arXiv 2024) [S1] | Builds a 3,000-image, 3-class COCO-format set (cars, ships, airplanes: about 2,000 images sampled from AI-TOD-v2 plus about 1,000 640×640 tiles of the Airbus Aircraft dataset) and benchmarks MMDetection models on it; tiny means under 32×32 px | Custom mix ("SkyFusion"); SAT-MTB for a tracking demo | Faster R-CNN, RetinaNet, FCOS, VarifocalNet, FoveaBox, RTMDet-T/S/M/L, DDOD, DetectoRS (R50/R101-FPN) | Best: DDOD R50-FPN 0.339 mAP; Faster R-CNN last at 0.103. All runs on a Colab T4. Writes out each detector's loss. No CenterNet; results not comparable with published AI-TOD-v2 numbers |
| **An Empirical Study of Methods for Small Object Detection from Satellite Imagery** (arXiv 2025) [S2] | Compares four detectors on cars in xView and on bee boxes (about 5–8 px) in SkySat imagery | xView (cars, 0.3 m GSD), SkySat (30 images, 0.5 m GSD) | YOLOv11, SSD, Faster R-CNN, Cascade R-CNN | xView: Cascade R-CNN 0.49 mAP50, YOLOv11 0.25, SSD 0.00. In v1 several tables and the conclusion are empty, and Cascade R-CNN is called both anchor-free and anchored |

## 4. Our analysis: CenterNet targets for tiny objects

The guiding question in CLAUDE.md is what each loss term does when the object is only a few pixels wide. We checked the official CenterNet code [S29], [S30]:

- The heatmap is predicted at input size divided by `down_ratio`, default
  **4**.
- Each object's Gaussian radius is
  `max(0, int(gaussian_radius((ceil(h), ceil(w)))))`, with box size measured
  **on the output grid** and `min_overlap = 0.7`. Sigma is
  `(2·radius + 1) / 6`.
- The centre is truncated to an integer cell, and the offset head regresses
  the remainder (`reg = ct − ct_int`). Default loss weights: heatmap 1, size
  0.1, offset 1.

Running the same `gaussian_radius` function on square objects *(est.)*:

| Object size (input px) | Size on output grid | Radius | Positive-heatmap cells |
|---|---|---|---|
| 8 | 2 | 0 | 1 |
| 12 | 3 | 0 | 1 |
| 13 | 4 (after `ceil`) | 1 | 9 |
| 16 | 4 | 1 | 9 |
| 32 | 8 | 2 | 25 |
| 64 | 16 | 4 | 81 |

Elongated vehicles behave the same way: an 8×16 px box also gets radius 0,
a 10×20 px box radius 1 *(est.)*.

**What this means *(est.)*:**

1. **Square objects of 12 px or less get radius 0.** Their target is a
   single 1 at the centre cell and 0 everywhere else, so the focal loss's
   penalty-reduction term `(1 − Y)^β` [S27] has no soft neighbourhood to act
   on. We measured this on the real annotations: 67.1% of AI-TOD-v2 objects get
   radius 0, against 18–29% on VisDrone and 23–25% on DOTA-v1.5 (see
   [`aerial-dataset.md`](../datasets/aerial-dataset.md)). This is the concrete
   form of D1: for most tiny objects the positive signal is a single pixel.
   (D1)
2. **One grid cell is a big error for a tiny box.** If the predicted centre
   lands one cell (4 px) off, IoU with the ground truth is 0.33 for an 8 px
   box, 0.50 for 12 px and 0.60 for 16 px, against 0.88 for 64 px. So the
   offset head carries most of the localisation for tiny objects, and AP at
   IoU 0.5 is decided by sub-cell accuracy. (D2)
3. **Nearby tiny objects collide.** Two vehicles whose centres fall in the
   same 4×4 px cell map to one heatmap peak, and only one can be detected.
   Measured at native resolution, it is rare: 0.4% of AI-TOD-v2 objects and
   0.2–2.1% on VisDrone and DOTA-v1.5. It becomes more common if images are
   downscaled for training. (D2)

These three points could be the core of a short "why CenterNet fails on tiny
objects" analysis, and they suggest direct experiments: a minimum radius, a
radius from the receptive field as in RFLA, an "inside the box" target, or
stride 2.

## 5. Suggested reading order and open questions

**Read first** (in this order): NWD-RKA [S5] (best explanation of why IoU
fails, and the AI-TOD-v2 paper), RFLA [S6] (key paper, receptive fields),
the SODA survey sections on label assignment [S11], YOLC [S10] (a modern
CenterNet adaptation), Point Teacher [S21] (weak supervision). Then DotD [S4]
and DQ-DETR [S15] as needed.

**Open questions:**

- Title of the CenterNet-based satellite-video paper (see CLAUDE.md), and
  whether it is public yet.
- Which satellite-video dataset the satellite-video lead refers to (VISO,
  SAT-MTB or another), and whether we may use it.

**Open items:**

- [ ] Confirm the AI-TOD-v2 licence (annotations are now downloaded and measured).
- [ ] Get VisDrone licence terms.
- [ ] Read the M-CenterNet section of the AI-TOD paper (IEEE).
- [ ] Get the per-dataset AP tables from RFLA (only the AI-TOD ablation is
      checked here).
- [ ] Search for any work that changes CenterNet's heatmap target using
      Gaussian or receptive-field distances (gap claimed in 3.1).

## 6. Sources

- [S1] Kailas PS et al., *Analysis of Object Detection Models for Tiny Object in Satellite Imagery: A Dataset-Centric Approach*, arXiv 2412.10453 — <https://arxiv.org/abs/2412.10453>
- [S2] Yuan et al., *An Empirical Study of Methods for Small Object Detection from Satellite Imagery*, arXiv 2502.03674v1 — <https://arxiv.org/abs/2502.03674v1>
- [S3] AI-TOD / M-CenterNet abstract, ICPR 2020 author page — <https://ailb-web.ing.unimore.it/icpr/author/3284>
- [S4] Xu et al., *Dot Distance for Tiny Object Detection in Aerial Images*, CVPRW 2021 — <https://openaccess.thecvf.com/content/CVPR2021W/EarthVision/html/Xu_Dot_Distance_for_Tiny_Object_Detection_in_Aerial_Images_CVPRW_2021_paper.html>
- [S5] Xu et al., *Detecting tiny objects in aerial images: A normalized Wasserstein distance and a new benchmark* (NWD-RKA, AI-TOD-v2), ISPRS J. 2022 — <https://arxiv.org/abs/2206.13996>
- [S6] Xu et al., *RFLA: Gaussian Receptive Field based Label Assignment for Tiny Object Detection*, ECCV 2022 — <https://arxiv.org/abs/2208.08738> · code <https://github.com/Chasel-Tsui/mmdet-rfla>
- [S7] Wang et al., *A Normalized Gaussian Wasserstein Distance for Tiny Object Detection*, arXiv 2110.13389 (cited in [S1]) — **TBD** read
- [S8] Shi et al., *Similarity Distance-Based Label Assignment for Tiny Object Detection*, arXiv 2407.02394 — <https://arxiv.org/abs/2407.02394>
- [S9] Zhu et al., *Detection and Tracking Meet Drones Challenge* (VisDrone), TPAMI 2021 — <https://arxiv.org/abs/2001.06303>
- [S10] Liu et al., *YOLC: You Only Look Clusters for Tiny Object Detection in Aerial Images*, IEEE T-ITS 2024 — <https://arxiv.org/abs/2404.06180> · code <https://github.com/dawn-ech/YOLC>
- [S11] Cheng et al., *Towards Large-Scale Small Object Detection: Survey and Benchmarks* (SODA), TPAMI 2023 — <https://arxiv.org/abs/2207.14096>
- [S12] Yin et al., *Detecting and Tracking Small and Dense Moving Objects in Satellite Videos: A Benchmark* (VISO), TGRS 2021 — <https://arxiv.org/abs/2111.12960>
- [S13] Xiao et al., *DSFNet: Dynamic and Static Fusion Network for Moving Object Detection in Satellite Videos*, IEEE GRSL 2022 — <https://ieeexplore.ieee.org/document/9594855>
- [S14] Xiao et al., *Highly Efficient and Unsupervised Framework for Moving Object Detection in Satellite Videos* (HiEUM), arXiv 2411.15895 — <https://arxiv.org/abs/2411.15895>
- [S15] Huang et al., *DQ-DETR: DETR with Dynamic Query for Tiny Object Detection*, ECCV 2024 — <https://arxiv.org/abs/2404.03507>
- [S16] Hu et al., *Dome-DETR: DETR with Density-Oriented Feature-Query Manipulation for Efficient Tiny Object Detection*, ACM MM 2025 — <https://arxiv.org/abs/2505.05741>
- [S17] Pailla et al., *Object detection on aerial imagery using CenterNet*, arXiv 1908.08244 — <https://arxiv.org/abs/1908.08244>
- [S18] *A Combined Frame Difference and Convolution Method for Moving Vehicle Detection in Satellite Videos*, Sensors 25(2):306, 2025 — <https://doi.org/10.3390/s25020306>
- [S19] *Deep Vehicle Detection in Satellite Video*, arXiv 2204.06828 — <https://arxiv.org/abs/2204.06828>
- [S20] Chen et al., *Point-to-Box Network for Accurate Object Detection via Single Point Supervision* (P2BNet), ECCV 2022 — <https://arxiv.org/abs/2207.06827>
- [S21] Zhu et al., *Tiny Object Detection with Single Point Supervision* (Point Teacher), arXiv 2412.05837 — <https://arxiv.org/abs/2412.05837>
- [S22] Luo et al., *PointOBB: Learning Oriented Object Detection via Single Point Supervision*, CVPR 2024 — <https://arxiv.org/abs/2311.14757>
- [S23] Akyon et al., *Slicing Aided Hyper Inference and Fine-tuning for Small Object Detection* (SAHI), ICIP 2022 — <https://arxiv.org/abs/2202.06934> · code <https://github.com/obss/sahi>
- [S24] Du et al., *Adaptive Sparse Convolutional Networks with Global Context Enhancement for Faster Object Detection on Drone Images* (CEASC), CVPR 2023 — <https://arxiv.org/abs/2303.14488>
- [S25] Zhao et al., *Bridging the Scale Gap: Balanced Tiny and General Object Detection in Remote Sensing Imagery* (ScaleBridge-Det), arXiv 2512.01665 — <https://arxiv.org/abs/2512.01665>
- [S26] *Remote Sensing Object Detection Meets Deep Learning: A Meta-review of Challenges and Advances*, arXiv 2309.06751 — <https://arxiv.org/abs/2309.06751>
- [S27] Zhou et al., *Objects as Points* (CenterNet), arXiv 1904.07850 — <https://arxiv.org/abs/1904.07850>
- [S28] DSFNet repository — <https://github.com/ChaoXiao12/Moving-object-detection-DSFNet>
- [S29] CenterNet target generation, `ctdet.py` — <https://github.com/xingyizhou/CenterNet/blob/master/src/lib/datasets/sample/ctdet.py>
- [S30] CenterNet `gaussian_radius` and `draw_umich_gaussian`, `image.py`; defaults in `opts.py` — <https://github.com/xingyizhou/CenterNet/blob/master/src/lib/utils/image.py>
