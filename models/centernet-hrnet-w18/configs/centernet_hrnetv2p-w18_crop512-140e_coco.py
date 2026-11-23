# CenterNet with an HRNetV2-W18 backbone, for MMDetection 3.x.
#
# NOT TRIED YET. Written from MMDetection's own configs:
#   - CenterNet: configs/centernet/centernet_r18-dcnv2_8xb16-crop512-140e_coco.py
#   - HRNet-W18: configs/hrnet/fcos_hrnetv2p-w18-gn-head_4xb4-1x_coco.py
#     (which builds on fcos_hrnetv2p-w32-gn-head_4xb4-1x_coco.py)
# Only the backbone and neck change. HRFPN with num_outs=1 merges the four
# HRNet branches into one stride-4 map, which MMDetection's CenterNet head
# expects (it takes exactly one feature map).
#
# Run from the mmdetection folder, e.g.
#   python tools/train.py /path/to/tiny-object-detection/models/centernet-hrnet-w18/configs/centernet_hrnetv2p-w18_crop512-140e_coco.py
# The "mmdet::" prefix loads the base config from the installed MMDetection.

_base_ = 'mmdet::centernet/centernet_r18-dcnv2_8xb16-crop512-140e_coco.py'

model = dict(
    backbone=dict(
        _delete_=True,
        type='HRNet',
        extra=dict(
            stage1=dict(
                num_modules=1,
                num_branches=1,
                block='BOTTLENECK',
                num_blocks=(4, ),
                num_channels=(64, )),
            stage2=dict(
                num_modules=1,
                num_branches=2,
                block='BASIC',
                num_blocks=(4, 4),
                num_channels=(18, 36)),
            stage3=dict(
                num_modules=4,
                num_branches=3,
                block='BASIC',
                num_blocks=(4, 4, 4),
                num_channels=(18, 36, 72)),
            stage4=dict(
                num_modules=3,
                num_branches=4,
                block='BASIC',
                num_blocks=(4, 4, 4, 4),
                num_channels=(18, 36, 72, 144))),
        init_cfg=dict(
            type='Pretrained', checkpoint='open-mmlab://msra/hrnetv2_w18')),
    neck=dict(
        _delete_=True,
        type='HRFPN',
        in_channels=[18, 36, 72, 144],
        out_channels=64,
        num_outs=1),
    bbox_head=dict(in_channels=64, feat_channels=64))

# For AI-TOD-v2, keep up to 1,500 detections per image (the AI-TOD evaluation
# counts up to 1,500). COCO keeps the default 100.
# model = dict(test_cfg=dict(topk=1500, max_per_img=1500))
