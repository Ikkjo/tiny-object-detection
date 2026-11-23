# CenterNet Update with ResNet-50 and FPN

An updated CenterNet by the same author, with an FPN so it predicts on several
resolutions. It is our **CenterNet runner-up** for Track B of issue #2. The
reasons are in the
[Track B notes](../../docs/models/standard-centernet-and-two-stage.md).

How to run it: [README.md](README.md).

## Links

- **Paper:** [Probabilistic two-stage detection](https://arxiv.org/abs/2103.07461) (CenterNet2, Zhou et al., 2021)
- **MMDetection configs and weights:** [configs/centernet](https://github.com/open-mmlab/mmdetection/tree/main/configs/centernet)
- **Author's code (Detectron2):** [CenterNet2](https://github.com/xingyizhou/CenterNet2), [model zoo](https://github.com/xingyizhou/CenterNet2/blob/master/docs/MODEL_ZOO.md)

## Properties

| Property | Value | Source |
|---|---|---|
| Parameters / FLOPs | **TBD** | — |
| Output stride | FPN levels with strides 8, 16, 32, 64 and 128, so the finest is **8**. Objects are assigned to a level by size | [MMDetection config](https://github.com/open-mmlab/mmdetection/blob/main/configs/centernet/centernet-update_r50-caffe_fpn_ms-1x_coco.py), [CenterNet2 model zoo](https://github.com/xingyizhou/CenterNet2/blob/master/docs/MODEL_ZOO.md) |
| Training memory | 3.3 GB per GPU (MMDetection) | [MMDetection configs page](https://github.com/open-mmlab/mmdetection/tree/main/configs/centernet) |
| Training schedule | 12 epochs, SGD, learning rate 0.01 per batch of 16 | [MMDetection configs page](https://github.com/open-mmlab/mmdetection/tree/main/configs/centernet) |

## Published results

| Dataset | Result | Source |
|---|---|---|
| COCO val 2017 | 40.2 AP. AP_S: **TBD** | [MMDetection configs page](https://github.com/open-mmlab/mmdetection/tree/main/configs/centernet) |
| AI-TOD-v2 | None found | — |

## What changed from the original CenterNet

From the [MMDetection configs page](https://github.com/open-mmlab/mmdetection/tree/main/configs/centernet)
and the [CenterNet2 model zoo](https://github.com/xingyizhou/CenterNet2/blob/master/docs/MODEL_ZOO.md):

- the box is encoded as distances to its 4 sides, with a GIoU loss
- the regression loss is also applied in the 3×3 region around the centre
- more pixels count as positives in the heatmap loss
- FPN levels, with objects assigned to a level by size
- standard NMS instead of max pooling

## Strengths and weaknesses

**Strengths:** easy to run in a current framework, uses little memory, and
predicts on several resolutions, which is one of our research directions.

**Weaknesses:** it changes the original CenterNet loss and how positives are
chosen, so it is a different model from the one in the paper. Its finest
output stride is 8, coarser than the original's 4. There are no published
tiny-object results. MMDetection notes that it sometimes doesn't converge.
