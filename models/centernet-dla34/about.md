# CenterNet with DLA-34

CenterNet predicts each object as its centre point on a heatmap, plus the box
size and a small offset. DLA-34 is the backbone the paper uses for its main
speed and accuracy results. It is our **CenterNet nominee** for Track B of
issue #2. The reasons are in the
[Track B notes](../../docs/models/standard-centernet-and-two-stage.md).

How to run it: [README.md](README.md).

## Links

- **Paper:** [Objects as Points](https://arxiv.org/abs/1904.07850) (Zhou et al., 2019)
- **Backbone paper:** [Deep Layer Aggregation](https://arxiv.org/abs/1707.06484) (Yu et al., 2018)
- **Official code:** [xingyizhou/CenterNet](https://github.com/xingyizhou/CenterNet)
- **Model zoo:** [MODEL_ZOO.md](https://github.com/xingyizhou/CenterNet/blob/master/readme/MODEL_ZOO.md)
- **Re-implementation in Detectron2:** [CenterNet2](https://github.com/xingyizhou/CenterNet2) (`CenterNet-S4_DLA_8x`, see its [model zoo](https://github.com/xingyizhou/CenterNet2/blob/master/docs/MODEL_ZOO.md)). It changes the loss, see below.
- **MMDetection:** has CenterNet only with ResNet-18 ([configs](https://github.com/open-mmlab/mmdetection/tree/main/configs/centernet)), not DLA-34.

## Properties

| Property | Value | Source |
|---|---|---|
| Output stride | 4 (a 512×512 input gives a 128×128 output) | [paper](https://arxiv.org/abs/1904.07850) |
| Parameters / FLOPs | DLA-34 backbone: 15.7M parameters, 3.1 GMACs at 224×224 (ImageNet classifier version). Full detector: **TBD** | [timm model card](https://huggingface.co/timm/dla34.in1k) |
| Loss | Focal loss on the heatmap (α = 2, β = 4), L1 for size (λ_size = 0.1) and offset (λ_off = 1) | [paper](https://arxiv.org/abs/1904.07850) |
| Training in the paper | 512×512 input, batch 128 on 8 GPUs, 140 epochs (2.5 days on 8 TITAN V). The 37.4 AP model (`2x`) uses 230 epochs | [paper](https://arxiv.org/abs/1904.07850), [model zoo](https://github.com/xingyizhou/CenterNet/blob/master/readme/MODEL_ZOO.md) |
| Training memory | **TBD** | — |
| Test speed | 19 ms per image (no augmentation, TITAN Xp) | [model zoo](https://github.com/xingyizhou/CenterNet/blob/master/readme/MODEL_ZOO.md) |
| Code setup | Tested with PyTorch 0.4.1, CUDA 9.0; needs DCNv2 compiled and an NVIDIA GPU | [install guide](https://github.com/xingyizhou/CenterNet/blob/master/readme/INSTALL.md), [model zoo](https://github.com/xingyizhou/CenterNet/blob/master/readme/MODEL_ZOO.md) |

## Published results

| Dataset | Result | Source |
|---|---|---|
| COCO val 2017 | 37.4 AP (no augmentation), 39.2 with flip, 41.7 with flip and multi-scale | [model zoo](https://github.com/xingyizhou/CenterNet/blob/master/readme/MODEL_ZOO.md) |
| COCO test-dev (flip) | 39.2 AP, **AP_S 19.9**, AP_M 43.0, AP_L 51.4 | [paper](https://arxiv.org/abs/1904.07850), Table 2 |
| AI-TOD-v2 | No plain CenterNet result found | — |
| AI-TOD (v1) | M-CenterNet (a CenterNet variant with DLA-34): 14.5 AP | [paper log](../../docs/literature/paper-log.md) |

## The re-implementation changes the loss

The Detectron2 version in CenterNet2 runs on a current PyTorch, but it changes
the parts we want to study: it uses a GIoU loss, more positive pixels per
object, and NMS ([CenterNet2 model zoo](https://github.com/xingyizhou/CenterNet2/blob/master/docs/MODEL_ZOO.md)).
So it can't replace the original for our research.

## Strengths and weaknesses

**Strengths:** it is the paper's main model, with published COCO results
including AP_S, so we can check our setup against it. Its output stride of 4
is the finest of the CenterNet options. Its loss is the one our research
directions are about (one positive pixel per object, the offset term).

**Weaknesses:** the official code is old and will take work to run on a
current setup. Nobody has published plain CenterNet results on AI-TOD-v2, so
we would be the first to measure it.
