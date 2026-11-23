# Cascade R-CNN with ResNet-50 and FPN

Faster R-CNN with three box-refinement stages in a row, each trained with a
stricter IoU threshold. It is our **two-stage runner-up** for Track B of
issue #2. The reasons are in the
[Track B notes](../../docs/models/standard-centernet-and-two-stage.md).

How to run it: [README.md](README.md).

## Links

- **Paper:** [Cascade R-CNN](https://arxiv.org/abs/1712.00726) (Cai & Vasconcelos, 2018)
- **MMDetection configs and weights:** [configs/cascade_rcnn](https://github.com/open-mmlab/mmdetection/tree/main/configs/cascade_rcnn)
- **AI-TOD code:** [mmdet-aitod](https://github.com/Chasel-Tsui/mmdet-aitod) (baseline and NWD-RKA configs)

## Properties

| Property | Value | Source |
|---|---|---|
| Parameters / FLOPs | **TBD** | — |
| Output stride | Same FPN levels as Faster R-CNN, so the finest is 4 | [Faster R-CNN about.md](../faster-rcnn-r50-fpn/about.md) |
| Training memory | 4.4 GB per GPU, 16.1 images/s at test time (MMDetection) | [MMDetection configs page](https://github.com/open-mmlab/mmdetection/tree/main/configs/cascade_rcnn) |

## Published results

| Dataset | Result | Source |
|---|---|---|
| COCO val 2017 | 40.3 AP (MMDetection) | [MMDetection configs page](https://github.com/open-mmlab/mmdetection/tree/main/configs/cascade_rcnn) |
| COCO test-dev | 40.6 AP, AP_S 22.6 (paper, ResNet-50) *(from a summary of the paper; check Table 6)* | [paper](https://arxiv.org/abs/1712.00726) |
| AI-TOD-v2 test | 15.1 AP, AP_vt 0.1, AP_t 11.5 *(from a summary of the paper's table; check)* | [NWD-RKA paper](https://arxiv.org/abs/2206.13996) |
| AI-TOD-v2 test, with NWD-RKA | 22.2 AP, AP_vt 7.8 *(from a summary of the paper's table; check)* | [NWD-RKA paper](https://arxiv.org/abs/2206.13996) |

## Strengths and weaknesses

**Strengths:** better than Faster R-CNN on both COCO and AI-TOD-v2 for little
extra memory (4.4 vs 4.0 GB).

**Weaknesses:** the extra stages help with box accuracy but not with finding
very tiny objects (AP_vt 0.1). It is slower, and some of its numbers still
need checking against the paper.
