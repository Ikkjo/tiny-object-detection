# Prompt: literature and dataset sweep for aerial tiny-object detection

**How to use.** Give everything below the line to an agent that has
unrestricted web access. Attach `scripts/aerial_size_stats.py` and
`docs/literature/paper-log.md` from the repo. Its output is designed to merge
straight into `paper-log.md`, `docs/datasets/aerial-dataset.md` and
`docs/datasets/stats/`.

---

## Who we are and what we need

We are a small research team working on **tiny object detection**: how well
existing detectors handle objects only a few pixels across, and how to
improve them. The work is tracked in two GitHub issues:

- **Issue #1:** choose datasets. This sweep covers the **aerial** part:
  drone, aerial and satellite imagery, both still images and video.
- **Issue #2:** choose models to benchmark on those datasets, on modest
  hardware (a single consumer GPU), then find where they fail and try to
  improve one.

Our starting point is point-based detectors (CornerNet, CenterNet) and their
loss functions: we ask which design choices break when an object is only a
few pixels wide. The research directions are:

1. the loss and label assignment (for example RFLA)
2. the low-resolution output grid that predictions are mapped back from
3. multi-scale prediction
4. CNN vs transformer backbones
5. weaker supervision

We are **not** limited to CenterNet: we benchmark detectors of every family.

Definitions: "tiny" means a box size sqrt(w·h) under 16 px (AI-TOD
convention: very tiny 2–8, tiny 8–16, small 16–32, medium 32–64 px). COCO
"small" is area under 32² px. Always say which definition a number uses.

## Your task

Do a systematic sweep for papers on **tiny or small object detection in
aerial and remote-sensing imagery** (drone, airborne, satellite; images and
video), published 2018–2026. For every paper you include, record which
**datasets** it uses and which **models** it proposes and compares. For every
dataset, record how to get it and, where possible, measure it. Our current
list is in the attached `paper-log.md` (IDs L01–L39). Re-check those entries
and fill their **TBD** fields, but your main job is to find what we missed.

### 1. Search: be systematic and log it

Use all of the following, and keep a search log (query or source, date,
number of hits screened, number kept):

- **Keyword searches** on arXiv, Google Scholar, Semantic Scholar, CVF Open
  Access, IEEE Xplore and ISPRS / MDPI Remote Sensing. Combine {tiny, small,
  extremely small, dim, dense} × {object detection} × {aerial, UAV, drone,
  remote sensing, satellite, satellite video, overhead}. Also search for
  {label assignment, loss, heatmap, keypoint, CenterNet, point supervision,
  super-resolution, slicing/tiling, density, DETR, foundation model} + tiny
  object.
- **Forward citations** (papers that cite) of these anchors: AI-TOD (Wang et
  al., ICPR 2020), NWD-RKA / AI-TOD-v2 (Xu et al., ISPRS J. 2022), RFLA (ECCV
  2022), DotD (CVPRW 2021), SODA (TPAMI 2023), VisDrone (TPAMI 2021), VISO
  (TGRS 2021), CenterNet "Objects as Points" (2019) restricted to aerial or
  remote-sensing papers, and YOLC (T-ITS 2024).
- **Backward citations:** the related-work sections and comparison tables of
  the 2024–2026 papers you find.
- **Curated lists:** GitHub "awesome" lists for tiny / small object detection
  and for aerial / remote-sensing detection, and leaderboards on the
  datasets (AI-TOD-v2, VisDrone-DET, SODA-A, DOTA).
- **Venues to scan directly** (2022–2026): CVPR, ICCV, ECCV, NeurIPS, AAAI,
  ACM MM, TPAMI, TIP, TGRS, ISPRS J., JSTARS, GRSL.

**Include** a paper if it proposes a method, dataset or benchmark for tiny
or small objects and reports experiments on at least one aerial or
remote-sensing dataset. Generic detectors (YOLO versions, DETR variants)
count only if a paper above reports them on an aerial tiny-object dataset;
then list them as models, not as papers. Surveys go in a separate list.

**Exclude**, with a one-line reason in the log: infrared small-target
segmentation (single-frame IRSTD), pure tracking with no detection results,
and papers with no experiments on aerial data.

Aim to screen at least 150 candidates and fully extract 40–80 papers.
Prioritise: (a) point-based / CenterNet-family methods on aerial data;
(b) loss and label-assignment methods; (c) papers with public code; (d)
2024–2026 work.

### 2. Per paper: read the paper itself

Read the abstract, the dataset section and the main results tables of the
actual paper (PDF or HTML). Don't rely on search snippets or summaries.
Record:

