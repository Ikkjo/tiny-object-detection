# CenterNet Update with ResNet-50 and FPN: how to run

An updated CenterNet by the same author, run in MMDetection 3.x. Model
details are in [about.md](about.md) and our results in
[results.md](results.md).

**Status:** not tried yet. This is our runner-up, used if the original
[CenterNet DLA-34](../centernet-dla34/) code can't be made to run.

The steps below are from MMDetection's
[install guide](https://github.com/open-mmlab/mmdetection/blob/main/docs/en/get_started.md),
[data guide](https://github.com/open-mmlab/mmdetection/blob/main/docs/en/user_guides/dataset_prepare.md),
[test guide](https://github.com/open-mmlab/mmdetection/blob/main/docs/en/user_guides/test.md)
and [train guide](https://github.com/open-mmlab/mmdetection/blob/main/docs/en/user_guides/train.md),
and from the [CenterNet configs page](https://github.com/open-mmlab/mmdetection/tree/main/configs/centernet).

## 1. Setup

MMDetection needs Python 3.7+, CUDA 9.2+ and PyTorch 1.8+.

1. Create a conda environment and install PyTorch (on a GPU machine):

   ```bash
   conda create --name openmmlab python=3.8 -y
   conda activate openmmlab
   conda install pytorch torchvision -c pytorch
   ```

   The guide says to follow the [official PyTorch instructions](https://pytorch.org/get-started/locally/)
   for the exact command for your CUDA version.

2. Install MMEngine and MMCV:

   ```bash
   pip install -U openmim
   mim install mmengine
   mim install "mmcv>=2.0.0"
   ```

3. Clone MMDetection (outside this repo) and install it from source:

   ```bash
   git clone https://github.com/open-mmlab/mmdetection.git
   cd mmdetection
   pip install -v -e .
   ```

The same environment is used for the COCO runs of
[Faster R-CNN](../faster-rcnn-r50-fpn/) and [Cascade R-CNN](../cascade-rcnn-r50-fpn/).

## 2. Data

MMDetection expects COCO in `mmdetection/data/coco/` (with `annotations/`,
`train2017/` and `val2017/`). The guide recommends keeping the dataset
elsewhere and linking it:

```bash
ln -s /path/to/tiny-object-detection/data/coco mmdetection/data/coco
```

**AI-TOD-v2:** MMDetection 3.x has no AI-TOD-v2 config, and its COCO
evaluation doesn't report the AI-TOD size bins (AP_vt, AP_t). **TBD**, shared
with the other MMDetection 3.x models (see
[CenterNet-HRNet-W18, step 4](../centernet-hrnet-w18/README.md#4-ai-tod-v2)):
write an AI-TOD-v2 dataset config, save the predictions as COCO JSON and score
them with [cocoapi-aitod](https://github.com/jwwangchn/cocoapi-aitod). The
config keeps 100 detections per image (`model.test_cfg.max_per_img`); raise it
to 1,500 for AI-TOD-v2, where a cap of 100 puts 26% of test objects out of
reach ([`scripts/detection_cap_stats.py`](../../scripts/detection_cap_stats.py)).

## 3. Weights

| Config | COCO val 2017 | Training memory | Checkpoint |
|---|---|---|---|
| [`centernet-update_r50-caffe_fpn_ms-1x_coco.py`](https://github.com/open-mmlab/mmdetection/blob/main/configs/centernet/centernet-update_r50-caffe_fpn_ms-1x_coco.py) | 40.2 AP | 3.3 GB | [model](https://download.openmmlab.com/mmdetection/v3.0/centernet/centernet-update_r50-caffe_fpn_ms-1x_coco/centernet-update_r50-caffe_fpn_ms-1x_coco_20230512_203845-8306baf2.pth) |

Put the checkpoint in `checkpoints/centernet-update-r50-fpn/` in this repo.

## 4. Test on COCO val 2017

Run from the `mmdetection` folder:

```bash
python tools/test.py \
    configs/centernet/centernet-update_r50-caffe_fpn_ms-1x_coco.py \
    /path/to/checkpoints/centernet-update-r50-fpn/centernet-update_r50-caffe_fpn_ms-1x_coco_20230512_203845-8306baf2.pth \
    --work-dir /path/to/tiny-object-detection/outputs/centernet-update-r50-fpn/<run name>
```

`--work-dir` saves the metrics to that folder. The expected result is
**40.2 AP**. Write it in [results.md](results.md).

## 5. Train

```bash
python tools/train.py configs/centernet/centernet-update_r50-caffe_fpn_ms-1x_coco.py
```

The configs page warns that this model's results vary a lot between runs and
it sometimes doesn't converge. If that happens, run it again or lower the
learning rate. **TBD:** batch size and learning rate for our GPU.
