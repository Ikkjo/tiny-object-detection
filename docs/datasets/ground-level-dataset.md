# Ground-level dataset

This note compares datasets for tiny object detection in street, driving, and everyday scenes. The ground-level dataset complements the [reference benchmark](reference-benchmark.md) and the [aerial dataset](aerial-dataset.md) in issue #1.

**Nominee: SODA-D** | **Runner-up: TinyPerson**. Reasons are in [section 4](#4-decision), and the cross-track summary is in [selection.md](selection.md).

**TBD** marks unverified values. "Measured" refers to statistics from the official annotations. The measurements use `sqrt(w * h)` for horizontal box size at native resolution, with strict cutoffs at 16 px and 32 px. The SODA paper defines Small as area up to and including 1024 px^2, or size <= 32 px. See the [measurement procedure](#7-sources) [S1], [S2].

## Which ground-level datasets test tiny objects?

- **SODA-D covers nine street and driving classes.** Of its 278,433 foreground boxes, 21.0% are under 16 px and 71.4% are under 32 px. The SODA paper reports CenterNet at 21.5 AP and 5.1 AP_eS and CornerNet at 24.6 AP and 6.5 AP_eS. [S1], [S2]
- **TinyPerson tests smaller boxes in coastal scenes.** In the standard detection split, 63.7% of non-ignore boxes are under 16 px. The share is 58.0% after excluding uncertain boxes. The benchmark scores one class, person, and includes elevated viewpoints. [S1], [S6]
- **Several pedestrian and face benchmarks limit which small objects count.** EuroCity Persons marks people under 20 px tall as ignore regions. WIDER FACE flags hard-to-recognise faces at 10 px or less. WiderPerson's baseline filters pedestrians under 20 px tall after resizing during training. [S10], [S12], [S14]

## 1. What this dataset is for

COCO checks whether our detector setups reproduce published scores, and AI-TOD-v2 pushes tiny-object detection to the extreme in overhead imagery. The ground-level dataset tests whether those same findings hold in street and everyday views, where scale varies sharply with depth, backgrounds are cluttered, and occlusion is heavy.

From issue #1's selection criteria, we weight six requirements:

| # | Criterion | Why it matters for us | Weight |
|---|---|---|---|
| C1 | Share of tiny and small objects, under 16 px and under 32 px | Without enough genuinely tiny objects, this track duplicates COCO | High |
| C2 | Multi-class ground-level scenes | Tests general detection on street scenes rather than a single rigid object class | High |
| C3 | Published baselines, including CenterNet if available | Lets us compare our runs directly with the literature | High |
| C4 | Fits modest hardware, download size, and resolution | High-resolution images need tiling, which multiplies training time and storage | Medium |
| C5 | Annotation quality, public test labels, and COCO JSON format | Avoids conversion bugs and hidden-test bottlenecks | Medium |
| C6 | Academic licence and open access | Usable for university research without approval forms or commercial blocks | Medium |

## 2. Contenders

We shortlisted SODA-D, TinyPerson, TT100K, WIDER FACE, and WiderPerson from issue #1. We ruled out CityPersons, EuroCity Persons, CrowdHuman, and other datasets during the literature review. See [section 5](#5-ruled-out-early).

### 2.1 Nominee: SODA-D

Multi-class driving benchmark for small object detection, built from Mapillary Vistas street scenes plus on-board camera, mobile phone, and web images [S2].

| Property | Value | Source |
|---|---|---|
| Domain, year | Driving and street scenes. IEEE TPAMI 2023, arXiv 2022 | [S2] |
| Paper / download link | [arXiv 2207.14096](https://arxiv.org/abs/2207.14096) / Official [OneDrive](https://nwpueducn-my.sharepoint.com/:f:/g/personal/gcheng_nwpu_edu_cn/EhXUvvPZLRRLnmo0QRmd4YUBvDLGMixS11_Sr6trwJtTrQ?e=PellK6) and BaiduNetDisk via [project page](https://shaunyuan22.github.io/SODA/) | [S2], [S3] |
| Images (per split) | 12,383 train, 5,017 val, 7,428 test; 24,828 total (measured) | [S1], [S2] |
| Instances | 134,301 train, 56,050 val, 88,082 test. 278,433 foreground boxes and 153,976 ignore regions in total. Measured counts match Table 4 | [S1], [S2] |
| Classes | 9: traffic-sign 30.9%, vehicle 24.9%, traffic-light 22.5%, people 12.9%, traffic-camera 2.7%, warning-cone 2.1%, rider 1.7%, motor 1.4%, bicycle 0.9% (measured) | [S1], [S2] |
| Share of objects under 16 px and under 32 px | **21.0% under 16 px and 71.4% under 32 px** across all splits. Measured mean 25.4 px, median 24.7 px, p10 12.4 px, p90 39.9 px. SODA area bands in px^2 are eS `(0, 144]` at 9.3% (25,834), rS `(144, 400]` at 25.5% (71,064), gS `(400, 1024]` at 36.7% (102,066), and Normal `(1024, 2000]` at 28.5% (79,469). The paper reports a mean of 20.31 px for its Small subset, size <= 32 px | [S1], [S2] |
| Image resolution / size on disk | Average 3407x2470 px [S2]; longest side min 640, median 3264, max 9504 px across 3,407 distinct sizes (measured) [S1]. Official archives on OneDrive: `Annotations.zip` 9.1 MB, `Images.zip` 24.92 GiB / 26.75 GB [S1], [S3] | [S1], [S2], [S3] |
| Annotation format | COCO-style JSON with horizontal boxes in `train.json`, `val.json`, and `test.json`. The authors use `ignore: 1` and `category_id: 10` for regions such as objects over 2000 px^2 or too blurred to confirm. The raw JSON omits `iscrowd` | [S1], [S2], [S4] |
| Licence and access | CC BY-NC 4.0, free for academic research, commercial use prohibited. Direct OneDrive download, no registration form | [S3] |
| Evaluation metric | `SODADeval` reports AP at IoU 0.50:0.95, AP50, and AP75 on the SODA Small band (area <= 1024 px^2), plus AP_eS, AP_rS, AP_gS, and AP_N. See [SODA-D evaluation](#soda-d-evaluation) | [S2], [S4] |
| Published baselines (CenterNet?) | Yes, Table 6 on test set, all R-50 except CornerNet Hourglass-104 and YOLOX CSP-Darknet: **CenterNet 21.5 AP** (AP50 48.8, AP75 15.6, **AP_eS 5.1**, AP_rS 16.2, AP_gS 29.6, AP_N 42.4), **CornerNet 24.6 AP** (AP_eS 6.5), Faster R-CNN 28.9, Cascade R-CNN 31.2, RetinaNet 28.2, FCOS 23.9, RepPoints 28.0, ATSS 26.8, YOLOX 26.7, Sparse R-CNN 24.2, Deformable-DETR 19.2, RFLA 29.7 [S2]. CFINet ICCV 2023 reaches 30.7 AP and 14.7 AP_eS [S5] | [S2], [S5] |
| How often used in the papers found | Four logged papers report SODA-D experiments (SODA, CFINet, DyFrDet and ReDHF) | [paper log](../literature/paper-log.md), [archive](../literature/paper-log-archive.md), [S20] |

Across the three splits, the measured share under 32 px ranges from 71.1% to 71.7%, a gap under 0.7 percentage points. The table combines all 278,433 foreground boxes. [S1]

| Bin (sqrt(w * h)) | Share | Notes |
|---|---|---|
| < 2 px | 0.0% | Min box size 1.0 px |
| 2-8 px (very tiny) | 1.6% | |
| 8-16 px (tiny) | 19.4% | 21.0% under 16 px total |
| 16-32 px (small) | 50.4% | 71.4% under 32 px total |
| 32-64 px (medium) | 28.6% | Capped at area <= 2000 px^2 (~44.7 px) |
| >= 64 px | 0.0% | Larger objects marked ignore |

At native resolution and stride 4, 12.9% of boxes produce a radius-0 Gaussian that covers just the centre cell. CenterNet uses one positive centre cell per object at any radius. The same-cell collision rate is 0.1% of boxes. Traffic cameras have the smallest median size at 17.4 px. The three most common classes, traffic signs, vehicles, and traffic lights, account for 78.2% of foreground boxes. [S1], [S23]

#### SODA-D evaluation

Use the `SODA-mmdetection` bbox protocol on the original test images. Map patch predictions back to original image IDs and coordinates, then merge them with per-class non-maximum suppression at IoU 0.50. The official config uses `test_wo_ignore.json`, which `generate_wo_ignore.py` creates by dropping category 10 annotations from `test.json`. Run `SODADeval` with category IDs 1 through 9 and the wrapper's `maxDets = [100, 300, 1000]`. It reports AP at 100 detections per class per image. Since category 10 is outside matching, a detection overlapping an ignore region can still count as a false positive. [S2], [S4]

The SODA paper crops 800x800 patches at stride 650 and resizes them to 1200x1200 for both training and evaluation. If we keep 800x800 as the model input, record that difference when comparing with Table 6. [S2], [S4]

For a supplemental AI-TOD size-bin comparison, use the same merged predictions and a copy of the foreground evaluation annotations. Set `iscrowd: 0` on each retained annotation because the raw JSON omits the field and stock `cocoapi-aitod` reads it for bbox matching and uses it in place of `ignore`. Keep categories 1 through 9 and set `maxDets = [1, 10, 100]` to score AP at the same cap as `SODADeval`. Label these scores as AI-TOD size-bin results. [S1], [S4], [S24]

### 2.2 Runner-up: TinyPerson

Dedicated tiny-person benchmark built from web videos of coastal, beach, and maritime scenes for long-range search and rescue [S6].

| Property | Value | Source |
|---|---|---|
| Domain, year | Coastal, beach, and ocean scenes, mixed ground and elevated/aerial viewpoints; WACV 2020 (arXiv Dec 2019) | [S6] |
| Paper / download link | [arXiv 1912.10664](https://arxiv.org/abs/1912.10664) / Official [Google Drive](https://drive.google.com/open?id=1KrH9uEC9q4RdKJz-k34Q6v5hRewU5HOw), Baidu Pan, and UCAS site via [PointTinyBenchmark](https://github.com/ucas-vg/PointTinyBenchmark/tree/TinyBenchmark) | [S6], [S7] |
| Images (per split) | Detection split (images with < 200 valid persons): 746 train, 786 test; 1,532 total (measured). Full set with dense images: 794 train, 816 test; 1,610 total (measured; matches Table 2) | [S1], [S6] |
| Instances | Detection split: 38,438 non-ignore boxes (32,120 normal + 6,318 uncertain) plus 5,358 ignore regions (measured). Full set with dense images: 72,651 total boxes, 42,197 train + 30,454 test (measured; matches Table 2) | [S1], [S6] |
| Classes | 2 fine-grained labels (`earth_person` 65.9%, `sea_person` 34.1% on detection split), merged into 1 class (`person`) for the detection benchmark | [S1], [S6] |
| Share of objects under 16 px and under 32 px | In the detection split, **63.7% are under 16 px and 87.1% are under 32 px** when including uncertain boxes. Excluding uncertain boxes as the authors do for training and evaluation gives **58.0% under 16 px and 84.7% under 32 px**. See the measured breakdown below | [S1], [S6] |
| Image resolution and size on disk | In the detection split, the longest side ranges from 700 to 6354 px across 113 distinct resolutions. The median is 1920 px overall and 3840 px in test. The annotation JSONs are 10.8 MB for train and 8.0 MB for test. The compressed image archive sizes are **TBD** | [S1], [S7] |
| Annotation format | COCO-style JSON with extra flags `ignore`, `uncertain`, `logo`, and `in_dense_image`. The official evaluation code is in `TOV_mmdetection` | [S1], [S7], [S8] |
| Licence and access | Public download links through Google Drive and Baidu Pan. Dataset licence **TBD**. The repository's MIT licence covers the code | [S7] |
| Evaluation metric | AP and log-average miss rate (MR), primarily at overlap 0.50, with 0.25 and 0.75 also reported. The evaluator uses IoU for regular boxes and intersection over detection area (IOD) for ignore regions, including uncertain boxes. Size bands in px include `tiny1 [2, 8]`, `tiny2 [8, 12]`, `tiny3 [12, 20]`, `tiny [2, 20]`, and `small [20, 32]` | [S6], [S8] |
| Published baselines (CenterNet?) | Tiny AP50 in the TinyPerson paper, Table 6. FCOS 16.90, RetinaNet 30.82, DSFD 31.15, Adaptive RetinaNet 41.25, Adaptive FreeAnchor 41.36, and Faster R-CNN FPN 43.55. Table 7 gives 47.29 for Faster R-CNN FPN with Monotone Scale Match. SSPNet Table I gives 59.13 with Faster R-CNN and 58.59 with Cascade R-CNN. RFLA Table 6 gives 26.5 with FCOS and 50.1 with Faster R-CNN. We found no plain CenterNet baseline in the papers checked | [S6], [S9], [S21] |
| How often used in the papers found | TinyPerson experiments appear in four logged papers (Scale Match, RFLA, SSPNet, and Point Teacher). The SODA survey and the survey by Kos and Belter also discuss the dataset | [paper log](../literature/paper-log.md), [archive](../literature/paper-log-archive.md), [S2], [S6], [S9], [S21], [S22], [S25] |

The standard detection split has 1,532 images. Mean and median box sizes are 18.2 px and 12.3 px with uncertain boxes included, and 20.1 px and 13.8 px with them excluded. TinyPerson Table 1 reports a mean of 18.0 px and a standard deviation of 17.4 px. [S1], [S6]

| Subset | Instances | 2-8 px | 8-16 px | < 16 px | < 32 px | CenterNet stride-4 radius-0 |
|---|---|---|---|---|---|---|
| Detection split (`aerial_size_stats.py`, incl. uncertain) | 38,438 | 26.6% | 37.1% | 63.7% | 87.1% | 52.0% |
| Detection split (excl. ignore and uncertain) | 32,120 | 19.5% | 38.5% | 58.0% | 84.7% | 45.3% |
| Full set with dense images (incl. uncertain) | 64,832 | 28.4% | 38.0% | 66.3% | 88.7% | 55.2% |

TinyPerson has public test annotations. Its paper uses overlapping sub-images to process large frames. [S6], [S7]

### 2.3 Other contenders

#### TT100K (Tsinghua-Tencent 100K)

| Property | Value | Source |
|---|---|---|
| Domain, year, paper link | Chinese street-view driving panoramas (Tencent Street View), CVPR 2016 ([CVF paper](https://openaccess.thecvf.com/content_cvpr_2016/html/Zhu_Traffic-Sign_Detection_and_CVPR_2016_paper.html)) | [S16] |
| Images / classes | 100,000 cropped images, of which about 10,000 contain about 30,000 traffic signs. The paper uses the 45 classes with at least 100 instances out of 221 raw classes | [S16] |
| C1 Tiny share | In 8,876 annotated train and test images, SODA Table 5 counts 71 eS instances at size <= 12 px. It puts another 2,800 in the rS band, which spans sizes above 12 px through 20 px. The table leaves the exact share under 16 px unresolved | [S2] |
| C2 Multi-class ground-level | All 45 evaluation classes are Chinese traffic signs | [S16] |
| C3 Published baselines | The paper compares its Caffe CNN with Fast R-CNN. We found no CenterNet benchmark in the sources checked | [S16], [S17] |
| C4 Hardware | 2048x2048 px images. Annotated image archive size **TBD**. The official download page lists `part1` at 17.7 GB and 16,555 images under "No sign Images" | [S16], [S17] |
| C5 Format and quality | Custom `annotations.json` with bounding boxes and polygon/ellipse masks; needs conversion to COCO JSON | [S16], [S17] |
| C6 Licence and access | CC BY-NC. The project page links directly to the 2016 annotations and lists the no-sign images separately | [S17] |

We ruled out TT100K because it covers traffic signs alone, has 71 instances in the eS band, and requires annotation conversion. [S2], [S16], [S17]

#### WIDER FACE

| Property | Value | Source |
|---|---|---|
| Domain, year, paper link | Everyday event photos gathered through search engines. The CVPR 2016 paper lists 60 event classes in Section 3.1. The project page lists 61 | [S10], [S11] |
| Images / classes | 32,203 images (40% train, 10% val, 50% test), 393,703 faces; 1 class (`face`) | [S10], [S11] |
| C1 Tiny share | SODA reports that half the faces are 10 to 50 px tall. TinyPerson Table 1 gives a mean box size of 32.8 px. WIDER FACE annotators flag hard-to-recognise faces at 10 px or less as ignore | [S2], [S6], [S10] |
| C2 Multi-class ground-level | The benchmark scores one class, face | [S10] |
| C3 Published baselines | The paper compares face detectors with PASCAL VOC AP at 0.50 on Easy, Medium, and Hard subsets | [S10] |
| C4 Hardware | Image resolutions vary. Archive size and fit for our target hardware are **TBD** | [S11] |
| C5 Format and quality | Custom `.mat` and `.txt` annotations require conversion to COCO JSON. The authors withhold test-set boxes | [S10], [S11] |
| C6 Licence and access | Public download links. Exact dataset licence **TBD** | [S11] |

We ruled out WIDER FACE because it scores faces alone and withholds test labels. [S10], [S11]

#### WiderPerson

| Property | Value | Source |
|---|---|---|
| Domain, year, paper link | Crowded everyday scenes gathered through search engines. IEEE TMM 2020, arXiv 2019 | [S12] |
| Images / classes | 13,382 images (8,000 train, 1,000 val, 4,382 test), 386,353 person boxes plus 13,433 ignore regions (~28.9 persons/image); 5 annotation tags, 1 evaluation class (`pedestrian`) | [S12], [S13] |
| C1 Tiny share | The Hard, Medium, and Easy subsets start at box heights of 20, 50, and 100 px. During training, the authors' baseline treats pedestrians under 20 px tall after resizing as ignore regions | [S12] |
| C2 Multi-class ground-level | Evaluation scores pedestrians and ignores riders, partially visible people, and crowds | [S12] |
| C3 Published baselines | The paper reports log-average miss rate (MR) for Improved Faster R-CNN and RetinaNet | [S12] |
| C4 Hardware | The authors resized images to 800-1400 px and trained on one Titan X GPU. Archive size and fit for our target hardware are **TBD** | [S12], [S13] |
| C5 Format and quality | Per-image `.jpg.txt` files (`class x1 y1 x2 y2`) needing conversion; fixed 0.41 aspect ratio for pedestrian boxes; test labels withheld | [S12], [S13] |
| C6 Licence and access | Free for academic and non-commercial use via Google Drive and Baidu Drive | [S12], [S13] |

We ruled out WiderPerson because it scores pedestrians alone, starts its Hard subset at 20 px box height, and withholds test labels. [S12], [S13]

## 3. Comparison

✅ = meets the criterion, ⚠️ = partly, ❌ = does not, ❓ = unknown.

| Criterion | SODA-D | TinyPerson | TT100K | WIDER FACE | WiderPerson |
|---|---|---|---|---|---|
| C1 Tiny and small object share | ✅ 21.0% < 16 px, 71.4% < 32 px | ✅ 58.0-63.7% < 16 px, 84.7-87.1% < 32 px | ⚠️ 71 eS at <= 12 px, share < 16 px TBD | ⚠️ Mean 32.8 px, hard-to-recognise faces at <= 10 px flagged | ❌ Hard subset starts at 20 px height |
| C2 Multi-class ground-level scenes | ✅ (9 street classes) | ❌ (1 class, coastal/elevated) | ❌ (traffic signs only) | ❌ (faces only) | ❌ (pedestrians only) |
| C3 Published baselines (incl. CenterNet) | ✅ CenterNet, CornerNet, and 10 others in Table 6 | ⚠️ Tiny-person baselines | ⚠️ Traffic-sign baselines | ⚠️ Face detector baselines | ⚠️ Pedestrian miss-rate baselines |
| C4 Fits modest hardware | ⚠️ 24.92 GiB, 3407x2470 px on average | ❓ Archive sizes TBD, median test long side 3840 px | ❓ Annotated archive size TBD, 2048x2048 px | ❓ Archive size and hardware fit TBD | ❓ Archive size and hardware fit TBD |
| C5 COCO JSON, quality, public test | ✅ COCO-style JSON, public test labels | ⚠️ COCO-style JSON, public test labels, custom IOD handling | ⚠️ Custom JSON, public test labels | ❌ Custom format, test labels withheld | ❌ Custom format, test labels withheld |
| C6 Licence and access | ✅ CC BY-NC 4.0, direct link | ⚠️ Public links, dataset licence TBD | ✅ CC BY-NC, direct link to 2016 annotations | ⚠️ Public links, exact terms TBD | ✅ Non-commercial research, public links |

## 4. Decision

We nominate **SODA-D** because it tests tiny objects across nine street categories and gives us published CenterNet and CornerNet baselines. **TinyPerson** is the runner-up. It tests smaller boxes and has public test labels. Its single person class and coastal scenes cover less of the ground-level research question. [S1], [S2], [S6]

We propose training and testing on 800x800 SODA-D inputs at stride 650, pending team agreement and a hardware check. A fixed training subset could reduce training time while keeping the full test split. If the SODA-D archives are inaccessible or exceed our budget, revisit TinyPerson once we confirm its download sizes and dataset terms. [S2], [S3], [S7]

## 5. Ruled out early

| Dataset | Domain | Link | Why dropped |
|---|---|---|---|
| CityPersons | Urban driving pedestrians | [arXiv 1702.05693](https://arxiv.org/abs/1702.05693) [S15] | Mean person box size 79.8 px. The default Reasonable pedestrian subset starts at 50 px box height [S6], [S15] |
| EuroCity Persons | European urban driving pedestrians and riders | [arXiv 1805.07193](https://arxiv.org/abs/1805.07193) [S14] | Labels pedestrians and rider subtypes. The authors mark people under 20 px tall as ignore regions [S14] |
| CrowdHuman | Crowded human scenes | [arXiv 1805.00123](https://arxiv.org/abs/1805.00123) [S18] | Built for crowd occlusion and NMS rather than tiny objects; 1 class; test labels hidden |
| Caltech-USA | Driving pedestrians | Cited in [S12], [S15] | 640x480 single-city video, ~0.32-1.4 persons/image, medium scale (>= 50 px reasonable set) |
| KITTI | Autonomous driving | Cited in [S12], [S14] | Single city, low density (< 1 pedestrian/image), mostly medium/large objects |
| SODA-10M | Autonomous driving | SODA Table 5 [S2] | Only 33 eS (<= 12 px) instances across 10,000 train/val images |
| TJU-DHD Traffic | Urban traffic | SODA Table 5 [S2] | Only 82 eS (<= 12 px) instances across 50,266 train/val images |
| GTSDB | German traffic signs | SODA Table 2 [S2], [S16] | 900 images, 1,206 instances; saturated (near-100% recall/precision) |
| LISA | US traffic signs | SODA Table 2 [S2] | 6,610 images, 7,855 instances; small volume, signs only |
| STS Dataset | Swedish traffic signs | SODA Table 2 [S2] | 3,488 instances across 20,000 frames; sparse, signs only |
| BSTLD | Traffic lights | SODA Table 2 [S2] | 13,427 images, 24,000 instances; traffic lights only (1 class) |

### Papers found, by domain

See the [paper log](../literature/paper-log.md) and its [archive](../literature/paper-log-archive.md) for the checked comparisons.

| Domain | Paper | Venue | Datasets used |
|---|---|---|---|
| General survey + driving | Cheng et al., *Towards Large-Scale Small Object Detection: Survey and Benchmarks* [S2] | TPAMI 2023 | SODA-D, SODA-A, reviews COCO, WIDER FACE, TinyPerson, TT100K, WiderPerson, EuroCity Persons |
| Driving (method) | Yuan et al., *CFINet: Small Object Detection via Coarse-to-fine Proposal Generation and Imitation Learning* [S5] | ICCV 2023 | SODA-D, SODA-A |
| Driving (method) | Yang et al., *DyFrDet: Towards Accurate Small Object Detection via Dynamic Frequency Suppression with Label Disambiguation* [S19] | arXiv 2026 | SODA-D, SODA-A, AI-TOD |
| Driving (method) | *ReDHF: Reviving the Discarded High-Resolution Feature for Transformer-Based Tiny Object Detection* [S20] | arXiv 2026 | SODA-D, AI-TOD-v2, VisDrone |
| Driving / traffic signs | Zhu et al., *Traffic-Sign Detection and Classification in the Wild* [S16] | CVPR 2016 | TT100K |
| Pedestrian / coastal | Yu et al., *Scale Match for Tiny Person Detection* [S6] | WACV 2020 | TinyPerson, Tiny CityPersons |
| Pedestrian / coastal (method) | Xu et al., *RFLA: Gaussian Receptive Field based Label Assignment for Tiny Object Detection* [S21] | ECCV 2022 | TinyPerson, AI-TOD, VisDrone, DOTA-v2.0 |
| Pedestrian / coastal (method) | Hong et al., *SSPNet: Scale Selection Pyramid Network for Tiny Person Detection from UAV Images* [S9] | GRSL 2022, online 2021 | TinyPerson |
| Pedestrian / coastal (method) | *Point Teacher: Tiny Object Detection with Single Point Supervision* [S22] | arXiv 2024 | TinyPerson, AI-TOD-v2, SODA-A |
| Pedestrian (crowd/street) | Zhang et al., *WiderPerson: A Diverse Dataset for Dense Pedestrian Detection in the Wild* [S12] | TMM 2020, arXiv 2019 | WiderPerson, CityPersons, Caltech-USA |
| Pedestrian (street) | Zhang et al., *CityPersons: A Diverse Dataset for Pedestrian Detection* [S15] | CVPR 2017 | CityPersons, Caltech-USA, KITTI |
| Pedestrian (street) | Braun et al., *The EuroCity Persons Dataset: A Novel Benchmark for Object Detection* [S14] | TPAMI 2019 | EuroCity Persons, CityPersons, Caltech-USA |
| Human (crowd) | Shao et al., *CrowdHuman: A Benchmark for Detecting Human in a Crowd* [S18] | arXiv 2018 | CrowdHuman, CityPersons, Caltech-USA, COCOPersons |
| Face | Yang et al., *WIDER FACE: A Face Detection Benchmark* [S10] | CVPR 2016 | WIDER FACE, FDDB |

DyFrDet reports 31.3 AP and 15.1 AP_eS on SODA-D test at 1200x1200 input in Table 7. ReDHF Table 7 reports 30.1 AP and 12.6 AP_eS with DINO-4scale and 38.7 AP and 21.4 AP_eS with Dome-DETR-L, both at 800x800 input. [S19], [S20]

## 6. Open items

- [ ] Download SODA-D `Images.zip` (24.92 GiB) onto the training machine and test `tools/img_split` (800x800 patches, stride 650) to see how many patches `train` and `test` produce.
- [ ] Once the target GPU is fixed, decide whether we train on full SODA-D `train` patches or a deterministic subset, and re-measure CenterNet's stride-4 radius-0 share at the chosen patch input size.
- [ ] Confirm TinyPerson's exact `train.tar.gz` and `test.tar.gz` sizes on Google Drive and check its exact licence wording on `vision.ucas.ac.cn/resource.asp`.

## 7. Sources

- [S1] We measured the official annotations in `data/` on 24 Nov 2026 with [`aerial_size_stats.py`](../../scripts/aerial_size_stats.py) in `--format coco` mode at stride 4. Pass SODA-D's train, val, and test files together for the combined results, or one at a time for the split results. For TinyPerson, pass the train and test files for the same split together.
  - The script keeps boxes with positive width and height and skips annotations with a truthy `ignore` or `iscrowd`. For the TinyPerson results excluding uncertain boxes, also remove annotations where `annotation.get("uncertain", False)` is truthy from copies of the detection JSONs before running the same command. Keep all image records.
  - For the SODA-D area bands, take `area = bbox[2] * bbox[3]` from each retained horizontal box. Count `lo < area <= hi` in each band and divide by 278,433 foreground boxes. The script's SODA area-band output covers polygon inputs.
  - The official SODA-D OneDrive `Annotations.zip` contains `train.json`, `val.json`, and `test.json`. It has 9,135,191 bytes and SHA-256 `a97964dc6af2be5f81c9c0725c354fdfc259b8deeb0037c1ad81cbf1262ff1fb`.
  - TinyPerson official Google Drive files under `tiny_set/annotations/` have the following sizes and SHA-256 digests.
    - `tiny_set_train.json`, 10,838,570 bytes, `4c2683bf695d6be08667c52e262ec4f1790ebeeba04cb5200424a05464a5eeea`
    - `tiny_set_test.json`, 7,995,907 bytes, `0cfcbbcc7433ad5bdc6b856df1d109188cda48035506bda1f16b7e2261c63d57`
    - `tiny_set_train_with_dense.json`, 18,024,921 bytes, `e2a5913be5fca7a0bdf763b59fd7f280911b229cf273eebf0e4c7c80e05a8cc0`
    - `tiny_set_test_with_dense.json`, 13,095,848 bytes, `16f4a9c847c17d75835cd6b6ae2be2f27e748077c8f9cd3b35d6d93ef38be10e`
- [S2] Cheng et al., *Towards Large-Scale Small Object Detection: Survey and Benchmarks* (SODA), IEEE TPAMI 2023: <https://arxiv.org/abs/2207.14096> (read PDF in full; Tables 2-8, Sec. 4-5)
- [S3] SODA official project page (CC BY-NC 4.0 licence, OneDrive and BaiduNetDisk links; SharePoint folder lists `Images.zip` at 26,754,343,886 bytes): <https://shaunyuan22.github.io/SODA/>
- [S4] SODA-D benchmark code. [Dataset config](https://github.com/shaunyuan22/SODA-mmdetection/blob/5ad1a5280d25e7159869c481bdbea5b2d603c2ff/configs/_base_/datasets/sodad.py), [wrapper](https://github.com/shaunyuan22/SODA-mmdetection/blob/5ad1a5280d25e7159869c481bdbea5b2d603c2ff/mmdet/datasets/sodad.py), [evaluator](https://github.com/shaunyuan22/SODA-mmdetection/blob/5ad1a5280d25e7159869c481bdbea5b2d603c2ff/mmdet/datasets/sodad_eval/sodadeval.py), and [annotation filter](https://github.com/shaunyuan22/SODA-mmdetection/blob/5ad1a5280d25e7159869c481bdbea5b2d603c2ff/tools/img_split/generate_wo_ignore.py).
- [S5] Yuan et al., *Small Object Detection via Coarse-to-fine Proposal Generation and Imitation Learning* (CFINet), ICCV 2023. [Tables 2 and 3](https://openaccess.thecvf.com/content/ICCV2023/papers/Yuan_Small_Object_Detection_via_Coarse-to-fine_Proposal_Generation_and_Imitation_Learning_ICCV_2023_paper.pdf).
- [S6] Yu et al., *Scale Match for Tiny Person Detection* (TinyPerson), WACV 2020: <https://arxiv.org/abs/1912.10664> (read PDF in full; Tables 1-8, Sec. 3-5)
- [S7] TinyPerson official repository. [Download instructions](https://github.com/ucas-vg/PointTinyBenchmark/tree/TinyBenchmark) and [software licence](https://github.com/ucas-vg/PointTinyBenchmark/blob/TinyBenchmark/LICENSE).
- [S8] UCAS-VG MMDetection toolbox for TinyPerson: <https://github.com/ucas-vg/TOV_mmdetection>
- [S9] Hong et al., *SSPNet: Scale Selection Pyramid Network for Tiny Person Detection from UAV Images*, IEEE GRSL vol. 19, 2022, online 2021. [IEEE publication](https://doi.org/10.1109/LGRS.2021.3103069) and [Table I in the preprint](https://arxiv.org/pdf/2107.01548#page=4).
- [S10] Yang et al., *WIDER FACE: A Face Detection Benchmark*, CVPR 2016: <https://arxiv.org/abs/1511.06523> (read PDF; Table 1, Sec. 3 and 5)
- [S11] WIDER FACE [project page](https://mmlab.ie.cuhk.edu.hk/projects/WIDERFace/index.html) and [CUHK dataset card](https://huggingface.co/datasets/CUHK-CSE/wider_face).
- [S12] Zhang et al., *WiderPerson: A Diverse Dataset for Dense Pedestrian Detection in the Wild*. [IEEE TMM February 2020 issue](https://ieeexplore.ieee.org/abstract/document/8764496) and [2019 arXiv preprint, Sections III to V](https://arxiv.org/abs/1909.12118).
- [S13] WiderPerson official page (format and split layout): <http://www.cbsr.ia.ac.cn/users/sfzhang/WiderPerson/>
- [S14] Braun et al., *The EuroCity Persons Dataset: A Novel Benchmark for Object Detection*, IEEE TPAMI 2019: <https://arxiv.org/abs/1805.07193> (read PDF; Table 1, Sec. 3.1-3.5)
- [S15] Zhang et al., *CityPersons: A Diverse Dataset for Pedestrian Detection*, CVPR 2017: <https://arxiv.org/abs/1702.05693> (read PDF; Tables 1-5, Sec. 3)
- [S16] Zhu et al., *Traffic-Sign Detection and Classification in the Wild* (TT100K), CVPR 2016: <https://openaccess.thecvf.com/content_cvpr_2016/html/Zhu_Traffic-Sign_Detection_and_CVPR_2016_paper.html> (read PDF; Sec. 3-5, Table 3)
- [S17] TT100K official page. [2016 annotations, no-sign archives, and CC BY-NC licence](https://cg.cs.tsinghua.edu.cn/traffic-sign/).
- [S18] Shao et al., *CrowdHuman: A Benchmark for Detecting Human in a Crowd*, arXiv 2018: <https://arxiv.org/abs/1805.00123> (read PDF; Tables 1-12, Sec. 3-4)
- [S19] Yang et al., *DyFrDet: Towards Accurate Small Object Detection via Dynamic Frequency Suppression with Label Disambiguation*, arXiv 2026. [Table 7 on SODA-D](https://arxiv.org/html/2608.02495#S4.T7).
- [S20] *ReDHF: Reviving the Discarded High-Resolution Feature for Transformer-Based Tiny Object Detection*, arXiv 2026. [Table 7 on SODA-D](https://arxiv.org/html/2611.07994#A3.T7).
- [S21] Xu et al., *RFLA: Gaussian Receptive Field based Label Assignment for Tiny Object Detection*, ECCV 2022. [Table 6 on TinyPerson](https://www.ecva.net/papers/eccv_2022/papers_ECCV/papers/136690518.pdf#page=13).
- [S22] *Point Teacher: Tiny Object Detection with Single Point Supervision*, arXiv 2024. [TinyPerson experiments](https://arxiv.org/html/2412.05837).
- [S23] CenterNet's [heatmap focal loss](https://github.com/xingyizhou/CenterNet/blob/master/src/lib/models/losses.py) uses heatmap values of 1 as positives.
- [S24] The official [AI-TOD bbox evaluator](https://github.com/jwwangchn/cocoapi-aitod/blob/44a230ae5197cb89bf9e5e62f313cac3ad30c7af/aitodpycocotools/aitodpycocotools/cocoeval.py) reads `iscrowd` for matching and reports size-band AP at `maxDets[2]`.
- [S25] Kos and Belter, *Deep Learning for Small and Tiny Object Detection: A Survey*, PAR 2023. [Survey PDF](https://yadda.icm.edu.pl/baztech/element/bwmeta1.element.baztech-0914b536-d052-40f7-b712-0487146494e0/c/Kos_Deep_PAR_3_2023.pdf).
