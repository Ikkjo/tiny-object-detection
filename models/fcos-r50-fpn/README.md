# FCOS with ResNet-50 and FPN: how to run

The standard anchor-free detector. Model details are in [about.md](about.md)
and our results in [results.md](results.md).

**Status:** not tried yet.

We use two codebases, because the AI-TOD-v2 configs (with the P2 and RFLA
versions) only exist for an older MMDetection:

| Dataset | Code | Environment |
|---|---|---|
| COCO | [MMDetection 3.x](https://github.com/open-mmlab/mmdetection) | `openmmlab` |
| AI-TOD-v2 | [mmdet-rfla](https://github.com/Chasel-Tsui/mmdet-rfla) (based on MMDetection 2.13.0) | `rfla` |

## COCO

The steps are from MMDetection's
[test guide](https://github.com/open-mmlab/mmdetection/blob/main/docs/en/user_guides/test.md)
and the [FCOS configs page](https://github.com/open-mmlab/mmdetection/tree/main/configs/fcos).

### 1. Setup and data

Use the `openmmlab` environment and COCO link from
[CenterNet Update](../centernet-update-r50-fpn/README.md#1-setup).

### 2. Weights

| Config | COCO val 2017 | Training memory | Checkpoint |
|---|---|---|---|
| [`fcos_r50-caffe_fpn_gn-head_1x_coco.py`](https://github.com/open-mmlab/mmdetection/blob/main/configs/fcos/fcos_r50-caffe_fpn_gn-head_1x_coco.py) | 36.6 AP | 3.6 GB | [model](https://download.openmmlab.com/mmdetection/v2.0/fcos/fcos_r50_caffe_fpn_gn-head_1x_coco/fcos_r50_caffe_fpn_gn-head_1x_coco-821213aa.pth) |

Put the checkpoint in `checkpoints/fcos-r50-fpn/` in this repo.

### 3. Test on COCO val 2017

Run from the `mmdetection` folder:

```bash
python tools/test.py \
    configs/fcos/fcos_r50-caffe_fpn_gn-head_1x_coco.py \
    /path/to/checkpoints/fcos-r50-fpn/fcos_r50_caffe_fpn_gn-head_1x_coco-821213aa.pth \
    --work-dir /path/to/tiny-object-detection/outputs/fcos-r50-fpn/<run name>
```

The expected result is **36.6 AP**.

## AI-TOD-v2

The steps are from the [mmdet-rfla README](https://github.com/Chasel-Tsui/mmdet-rfla),
its copy of MMDetection's
[get started guide](https://github.com/Chasel-Tsui/mmdet-rfla/blob/main/docs/get_started.md)
and [testing and training guide](https://github.com/Chasel-Tsui/mmdet-rfla/blob/main/docs/1_exist_data_model.md),
and the [cocoapi-aitod README](https://github.com/jwwangchn/cocoapi-aitod).

### 1. Setup (`rfla` environment)

mmdet-rfla needs Linux, Python 3.6+, PyTorch 1.3+, CUDA 9.2+, GCC 5+, MMCV
between 1.3.2 and 1.4.0
([version check](https://github.com/Chasel-Tsui/mmdet-rfla/blob/main/mmdet/__init__.py)),
and cocoapi-aitod.

1. Install MMCV with its CUDA operators (`mmcv-full`). The get started guide
   gives the form below; fill in the CUDA and PyTorch versions:

   ```bash
   pip install mmcv-full -f https://download.openmmlab.com/mmcv/dist/{cu_version}/{torch_version}/index.html
   ```

2. Install the AI-TOD evaluation code:

   ```bash
   pip install "git+https://github.com/jwwangchn/cocoapi-aitod.git#subdirectory=aitodpycocotools"
   ```

3. Clone mmdet-rfla (outside this repo) and install it:

   ```bash
   git clone https://github.com/Chasel-Tsui/mmdet-rfla.git
   cd mmdet-rfla
   pip install -r requirements/build.txt
   python setup.py develop
   ```

mmdet-aitod (Track B's `aitod` environment) accepts MMCV 1.3.17 to 1.6.0, so
the two ranges overlap at 1.3.17 to 1.4.0. But each repo installs its own
`mmdet` package, so we keep them in separate environments. **TBD:** the exact
PyTorch, CUDA and MMCV versions that work together.

### 2. Data

The AI-TOD-v2 config expects this layout
([dataset config](https://github.com/Chasel-Tsui/mmdet-rfla/blob/main/configs/_base_/datasets/aitodv2_detection.py)):

```text
mmdet-rfla/data/AI-TODv2/
├── annotations/
│   ├── small_trainval_v2_2.0.json
│   └── small_test_v2_2.0.json
├── trainval/
└── test/
```

Link our copy there:

```bash
ln -s /path/to/tiny-object-detection/data/AI-TODv2 mmdet-rfla/data/AI-TODv2
```

How to get AI-TOD-v2 is in the
[aerial dataset notes](../../docs/datasets/aerial-dataset.md). The evaluation
uses cocoapi-aitod directly
([`mmdet/datasets/aitod.py`](https://github.com/Chasel-Tsui/mmdet-rfla/blob/main/mmdet/datasets/aitod.py)),
so the output includes AP_vt and AP_t.

### 3. Configs

| Version | Config | Published AI-TOD-v2 result |
|---|---|---|
| As published | [`configs/baselines/aitodv2_fcos_r50_1x.py`](https://github.com/Chasel-Tsui/mmdet-rfla/blob/main/configs/baselines/aitodv2_fcos_r50_1x.py) | 13.4 AP, AP_vt 2.5 |
| P2 (stride 4) | [`configs/baselines/aitodv2_fcos_r50_p2_1x.py`](https://github.com/Chasel-Tsui/mmdet-rfla/blob/main/configs/baselines/aitodv2_fcos_r50_p2_1x.py) | none |
| RFLA | [`configs/rfla/aitodv2_fcos_r50_rfla_kld_1x.py`](https://github.com/Chasel-Tsui/mmdet-rfla/blob/main/configs/rfla/aitodv2_fcos_r50_rfla_kld_1x.py) | 15.6 AP, AP_vt 4.4 |
| P2 with RFLA | [`configs/rfla/aitodv2_fcos_r50_p2_rfla_kld_1x.py`](https://github.com/Chasel-Tsui/mmdet-rfla/blob/main/configs/rfla/aitodv2_fcos_r50_p2_rfla_kld_1x.py) | none |

All train for 12 epochs with batch 2 on one GPU. Results are from the
[RFLA README](https://github.com/Chasel-Tsui/mmdet-rfla#main-results), Table 2.

### 4. Weights

The RFLA README links a set of pretrained models
([OneDrive](https://1drv.ms/u/s!Ao5UiAkIbGJ7xRGZ3AYB7IW8zas2?e=opfU3x)).
Which models are in it is **TBD**. Until we know, we plan to train each
version ourselves.

### 5. Train and test

Run from the `mmdet-rfla` folder:

```bash
python tools/train.py <config> --work-dir /path/to/tiny-object-detection/outputs/fcos-r50-fpn/<run name>
```

```bash
python tools/test.py <config> <checkpoint> --eval bbox
```

Compare with the published results in the table above, and write ours in
[results.md](results.md).
