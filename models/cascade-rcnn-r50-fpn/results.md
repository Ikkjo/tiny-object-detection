# Cascade R-CNN with ResNet-50 and FPN: our results

One row per run. Raw outputs go in `outputs/cascade-rcnn-r50-fpn/<run name>/`
(not tracked by git). How to run the model: [README.md](README.md).

For each run, write down:
- **Run:** a short name, also used as the folder name in `outputs/`
- **Weights:** where the checkpoint came from (a download link, or the run that trained it)
- **Setup:** anything that differs from the README (PyTorch version, test options, GPU)

## COCO val 2017

COCO size bins use mask area (COCO's definition of "small" is under 32² px).

| Run | Weights | Setup | AP | AP50 | AP75 | AP_S | AP_M | AP_L | Expected | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | 40.3 AP ([MMDetection](https://github.com/open-mmlab/mmdetection/tree/main/configs/cascade_rcnn)) | |

## AI-TOD-v2 test

AI-TOD size bins use box size √(w·h): very tiny 2–8 px, tiny 8–16 px, small
16–32 px, medium 32–64 px.

| Run | Weights | Setup | AP | AP50 | AP75 | AP_vt | AP_t | AP_s | AP_m | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | |
