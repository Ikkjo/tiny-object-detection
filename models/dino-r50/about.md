# DINO with ResNet-50

A DETR-style detector: a transformer encoder refines the backbone features,
and a decoder turns 900 learned queries into boxes. It has no anchors and no
non-maximum suppression. It is our **anchor-free runner-up** for Track C of
issue #2. The reasons are in the
[Track C notes](../../docs/models/centernet-backbones-and-anchor-free.md).

How to run it: [README.md](README.md).

## Links

- **Paper:** [DINO: DETR with Improved DeNoising Anchor Boxes for End-to-End Object Detection](https://arxiv.org/abs/2203.03605) (Zhang et al., ICLR 2023)
- **MMDetection configs and weights:** [configs/dino](https://github.com/open-mmlab/mmdetection/tree/main/configs/dino)
- **AI-TOD-v2 results:** [DQ-DETR](https://arxiv.org/abs/2404.03507) (Huang et al., ECCV 2024), which builds on DINO and re-implements it as a baseline

## Properties

| Property | Value | Source |
|---|---|---|
| Feature levels | 4 scales: ResNet stages with strides 8, 16 and 32, plus one extra level (stride 64). The finest is **8** | [MMDetection config](https://github.com/open-mmlab/mmdetection/blob/main/configs/dino/dino-4scale_r50_8xb2-12e_coco.py) |
| Queries and detections kept | 900 queries; keeps the best 300 per image at test time | [MMDetection config](https://github.com/open-mmlab/mmdetection/blob/main/configs/dino/dino-4scale_r50_8xb2-12e_coco.py) |
| Parameters / FLOPs | **TBD** (measure) | — |
| Training in MMDetection | 12 epochs, batch 2 on each of 8 GPUs, AdamW with learning rate 1e-4 | [MMDetection config](https://github.com/open-mmlab/mmdetection/blob/main/configs/dino/dino-4scale_r50_8xb2-12e_coco.py) |
| Training memory | **TBD**. DQ-DETR trained on RTX 3090 GPUs with batch 1 "due to memory constraints" | [DQ-DETR paper](https://arxiv.org/abs/2404.03507) |

## Published results

| Dataset | Result | Source |
|---|---|---|
| COCO val 2017 | 49.0 AP (4 scales, 12 epochs, MMDetection) | [MMDetection DINO configs](https://github.com/open-mmlab/mmdetection/tree/main/configs/dino) |
| AI-TOD-v2 test | 25.9 AP, AP50 61.3, **AP_vt 12.7, AP_t 25.3**, AP_s 32.0, AP_m 39.7 (re-implemented by the DQ-DETR authors) | [DQ-DETR paper](https://arxiv.org/abs/2404.03507), Table 2 |
| AI-TOD-v2 test, for comparison | DQ-DETR 30.2 AP, AP_vt 15.3. In the same table, the best CNN detector is DetectoRS with RFLA, 25.7 AP, AP_vt 9.2 | [DQ-DETR paper](https://arxiv.org/abs/2404.03507), Table 2 |

## Caps on the number of objects

AI-TOD-v2 has images with up to 2,667 objects. With MMDetection's default of
300 detections per image, 7.0% of AI-TOD-v2 test objects can't be found
whatever the model does; with all 900 queries kept, 1.2%
([`scripts/detection_cap_stats.py`](../../scripts/detection_cap_stats.py)).
DQ-DETR's main change is to set the number of queries from an estimate of how
many objects the image holds ([DQ-DETR paper](https://arxiv.org/abs/2404.03507)).

## Strengths and weaknesses

**Strengths:** the best published AI-TOD-v2 result of any model we could
train, with very tiny objects found far more often than by the CNN detectors
(AP_vt 12.7). It is the base of the strongest tiny-object detectors (DQ-DETR,
Dome-DETR), so it shows how far a CenterNet-based detector is from the state
of the art.

**Weaknesses:** heavy to train. It starts at stride 8, dropping the stride-4
map; bringing that map back adds 1.4 AP on AI-TOD-v2
([ReDHF](https://arxiv.org/abs/2611.07994)). Its AI-TOD-v2 number comes from
another team's re-implementation, not from DINO's authors, and their training
settings for AI-TOD-v2 are not all stated.
