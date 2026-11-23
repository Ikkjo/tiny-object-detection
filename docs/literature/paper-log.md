# Paper log

This file lists the papers tied to the datasets and models we chose, one row
per paper, with the datasets it uses (issue #1) and the models it proposes or
compares (issue #2). A paper is here if it introduces one of our chosen
datasets or models (nominees and runners-up in
[`docs/datasets/selection.md`](../datasets/selection.md) and
[`docs/model-selection.md`](../model-selection.md)), or if one of those
choices rests on its results. Every other paper we looked at is in
[`paper-log-archive.md`](paper-log-archive.md), with the same columns. IDs
stay the same in both files, so gaps in the numbering here are papers in the
archive.

New papers go in this file if they are tied to a chosen dataset or model, and
in the archive otherwise. When a choice changes, move the rows that are
affected.

**How to read the columns**

- **Tied to:** which chosen dataset or model the paper belongs to.
- **Datasets:** aerial and remote-sensing datasets with experiments in the
  paper. Others are in brackets.
- **Method (built on):** what the paper proposes and which detector it
  modifies.
- **Models compared:** the baselines in its main results tables, as far as
  checked.
- **Checked:** `abstract` = only the abstract was read; `tables` = the
  dataset and results sections were read; `full` = read end to end. All of
  these so far were read through a web tool that extracts page content, not
  in full by a person.
- **Where to look:** for every **TBD**, the place in the paper that answers
  it. These are the items to check by hand.
- **Team verdict:** left empty for you after reading the abstract
  (keep / maybe / drop, and why).

Families: 2S = two-stage, 1S = one-stage anchor-based, AF = anchor-free
dense, PT = point/keypoint-based (CornerNet, CenterNet), DETR = query-based
transformer, FM = foundation model, OBB = oriented boxes.

## 1. Papers

| ID | Paper | Tied to | Year, venue | Datasets | Method (built on) | Models compared | Code | Checked | Where to look (TBD) | Team verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| L01 | [Objects as Points (CenterNet)](https://arxiv.org/abs/1904.07850) | CenterNet (every track) | 2019, arXiv | (COCO, KITTI) | CenterNet, PT; DLA-34, ResNet-18/101, Hourglass-104. Output stride 4; λ_size 0.1, λ_off 1. DLA-34: 37.4 AP on COCO val, AP_S 19.9 on test-dev (flip) | COCO test-dev table (Table 2): Mask R-CNN, Deform-v2, SNIPER, PANet, TridentNet (2S); CornerNet, ExtremeNet, FSAF, YOLOv3, RetinaNet, RefineDet (1S) | [xingyizhou/CenterNet](https://github.com/xingyizhou/CenterNet) (PyTorch 0.4.1, needs DCNv2) | tables | — | |
| L02 | [Tiny Object Detection in Aerial Images (AI-TOD, M-CenterNet)](https://cs.paperswithcode.com/paper/tiny-object-detection-in-aerial-images) | AI-TOD-v2: its images and the v1 labels it revises | 2020, ICPR | AI-TOD | M-CenterNet, PT, multiple centre points (DLA-34) | **TBD** | [jwwangchn/AI-TOD](https://github.com/jwwangchn/AI-TOD) (data) | abstract | IEEE Xplore (paywalled): benchmark table and M-CenterNet section. M-CenterNet on AI-TOD 14.5 AP is quoted in [SimD](https://arxiv.org/abs/2407.02394) Table II | |
| L04 | [NWD-RKA, AI-TOD-v2](https://arxiv.org/abs/2206.13996) | AI-TOD-v2 (introduces it); NWD-RKA | 2022, ISPRS J. | AI-TOD, AI-TOD-v2, VisDrone2019, DOTA-v2.0 | NWD metric + RKA assignment; plugged into Faster R-CNN, Cascade R-CNN, DetectoRS (others **TBD**) | AI-TOD-v2 benchmark: TridentNet, Faster R-CNN (R-50, R-101, HRNet-w32), Cascade R-CNN, DetectoRS, DotD, YOLOv3, RetinaNet, SSD-512, RepPoints, FoveaBox, FCOS, Grid R-CNN | [Chasel-Tsui/mmdet-aitod](https://github.com/Chasel-Tsui/mmdet-aitod) | tables | Confirm the full list of detectors NWD-RKA is added to (results tables per dataset) | |
| L05 | [RFLA](https://arxiv.org/abs/2208.08738) | RFLA (on Faster R-CNN and FCOS) | 2022, ECCV | AI-TOD, VisDrone2019, DOTA-v2.0 (+ TinyPerson) | Gaussian receptive-field label assignment; on Faster R-CNN and FCOS (+ Cascade R-CNN? **TBD**) | AI-TOD table: TridentNet, Faster R-CNN, Cascade RPN, Cascade R-CNN, DetectoRS, DotD, DetectoRS+NWD, SSD-512, RetinaNet, PAA, ATSS, RepPoints, OTA, AutoAssign, FCOS, M-CenterNet | [Chasel-Tsui/mmdet-rfla](https://github.com/Chasel-Tsui/mmdet-rfla) | tables (AI-TOD only) | Results tables for VisDrone, DOTA-v2.0, TinyPerson; which detectors carry RFLA | |
| L07 | [SODA survey and benchmarks](https://arxiv.org/abs/2207.14096) | Swin-T: backbone comparison on SODA-A | 2023, TPAMI | SODA-A (+ SODA-D) | Survey + two datasets | SODA-A: Rotated Faster R-CNN, Rotated RetinaNet, RoI Transformer, Gliding Vertex, Oriented R-CNN, S²A-Net, DODet, Oriented RepPoints, DHRec. SODA-D: includes CenterNet and CornerNet | [shaunyuan22.github.io/SODA](https://shaunyuan22.github.io/SODA/) | tables | Full SODA-D model list (Table 6) | |
| L12 | [DQ-DETR](https://arxiv.org/abs/2404.03507) | DINO: its AI-TOD-v2 result | 2024, ECCV | AI-TOD-v2 (others **TBD**) | Dynamic query count and position from a counting module, DETR | AI-TOD-v2 (Table 2): YOLOv3, RetinaNet, Faster R-CNN, Cascade R-CNN, DetectoRS, DotD, NWD-RKA, RFLA (on DetectoRS); DETR-DC5, Deformable-DETR, DAB-DETR, DINO (re-implemented, 25.9 AP) | [Katie0723/DQ-DETR](https://github.com/Katie0723/DQ-DETR) | tables | — | |
| L27 | [VisDrone challenge paper](https://arxiv.org/abs/2001.06303) | VisDrone2019-DET (aerial runner-up) | 2021, TPAMI | VisDrone (DET, VID, SOT, MOT) | Dataset + challenge report | CornerNet (Hourglass-104) baseline among others; challenge entries incl. RRNet and MSC-CenterNet (CenterNet-based) | [VisDrone/VisDrone-Dataset](https://github.com/VisDrone/VisDrone-Dataset) | tables | Full baseline list (Table 2) | |
| L28 | [CenterNet on aerial imagery](https://arxiv.org/abs/1908.08244) | CenterNet on VisDrone | 2019, arXiv | VisDrone2019 | CenterNet with several backbones and resolutions | **TBD** | **TBD** | abstract | Tables 1–4 (backbones, AP) | |
| L30 | [xView](https://arxiv.org/abs/1802.07856) | xView: part of AI-TOD-v2's images are cut from it | 2018, arXiv | xView | Dataset | SSD baseline | — | abstract | — | |
| L40 | [Microsoft COCO](https://arxiv.org/abs/1405.0312) | MS COCO 2017 (reference benchmark) | 2014, ECCV | (COCO) | Dataset; 80 classes; "small" = area under 32² px | — | [cocodataset.org](https://cocodataset.org) | dataset section | — | |
| L41 | [LVIS](https://arxiv.org/abs/1908.03195) | LVIS v1.0 (reference runner-up) | 2019, CVPR | (LVIS, on COCO images) | Dataset with ~1,200 classes and federated (not exhaustive) labels | Mask R-CNN baselines (**TBD**) | [lvis-dataset/lvis-api](https://github.com/lvis-dataset/lvis-api) | dataset section | Baseline tables | |
| L49 | [Faster R-CNN](https://arxiv.org/abs/1506.01497) | Faster R-CNN | 2015, NeurIPS | (VOC, COCO) | Region proposal network + Fast R-CNN head, 2S | **TBD** | MMDetection, torchvision, Detectron2 | code only | Results tables | |
| L50 | [Feature Pyramid Networks (FPN)](https://arxiv.org/abs/1612.03144) | FPN (in Faster R-CNN, Cascade R-CNN, FCOS) | 2017, CVPR | (COCO) | Feature pyramid added to Faster R-CNN, 2S. R-50 on COCO minival: 33.9 AP, AP_S 17.8 (Table 3c) | Faster R-CNN without FPN (ablations); test-dev table (Table 4) | MMDetection, torchvision, Detectron2 | tables | — | |
| L51 | [Cascade R-CNN](https://arxiv.org/abs/1712.00726) | Cascade R-CNN | 2018, CVPR | (COCO, VOC) | Three box-refinement stages with rising IoU thresholds, on FPN Faster R-CNN, 2S | FPN Faster R-CNN baselines (Tables 5, 6) | MMDetection, Detectron2 | tables (partly from a summary) | Table 6 R-50 row (AP_S 22.6) and the parameter table | |
| L52 | [Deep Layer Aggregation (DLA)](https://arxiv.org/abs/1707.06484) | DLA-34 (CenterNet's backbone) | 2018, CVPR | (ImageNet, others) | Backbone that merges features across stages; DLA-34 is CenterNet's main backbone | **TBD** | timm (`dla34`, 15.7M params) | full | DLA-34 parameter count (paper gives only "about 30% fewer than ResNet-34"); classification comparison tables | |
| L53 | [Probabilistic two-stage detection (CenterNet2, "CenterNet Update")](https://arxiv.org/abs/2103.07461) | CenterNet Update | 2021, arXiv | (COCO, LVIS, Objects365) | CenterNet as the first stage of a two-stage detector; also an updated CenterNet with FPN and GIoU loss (40.2 AP on COCO val, R-50) | **TBD** | [xingyizhou/CenterNet2](https://github.com/xingyizhou/CenterNet2) (Detectron2); MMDetection | code only | Main tables, AP_S | |
| L55 | [HRNet (HRNetV2)](https://arxiv.org/abs/1908.07919) | HRNet-W18 | 2020, TPAMI | (COCO, Cityscapes, others) | Backbone that keeps a stride-4 branch through the whole network; HRNetV2p adds a pyramid for detection. FCOS with HRNetV2-W18: 35.2 AP, AP_S 20.4 on COCO | Faster R-CNN, Cascade R-CNN, FCOS with ResNet and HRNet backbones | [HRNet-Object-Detection](https://github.com/HRNet/HRNet-Object-Detection); MMDetection | tables | — | |
| L56 | [Swin Transformer](https://arxiv.org/abs/2103.14030) | Swin-T | 2021, ICCV | (COCO, ImageNet, ADE20K) | Hierarchical transformer backbone with shifted local windows, strides 4–32. Swin-T 28M parameters; +3.4–4.2 box AP over ResNet-50 | Cascade Mask R-CNN, ATSS, RepPoints v2, Sparse R-CNN with ResNet-50 vs Swin-T | [microsoft/Swin-Transformer](https://github.com/microsoft/Swin-Transformer); MMDetection | tables | — | |
| L59 | [FCOS](https://arxiv.org/abs/1904.01355) | FCOS | 2019, ICCV | (COCO) | Anchor-free per-pixel detector with centre-ness, AF. ResNet-50: 37.1 AP, AP_S 21.3 on minival | RetinaNet and others (**TBD**) | MMDetection; [AdelaiDet](https://github.com/aim-uofa/AdelaiDet) | tables | Main comparison table | |
| L60 | [TTFNet](https://arxiv.org/abs/1909.00700) | TTFNet's training target (planned CenterNet head option) | 2020, AAAI | (COCO) | CenterNet with an elliptical Gaussian target and box regression from a Gaussian area (GIoU), PT. TTFNet-18 28.1 AP, AP_S 11.8; trains ~7× faster than CenterNet | CenterNet and real-time detectors (**TBD**) | [ZJULearning/ttfnet](https://github.com/ZJULearning/ttfnet) (early MMDetection) | tables | MMDetection version in the repo | |
| L61 | [DINO (DETR)](https://arxiv.org/abs/2203.03605) | DINO | 2023, ICLR | (COCO) | DETR with denoising anchor boxes, DETR. R-50, 4 scales, 12 epochs: 49.0 AP (MMDetection) | **TBD** | MMDetection | code only | Results tables | |
| L62 | [Transformers in small object detection: benchmark and survey](https://arxiv.org/abs/2309.04902) | Swin-T: why transformer backbones | 2025, ACM CSUR | (survey; datasets **TBD**) | Survey of 60+ transformer small-object detectors; finds they lead on most datasets, credited to context from attention | — | — | abstract | Dataset list and benchmark tables | |
| L63 | [Small object detection for birds with Swin Transformer](https://arxiv.org/abs/2511.22310) | Swin-T: window size for small objects | 2023, MVA (arXiv 2025) | SOD4SB | CenterNet with a Swin backbone and Swin neck, PT; smaller windows (size 2) better for small objects | **TBD** | **TBD** | abstract | Ablation on window size | |
| L64 | [ReDHF](https://arxiv.org/abs/2611.07994) | DINO: dropping the stride-4 map hurts tiny objects | 2026, arXiv | AI-TOD-v2, VisDrone, SODA-D | Brings back the stride-4 feature that DETR-style detectors drop, DETR. +1.4 AP on AI-TOD-v2 | DETR-family detectors (**TBD**) | **TBD** | abstract | Main tables | |
| L67 | [Corner2Net](https://arxiv.org/abs/2411.15772) | Hourglass-104: parameter count | 2024, arXiv | (COCO) | Cascade corner detector, PT. Its table lists CenterNet with Hourglass-104: 186.44M parameters, 42.1 AP, AP_S 24.1 on test-dev | Keypoint detectors incl. CenterNet, CornerNet (**TBD**) | **TBD** | tables | — | |

## 2. Chosen models

The models on our shortlist ([`docs/model-selection.md`](../model-selection.md))
and the papers above that they come from. Track A (lightweight) is still being
chosen; the models seen so far for it are in the
[archive](paper-log-archive.md#2-models-seen-so-far).

| Model | Family | Papers | Framework / code | Notes |
|---|---|---|---|---|
| CenterNet with DLA-34 or Hourglass-104 | PT | L01, L28, L52, L67 | Official repo (PyTorch 0.4.1 + DCNv2); MMDetection (ResNet-18 only) | Our starting point. DLA-34: 37.4 AP on COCO val, AP_S 19.9 on test-dev. Hourglass-104: 40.3 AP on COCO val, 186.44M parameters (L67). Trails anchor-based detectors on SODA-D's smallest objects (L07). No plain CenterNet result on AI-TOD-v2 found |
| CenterNet with HRNet-W18 or Swin-T (our builds) | PT | L55, L56, L63 | MMDetection 3.x, our configs | No published COCO or AI-TOD-v2 results. Swin-T lowered one-stage detectors on SODA-A (L07) |
| CenterNet Update (CenterNet with FPN) | PT | L53 | MMDetection 3.x; CenterNet2 (Detectron2) | 40.2 AP on COCO val (R-50); changes the loss (GIoU, more positives) and adds FPN levels |
| TTFNet (training target only) | PT | L60 | Official repo (early MMDetection) | Not run as a detector; its target is a planned option for our CenterNet head |
| Faster R-CNN | 2S | L04, L05, L49, L50 | MMDetection, Detectron2, torchvision | Host for NWD-RKA and RFLA. R-50-FPN on AI-TOD-v2: 12.8 AP, AP_vt 0.0 (L04, L05) |
| Cascade R-CNN | 2S | L04, L51 | MMDetection | R-50-FPN on AI-TOD-v2: 15.1 AP, AP_vt 0.1 (L04; also in L12, Table 2, and in the training log of mmdet-aitod's config) |
| FCOS | AF | L04, L05, L59 | MMDetection; mmdet-rfla | R-50 on AI-TOD-v2: 13.4 AP, AP_vt 2.5; with RFLA 15.6 (L05 repo) |
| NWD-RKA, RFLA (label assignment) | on 2S / AF | L04, L05 | mmdet-aitod, mmdet-rfla | Faster R-CNN R-50 on AI-TOD-v2: 21.4 AP (NWD-RKA), 22.6 AP (RFLA) |
| DINO | DETR | L12, L61, L64 | MMDetection | 49.0 AP on COCO val (R-50, 12 epochs); 25.9 AP on AI-TOD-v2 (L12, re-implemented). DQ-DETR, built on it, 30.2 AP (L12) |
