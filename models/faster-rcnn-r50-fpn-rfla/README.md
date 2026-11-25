# Faster R-CNN with ResNet-50, FPN and RFLA: how to run

Faster R-CNN with RFLA label assignment, using the official mmdet-rfla code,
on AI-TOD-v2 only. Model details are in [about.md](about.md) and our results
in [results.md](results.md).

**Status:** not tried yet. Reproducing this model's published result is the
first AI-TOD-v2 run we plan, to check our data, training and evaluation.

The steps are from the [mmdet-rfla README](https://github.com/Chasel-Tsui/mmdet-rfla)
and its copy of MMDetection's
[testing and training guide](https://github.com/Chasel-Tsui/mmdet-rfla/blob/main/docs/1_exist_data_model.md).

## 1. Setup and data

Use the `rfla` environment and the AI-TOD-v2 link from
[FCOS, AI-TOD-v2 steps 1 and 2](../fcos-r50-fpn/README.md#1-setup-rfla-environment).

## 2. Config

[`configs/rfla/aitodv2_faster_r50_rfla_kld_1x.py`](https://github.com/Chasel-Tsui/mmdet-rfla/blob/main/configs/rfla/aitodv2_faster_r50_rfla_kld_1x.py).
It loads the AI-TOD-v2 dataset config (`aitodv2_detection.py`) and trains for
12 epochs with batch 2 on one GPU and learning rate 0.005.

## 3. Weights

The RFLA README links a set of pretrained models
([OneDrive](https://1drv.ms/u/s!Ao5UiAkIbGJ7xRGZ3AYB7IW8zas2?e=opfU3x)).
**TBD:** whether this model is in it. If it is, testing it checks our
evaluation before we spend time on training. Put it in
`checkpoints/faster-rcnn-r50-fpn-rfla/`.

## 4. Train and test

Run from the `mmdet-rfla` folder:

```bash
python tools/train.py configs/rfla/aitodv2_faster_r50_rfla_kld_1x.py \
    --work-dir /path/to/tiny-object-detection/outputs/faster-rcnn-r50-fpn-rfla/<run name>
```

```bash
python tools/test.py configs/rfla/aitodv2_faster_r50_rfla_kld_1x.py <checkpoint> --eval bbox
```

The published result to compare with is **22.6 AP, AP_vt 8.6, AP_t 21.7**
([RFLA README](https://github.com/Chasel-Tsui/mmdet-rfla#main-results),
Table 2). Write ours in [results.md](results.md).
