# Faster R-CNN with ResNet-50, FPN and RFLA

Faster R-CNN with RFLA label assignment. RFLA models each location's
receptive field and each object as 2-D Gaussians, and decides which locations
learn from which object by the distance between them, instead of by IoU. It
is our **label-assignment nominee** for Track C of issue #2. The plain
Faster R-CNN is Track B's two-stage nominee
([faster-rcnn-r50-fpn](../faster-rcnn-r50-fpn/)). The reasons are in the
[Track C notes](../../docs/models/centernet-backbones-and-anchor-free.md).

How to run it: [README.md](README.md).

## Links

- **Paper:** [RFLA: Gaussian Receptive Field based Label Assignment for Tiny Object Detection](https://arxiv.org/abs/2208.08738) (Xu et al., ECCV 2022)
- **Official code:** [mmdet-rfla](https://github.com/Chasel-Tsui/mmdet-rfla), built on MMDetection 2.13.0
- **Config:** [`configs/rfla/aitodv2_faster_r50_rfla_kld_1x.py`](https://github.com/Chasel-Tsui/mmdet-rfla/blob/main/configs/rfla/aitodv2_faster_r50_rfla_kld_1x.py)

## Properties

| Property | Value | Source |
|---|---|---|
| Output stride | FPN levels with strides 4 to 64, so the finest is **4** | [config](https://github.com/Chasel-Tsui/mmdet-rfla/blob/main/configs/rfla/aitodv2_faster_r50_rfla_kld_1x.py) |
| What RFLA changes | The RPN's assigner: a hierarchical assigner using a KL-divergence-based receptive-field distance (top-k of 3, then 1, decay 0.9) | [config](https://github.com/Chasel-Tsui/mmdet-rfla/blob/main/configs/rfla/aitodv2_faster_r50_rfla_kld_1x.py), [paper](https://arxiv.org/abs/2208.08738) |
| Parameters / FLOPs | Same network as Faster R-CNN R50-FPN: 41.8M parameters (torchvision version); RFLA adds none | [torchvision](https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.detection.fasterrcnn_resnet50_fpn.html) |
| Training on AI-TOD-v2 | 800×800, batch 2 on one GPU, learning rate 0.005, 12 epochs, up to 3,000 detections per image | [config](https://github.com/Chasel-Tsui/mmdet-rfla/blob/main/configs/rfla/aitodv2_faster_r50_rfla_kld_1x.py) |
| Hardware in the paper | One RTX 3090 | [paper](https://arxiv.org/abs/2208.08738) |

## Published results

| Dataset | Result | Source |
|---|---|---|
| AI-TOD-v2 test | 22.6 AP, AP50 54.8, AP75 14.5, **AP_vt 8.6, AP_t 21.7**, AP_s 28.8, AP_m 35.5 | [mmdet-rfla README](https://github.com/Chasel-Tsui/mmdet-rfla#main-results), Table 2 |
| AI-TOD-v2 test, without RFLA | 12.8 AP, AP_vt 0.0, AP_t 9.2 | [mmdet-rfla README](https://github.com/Chasel-Tsui/mmdet-rfla#main-results), Table 2 |
| AI-TOD-v2 test, RFLA on DetectoRS | 25.7 AP, AP_vt 9.2 | [mmdet-rfla README](https://github.com/Chasel-Tsui/mmdet-rfla#main-results), Table 2 |
| AI-TOD (v1) test | 21.1 AP, AP_vt 9.5 | [mmdet-rfla README](https://github.com/Chasel-Tsui/mmdet-rfla#main-results), Table 1 |

## Strengths and weaknesses

**Strengths:** the largest published gain from label assignment alone on our
dataset: 12.8 → 22.6 AP with the same network. Official configs and an
evaluation with AI-TOD's size ranges. Reproducing it is the first check that
our AI-TOD-v2 setup is right.

**Weaknesses:** its code is on MMDetection 2.13.0, which needs its own
environment. The README warns the code is not meant for everyday datasets
like COCO, so we run it on AI-TOD-v2 only. Which pretrained models its
download link holds is **TBD**.
