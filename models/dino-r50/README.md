# DINO with ResNet-50: how to run

A DETR-style anchor-free detector, run in MMDetection 3.x. Model details are
in [about.md](about.md) and our results in [results.md](results.md).

**Status:** not tried yet. This is our anchor-free runner-up; we add it if the
GPU allows (its training memory is still **TBD**).

The steps below are from MMDetection's
[test guide](https://github.com/open-mmlab/mmdetection/blob/main/docs/en/user_guides/test.md),
[train guide](https://github.com/open-mmlab/mmdetection/blob/main/docs/en/user_guides/train.md)
and the [DINO configs page](https://github.com/open-mmlab/mmdetection/tree/main/configs/dino).

## 1. Setup and data

Use the `openmmlab` environment and COCO link from
[CenterNet Update](../centernet-update-r50-fpn/README.md#1-setup).

## 2. Weights

| Config | COCO val 2017 | Checkpoint |
|---|---|---|
| [`dino-4scale_r50_8xb2-12e_coco.py`](https://github.com/open-mmlab/mmdetection/blob/main/configs/dino/dino-4scale_r50_8xb2-12e_coco.py) | 49.0 AP | [model](https://download.openmmlab.com/mmdetection/v3.0/dino/dino-4scale_r50_8xb2-12e_coco/dino-4scale_r50_8xb2-12e_coco_20221202_182705-55b2bba2.pth) |

Put the checkpoint in `checkpoints/dino-r50/` in this repo.

## 3. Test on COCO val 2017

Run from the `mmdetection` folder:

```bash
python tools/test.py \
    configs/dino/dino-4scale_r50_8xb2-12e_coco.py \
    /path/to/checkpoints/dino-r50/dino-4scale_r50_8xb2-12e_coco_20221202_182705-55b2bba2.pth \
    --work-dir /path/to/tiny-object-detection/outputs/dino-r50/<run name>
```

The expected result is **49.0 AP**.

## 4. AI-TOD-v2

**TBD**, shared with the other MMDetection 3.x models (see
[CenterNet-HRNet-W18, step 4](../centernet-hrnet-w18/README.md#4-ai-tod-v2)).
Two things specific to DINO:

- keep all 900 queries at test time (`model.test_cfg.max_per_img=900`); the
  config keeps 300
- the published AI-TOD-v2 result to compare with is **25.9 AP, AP_vt 12.7**,
  from the DQ-DETR authors' re-implementation, which trained with batch 1
  ([DQ-DETR paper](https://arxiv.org/abs/2404.03507))

Train with the COCO config as the base and `--auto-scale-lr` on fewer than 8
GPUs (train guide). **TBD:** training memory at AI-TOD-v2's 800×800 size.
