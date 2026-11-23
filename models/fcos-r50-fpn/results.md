# FCOS with ResNet-50 and FPN: our results

One row per run. Raw outputs go in `outputs/fcos-r50-fpn/<run name>/`
(not tracked by git). How to run the model: [README.md](README.md).

For each run, write down:
- **Run:** a short name, also used as the folder name in `outputs/`
- **Weights:** where the checkpoint came from (a download link, or the run that trained it)
- **Setup:** anything that differs from the README (PyTorch version, config or test options, GPU, detections kept)

## COCO val 2017

COCO size bins use mask area (COCO's definition of "small" is under 32² px).

| Run | Weights | Setup | AP | AP50 | AP75 | AP_S | AP_M | AP_L | Expected | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | 36.6 AP ([configs page](https://github.com/open-mmlab/mmdetection/tree/main/configs/fcos)) | |

## AI-TOD-v2 test

AI-TOD size bins use box size √(w·h): very tiny 2–8 px, tiny 8–16 px, small
16–32 px, medium 32–64 px.

| Run | Version | Weights | Setup | AP | AP50 | AP75 | AP_vt | AP_t | AP_s | AP_m | Expected | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | As published | | | | | | | | | | 13.4 AP, AP_vt 2.5 ([RFLA README](https://github.com/Chasel-Tsui/mmdet-rfla#main-results)) | |
| | P2 | | | | | | | | | | none published | |
| | RFLA | | | | | | | | | | 15.6 AP, AP_vt 4.4 ([RFLA README](https://github.com/Chasel-Tsui/mmdet-rfla#main-results)) | |
| | P2 + RFLA | | | | | | | | | | none published | |
