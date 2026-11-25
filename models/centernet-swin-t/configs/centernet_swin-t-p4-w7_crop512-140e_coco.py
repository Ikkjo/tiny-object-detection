# CenterNet with a Swin-T backbone, for MMDetection 3.x.
#
# NOT TRIED YET. Written from MMDetection's own configs:
#   - CenterNet: configs/centernet/centernet_r18-dcnv2_8xb16-crop512-140e_coco.py
#   - Swin-T backbone and optimizer: configs/swin/retinanet_swin-t-p4-w7_fpn_1x_coco.py
#     and configs/swin/mask-rcnn_swin-t-p4-w7_fpn_1x_coco.py
# Only the backbone, neck and optimizer change. Swin-T gives four maps
# (strides 4, 8, 16, 32); HRFPN with num_outs=1 merges them into one stride-4
# map, the same neck as our CenterNet-HRNet-W18 config.
#
# Swin works on 7x7 windows of stride-4 tokens. A CenterNet with a Swin neck
# for small birds (arXiv 2511.22310) found smaller windows worked better on
# small objects; window_size is the first setting to try changing.
#
# Run from the mmdetection folder, e.g.
#   python tools/train.py /path/to/tiny-object-detection/models/centernet-swin-t/configs/centernet_swin-t-p4-w7_crop512-140e_coco.py

_base_ = 'mmdet::centernet/centernet_r18-dcnv2_8xb16-crop512-140e_coco.py'

pretrained = 'https://github.com/SwinTransformer/storage/releases/download/v1.0.0/swin_tiny_patch4_window7_224.pth'  # noqa

model = dict(
    backbone=dict(
        _delete_=True,
        type='SwinTransformer',
        embed_dims=96,
        depths=[2, 2, 6, 2],
        num_heads=[3, 6, 12, 24],
        window_size=7,
        mlp_ratio=4,
        qkv_bias=True,
        qk_scale=None,
        drop_rate=0.,
        attn_drop_rate=0.,
        drop_path_rate=0.2,
        patch_norm=True,
        out_indices=(0, 1, 2, 3),
        with_cp=False,
        convert_weights=True,
        init_cfg=dict(type='Pretrained', checkpoint=pretrained)),
    neck=dict(
        _delete_=True,
        type='HRFPN',
        in_channels=[96, 192, 384, 768],
        out_channels=64,
        num_outs=1),
    bbox_head=dict(in_channels=64, feat_channels=64))

# Optimizer from MMDetection's Swin-T configs (AdamW, no weight decay on
# norms and position tables), keeping CenterNet's gradient clipping.
optim_wrapper = dict(
    type='OptimWrapper',
    clip_grad=dict(max_norm=35, norm_type=2),
    paramwise_cfg=dict(
        custom_keys={
            'absolute_pos_embed': dict(decay_mult=0.),
            'relative_position_bias_table': dict(decay_mult=0.),
            'norm': dict(decay_mult=0.)
        }),
    optimizer=dict(
        _delete_=True,
        type='AdamW',
        lr=0.0001,
        betas=(0.9, 0.999),
        weight_decay=0.05))

# For AI-TOD-v2, keep up to 1,500 detections per image (the AI-TOD evaluation
# counts up to 1,500). COCO keeps the default 100.
# model = dict(test_cfg=dict(topk=1500, max_per_img=1500))