| Field | Notes |
|---|---|
| title, authors (first author et al.), year, venue, arXiv / DOI link | |
| one-sentence summary | in your own words |
| relevance tags | any of: point-based, label-assignment/loss, multi-scale, super-resolution, slicing/tiling, density/clustering, DETR, foundation-model, weak/point supervision, video/temporal, oriented boxes, efficiency, dataset, benchmark, survey |
| datasets | every dataset with experiments, split used, metric (AP, AP50, AP_vt…) |
| proposed method | name, detector it is built on, backbone, input size |
| models compared | every baseline in the main table, with backbone |
| key numbers | the paper's own main result and the strongest baseline on each aerial dataset, with the table number |
| CenterNet / CornerNet results? | yes/no; if yes the numbers and table |
| code | repository URL, framework (MMDetection, MMRotate, Ultralytics, Detectron2, own), pretrained weights released? |
| hardware | GPU(s), training epochs, if stated |
| what was read | abstract / tables / full |
| TBD | any field you could not verify, plus **where** it is (section, table, page) |

### 3. Per dataset

For every dataset that appears in the included papers:

| Field | Notes |
|---|---|
| name, version, paper link, year | |
| domain | drone / airborne / satellite; still images / video; RGB / thermal / multispectral |
| GSD or flight altitude | if stated |
| images or frames, videos, instances, classes (names) | per split |
| image resolution | |
| annotation type and format | horizontal / oriented box / point; COCO JSON, DOTA txt, VisDrone txt, MOT, other |
| ignore regions, "difficult" flags, crowd labels | |
| official download, mirrors (Kaggle, Hugging Face, GitHub releases) | note which is official |
| annotation-only download available? | link and size |
| licence and access conditions | form, registration, academic only |
| test labels public? | |
| papers that use it | IDs |

**Measure it where you can.** If annotations can be downloaded without the
images, run the attached script:

```
python3 -I aerial_size_stats.py --format {coco,visdrone,dota,xview,sodaa} \
    --name "<dataset>/<split>" --json <dataset>_<split>.json <annotation path>
```

Run it once per split. For VisDrone and DOTA, add `--sizes sizes.json` (file
stem → [width, height]) if you can get image sizes without downloading the
images. If a format isn't supported, either add a loader (keep the output
fields identical) or compute the same fields yourself:

- box size sqrt(w·h): mean, median, p10, p90
- shares in the AI-TOD bins, < 16 and < 32 px
- for oriented boxes, sqrt(polygon area)
- objects per image
- image resolution
- per-class counts and median size
- CenterNet radius-0 share and stride-4 centre collisions

**Do not download images** unless annotations are only distributed inside
the image archive. In that case, stream the archive and keep only the
annotation files and each image's width and height. Write a provenance line
for every file: URL, official or mirror, date, size, SHA-256.

### 4. Per model (for issue #2)

For every model that appears as a method or a baseline:

| Field | Notes |
|---|---|
| name, family | two-stage, one-stage anchor-based, anchor-free dense, point-based, DETR, foundation model; horizontal or oriented |
| paper link, year | |
| maintained implementation | repo, framework, last commit year |
| backbones used in the papers | |
| parameters and FLOPs | if reported |
| output stride | for dense and point-based heads |
| pretrained weights | COCO / ImageNet / dataset-specific |
| reported results on aerial tiny-object datasets | dataset, metric, value, source paper ID and table |
| can it take a CenterNet backbone, or is it CenterNet-based? | |
| estimated VRAM to train at about 1024 px | only if stated somewhere; otherwise TBD |

## Output

Return these files:

1. `papers.csv`: one row per included paper. Columns, in this order: `id`
   (keep L01–L39 for known papers, number new ones N001…), `title`, `year`,
   `venue`, `link`, `summary`, `tags`, `datasets`, `method`, `built_on`,
   `backbone`, `models_compared`, `key_results`, `centernet_results`, `code`,
   `framework`, `hardware`, `read_level`, `tbd_where`.
2. `datasets.csv`: one row per dataset with the fields in section 3.
3. `models.csv`: one row per model with the fields in section 4.
4. `stats/<dataset>_<split>.json`: script output for every dataset you
   could measure.
5. `PROVENANCE.md`: one line per downloaded file.
6. `search_log.md`: queries and sources, hit counts, exclusions with
   reasons.
7. `summary.md`, at most two pages:
   - which datasets are most used, and which are genuinely tiny by
     measurement
   - which models recur as baselines
   - what has been done with point-based detectors on aerial data
   - any paper that already changes CenterNet's heatmap target, Gaussian
     radius or output stride for tiny objects (we believe this is a gap;
     confirm or refute it)
   - papers that explain why a detector family fails on tiny objects

## Rules

- Every number needs a source (paper ID + table or section, or a file you
  measured). Never estimate or fill a gap from memory. Write **TBD** and say
  where the answer is.
- Mark anything you computed yourself as *(est.)*.
- Report disagreements between sources (for example a dataset's paper and
  its README giving different counts) instead of picking one.
- Prefer official sources; label mirrors as mirrors.
- Keep quotes from papers under 125 characters and put everything else in
  your own words.
