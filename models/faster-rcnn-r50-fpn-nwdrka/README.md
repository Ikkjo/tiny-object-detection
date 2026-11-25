# Faster R-CNN with ResNet-50, FPN and NWD-RKA: how to run

Faster R-CNN with NWD-RKA label assignment, using the official mmdet-aitod
code, on AI-TOD-v2 only. Model details are in [about.md](about.md) and our
results in [results.md](results.md).

**Status:** not tried yet.

The steps are from the [mmdet-aitod README](https://github.com/Chasel-Tsui/mmdet-aitod)
and the same MMDetection 2.x test and train commands as Track B's
[Faster R-CNN on AI-TOD-v2](../faster-rcnn-r50-fpn/README.md#ai-tod-v2).

## 1. Setup and data

Use the `aitod` environment and the AI-TOD-v2 link from
[Faster R-CNN, AI-TOD-v2 steps 1 and 2](../faster-rcnn-r50-fpn/README.md#1-setup).
Nothing extra is needed.

## 2. Config

[`configs_nwdrka/nwd_rka/aitodv2_faster_r50_nwdrka_1x.py`](https://github.com/Chasel-Tsui/mmdet-aitod/blob/main/mmdet-nwdrka/configs_nwdrka/nwd_rka/aitodv2_faster_r50_nwdrka_1x.py).
Unlike the plain Faster R-CNN baseline config, this one loads the AI-TOD-v2
dataset file (`aitodv2_detection.py`), so it needs no change. It trains for 12
epochs with batch 2 and learning rate 0.01.

## 3. Weights

mmdet-aitod publishes no weights for this model, so we train it.

## 4. Train and test

Run from `mmdet-aitod/mmdet-nwdrka`:

```bash
python tools/train.py configs_nwdrka/nwd_rka/aitodv2_faster_r50_nwdrka_1x.py \
    --work-dir /path/to/tiny-object-detection/outputs/faster-rcnn-r50-fpn-nwdrka/<run name>
```

```bash
python tools/test.py configs_nwdrka/nwd_rka/aitodv2_faster_r50_nwdrka_1x.py <checkpoint> --eval bbox
```

The published result to compare with is **21.4 AP, AP_vt 7.7, AP_t 20.7**.
The full log of that run is at the top of the config file, including per-class
AP, so we can compare more than the headline number. Write ours in
[results.md](results.md).
