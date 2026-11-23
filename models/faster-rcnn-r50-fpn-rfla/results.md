# Faster R-CNN with ResNet-50, FPN and RFLA: our results

One row per run. Raw outputs go in `outputs/faster-rcnn-r50-fpn-rfla/<run name>/`
(not tracked by git). How to run the model: [README.md](README.md).

For each run, write down:
- **Run:** a short name, also used as the folder name in `outputs/`
- **Weights:** where the checkpoint came from (a download link, or the run that trained it)
- **Setup:** anything that differs from the README (config changes, GPU, batch size, detections kept)

## AI-TOD-v2 test

AI-TOD size bins use box size √(w·h): very tiny 2–8 px, tiny 8–16 px, small
16–32 px, medium 32–64 px.

| Run | Weights | Setup | AP | AP50 | AP75 | AP_vt | AP_t | AP_s | AP_m | Expected | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | 22.6 AP, AP_vt 8.6 ([RFLA README](https://github.com/Chasel-Tsui/mmdet-rfla#main-results)) | |
