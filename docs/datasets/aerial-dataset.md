# Aerial dataset

This is the research for choosing our **aerial dataset**: drone, airborne or
satellite images with tiny objects. We use three datasets in total, and the
other two are the [reference benchmark](reference-benchmark.md) and the
[ground-level dataset](ground-level-dataset.md). This is part of issue #1
(Select datasets for tiny object detection).

**Nominee: AI-TOD-v2** · **Runner-up: VisDrone2019-DET**. The reasons for the
choice are in [section 4](#4-decision), and the summary is in
[selection.md](selection.md).

Every number has a source, listed in [section 7](#7-sources). **TBD** means
we haven't checked it against a primary source yet, and *(est.)* means we
derived the number ourselves. "Measured" means we computed it from the
annotation files with
[`scripts/aerial_size_stats.py`](../../scripts/aerial_size_stats.py) [S1].
Object size is the box size √(w·h) in pixels, at the image's original
resolution. "Tiny" means under 16 px (the AI-TOD definition), and COCO's
"small" means an area under 32² px.

## Short answer: which aerial datasets do tiny-object papers use, and how tiny are they?

- **AI-TOD-v2 and VisDrone are used most.** Of the 27 aerial papers we logged ([`paper-log.md`](../literature/paper-log.md) and its [archive](../literature/paper-log-archive.md)), VisDrone
  appears in 12, AI-TOD-v2 in 9, AI-TOD (v1) in 7, DOTA in 6 and SODA-A in 4
  *(est.)*.
- **Only AI-TOD-v2 has tiny objects almost everywhere.** 85.9% of its objects
  are under 16 px and 98.2% under 32 px (measured). SODA-A comes second: 48.3% under 16 px by
  horizontal box, 64.9% by oriented polygon. VisDrone (26–36% under 16 px),
  xView (36%) and DOTA (32–38%) have objects of many sizes, and their tiny
  objects come from only a few classes: people in VisDrone, small cars in xView, small
  vehicles in DOTA (measured).
- **This matters a lot for CenterNet.** With CenterNet's default settings, 67%
  of AI-TOD-v2 objects get a heatmap target of a single pixel, against
  27% on SODA-A, 24% on xView, 19–29% on VisDrone and 23–30% on DOTA (measured at the original
  image size, using CenterNet's own code for building targets [S35]).
- **DOTA barely evaluates tiny objects.** 86% of DOTA-v2.0 objects under 16 px
  are marked "difficult" (measured), and DOTA's official evaluation leaves
  difficult objects out of the score [S40]. So on DOTA, a detector that misses
  tiny objects hardly loses any points.

## 1. What this dataset is for

We expect tiny objects to cause the most trouble for detectors on the aerial
dataset, so this is where we look for the reasons. From that we made the
criteria below, based on the selection criteria in issue #1.

| # | Criterion | Why it matters for us | Weight |
|---|---|---|---|
| C1 | **Share of genuinely tiny objects** (under 16 px, and under 8 px) | The point of the project. It also decides how often CenterNet's heatmap target collapses to one pixel | High |
| C2 | **Widely used**, with published baselines (CenterNet if possible) | Results must be comparable with the literature | High |
| C3 | **Annotation quality** (missing labels, ignore regions) | With noisy labels, false positives on tiny objects can't be interpreted | High |
| C4 | **Fits modest hardware** (image count, image size, download) | We have limited GPU and disk; very large images must be tiled | Medium |
| C5 | **Format:** horizontal boxes in COCO JSON, or easy to convert | CenterNet and most baselines use horizontal boxes | Medium |
| C6 | **Licence and access** allow academic use | Must be usable for research without extra agreements | Medium |

## 2. Contenders

We took the shortlist from the datasets used in the papers we logged (the
paper list is in [section 5](#5-ruled-out-early)). We looked at six:
AI-TOD-v2, VisDrone2019-DET, DOTA, SODA-A, xView and the satellite-video
dataset VISO. AI-TOD-R is a version of AI-TOD-v2 with rotated boxes.

### 2.1 Nominee: AI-TOD-v2

Tiny objects in aerial and satellite images, collected from five existing
datasets and relabelled to fix missing annotations.

| Property | Value | Source |
|---|---|---|
| Domain, year | Aerial and satellite images taken from DOTA, xView, VisDrone, Airbus-Ship and DIOR; AI-TOD 2020, v2 2022 | [S2], [S4] |
| Paper / download | [arXiv 2206.13996](https://arxiv.org/abs/2206.13996) / annotations on Google Drive via the [project page](https://chasel-tsui.github.io/AI-TOD-v2/); images generated from the xView train set with the [AI-TOD toolkit](https://github.com/jwwangchn/AI-TOD) | [S4], [S5], [S3] |
| Images | 11,214 train, 2,804 val, 14,018 test; 28,036 in total (measured; matches the paper) | [S1], [S4] |
| Instances | 301,494 train, 75,082 val, 376,119 test, plus 51 crowd boxes (measured). The paper gives 752,745 in its text and 752,754 in its table; we count 752,746 including crowd | [S1], [S4] |
| Classes | 8: vehicle (88.0% of instances), ship 4.9%, person 4.6%, storage-tank 1.9%, airplane, bridge, swimming-pool, wind-mill (each 0.2% or less) (measured) | [S1] |
| Share under 16 px / under 32 px | **85.9% / 98.2%** (measured). Under 8 px: 12.4%. Matches the paper's 12.4 / 73.4 / 12.4 / 1.8% for the very tiny / tiny / small / medium bins | [S1], [S4] |
| Object size | Mean 12.7 px, median 11.8, p10 7.7, p90 17.3. Person median 9.8 px, vehicle 11.8 px, airplane 21.4 px (measured) | [S1] |
| Objects per image | Mean 26.8, median 4, max 2,667; 0.1% of images empty (measured) | [S1] |
| Image resolution | 800×800 (longest side 800–801 px) (measured) | [S1] |
| CenterNet targets, stride 4 | 67.1% of objects get a one-pixel heatmap target; 0.4% share a centre cell with another object (measured) | [S1], [S35] |
| Size on disk | Annotations 270 MB (four JSON files); full mirror with images 25 GB | [S1], [S6] |
| Annotation format | COCO JSON, horizontal boxes | [S1] |
| Licence and access | AI-TOD: CC BY-NC-SA 4.0, non-commercial. v2 licence not stated (**TBD**). Generating the images needs the xView train set (CC BY-NC-SA 4.0, registration) | [S3], [S19] |
| Evaluation metric | COCO-style AP plus AP_vt / AP_t / AP_s / AP_m for the AI-TOD size bins, via `cocoapi-aitod` | [S4], [S3] |
| Published baselines | DetectoRS + NWD-RKA 24.7 AP (strongest baseline in that paper: DotD 20.4); DQ-DETR 30.2 AP; YOLOv11-M 30.5 AP; ScaleBridge-Det (3 B parameters) 35.7 AP. No CenterNet result found; M-CenterNet scores 14.5 AP on AI-TOD v1 | [S4], [S37], [S36], [S34] |
| How often used | 9 of 27 logged papers, nearly all from 2022 onward *(est.)* | [paper-log](../literature/paper-log.md), [archive](../literature/paper-log-archive.md) |

**Object sizes in detail** (measured, all splits; per-split values differ by
under 1 point):

| AI-TOD bin, box size √(w·h) | Share |
|---|---|
| under 2 px | 0.0% |
| 2–8 px (very tiny) | 12.4% |
| 8–16 px (tiny) | 73.4% |
| 16–32 px (small) | 12.3% |
| 32–64 px (medium) | 1.8% |
| over 64 px | 0.0% |

Our shares are the same as the paper's (12.4 / 73.4 / 12.4 / 1.8%) [S4], so
the script measures this format correctly.

**Strengths:** no other dataset in use has as many tiny objects. The labels
were cleaned to add missed objects, and most recent tiny-object methods report
results on it. The images are only 800×800, so we don't need to cut them into
tiles. The boxes are horizontal and in COCO JSON, which CenterNet uses
directly.

**Weaknesses:** 88% of the objects are vehicles, so results for the other
seven classes rest on few examples. The number of objects per image varies a
lot (median 4, max 2,667). Its images come from VisDrone, DOTA and xView. To
get the images we have to download xView (20.7 GB) and run the AI-TOD tool
that cuts them out. There are no published CenterNet results for it.

**Variant: AI-TOD-R.** The same 28,036 images, relabelled with rotated boxes:
752,460 objects, mean size 10.62 px [S7]. We would only need it if we work
with rotated boxes. Download: Google Drive via the [project page](https://chasel-tsui.github.io/AI-TOD-R/) [S8].

### 2.2 Runner-up: VisDrone2019-DET

Drone images of streets and squares in 14 Chinese cities.

| Property | Value | Source |
|---|---|---|
| Domain, year | Drone, urban and suburban, day and night; 2019 challenge, TPAMI 2021 | [S9] |
| Paper / download | [arXiv 2001.06303](https://arxiv.org/abs/2001.06303) / Google Drive and Baidu links on [VisDrone-Dataset](https://github.com/VisDrone/VisDrone-Dataset); mirrored in Ultralytics' GitHub releases | [S9], [S10], [S11] |
| Images | 6,471 train, 548 val, 1,610 test-dev (measured; matches the paper); 1,580 test-challenge without public labels | [S1], [S9] |
| Instances | 343,204 train, 38,759 val, 75,102 test-dev, excluding ignore regions and the "others" class (measured; val matches Ultralytics' count) | [S1], [S12] |
| Classes | 10: car 42.2%, pedestrian 23.1%, motor 8.6%, people 7.9%, van, bicycle, tricycle, truck, awning-tricycle, bus (train, measured) | [S1] |
| Share under 16 px / under 32 px | Train **26.0% / 60.5%**, val 30.8% / 68.6%, test-dev **36.4%** / 67.7%. Under 8 px: 5.3% train, 13.0% test-dev (measured) | [S1] |
| Object size | Median 26.1 px train, 21.9 px test-dev. Pedestrian median 17.7 px in train vs 11.8 px in test-dev (measured) | [S1] |
| Objects per image | Train mean 53, median 42, max 902 (measured) | [S1] |
| Image resolution | Longest side 480–2,000 px, median 1,400 (train, measured) | [S1] |
| CenterNet targets, stride 4 | One-pixel target: 18.5% train, 22.4% val, 28.9% test-dev. Shared centre cell: 1.4–2.1% (measured) | [S1], [S35] |
| Size on disk | 1.44 GB train, 0.07 GB val, 0.28 GB test-dev (images included) | [S10] |
| Annotation format | One text file per image: x, y, w, h, score, class, truncation, occlusion. Class 0 = ignore region | [S1], [S9] |
| Licence and access | Direct download; licence not stated on the official page (**TBD**) | [S10] |
| Evaluation metric | COCO-style AP at IoU 0.50:0.95, AP50, AP75, AR up to 500 detections | [S9] |
| Published baselines | CornerNet (Hourglass-104) 23.43 AP on test-dev; CenterNet-based challenge entries RRNet 29.13 AP and MSC-CenterNet 31.13 AP; best 2020 entry 34.57 AP. DetectoRS 25.7 → 27.4 AP with NWD-RKA | [S9], [S4] |
| How often used | 12 of 27 logged papers *(est.)* | [paper-log](../literature/paper-log.md), [archive](../literature/paper-log-archive.md) |

**Strengths:** it is the aerial dataset used most often, it can be downloaded
directly, there are results for CenterNet-style detectors, and the images are
small enough to train on without cutting them into tiles.

**Weaknesses:** most of its objects aren't tiny (median 26 px in train). The
tiny ones are mostly in the pedestrian and people classes. **Objects in
test-dev are smaller than in train** (13.0% vs 5.3% under 8 px), so a model is
tested on smaller objects than it mostly saw during training. That makes it a
useful test of how well a model generalises, but it also makes our test-dev
numbers harder to compare with other papers.

**Why it is the runner-up:** of all the contenders it best meets C2, C4 and C5,
and it is the easiest to set up. It came second because most of its objects
aren't tiny (C1).

### 2.3 Other contenders

#### DOTA (v1.5 and v2.0 measured)

| Property | Value | Source |
|---|---|---|
| Domain, year, paper | Aerial and satellite; v1.0 2018, v1.5 and v2.0 2021 ([arXiv 2102.12219](https://arxiv.org/abs/2102.12219)). Image sources in the v2.0 metadata (train, val and test-dev): Google Earth 4,606, Jilin-1 257, Gaofen-2 199, airborne 153 (measured) | [S13], [S14], [S1] |
| Images / classes | v2.0: 1,830 train, 593 val (measured), 2,792 test-dev (metadata only); 11,268 in total incl. test-challenge; 18 classes. v1.5: 1,411 train, 458 val, 16 classes (measured) | [S1], [S13] |
| Instances | v2.0: 268,627 train, 81,048 val (measured); 1,793,658 in total incl. test sets. v1.5: 210,631 train, 69,565 val (measured) | [S1], [S13] |
| C1 Tiny share | v2.0 train + val: **38.0%** under 16 px by horizontal box, **53.7%** by oriented polygon; 68.8% / 80.6% under 32 px. Small-vehicle is 62.7% of instances, median 15.1 px; the other classes have medians of 18–330 px. One-pixel CenterNet target: 29.3%. v1.5 train: 31.8% / 50.0% (measured). v1.0 did not annotate objects under 10 px | [S1], [S13] |
| C2 Published results | Standard oriented-detection benchmark; NWD-RKA reports DetectoRS 40.8 → 41.9 AP on v2.0. No CenterNet result found | [S4] |
| C3 Annotation quality | **48% of v2.0 train + val objects are flagged "difficult", and 86% of those under 16 px** (16–32 px: 42%; 32 px and up: 9%) (measured). The official evaluation removes difficult objects from the recall count and does not count detections matched to them; AP at IoU 0.5 [S40]. v1.5: 47% difficult (measured) | [S1], [S40] |
| C4 Hardware | Images up to 13,383 px and 10,206 objects per image (measured); must be tiled. Labels 78 MB for train + val | [S1] |
| C5 Format | Text files, four corners per object. The v2.0 download also includes a horizontal-box version of the same objects (checked: same object counts, all axis-aligned) | [S14], [S1] |
| C6 Licence | Academic, non-commercial only; Google Earth terms apply | [S14] |

The labels don't include image sizes, so the resolution figures only cover the
1,869 v1.x images, whose sizes we got from the v1.5 download.

**Why we didn't choose it:** the images are very large (C4), only about a
third of the objects are tiny by box size (C1), and most tiny objects are
marked "difficult" and left out of the official score (C3). Horizontal boxes
around rotated vehicles also include a lot of background, which makes the
objects look bigger than they are (median 19.9 px by box vs 14.8 px by
outline on v2.0, measured).

#### SODA-A

| Property | Value | Source |
|---|---|---|
| Domain, year, paper | Google Earth aerial; TPAMI 2023 ([arXiv 2207.14096](https://arxiv.org/abs/2207.14096)) | [S15] |
| Images / classes | 1,067 train, 576 val, 870 test; 2,513 in total. Longest side 1,986–4,800 px, median 4,800. 9 classes: small-vehicle 60.3%, container 15.9%, ship 7.5%, storage-tank 4.1%, airplane, swimming-pool, windmill, large-vehicle, helicopter (measured) | [S1] |
| Instances | 344,228 train, 231,439 val, 296,402 test; 872,069 in total, plus 6,678 ignore regions (measured; matches the paper exactly) | [S1], [S15] |
| C1 Tiny share | **48.3%** under 16 px by horizontal box, **64.9%** by oriented polygon; 89.2% / 96.0% under 32 px. Median 16.4 px (box), 13.9 px (polygon). In SODA's own area bins: 35.0% extremely small (≤ 144 px²), 41.7% relatively small, 19.4% generally small, 4.0% normal. One-pixel CenterNet target: 27.1% (measured) | [S1] |
| C1 Per class | Small-vehicle median 14.0 px, 65.7% under 16 px; storage-tank 47.9% under 16 px; the other classes mostly 20–35 px (measured) | [S1] |
| C1 Split shift | Val is tinier than train: 45.2% vs 28.7% extremely small; 54.7% vs 44.1% under 16 px by box (measured) | [S1] |
| C2 Published results | Oriented detectors: RoI Transformer 36.0 AP best, Oriented RepPoints 26.3 AP. No CenterNet | [S15] |
| C3 Annotation quality | Ignore regions as polygons; objects cut by the image border are kept as polygons with more than four corners (measured) | [S1] |
| C4 Hardware | Mean 347 objects per image, max 11,137 (measured); large images must be tiled. Annotations 402 MB; Kaggle mirror with images 11 GB | [S1], [S17] |
| C5 Format | One JSON per image with an oriented polygon per object; horizontal boxes must be derived | [S1] |
| C6 Licence | CC BY-NC 4.0, academic only | [S16] |

**Why we didn't choose it:** after AI-TOD-v2 it has the most tiny objects of
the datasets we measured, but its images must be cut into tiles (C4), it uses
rotated outlines (C5), and there are no CenterNet results for it (C2). Like
VisDrone, its val split has smaller objects than its train split.

#### xView

| Property | Value | Source |
|---|---|---|
| Domain, year, paper | WorldView-3 satellite, 0.3 m GSD; 2018 ([arXiv 1802.07856](https://arxiv.org/abs/1802.07856)) | [S18] |
| Images / classes | 847 image IDs in the train labels (measured), against 846 train images in the download (one labelled image, `1395.tif`, has no image file); 282 val images without public labels; 1,413 images in total. 60 classes | [S1], [S41], [S11], [S13], [S18] |
| Instances | 601,849 train boxes in the 60 classes, plus 88 boxes with other type IDs, ignored (measured). Over 1 million across all splits | [S1], [S18] |
| C1 Tiny share | **36.0%** under 16 px, 60.5% under 32 px; median 24.4 px; only 1.1% under 8 px. Small car is 35.2% of boxes, median 12.4 px, 89.2% under 16 px; building is 52.6%, median 40 px. One-pixel CenterNet target: 24.0% (measured) | [S1] |
| C2 Published results | Used by SAHI and by one benchmark study; few others | [S39], [S38] |
| C3 Annotation quality | Two classes (building, small car) make up 87.8% of boxes; 19 of the 60 classes have fewer than 200 boxes. Mean 711 objects per image, max 7,618 (measured) | [S1] |
| C4 Hardware | 20.7 GB with images; very large scenes (image sizes not in the labels, **TBD**) | [S11] |
| C5 Format | One GeoJSON file with pixel boxes (`bounds_imcoords`) and numeric type IDs (checked) | [S1] |
| C6 Licence | CC BY-NC-SA 4.0; registration required. The official download page did not work for us (its link service failed), so the labels came from a Kaggle mirror | [S19], [S1] |

**Why we didn't choose it:** only a third of its objects are tiny, and almost
all of those are small cars (C1). Two classes make up most of the boxes (C3),
and the scenes are large (C4). Its images are also already part of AI-TOD-v2,
which is how most papers use them.

#### VISO (satellite video)

| Property | Value | Source |
|---|---|---|
| Domain, year, paper | Jilin-1 satellite video, 10 fps; TGRS 2021 ([arXiv 2111.12960](https://arxiv.org/abs/2111.12960)) | [S20] |
| Images / classes | Paper: 47 videos, 1,646,038 instances. README: 40 videos, 853,911 boxes (the two disagree, **TBD**). Classes: plane, car, ship, train | [S20], [S21] |
| C1 Tiny share | Small moving objects; measured share **TBD** | [S20] |
| C2 Published results | Moving-object detectors such as DSFNet and HiEUM (CenterNet-derived) | [paper-log archive](../literature/paper-log-archive.md) |
| C3 Annotation quality | Manual horizontal boxes | [S21] |
| C4 Hardware | Frames of 12000×5000 px per the README (**TBD**) | [S21] |
| C5 Format | **TBD** | — |
| C6 Licence | CC BY-NC-SA 4.0; Google Drive or Baidu download | [S21] |

**Why we didn't choose it:** it is a video dataset, and detecting objects that
move over time is a different problem from detecting them in single images.
We didn't measure it. It could be useful later, since satellite-video
detectors often use CenterNet-style heads.

## 3. Comparison

✅ = meets the criterion, ⚠️ = partly, ❌ = does not, ❓ = unknown.

| Criterion | **AI-TOD-v2** (nominee) | **VisDrone** (runner-up) | DOTA-v1.5 / v2.0 | SODA-A | xView | VISO |
|---|---|---|---|---|---|---|
| C1 Tiny share | ✅ 85.9% under 16 px | ❌ 26–36% | ⚠️ 32–38% by box, 50–54% by polygon | ⚠️ 48% by box, 65% by polygon | ⚠️ 36% under 16 px, nearly all small cars | ❓ Not measured |
| C2 Published results, incl. CenterNet | ⚠️ Many recent results; no CenterNet (M-CenterNet on v1) | ✅ Many; CornerNet and CenterNet-based entries | ⚠️ Many oriented results; no CenterNet | ⚠️ Oriented benchmark; no CenterNet | ⚠️ Few | ⚠️ Video detectors only |
| C3 Annotation quality | ✅ Relabelled to fix missing labels | ✅ Ignore regions | ❌ 86% of objects under 16 px flagged difficult and left out of the score | ✅ Ignore labels | ⚠️ 2 classes are 88% of boxes; 19 classes under 200 boxes | ❓ |
| C4 Fits modest hardware | ⚠️ 800×800 images, but xView needed to build them | ✅ Small download, no tiling | ❌ Images up to 13k px | ❌ Large images | ❌ Large scenes | ❌ Very large frames |
| C5 Format | ✅ COCO JSON, horizontal | ✅ Simple text, horizontal | ⚠️ Oriented; horizontal-box version included | ⚠️ Oriented | ⚠️ GeoJSON | ❓ |
| C6 Licence and access | ⚠️ Non-commercial; xView registration | ❓ Not stated | ⚠️ Academic only | ⚠️ Academic only | ⚠️ Non-commercial, registration | ⚠️ Non-commercial |

## 4. Decision

**Nominee: AI-TOD-v2.** We train on trainval (14,018 images) and evaluate on
test (14,018 images, public labels), as DQ-DETR does [S37]. We report AP with AI-TOD's size ranges (very tiny, tiny, small,
medium) using `cocoapi-aitod` [S3].

Why we chose it:

1. **It is the only contender where almost all objects are tiny.** 85.9% are
   under 16 px (C1). For the CenterNet question it is the hardest test: two
   thirds of its objects get a heatmap target of a single pixel.
2. **Recent tiny-object methods report results on it** (NWD-RKA, DQ-DETR,
   ScaleBridge-Det and others), so we have results to compare with (C2) [S4],
   [S37], [S36].
3. **The labels were cleaned** to add more than 50,000 missed objects (C3) [S4], so
   a false positive is less likely to be an unlabelled object.
4. **It works with our hardware once the images are made.** The images are
   800×800, so no tiling is needed (C4), and the boxes are horizontal COCO JSON
   (C5).

One dataset is enough. AI-TOD-v2 has 28,036 images and 752,746 objects (measured),
so it is large enough on its own, and we don't need a second aerial dataset
for the final decision.

**Runner-up: VisDrone2019-DET.** It is the aerial dataset used most often, and
it is the easiest to get and train on (C2, C4, C5). It came second because
most of its objects aren't tiny (C1). **SODA-A** would be the runner-up if we
cared more about the share of tiny objects than about ease of use: 48–65% of
its objects are under 16 px, but it needs tiling and rotated boxes, and fewer
papers report on it.

Why we didn't choose the others:

- **DOTA**: the images are very large (C4), and most of its tiny objects are
  marked "difficult" and left out of the official score (C3).
- **SODA-A**: rotated boxes and very large images (C4, C5).
- **xView**: only a third of its objects are tiny, almost all of them small
  cars; two classes make up most of the boxes; large scenes; and its images
  are already in AI-TOD-v2.
- **VISO**: a video dataset; we may come back to it later.

The main limitation is getting the images. AI-TOD-v2 only publishes labels,
and the images have to be cut out of the xView training images with the
AI-TOD tool [S3]. xView's official download page didn't work for us, but the
xView images are also on Kaggle [S42], and so is a full copy of AI-TOD-v2 with
images (about 25 GB) [S6]. Other limitations: 88% of the objects are vehicles,
and there are no published CenterNet results, so we will produce the first
CenterNet baseline ourselves.

We would change the decision if:
- we can't get the AI-TOD-v2 images at all
- the team decides the share of tiny objects matters less than how widely a
  dataset is used, which would favour VisDrone

## 5. Ruled out early

| Dataset | Domain | Link | Why dropped |
|---|---|---|---|
| AI-TOD (v1) | Aerial | [S2] | Same images as AI-TOD-v2 with missing labels that v2 fixes [S4] |
| DOTA-v1.0 | Aerial | [S13] | Objects under 10 px were not annotated; v1.5 adds them on the same images |
| SkyFusion | Mix of AI-TOD-v2 + Airbus Aircraft | [S32], [S33] | A 3,000-image subset of AI-TOD-v2 plus one extra source; one published study |
| DIOR / DIOR-R | Aerial | [paper-log archive](../literature/paper-log-archive.md) | Multi-scale rather than tiny; used in tiny-object papers only as a general benchmark |

### Not yet assessed

Found in the papers but not yet checked against the criteria:

| Dataset | Domain | Facts so far | Source |
|---|---|---|---|
| XS-VID | Drone video | 38 segments, 12,230 frames at 1024×1024, 258,944 instances, 8 classes; size bins at 12² / 20² / 32² px; CC BY 4.0, Hugging Face | [S22], [S23], [S24] |
| RGBT-Tiny | Drone, RGB + thermal | 115 sequences, about 93K frames at 640×512, about 1.2 M boxes, 7 classes, over 81% under 16×16; access by request form | [S25], [S26], [S27] |
| SAT-MTB | Satellite video | Horizontal-box subset: 144 videos, 33,228 frames, 308,204 instances | [S28], [S29], [S30] |
| DTOD | **TBD** | 11,600 images (9,280 / 2,320), 1,019,800 instances, 88 objects per image on average; origin paper **TBD** | [S31] |
| UAVDT | Drone video | Used by CEASC and YOLC; facts **TBD** | [paper-log archive](../literature/paper-log-archive.md) |

### Papers found

The papers behind this note, with the datasets and models each one uses, are
in [`docs/literature/paper-log.md`](../literature/paper-log.md) and its
[archive](../literature/paper-log-archive.md). The aerial
papers and how they relate to the research directions are discussed in
[`docs/literature/aerial-papers.md`](../literature/aerial-papers.md).

## 6. Open items

- [ ] Get the AI-TOD-v2 images (xView train images + the AI-TOD tool, or a
      full copy from Kaggle) on the machine we train on.
- [ ] Measure VISO (annotation files needed; the download link is in
      section 2.3), if satellite video stays in scope.
- [ ] Confirm the source of the AI-TOD-v2, SODA-A and DOTA-v2.0 files, and the
      AI-TOD-v2 licence.
- [ ] xView image sizes (not in the labels).
- [ ] Compare the VisDrone and DOTA-v1.5 mirror files with the official
      archives.
- [ ] VisDrone licence.
- [ ] Find DTOD's origin paper; collect UAVDT facts.
- [ ] Re-measure the CenterNet figures at the training input size we choose.
- [ ] Decide whether RGBT-Tiny (request form) is worth it.

## 7. Sources

- [S1] Our measurement: [`scripts/aerial_size_stats.py`](../../scripts/aerial_size_stats.py) run on the annotation files. VisDrone2019-DET and DOTA-v1.5 from the Ultralytics GitHub release archives (downloaded 21 Nov 2026; images streamed and discarded, only annotations and image sizes kept). AI-TOD-v2, SODA-A and DOTA-v2.0 annotation files from the official download folders (downloaded 22 Nov 2026). xView train labels from the Kaggle mirror hassanmojab/xview-dataset (downloaded 22 Nov 2026). The files and a provenance log with URLs and SHA-256 checksums are kept outside the repo
- [S2] Wang et al., *Tiny Object Detection in Aerial Images* (AI-TOD), ICPR 2020 — <https://cs.paperswithcode.com/paper/tiny-object-detection-in-aerial-images>
- [S3] AI-TOD repository (toolkit, licence, `cocoapi-aitod`) — <https://github.com/jwwangchn/AI-TOD>
- [S4] Xu et al., *Detecting tiny objects in aerial images: A normalized Wasserstein distance and a new benchmark* (AI-TOD-v2), ISPRS J. 2022 — <https://arxiv.org/abs/2206.13996>
- [S5] AI-TOD-v2 project page — <https://chasel-tsui.github.io/AI-TOD-v2/>
- [S6] Kaggle mirror of AI-TOD-v2 (file sizes, total size) — <https://www.kaggle.com/datasets/amongus1504/tod-aitodv2-full>
- [S7] Xu et al., *Oriented Tiny Object Detection: A Dataset, Benchmark, and Dynamic Unbiased Learning* (AI-TOD-R) — <https://arxiv.org/abs/2412.11582>
- [S8] AI-TOD-R project page — <https://chasel-tsui.github.io/AI-TOD-R/>
- [S9] Zhu et al., *Detection and Tracking Meet Drones Challenge* (VisDrone), TPAMI 2021 — <https://arxiv.org/abs/2001.06303>
- [S10] VisDrone dataset repository — <https://github.com/VisDrone/VisDrone-Dataset>
- [S11] Ultralytics dataset configs (`VisDrone.yaml`, `DOTAv1.5.yaml`, `xView.yaml`) — <https://github.com/ultralytics/ultralytics/tree/main/ultralytics/cfg/datasets>; release archives — <https://github.com/ultralytics/assets/releases/tag/v0.0.0>
- [S12] Ultralytics VisDrone documentation — <https://docs.ultralytics.com/datasets/detect/visdrone>
- [S13] Ding et al., *Object Detection in Aerial Images: A Large-Scale Benchmark and Challenges* (DOTA-v2.0), TPAMI 2021 — <https://arxiv.org/abs/2102.12219>
- [S14] DOTA dataset page (downloads, format, licence) — <https://captain-whu.github.io/DOTA/dataset.html>
- [S15] Cheng et al., *Towards Large-Scale Small Object Detection: Survey and Benchmarks* (SODA), TPAMI 2023 — <https://arxiv.org/abs/2207.14096>
- [S16] SODA project page (downloads, licence) — <https://shaunyuan22.github.io/SODA/>
- [S17] Kaggle mirror of SODA-A — <https://www.kaggle.com/datasets/shubham6147/soda-a-small-object-detection-dataset-aerial>
- [S18] Lam et al., *xView: Objects in Context in Overhead Imagery* — <https://arxiv.org/abs/1802.07856>
- [S19] xView licence as reproduced in a CDAO dataset card — <https://huggingface.co/datasets/CDAO/xview-subset-classification>
- [S20] Yin et al., *Detecting and Tracking Small and Dense Moving Objects in Satellite Videos: A Benchmark* (VISO), TGRS 2021 — <https://arxiv.org/abs/2111.12960>
- [S21] VISO repository — <https://github.com/QingyongHu/VISO>
- [S22] Guo et al., *XS-VID* — <https://arxiv.org/abs/2407.18137>
- [S23] XS-VID on Hugging Face — <https://huggingface.co/datasets/lanlanlan23/XS-VID>
- [S24] XS-VID summary (segment, frame and instance counts; **TBD** confirm against the paper) — <https://chatpaper.com/paper/42716>
- [S25] Ying et al., *Visible-Thermal Tiny Object Detection: A Benchmark Dataset and Baselines* (RGBT-Tiny), TPAMI 2025 — <https://arxiv.org/abs/2406.14482>
- [S26] RGBT-Tiny repository — <https://github.com/XinyiYing/RGBT-Tiny>
- [S27] RGBT-Tiny image resolution, from *Small Object Detection in Complex Backgrounds with Multi-Scale Attention and Global Relation Modeling* — <https://arxiv.org/abs/2603.03788>
- [S28] Li et al., *A Multitask Benchmark Dataset for Satellite Video* (SAT-MTB), TGRS 2023 — <https://doi.org/10.1109/TGRS.2023.3278075>
- [S29] SAT-MTB subset counts, from *Learn Temporal Consistency For Robust Satellite Video Detector* — <https://arxiv.org/abs/2606.15112>
- [S30] CAS satellite-video datasets page — <https://csu.cas.cn/gb/kybm/sjlyzx/gcxx_sjj/sjj_wxxl/>
- [S31] DTOD figures as reported in *Learning Where to Focus: Density-Driven Guidance for Detecting Dense Tiny Objects* — <https://arxiv.org/abs/2512.22949>
- [S32] SkyFusion on Kaggle — <https://www.kaggle.com/datasets/kailaspsudheer/tiny-object-detection>
- [S33] Kailas PS et al., *Analysis of Object Detection Models for Tiny Object in Satellite Imagery* — <https://arxiv.org/abs/2412.10453>
- [S34] Shi et al., *Similarity Distance-Based Label Assignment for Tiny Object Detection* (M-CenterNet on AI-TOD, Table II) — <https://arxiv.org/abs/2407.02394>
- [S35] CenterNet target generation (`ctdet.py`, `image.py`) — <https://github.com/xingyizhou/CenterNet/tree/master/src/lib>
- [S36] Zhao et al., *Bridging the Scale Gap* (ScaleBridge-Det; AI-TOD-v2 comparison table) — <https://arxiv.org/abs/2512.01665>
- [S37] Huang et al., *DQ-DETR*, ECCV 2024 — <https://arxiv.org/abs/2404.03507>
- [S38] Yuan et al., *An Empirical Study of Methods for Small Object Detection from Satellite Imagery* — <https://arxiv.org/abs/2502.03674>
- [S39] Akyon et al., *SAHI*, ICIP 2022 — <https://arxiv.org/abs/2202.06934>
- [S40] DOTA devkit evaluation for oriented boxes (`dota_evaluation_task1.py`: difficult objects excluded from `npos` and from matching; `ovthresh=0.5`) — <https://github.com/CAPTAIN-WHU/DOTA_devkit/blob/master/dota_evaluation_task1.py>
- [S41] xView challenge data page (train_images: 846 images; val_images: 282 images; download links) — <https://challenge.xviewdataset.org/data-download>
- [S42] Kaggle mirror of the xView download (train images, train labels, val images; 20.8 GB) — <https://www.kaggle.com/datasets/hassanmojab/xview-dataset>
