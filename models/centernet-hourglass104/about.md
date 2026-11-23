# CenterNet with Hourglass-104

CenterNet predicts each object as its centre point on a heatmap, plus the box
size and a small offset. Hourglass-104 is the most accurate backbone in the
CenterNet paper: two stacked hourglass modules, each downsampling and then
upsampling with skip connections. It is our **reference model, inference
only**, for Track C of issue #2. The reasons are in the
[Track C notes](../../docs/models/centernet-backbones-and-anchor-free.md).

How to run it: [README.md](README.md).

## Links

- **Paper:** [Objects as Points](https://arxiv.org/abs/1904.07850) (Zhou et al., 2019)
- **Official code:** [xingyizhou/CenterNet](https://github.com/xingyizhou/CenterNet)
- **Model zoo:** [MODEL_ZOO.md](https://github.com/xingyizhou/CenterNet/blob/master/readme/MODEL_ZOO.md)
- **MMDetection:** has Hourglass-104 only in CornerNet, not in CenterNet

## Properties

| Property | Value | Source |
|---|---|---|
| Output stride | 4 | [paper](https://arxiv.org/abs/1904.07850) |
| Parameters | 186.44M | [Corner2Net](https://arxiv.org/abs/2411.15772), comparison table |
| Test time (TITAN Xp) | 71 ms per image with no augmentation, 129 ms with flip, 674 ms with multi-scale | [model zoo](https://github.com/xingyizhou/CenterNet/blob/master/readme/MODEL_ZOO.md) |
| Training in the official repo | 109 hours on 5 GPUs, batch 24, 50 epochs, fine-tuned from an ExtremeNet model | [model zoo](https://github.com/xingyizhou/CenterNet/blob/master/readme/MODEL_ZOO.md), [training script](https://github.com/xingyizhou/CenterNet/blob/master/experiments/ctdet_coco_hg.sh) |
| Code setup | Same as CenterNet DLA-34: tested with PyTorch 0.4.1. The Hourglass network itself has no deformable convolutions, but the model loader imports the DLA and ResNet networks that need DCNv2, so DCNv2 must still compile (or those imports be removed, *untried*) | [install guide](https://github.com/xingyizhou/CenterNet/blob/master/readme/INSTALL.md), [model.py](https://github.com/xingyizhou/CenterNet/blob/master/src/lib/models/model.py) |
| Detections kept per image | 100, set both by the `--K` test option and by a fixed `max_per_image = 100` in the detector code. On AI-TOD-v2 a cap of 100 puts 26.1% of test objects out of reach, so we raise both to 1,500 | [opts.py](https://github.com/xingyizhou/CenterNet/blob/master/src/lib/opts.py), [base_detector.py](https://github.com/xingyizhou/CenterNet/blob/master/src/lib/detectors/base_detector.py), [`scripts/detection_cap_stats.py`](../../scripts/detection_cap_stats.py) |

## Published results

| Dataset | Result | Source |
|---|---|---|
| COCO val 2017 | 40.3 AP (no augmentation), 42.2 with flip, 45.1 with flip and multi-scale | [model zoo](https://github.com/xingyizhou/CenterNet/blob/master/readme/MODEL_ZOO.md) |
| COCO test-dev | 42.1 AP, AP_S 24.1 (as quoted in Corner2Net's comparison table) | [Corner2Net](https://arxiv.org/abs/2411.15772) |
| AI-TOD-v2 | None found | — |

## Why inference only

Training it costs days on several GPUs, which we don't have. Running the
published COCO model costs about 6 minutes for the 5,000 images of COCO val
at 71 ms each *(est.)*, and shows what CenterNet reaches with its strongest
backbone, including on COCO's tiniest objects when scored with AI-TOD's size
ranges.

It can also run on AI-TOD-v2 without training. COCO's car, bus, truck, boat,
person and airplane cover AI-TOD's vehicle, ship, person and airplane, which
are 97.7% of AI-TOD-v2 objects (per-class counts from
`scripts/aerial_size_stats.py`, see the
[aerial dataset notes](../../docs/datasets/aerial-dataset.md)). That result
would mostly measure the gap between everyday photos and aerial images, so it
is optional.

## Strengths and weaknesses

**Strengths:** the best published CenterNet, from the official code, with
COCO weights. It gives an upper reference for the CenterNet backbones we
train.

**Weaknesses:** too heavy to train or to change, and it needs the same old
code setup as CenterNet DLA-34.
