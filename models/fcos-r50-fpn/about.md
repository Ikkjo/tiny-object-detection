# FCOS with ResNet-50 and FPN

An anchor-free, one-stage detector: every location on the FPN levels predicts
a class, the distances to the four box sides, and a centre-ness score. It is
our **anchor-free nominee** for Track C of issue #2. We run it in four
versions on AI-TOD-v2: as published, with a stride-4 level (P2), with RFLA
label assignment, and with both. The reasons are in the
[Track C notes](../../docs/models/centernet-backbones-and-anchor-free.md).

How to run it: [README.md](README.md).

## Links

- **Paper:** [FCOS: Fully Convolutional One-Stage Object Detection](https://arxiv.org/abs/1904.01355) (Tian et al., ICCV 2019)
- **MMDetection configs and weights (COCO):** [configs/fcos](https://github.com/open-mmlab/mmdetection/tree/main/configs/fcos)
- **AI-TOD-v2 configs:** [mmdet-rfla](https://github.com/Chasel-Tsui/mmdet-rfla) (`configs/baselines/aitodv2_fcos_r50_1x.py`, `aitodv2_fcos_r50_p2_1x.py`, `configs/rfla/aitodv2_fcos_r50_rfla_kld_1x.py`, `aitodv2_fcos_r50_p2_rfla_kld_1x.py`)
- **RFLA paper:** [RFLA: Gaussian Receptive Field based Label Assignment for Tiny Object Detection](https://arxiv.org/abs/2208.08738) (Xu et al., ECCV 2022)

## Properties

| Property | Value | Source |
|---|---|---|
| Output stride | FPN levels with strides 8, 16, 32, 64 and 128, so the finest is **8**. The P2 version uses strides 4 to 64 | [paper](https://arxiv.org/abs/1904.01355), [mmdet-rfla P2 config](https://github.com/Chasel-Tsui/mmdet-rfla/blob/main/configs/baselines/aitodv2_fcos_r50_p2_1x.py) |
| Parameters / FLOPs | **TBD** (measure) | — |
| Training memory | 3.6 GB per GPU, 22.7 images/s at test time (MMDetection, COCO, 1x) | [MMDetection FCOS configs](https://github.com/open-mmlab/mmdetection/tree/main/configs/fcos) |
| Training on AI-TOD-v2 | 800×800 input, batch 2, learning rate 0.005, 12 epochs, up to 3,000 detections per image. Uses FCOS's later improvements (centre sampling, normalised box targets, centre-ness on the regression branch) and a DIoU loss (GIoU in the P2 config) | [mmdet-rfla config](https://github.com/Chasel-Tsui/mmdet-rfla/blob/main/configs/baselines/aitodv2_fcos_r50_1x.py) |
| Code | COCO: MMDetection 3.x. AI-TOD-v2: mmdet-rfla, built on MMDetection 2.13.0 | [MMDetection](https://github.com/open-mmlab/mmdetection/tree/main/configs/fcos), [mmdet-rfla `mmdet/version.py`](https://github.com/Chasel-Tsui/mmdet-rfla/blob/main/mmdet/version.py) |

## Published results

| Dataset | Version | Result | Source |
|---|---|---|---|
| COCO minival | Paper, ResNet-50 | 37.1 AP, **AP_S 21.3** | [paper](https://arxiv.org/abs/1904.01355) |
| COCO val 2017 | MMDetection, ResNet-50 caffe, 1x | 36.6 AP (38.7 with the improvements) | [MMDetection FCOS configs](https://github.com/open-mmlab/mmdetection/tree/main/configs/fcos) |
| AI-TOD-v2 test | As published | 13.4 AP, AP50 32.4, **AP_vt 2.5, AP_t 12.4**, AP_s 19.0, AP_m 26.7 | [mmdet-rfla README](https://github.com/Chasel-Tsui/mmdet-rfla#main-results), Table 2 |
| AI-TOD-v2 test | With RFLA | 15.6 AP, AP50 38.2, **AP_vt 4.4, AP_t 14.6**, AP_s 20.9, AP_m 29.5 | [mmdet-rfla README](https://github.com/Chasel-Tsui/mmdet-rfla#main-results), Table 2 |
| AI-TOD-v2 test | P2, and P2 with RFLA | None published (configs exist) | — |
| AI-TOD-v2 test | As published, in the NWD-RKA paper | 12.0 AP, AP_vt 2.2 | [NWD-RKA paper](https://arxiv.org/abs/2206.13996) |
| AI-TOD (v1) test | As published → P2 | 12.6 → 15.4 AP; AP_vt 2.3 → **6.0** | [mmdet-rfla README](https://github.com/Chasel-Tsui/mmdet-rfla#main-results), Table 1 |
| AI-TOD (v1) test | P2 with RFLA | 16.3 AP, AP_vt 7.3 | [mmdet-rfla README](https://github.com/Chasel-Tsui/mmdet-rfla#main-results), Table 1 |

## Strengths and weaknesses

**Strengths:** the standard anchor-free baseline, with published AI-TOD-v2
results and configs for every version we want. The P2 version isolates the
effect of output stride in a second detector family, and RFLA isolates the
effect of label assignment.

**Weaknesses:** weak on AI-TOD-v2 as published (13.4 AP). The P2 versions
have no published AI-TOD-v2 numbers, so those we measure ourselves. The
AI-TOD-v2 configs are in an older MMDetection than the COCO ones.
