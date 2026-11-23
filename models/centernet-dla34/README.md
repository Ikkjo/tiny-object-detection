# CenterNet with DLA-34: how to run

CenterNet ("Objects as Points") with the DLA-34 backbone, using the official
code. Model details are in [about.md](about.md) and our results in
[results.md](results.md).

**Status:** not tried yet. The official code was written for PyTorch 0.4.1
and a compiled CUDA extension (DCNv2), and needs an NVIDIA GPU. We don't know
yet whether it runs on a current setup. This is the first open item in the
[Track B notes](../../docs/models/standard-centernet-and-two-stage.md#6-open-items).
If it can't be made to run, we use the runner-up,
[CenterNet Update](../centernet-update-r50-fpn/).

All steps below are from the official
[install guide](https://github.com/xingyizhou/CenterNet/blob/master/readme/INSTALL.md),
[data guide](https://github.com/xingyizhou/CenterNet/blob/master/readme/DATA.md)
and [getting started guide](https://github.com/xingyizhou/CenterNet/blob/master/readme/GETTING_STARTED.md).

## 1. Setup

The guide was tested on Ubuntu 16.04 with Python 3.6 and PyTorch 0.4.1.

1. Create a conda environment:

   ```bash
   conda create --name CenterNet python=3.6
   conda activate CenterNet
   ```

2. Install PyTorch 0.4.1:

   ```bash
   conda install pytorch=0.4.1 torchvision -c pytorch
   ```

   The guide also asks to turn off cuDNN batch normalization by editing
   `torch/nn/functional.py` (line 1254 for PyTorch 0.4.1). For other PyTorch
   versions, find the line with `torch.batch_norm` and replace
   `torch.backends.cudnn.enabled` with `False`. The authors saw slightly worse
   training results without this change.

3. Install the COCO API:

   ```bash
   git clone https://github.com/cocodataset/cocoapi.git $COCOAPI
   cd $COCOAPI/PythonAPI
   make
   python setup.py install --user
   ```

4. Clone CenterNet (outside this repo) and install its requirements:

   ```bash
   git clone https://github.com/xingyizhou/CenterNet $CenterNet_ROOT
   cd $CenterNet_ROOT
   pip install -r requirements.txt
   ```

5. Compile DCNv2 (deformable convolution):

   ```bash
   cd $CenterNet_ROOT/src/lib/models/networks/DCNv2
   ./make.sh
   ```

   This is the step most likely to fail on a current PyTorch. **TBD:** which
   DCNv2 build works with a newer PyTorch.

## 2. Data

CenterNet expects COCO in `$CenterNet_ROOT/data/coco/`:

```text
data/coco/
├── annotations/
│   ├── instances_train2017.json
│   └── instances_val2017.json
├── train2017/
└── val2017/
```

We keep the dataset in this repo's `data/coco/` and link it there instead of
copying:

```bash
ln -s /path/to/tiny-object-detection/data/coco $CenterNet_ROOT/data/coco
```

**AI-TOD-v2:** CenterNet has no AI-TOD-v2 config. **TBD:** we need to add
AI-TOD-v2 as a new dataset in the code (it is in COCO format, so this should
follow the COCO dataset class).

## 3. Weights

The COCO model we use is `ctdet_coco_dla_2x` (37.4 AP on COCO val 2017). It is
linked from the
[model zoo](https://github.com/xingyizhou/CenterNet/blob/master/readme/MODEL_ZOO.md)
as a Google Drive file:
[ctdet_coco_dla_2x.pth](https://drive.google.com/file/d/18Q3fzzAsha_3Qid6mn4jcIFPeOGUaj1d).

Put it in `$CenterNet_ROOT/models/`, or keep it in
`checkpoints/centernet-dla34/` in this repo and pass that path to
`--load_model`.

## 4. Test on COCO val 2017

Run from `$CenterNet_ROOT/src`:

```bash
python test.py ctdet --exp_id coco_dla --keep_res --load_model ../models/ctdet_coco_dla_2x.pth
```

If the setup is right, this gives **37.4 AP**. `--keep_res` keeps the original
image size; without it the images are resized to 512×512. With `--flip_test`
the expected AP is 39.2, and with
`--flip_test --test_scales 0.5,0.75,1,1.25,1.5` it is 41.7.

Our first run should match 37.4 AP (the authors saw up to 0.4 AP difference
between training runs). Write the result in [results.md](results.md).

## 5. Train

The training scripts for each model are in the repo's
[experiments](https://github.com/xingyizhou/CenterNet/tree/master/experiments)
folder. The paper trained on 8 GPUs. For fewer GPUs, the guide says to scale
the learning rate with the batch size. Its example for 2 GPUs:

```bash
python main.py ctdet --exp_id coco_dla --batch_size 32 --master_batch 15 --lr 1.25e-4 --gpus 0,1
```

Add `--resume` to continue a stopped run. **TBD:** batch size and learning
rate for our GPU.
