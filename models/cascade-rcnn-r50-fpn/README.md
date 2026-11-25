# Cascade R-CNN with ResNet-50 and FPN: how to run

Faster R-CNN with three box-refinement stages. Model details are in
[about.md](about.md) and our results in [results.md](results.md).

**Status:** not tried yet. The setup is the same as for
[Faster R-CNN](../faster-rcnn-r50-fpn/README.md); only the config and weights
change.

| Dataset | Code | Environment |
|---|---|---|
| COCO | [MMDetection 3.x](https://github.com/open-mmlab/mmdetection) | `openmmlab` |
| AI-TOD-v2 | [mmdet-aitod](https://github.com/Chasel-Tsui/mmdet-aitod) (based on MMDetection 2.24.1) | `aitod` |

## COCO

Setup and data: the same `openmmlab` environment and COCO link as
[CenterNet Update](../centernet-update-r50-fpn/README.md#1-setup).

### Weights

From the [Cascade R-CNN configs page](https://github.com/open-mmlab/mmdetection/tree/main/configs/cascade_rcnn):

| Config | COCO val 2017 | Training memory | Checkpoint |
|---|---|---|---|
| [`cascade-rcnn_r50_fpn_1x_coco.py`](https://github.com/open-mmlab/mmdetection/blob/main/configs/cascade_rcnn/cascade-rcnn_r50_fpn_1x_coco.py) | 40.3 AP | 4.4 GB | [model](https://download.openmmlab.com/mmdetection/v2.0/cascade_rcnn/cascade_rcnn_r50_fpn_1x_coco/cascade_rcnn_r50_fpn_1x_coco_20200316-3dc56deb.pth) |

Put the checkpoint in `checkpoints/cascade-rcnn-r50-fpn/` in this repo.

### Test on COCO val 2017

Run from the `mmdetection` folder
([test guide](https://github.com/open-mmlab/mmdetection/blob/main/docs/en/user_guides/test.md)):

```bash
python tools/test.py \
    configs/cascade_rcnn/cascade-rcnn_r50_fpn_1x_coco.py \
    /path/to/checkpoints/cascade-rcnn-r50-fpn/cascade_rcnn_r50_fpn_1x_coco_20200316-3dc56deb.pth \
    --work-dir /path/to/tiny-object-detection/outputs/cascade-rcnn-r50-fpn/<run name>
```

The expected result is **40.3 AP**.

## AI-TOD-v2

Setup and data: the same `aitod` environment and AI-TOD-v2 link as
[Faster R-CNN](../faster-rcnn-r50-fpn/README.md#ai-tod-v2).

### Config

The baseline config is
[`configs_nwdrka/baseline/aitodv2_cascade_rcnn_r50_baseline_1x.py`](https://github.com/Chasel-Tsui/mmdet-aitod/blob/main/mmdet-nwdrka/configs_nwdrka/baseline/aitodv2_cascade_rcnn_r50_baseline_1x.py).
It loads `aitodv2_detection.py`, so it points to the AI-TOD-v2 files.

### Weights

No published weights for the plain Cascade R-CNN on AI-TOD-v2 found, so we
plan to train it ourselves.

### Train and test

Run from `mmdet-aitod/mmdet-nwdrka`:

```bash
python tools/train.py configs_nwdrka/baseline/aitodv2_cascade_rcnn_r50_baseline_1x.py --work-dir /path/to/tiny-object-detection/outputs/cascade-rcnn-r50-fpn/<run name>
```

```bash
python tools/test.py configs_nwdrka/baseline/aitodv2_cascade_rcnn_r50_baseline_1x.py <checkpoint> --eval bbox
```

The published result to compare with is **15.1 AP, AP_vt 0.1, AP_t 11.5**
([NWD-RKA paper](https://arxiv.org/abs/2206.13996)). The log of that run is at
the top of the config file, including per-class AP, so we can compare more
than the headline number.
