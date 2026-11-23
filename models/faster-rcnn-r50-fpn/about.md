# Faster R-CNN with ResNet-50 and FPN

The standard two-stage detector: a region proposal network suggests boxes,
then a second stage classifies them and refines the box. FPN adds predictions
from several resolutions. It is our **two-stage nominee** for Track B of
issue #2. The reasons are in the
[Track B notes](../../docs/models/standard-centernet-and-two-stage.md).

How to run it: [README.md](README.md).

## Links

- **Papers:** [Faster R-CNN](https://arxiv.org/abs/1506.01497) (Ren et al., 2015), [FPN](https://arxiv.org/abs/1612.03144) (Lin et al., 2017)
- **MMDetection configs and weights:** [configs/faster_rcnn](https://github.com/open-mmlab/mmdetection/tree/main/configs/faster_rcnn)
- **torchvision:** [`fasterrcnn_resnet50_fpn`](https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.detection.fasterrcnn_resnet50_fpn.html)
- **AI-TOD code:** [mmdet-aitod](https://github.com/Chasel-Tsui/mmdet-aitod) (baseline and NWD-RKA configs)
- **RFLA code:** [mmdet-rfla](https://github.com/Chasel-Tsui/mmdet-rfla)

## Properties

| Property | Value | Source |
|---|---|---|
| Parameters / FLOPs | 41.8M parameters, 134.4 GFLOPs (torchvision version) | [torchvision](https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.detection.fasterrcnn_resnet50_fpn.html) |
| Output stride | FPN levels with strides 4, 8, 16, 32 and 64, so the finest is **4** | [MMDetection model config](https://github.com/open-mmlab/mmdetection/blob/main/configs/_base_/models/faster-rcnn_r50_fpn.py) |
| Training memory | 4.0 GB per GPU, 21.4 images/s at test time (MMDetection) | [MMDetection configs page](https://github.com/open-mmlab/mmdetection/tree/main/configs/faster_rcnn) |
| Training on AI-TOD-v2 | 12 epochs, batch 2 per GPU, learning rate 0.01 | [mmdet-aitod config](https://github.com/Chasel-Tsui/mmdet-aitod/blob/main/mmdet-nwdrka/configs_nwdrka/baseline/aitodv2_faster_rcnn_r50_baseline_1x.py) |

## Published results

| Dataset | Result | Source |
|---|---|---|
| COCO val 2017 | 37.4 AP (MMDetection) | [MMDetection configs page](https://github.com/open-mmlab/mmdetection/tree/main/configs/faster_rcnn) |
| COCO minival | 33.9 AP, **AP_S 17.8** (FPN paper, ResNet-50) | [FPN paper](https://arxiv.org/abs/1612.03144), Table 3c |
| AI-TOD-v2 test | 12.8 AP, AP50 29.9, **AP_vt 0.0, AP_t 9.2**, AP_s 24.6, AP_m 37.0 | [RFLA README](https://github.com/Chasel-Tsui/mmdet-rfla#main-results), Table 2 |
| AI-TOD-v2 test, with RFLA | 22.6 AP, AP_vt 8.6 | [RFLA README](https://github.com/Chasel-Tsui/mmdet-rfla#main-results), Table 2 |
| AI-TOD-v2 test, with NWD-RKA | 21.4 AP, AP_vt 7.7 | [NWD-RKA paper](https://arxiv.org/abs/2206.13996) |

## Strengths and weaknesses

**Strengths:** the model most tiny-object methods are built on (NWD-RKA,
RFLA, SimD, CFINet, see the [paper log](../../docs/literature/paper-log.md)
and its [archive](../../docs/literature/paper-log-archive.md)),
with published AI-TOD-v2 results both with and without those methods. Runs in
every major framework with pretrained weights, and fits a modest GPU.

**Weaknesses:** on AI-TOD-v2 it finds almost none of the very tiny objects
(AP_vt 0.0). This is exactly the weakness tiny-object methods try to fix, so
it is useful for comparison, but it is a weak baseline on its own.
