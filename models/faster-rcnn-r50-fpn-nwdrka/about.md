# Faster R-CNN with ResNet-50, FPN and NWD-RKA

Faster R-CNN with NWD-RKA label assignment. NWD-RKA compares boxes as 2-D
Gaussians with a normalised Wasserstein distance (NWD), and picks positive
locations by ranking (RKA) instead of with a fixed IoU threshold. It is our
**label-assignment runner-up** for Track C of issue #2. The plain
Faster R-CNN is Track B's two-stage nominee
([faster-rcnn-r50-fpn](../faster-rcnn-r50-fpn/)). The reasons are in the
[Track C notes](../../docs/models/centernet-backbones-and-anchor-free.md).

How to run it: [README.md](README.md).

## Links

- **Paper:** [Detecting tiny objects in aerial images: A normalized Wasserstein distance and a new benchmark](https://arxiv.org/abs/2206.13996) (Xu et al., ISPRS J. 2022). It also introduces AI-TOD-v2.
- **Official code:** [mmdet-aitod](https://github.com/Chasel-Tsui/mmdet-aitod), built on MMDetection 2.24.1
- **Config:** [`configs_nwdrka/nwd_rka/aitodv2_faster_r50_nwdrka_1x.py`](https://github.com/Chasel-Tsui/mmdet-aitod/blob/main/mmdet-nwdrka/configs_nwdrka/nwd_rka/aitodv2_faster_r50_nwdrka_1x.py). The top of the file holds the log of the training run behind the published result.

## Properties

| Property | Value | Source |
|---|---|---|
| Output stride | FPN levels with strides 4 to 64, so the finest is **4** | [config](https://github.com/Chasel-Tsui/mmdet-aitod/blob/main/mmdet-nwdrka/configs_nwdrka/nwd_rka/aitodv2_faster_r50_nwdrka_1x.py) |
| What NWD-RKA changes | The RPN's assigner: ranking-based assignment (top 2) with NWD instead of IoU. The second stage keeps IoU | [config](https://github.com/Chasel-Tsui/mmdet-aitod/blob/main/mmdet-nwdrka/configs_nwdrka/nwd_rka/aitodv2_faster_r50_nwdrka_1x.py), [paper](https://arxiv.org/abs/2206.13996) |
| Parameters / FLOPs | Same network as Faster R-CNN R50-FPN: 41.8M parameters (torchvision version); NWD-RKA adds none | [torchvision](https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.detection.fasterrcnn_resnet50_fpn.html) |
| Training on AI-TOD-v2 | 800×800, batch 2, learning rate 0.01, 12 epochs, up to 3,000 detections per image | [config](https://github.com/Chasel-Tsui/mmdet-aitod/blob/main/mmdet-nwdrka/configs_nwdrka/nwd_rka/aitodv2_faster_r50_nwdrka_1x.py), [dataset config](https://github.com/Chasel-Tsui/mmdet-aitod/blob/main/mmdet-nwdrka/configs_nwdrka/_base_/datasets/aitodv2_detection.py) |
| Evaluation | Counts up to 1,500 detections per image, with AI-TOD's size ranges | [`mmdet/datasets/aitodv2.py`](https://github.com/Chasel-Tsui/mmdet-aitod/blob/main/mmdet-nwdrka/mmdet/datasets/aitodv2.py) |

## Published results

| Dataset | Result | Source |
|---|---|---|
| AI-TOD-v2 test | 21.4 AP, AP50 53.2, **AP_vt 7.7, AP_t 20.7**, AP_s 26.8, AP_m 35.2 | [config](https://github.com/Chasel-Tsui/mmdet-aitod/blob/main/mmdet-nwdrka/configs_nwdrka/nwd_rka/aitodv2_faster_r50_nwdrka_1x.py) (log), [paper](https://arxiv.org/abs/2206.13996) |
| AI-TOD-v2 test, without NWD-RKA | 12.8 AP, AP_vt 0.0, AP_t 9.2 | [mmdet-rfla README](https://github.com/Chasel-Tsui/mmdet-rfla#main-results), Table 2 |
| AI-TOD-v2 test, NWD-RKA on DetectoRS | 24.7 AP, AP_vt 9.7 | [DQ-DETR paper](https://arxiv.org/abs/2404.03507), Table 2 |

## Strengths and weaknesses

**Strengths:** from the paper that introduced AI-TOD-v2, with the training log
inside the config, so we know exactly what a correct run looks like. It runs
in mmdet-aitod, the same code and environment as Track B's Faster R-CNN on
AI-TOD-v2.

**Weaknesses:** on Faster R-CNN, a little below RFLA in every size range
(21.4 vs 22.6 AP overall). Its code is
on MMDetection 2.24.1.
