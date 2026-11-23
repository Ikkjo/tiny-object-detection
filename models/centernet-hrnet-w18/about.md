# CenterNet with HRNet-W18

CenterNet predicts each object as its centre point on a heatmap, plus the box
size and a small offset. Here its backbone is HRNet-W18, which keeps a branch
at 1/4 of the input size through the whole network. It is our **CenterNet
backbone nominee** for Track C of issue #2. The reasons are in the
[Track C notes](../../docs/models/centernet-backbones-and-anchor-free.md).

How to run it: [README.md](README.md).

## Links

- **CenterNet paper:** [Objects as Points](https://arxiv.org/abs/1904.07850) (Zhou et al., 2019)
- **HRNet paper:** [Deep High-Resolution Representation Learning for Visual Recognition](https://arxiv.org/abs/1908.07919) (Wang et al., TPAMI 2020)
- **MMDetection CenterNet:** [configs/centernet](https://github.com/open-mmlab/mmdetection/tree/main/configs/centernet)
- **MMDetection HRNet:** [configs/hrnet](https://github.com/open-mmlab/mmdetection/tree/main/configs/hrnet)
- **Neck we use:** [HRFPN](https://github.com/open-mmlab/mmdetection/blob/main/mmdet/models/necks/hrfpn.py)
- **Related code:** [FairMOT](https://github.com/ifzhang/FairMOT) uses HRNet-W18 with a CenterNet-style head (for tracking)

No published detector combines CenterNet and HRNet. We build it from the
MMDetection parts above; our config is in [configs/](configs/).

## Properties

| Property | Value | Source |
|---|---|---|
| Output stride | 4. HRFPN upsamples HRNet's four branches (strides 4, 8, 16, 32) to stride 4 and merges them; with one output it gives a single stride-4 map, which is what MMDetection's CenterNet head expects | [HRFPN code](https://github.com/open-mmlab/mmdetection/blob/main/mmdet/models/necks/hrfpn.py), [CenterNet head code](https://github.com/open-mmlab/mmdetection/blob/main/mmdet/models/dense_heads/centernet_head.py) |
| Parameters / FLOPs | Full detector: **TBD** (measure). For scale: Faster R-CNN with HRNetV2-W18 has 26.2M parameters and 159.1 GFLOPs | [HRNet detection repo](https://github.com/HRNet/HRNet-Object-Detection) |
| Loss | Same as CenterNet: focal loss on the heatmap, L1 for size (weight 0.1) and offset (weight 1) | [MMDetection CenterNet config](https://github.com/open-mmlab/mmdetection/blob/main/configs/centernet/centernet_r18-dcnv2_8xb16-crop512-140e_coco.py) |
| Pretrained weights | ImageNet HRNetV2-W18 (`open-mmlab://msra/hrnetv2_w18`). No COCO-trained CenterNet-HRNet exists | [MMDetection HRNet config](https://github.com/open-mmlab/mmdetection/blob/main/configs/hrnet/fcos_hrnetv2p-w18-gn-head_4xb4-1x_coco.py) |
| Training memory | **TBD**. For scale, in MMDetection: Faster R-CNN with HRNetV2-W18 6.6 GB, FCOS with HRNetV2-W18 13.0 GB (4 images per GPU) | [MMDetection HRNet configs](https://github.com/open-mmlab/mmdetection/tree/main/configs/hrnet) |
| Training recipe | We start from MMDetection's CenterNet ResNet-18 recipe: 512×512 crops, 140 epochs, batch 16 on 8 GPUs | [MMDetection CenterNet config](https://github.com/open-mmlab/mmdetection/blob/main/configs/centernet/centernet_r18-dcnv2_8xb16-crop512-140e_coco.py) |
| Detections kept per image | 100 in MMDetection's CenterNet config. On AI-TOD-v2 we raise it to 1,500 (see the Track C notes, section 6) | [MMDetection CenterNet config](https://github.com/open-mmlab/mmdetection/blob/main/configs/centernet/centernet_r18-dcnv2_8xb16-crop512-140e_coco.py) |

## Published results

| Dataset | Result | Source |
|---|---|---|
| COCO | None for this combination. The closest MMDetection CenterNet (ResNet-18 with deformable convolutions): 29.5 AP, 3.47 GB | [MMDetection CenterNet configs](https://github.com/open-mmlab/mmdetection/tree/main/configs/centernet) |
| COCO, same backbone in FCOS | HRNetV2-W18: 35.2 AP, **AP_S 20.4** (paper); 35.3 AP in MMDetection | [HRNet paper](https://arxiv.org/abs/1908.07919), [MMDetection HRNet configs](https://github.com/open-mmlab/mmdetection/tree/main/configs/hrnet) |
| AI-TOD-v2 | None found | — |

## Strengths and weaknesses

**Strengths:** the network keeps a branch at CenterNet's output resolution
from start to end, instead of recovering it by upsampling, so it tests whether
keeping the detail helps tiny objects. Only the backbone
changes; the head and loss are CenterNet's.

**Weaknesses:** it doesn't change the training target: at stride 4, 67% of
AI-TOD-v2 objects still get a one-pixel heatmap target
([aerial dataset notes](../../docs/datasets/aerial-dataset.md)). With no
published result for this combination, our COCO number has nothing to be
checked against.
