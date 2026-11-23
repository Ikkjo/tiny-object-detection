# CenterNet with Hourglass-104: how to run

CenterNet ("Objects as Points") with the Hourglass-104 backbone, using the
official code, for **inference only**. Model details are in
[about.md](about.md) and our results in [results.md](results.md).

**Status:** not tried yet. It uses the same official code and environment as
[CenterNet DLA-34](../centernet-dla34/README.md) (Track B), so we set it up
once for both.

All steps below are from the official
[getting started guide](https://github.com/xingyizhou/CenterNet/blob/master/readme/GETTING_STARTED.md),
[model zoo](https://github.com/xingyizhou/CenterNet/blob/master/readme/MODEL_ZOO.md)
and [training script](https://github.com/xingyizhou/CenterNet/blob/master/experiments/ctdet_coco_hg.sh).

## 1. Setup and data

Follow [CenterNet DLA-34, steps 1 and 2](../centernet-dla34/README.md#1-setup)
(the `centernet` environment, COCO in `$CenterNet_ROOT/data/coco/`).

Hourglass-104 itself has no deformable convolutions, but the code's model
loader (`src/lib/models/model.py`) imports the DLA and ResNet networks that
need DCNv2. If DCNv2 won't compile, commenting out those imports should let
the Hourglass model load *(our idea, untried)*.

## 2. Weights

The COCO model is `ctdet_coco_hg` (40.3 AP on COCO val 2017), linked from the
[model zoo](https://github.com/xingyizhou/CenterNet/blob/master/readme/MODEL_ZOO.md)
as a Google Drive file:
[ctdet_coco_hg.pth](https://drive.google.com/file/d/13F904yXltGIqa_K3g3-FLleaNX0n7c9O).

Put it in `$CenterNet_ROOT/models/`, or keep it in
`checkpoints/centernet-hourglass104/` in this repo and pass that path to
`--load_model`.

## 3. Test on COCO val 2017

Run from `$CenterNet_ROOT/src`. The getting started guide gives:

```bash
python test.py ctdet --exp_id coco_hg --arch hourglass --fix_res --load_model ../models/ctdet_coco_hg.pth
```

The training script tests with `--keep_res` instead of `--fix_res`
(`--fix_res` resizes to 512×512; `--keep_res` keeps the original size).
**TBD:** which of the two gives the published **40.3 AP**; try both and note
it in [results.md](results.md). Add `--flip_test` for the 42.2 AP setting and
`--flip_test --test_scales 0.5,0.75,1,1.25,1.5` for 45.1 AP.

To score COCO's tiny objects with AI-TOD's size ranges, we also need the
predictions as a COCO JSON file. **TBD:** where `test.py` saves them (look in
`$CenterNet_ROOT/exp/ctdet/coco_hg/`).

## 4. AI-TOD-v2 without training (optional)

**TBD.** It needs:

- AI-TOD-v2 added as a dataset in the code (Track B needs the same, see
  [CenterNet DLA-34, step 2](../centernet-dla34/README.md#2-data))
- a mapping from COCO's classes to AI-TOD's (car, bus, truck → vehicle;
  boat → ship; person → person; airplane → airplane)
- 1,500 detections per image instead of 100. Two settings cap it: the `--K`
  option (default 100, [opts.py](https://github.com/xingyizhou/CenterNet/blob/master/src/lib/opts.py))
  and `self.max_per_image = 100`, written into
  [base_detector.py](https://github.com/xingyizhou/CenterNet/blob/master/src/lib/detectors/base_detector.py).
  Both need changing
