# CenterNet with HRNet-W18: how to run

CenterNet with an HRNet-W18 backbone, in MMDetection 3.x. Model details are
in [about.md](about.md) and our results in [results.md](results.md).

**Status:** not tried yet. No published model or config exists for this
combination, so we wrote our own config from MMDetection's CenterNet and HRNet
configs: [configs/centernet_hrnetv2p-w18_crop512-140e_coco.py](configs/centernet_hrnetv2p-w18_crop512-140e_coco.py).
It has not been run.

The steps below are from MMDetection's
[install guide](https://github.com/open-mmlab/mmdetection/blob/main/docs/en/get_started.md),
[test guide](https://github.com/open-mmlab/mmdetection/blob/main/docs/en/user_guides/test.md),
[train guide](https://github.com/open-mmlab/mmdetection/blob/main/docs/en/user_guides/train.md)
and [config guide](https://github.com/open-mmlab/mmdetection/blob/main/docs/en/user_guides/config.md).

## 1. Setup and data

Use the `openmmlab` environment and the COCO link from
[CenterNet Update](../centernet-update-r50-fpn/README.md#1-setup). HRNet needs
nothing extra.

## 2. Check the setup first

Before training our own combination, check that MMDetection's CenterNet
reproduces its published result. Download the ResNet-18 model from the
[CenterNet configs page](https://github.com/open-mmlab/mmdetection/tree/main/configs/centernet)
([checkpoint](https://download.openmmlab.com/mmdetection/v2.0/centernet/centernet_resnet18_dcnv2_140e_coco/centernet_resnet18_dcnv2_140e_coco_20210702_155131-c8cd631f.pth))
into `checkpoints/centernet-hrnet-w18/`, then run from the `mmdetection`
folder:

```bash
python tools/test.py \
    configs/centernet/centernet_r18-dcnv2_8xb16-crop512-140e_coco.py \
    /path/to/checkpoints/centernet-hrnet-w18/centernet_resnet18_dcnv2_140e_coco_20210702_155131-c8cd631f.pth \
    --work-dir /path/to/tiny-object-detection/outputs/centernet-hrnet-w18/<run name>
```

The expected result is **29.5 AP** (the configs page says 29.4 to 29.8 is
normal). This config uses deformable convolutions, so it needs the full MMCV
with CUDA operators.

## 3. Train on COCO

There are no pretrained weights for the whole detector; the HRNet-W18
ImageNet weights download automatically the first time (set in the config).

```bash
python tools/train.py \
    /path/to/tiny-object-detection/models/centernet-hrnet-w18/configs/centernet_hrnetv2p-w18_crop512-140e_coco.py \
    --work-dir /path/to/tiny-object-detection/outputs/centernet-hrnet-w18/<run name>
```

The base recipe is 140 epochs with batch 16 on each of 8 GPUs. On fewer GPUs,
add `--auto-scale-lr` to scale the learning rate with the total batch size
(train guide). **TBD:** batch size for our GPU, and whether 140 epochs fits
our time budget.

Then test as in step 2, with our config and the new checkpoint. There is no
published number to compare with.

## 4. AI-TOD-v2

**TBD**, shared with the other MMDetection 3.x models (see the
[Track C open items](../../docs/models/centernet-backbones-and-anchor-free.md#7-open-items)):

- a dataset config: COCO format with AI-TOD-v2's 8 classes, set through
  `metainfo` as in the train guide's custom-dataset example
- `model.test_cfg.topk` and `max_per_img` raised from 100 to 1,500
- save predictions as COCO JSON (`test_evaluator.format_only=True` and
  `test_evaluator.outfile_prefix=...`, from the config guide) and score them
  with [cocoapi-aitod](https://github.com/jwwangchn/cocoapi-aitod) to get
  AP_vt and AP_t
