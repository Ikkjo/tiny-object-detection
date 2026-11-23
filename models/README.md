# Models

Each model we benchmark has its own folder here. Opening a folder shows its
`README.md`, which says how to set the model up and run it. The other files
hold everything else about the model.

## What is in each model folder

| File | What it has |
|---|---|
| `README.md` | How to run the model: setup, data paths, weights, and the commands for testing and training |
| `about.md` | What the model is: paper, code, output stride, published results, memory, strengths and weaknesses, with sources |
| `results.md` | Our own results, one row per run, with the config and checkpoint used |
| `configs/` | Our own config files, once we start changing the model (not created yet) |

The research that compares models and explains why we chose them is in
[`docs/models/`](../docs/models/). This folder is for the models we chose.

## Where large files go

Weights, datasets and raw outputs are never committed (see `.gitignore`).

- **Weights:** `checkpoints/<model folder>/`, e.g.
  `checkpoints/faster-rcnn-r50-fpn/`
- **Datasets:** `data/coco/`, `data/AI-TODv2/`
- **Raw outputs** (logs, prediction files, visualisations):
  `outputs/<model folder>/<run name>/`

`results.md` records where each file came from (the download link or the
training run), so anyone can get the same file again.

## Models

| Folder | Model | Role | Code |
|---|---|---|---|
| [`centernet-dla34`](centernet-dla34/) | CenterNet with DLA-34 | CenterNet nominee | Official CenterNet repo |
| [`centernet-update-r50-fpn`](centernet-update-r50-fpn/) | CenterNet Update with ResNet-50 and FPN | CenterNet runner-up | MMDetection 3.x |
| [`faster-rcnn-r50-fpn`](faster-rcnn-r50-fpn/) | Faster R-CNN with ResNet-50 and FPN | Two-stage nominee | MMDetection 3.x (COCO), mmdet-aitod (AI-TOD-v2) |
| [`cascade-rcnn-r50-fpn`](cascade-rcnn-r50-fpn/) | Cascade R-CNN with ResNet-50 and FPN | Two-stage runner-up | MMDetection 3.x (COCO), mmdet-aitod (AI-TOD-v2) |
| [`centernet-hrnet-w18`](centernet-hrnet-w18/) | CenterNet with HRNet-W18 | CenterNet backbone nominee (Track C) | MMDetection 3.x, our config |
| [`centernet-swin-t`](centernet-swin-t/) | CenterNet with Swin-T | CenterNet backbone runner-up (Track C) | MMDetection 3.x, our config |
| [`centernet-hourglass104`](centernet-hourglass104/) | CenterNet with Hourglass-104 | Reference, inference only (Track C) | Official CenterNet repo |
| [`fcos-r50-fpn`](fcos-r50-fpn/) | FCOS with ResNet-50 and FPN (also with P2 and RFLA) | Anchor-free nominee (Track C) | MMDetection 3.x (COCO), mmdet-rfla (AI-TOD-v2) |
| [`dino-r50`](dino-r50/) | DINO with ResNet-50 | Anchor-free runner-up (Track C) | MMDetection 3.x |
| [`faster-rcnn-r50-fpn-rfla`](faster-rcnn-r50-fpn-rfla/) | Faster R-CNN with ResNet-50, FPN and RFLA | Label-assignment nominee (Track C) | mmdet-rfla (AI-TOD-v2 only) |
| [`faster-rcnn-r50-fpn-nwdrka`](faster-rcnn-r50-fpn-nwdrka/) | Faster R-CNN with ResNet-50, FPN and NWD-RKA | Label-assignment runner-up (Track C) | mmdet-aitod (AI-TOD-v2 only) |

## Adding a model

1. Make a folder named after the model and backbone, in lowercase with
   hyphens, e.g. `retinanet-r50-fpn`.
2. Copy the three files from an existing folder and fill them in. Every
   command in `README.md` should come from the model's own docs, with a link.
   Mark anything we haven't tried yet.
3. Add the model to the table above.

## Code environments

The models need different, incompatible environments, so we keep one
environment for each:

| Environment | Used for | Main versions |
|---|---|---|
| `centernet` | Official CenterNet code | Python 3.6, PyTorch 0.4.1 ([install guide](https://github.com/xingyizhou/CenterNet/blob/master/readme/INSTALL.md)) |
| `openmmlab` | MMDetection 3.x | Python 3.8, PyTorch 1.8+, MMCV 2.x ([install guide](https://github.com/open-mmlab/mmdetection/blob/main/docs/en/get_started.md)) |
| `aitod` | mmdet-aitod (MMDetection 2.24.1) | MMCV from 1.3.17 to 1.6.0 ([mmdet/\_\_init\_\_.py](https://github.com/Chasel-Tsui/mmdet-aitod/blob/main/mmdet-nwdrka/mmdet/__init__.py)), PyTorch 1.3+ ([README](https://github.com/Chasel-Tsui/mmdet-aitod)) |
| `rfla` | mmdet-rfla (MMDetection 2.13.0) | MMCV from 1.3.2 to 1.4.0 ([mmdet/\_\_init\_\_.py](https://github.com/Chasel-Tsui/mmdet-rfla/blob/main/mmdet/__init__.py)), PyTorch 1.3+ ([README](https://github.com/Chasel-Tsui/mmdet-rfla)) |

The code repositories themselves (CenterNet, MMDetection, mmdet-aitod, mmdet-rfla) are
cloned outside this repo. Each model's `README.md` says which one it needs.
