# CenterNet with Swin-T: how to run

CenterNet with a Swin-T backbone, in MMDetection 3.x. Model details are in
[about.md](about.md) and our results in [results.md](results.md).

**Status:** not tried yet. No published model or config exists for this
combination, so we wrote our own config from MMDetection's CenterNet and Swin
configs: [configs/centernet_swin-t-p4-w7_crop512-140e_coco.py](configs/centernet_swin-t-p4-w7_crop512-140e_coco.py).
It has not been run.

The steps below are from MMDetection's
[install guide](https://github.com/open-mmlab/mmdetection/blob/main/docs/en/get_started.md),
[train guide](https://github.com/open-mmlab/mmdetection/blob/main/docs/en/user_guides/train.md)
and [test guide](https://github.com/open-mmlab/mmdetection/blob/main/docs/en/user_guides/test.md).

## 1. Setup and data

Use the `openmmlab` environment and the COCO link from
[CenterNet Update](../centernet-update-r50-fpn/README.md#1-setup). Swin needs
nothing extra.

Check the CenterNet setup first with MMDetection's ResNet-18 model, as in
[CenterNet-HRNet-W18, step 2](../centernet-hrnet-w18/README.md#2-check-the-setup-first).

## 2. Train on COCO

The Swin-T ImageNet weights download automatically the first time (set in the
config).

```bash
python tools/train.py \
    /path/to/tiny-object-detection/models/centernet-swin-t/configs/centernet_swin-t-p4-w7_crop512-140e_coco.py \
    --work-dir /path/to/tiny-object-detection/outputs/centernet-swin-t/<run name>
```

On fewer than 8 GPUs, add `--auto-scale-lr` (train guide). **TBD:** batch
size for our GPU; whether 140 epochs is needed with AdamW (MMDetection's Swin
detectors train for 12 or 36 epochs).

## 3. Test

```bash
python tools/test.py \
    /path/to/tiny-object-detection/models/centernet-swin-t/configs/centernet_swin-t-p4-w7_crop512-140e_coco.py \
    /path/to/checkpoints/centernet-swin-t/<checkpoint file> \
    --work-dir /path/to/tiny-object-detection/outputs/centernet-swin-t/<run name>
```

There is no published number to compare with.

## 4. Window size

To try smaller windows, change `model.backbone.window_size` (for example to
2, the setting the birds paper found best for small objects). The ImageNet
weights were trained with window 7, so their position tables won't match a
different window size; **TBD:** how MMDetection handles that when loading
(it may need the tables resized or re-initialised).

## 5. AI-TOD-v2

Same as [CenterNet-HRNet-W18, step 4](../centernet-hrnet-w18/README.md#4-ai-tod-v2):
dataset config, 1,500 detections per image, and scoring with cocoapi-aitod
(**TBD**).
