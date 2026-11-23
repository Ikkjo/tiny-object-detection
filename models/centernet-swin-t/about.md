# CenterNet with Swin-T

CenterNet predicts each object as its centre point on a heatmap, plus the box
size and a small offset. Here its backbone is Swin-T, a transformer that
computes attention inside local windows and gives feature maps at strides 4,
8, 16 and 32 like a ResNet. It is our **CenterNet backbone runner-up** for
Track C of issue #2. The reasons are in the
[Track C notes](../../docs/models/centernet-backbones-and-anchor-free.md).

How to run it: [README.md](README.md).

## Links

- **CenterNet paper:** [Objects as Points](https://arxiv.org/abs/1904.07850) (Zhou et al., 2019)
- **Swin paper:** [Swin Transformer: Hierarchical Vision Transformer using Shifted Windows](https://arxiv.org/abs/2103.14030) (Liu et al., ICCV 2021)
- **MMDetection CenterNet:** [configs/centernet](https://github.com/open-mmlab/mmdetection/tree/main/configs/centernet)
- **MMDetection Swin:** [configs/swin](https://github.com/open-mmlab/mmdetection/tree/main/configs/swin)
- **Closest published work:** [Small Object Detection for Birds with Swin Transformer](https://arxiv.org/abs/2511.22310), a CenterNet with a Swin backbone and a Swin neck

No published model exists for CenterNet with a Swin-T backbone on COCO or
AI-TOD-v2. Our config is in [configs/](configs/).

## Properties

| Property | Value | Source |
|---|---|---|
| Output stride | 4, using the same HRFPN neck as CenterNet-HRNet-W18 to merge Swin's four maps into one stride-4 map *(untried)* | [Swin paper](https://arxiv.org/abs/2103.14030), [HRFPN code](https://github.com/open-mmlab/mmdetection/blob/main/mmdet/models/necks/hrfpn.py) |
| Parameters / FLOPs | Swin-T backbone: 28M parameters, 4.5 GFLOPs at 224×224 (classification). Full detector: **TBD** | [Swin paper](https://arxiv.org/abs/2103.14030) |
| Window | 7×7 tokens, each token a 4×4 patch | [MMDetection Swin config](https://github.com/open-mmlab/mmdetection/blob/main/configs/swin/retinanet_swin-t-p4-w7_fpn_1x_coco.py) |
| Pretrained weights | ImageNet-1K Swin-T, linked from MMDetection's Swin configs | [MMDetection Swin config](https://github.com/open-mmlab/mmdetection/blob/main/configs/swin/retinanet_swin-t-p4-w7_fpn_1x_coco.py) |
| Optimizer | AdamW, learning rate 1e-4, weight decay 0.05, as in MMDetection's Swin configs | [MMDetection Swin config](https://github.com/open-mmlab/mmdetection/blob/main/configs/swin/mask-rcnn_swin-t-p4-w7_fpn_1x_coco.py) |
| Training memory | **TBD**. For scale: Mask R-CNN with Swin-T uses 7.6 GB per GPU in MMDetection | [MMDetection Swin configs](https://github.com/open-mmlab/mmdetection/tree/main/configs/swin) |

## Published results

| Dataset | Result | Source |
|---|---|---|
| COCO, other detectors | Swin-T beats ResNet-50 by 3.4–4.2 box AP in Cascade Mask R-CNN, ATSS, RepPoints v2 and Sparse R-CNN. Mask R-CNN with Swin-T: 42.7 box AP (MMDetection, 1x schedule) | [Swin paper](https://arxiv.org/abs/2103.14030), [MMDetection Swin configs](https://github.com/open-mmlab/mmdetection/tree/main/configs/swin) |
| SODA-A (aerial, small objects) | Swin-T **lowered** one-stage detectors (Rotated RetinaNet −3.5 AP) and helped two-stage ones by 0.1–1.2 AP, compared with ResNet-50 | [SODA paper](https://arxiv.org/abs/2207.14096) |
| Small birds (SOD4SB) | CenterNet with Swin: smaller windows (size 2) worked better on small objects | [Birds paper](https://arxiv.org/abs/2511.22310) |
| AI-TOD-v2 | None found | — |

## Strengths and weaknesses

**Strengths:** it keeps CenterNet's head and loss and changes only the
feature extractor, so it tests whether attention helps CenterNet on tiny
objects (research direction 4). A survey of transformer small-object
detectors credits the context that attention adds for their lead on most
datasets ([survey](https://arxiv.org/abs/2309.04902)).

**Weaknesses:** the SODA-A result suggests a transformer backbone can hurt
one-stage detectors on small objects. It uses more memory than a ResNet, and
the window size chosen for ImageNet may not suit 8–16 px objects.
