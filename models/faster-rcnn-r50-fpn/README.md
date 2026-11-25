# Faster R-CNN with ResNet-50 and FPN: how to run

The standard two-stage detector. Model details are in [about.md](about.md) and
our results in [results.md](results.md).

**Status:** not tried yet.

We use two codebases, because the AI-TOD-v2 configs and evaluation only exist
for an older MMDetection:

| Dataset | Code | Environment |
|---|---|---|
| COCO | [MMDetection 3.x](https://github.com/open-mmlab/mmdetection) | `openmmlab` |
| AI-TOD-v2 | [mmdet-aitod](https://github.com/Chasel-Tsui/mmdet-aitod) (based on MMDetection 2.24.1) | `aitod` |

## COCO

The steps are from MMDetection's
[install guide](https://github.com/open-mmlab/mmdetection/blob/main/docs/en/get_started.md),
[test guide](https://github.com/open-mmlab/mmdetection/blob/main/docs/en/user_guides/test.md)
and the [Faster R-CNN configs page](https://github.com/open-mmlab/mmdetection/tree/main/configs/faster_rcnn).

### 1. Setup and data

Use the same `openmmlab` environment and COCO link as
[CenterNet Update](../centernet-update-r50-fpn/README.md#1-setup).

### 2. Weights

| Config | COCO val 2017 | Training memory | Checkpoint |
|---|---|---|---|
| [`faster-rcnn_r50_fpn_1x_coco.py`](https://github.com/open-mmlab/mmdetection/blob/main/configs/faster_rcnn/faster-rcnn_r50_fpn_1x_coco.py) | 37.4 AP | 4.0 GB | [model](https://download.openxlab.org.cn/models/mmdetection/FasterR-CNN/weight/faster-rcnn_r50_fpn_1x_coco) |

Put the checkpoint in `checkpoints/faster-rcnn-r50-fpn/` in this repo.

### 3. Test on COCO val 2017

Run from the `mmdetection` folder:

```bash
python tools/test.py \
    configs/faster_rcnn/faster-rcnn_r50_fpn_1x_coco.py \
    /path/to/checkpoints/faster-rcnn-r50-fpn/<checkpoint file> \
    --work-dir /path/to/tiny-object-detection/outputs/faster-rcnn-r50-fpn/<run name>
```

The expected result is **37.4 AP**.

### Quick check without MMDetection

torchvision also has this model with COCO weights
([`fasterrcnn_resnet50_fpn`](https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.detection.fasterrcnn_resnet50_fpn.html)).
It is an easy way to look at predictions, but for our numbers we use
MMDetection so all models are evaluated the same way.

## AI-TOD-v2

The steps are from the [mmdet-aitod README](https://github.com/Chasel-Tsui/mmdet-aitod)
and the [cocoapi-aitod README](https://github.com/jwwangchn/cocoapi-aitod).

### 1. Setup

mmdet-aitod needs Linux, Python 3.6+, PyTorch 1.3+, CUDA 9.2+, GCC 5+, MMCV
between 1.3.17 and 1.6.0
([version check](https://github.com/Chasel-Tsui/mmdet-aitod/blob/main/mmdet-nwdrka/mmdet/__init__.py)),
and cocoapi-aitod.

1. Install the AI-TOD evaluation code, which adds the AI-TOD size bins:

   ```bash
   pip install "git+https://github.com/jwwangchn/cocoapi-aitod.git#subdirectory=aitodpycocotools"
   ```

2. Clone mmdet-aitod (outside this repo) and install it:

   ```bash
   git clone https://github.com/Chasel-Tsui/mmdet-aitod.git
   cd mmdet-aitod/mmdet-nwdrka
   pip install -r requirements/build.txt
   python setup.py develop
   ```

**TBD:** the exact PyTorch, CUDA and MMCV versions that work together. The
README only gives minimum versions.

### 2. Data

The AI-TOD-v2 config expects this layout
([dataset config](https://github.com/Chasel-Tsui/mmdet-aitod/blob/main/mmdet-nwdrka/configs_nwdrka/_base_/datasets/aitodv2_detection.py)):

```text
mmdet-nwdrka/data/AI-TODv2/
├── annotations/
│   ├── small_trainval_v2_2.0.json
│   └── small_test_v2_2.0.json
├── trainval/
└── test/
```

Link our copy there:

```bash
ln -s /path/to/tiny-object-detection/data/AI-TODv2 mmdet-nwdrka/data/AI-TODv2
```

How to get AI-TOD-v2 is in the
[aerial dataset notes](../../docs/datasets/aerial-dataset.md).

### 3. Config

The baseline config is
[`configs_nwdrka/baseline/aitodv2_faster_rcnn_r50_baseline_1x.py`](https://github.com/Chasel-Tsui/mmdet-aitod/blob/main/mmdet-nwdrka/configs_nwdrka/baseline/aitodv2_faster_rcnn_r50_baseline_1x.py).
It trains for 12 epochs with batch 2 per GPU and learning rate 0.01.

**Check before using it:** although its name says AI-TOD-v2, this config
loads `aitod_detection.py`, which points to the AI-TOD **v1** files
(`data/AI-TOD/`, `small_trainval_v1_1.0.json`). The Cascade R-CNN baseline
loads `aitodv2_detection.py` instead. For AI-TOD-v2 we change the dataset line
in the `_base_` list to `'../_base_/datasets/aitodv2_detection.py'`. When we
make that change, we keep the changed copy in a `configs/` folder here.

### 4. Weights

mmdet-aitod has no published weights for the plain Faster R-CNN. The RFLA repo
links a set of pretrained models
([OneDrive, from the RFLA README](https://github.com/Chasel-Tsui/mmdet-rfla#main-results)),
but which models are in it is **TBD**. So we plan to train it ourselves.

### 5. Train and test

Run from `mmdet-aitod/mmdet-nwdrka`:

```bash
python tools/train.py <config> --work-dir /path/to/tiny-object-detection/outputs/faster-rcnn-r50-fpn/<run name>
```

```bash
python tools/test.py <config> <checkpoint> --eval bbox
```

The published result to compare with is **12.8 AP, AP_vt 0.0, AP_t 9.2**
([RFLA README](https://github.com/Chasel-Tsui/mmdet-rfla#main-results), Table 2).
The output includes AP_vt and AP_t: mmdet-aitod's AI-TOD-v2 dataset class
scores with the AI-TOD version of the COCO API and counts up to 1,500
detections per image
([`mmdet/datasets/aitodv2.py`](https://github.com/Chasel-Tsui/mmdet-aitod/blob/main/mmdet-nwdrka/mmdet/datasets/aitodv2.py)).
The configs keep up to 3,000 detections per image, so nothing is cut before
scoring.
