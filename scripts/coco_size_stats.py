"""Object size statistics for a COCO-format instances file.

Usage: python3 -I scripts/coco_size_stats.py <instances.json> [<instances.json> ...]

Reports, excluding crowd annotations:
  - counts of images, instances, categories
  - COCO's official bins using the "area" field (segmentation-mask area):
    small < 32^2, medium 32^2-96^2, large >= 96^2, plus finer < 8^2 and < 16^2
  - AI-TOD-style bins using absolute box size sqrt(w*h):
    very tiny 2-8, tiny 8-16, small 16-32, medium 32-64, larger > 64 (and < 2)
  - image resolution summary
"""
import json
import math
import statistics
import sys


def pct(n, total):
    return f"{n:>9,}  {100 * n / total:5.1f}%"


def report(path):
    with open(path) as f:
        d = json.load(f)
    anns = [a for a in d["annotations"] if not a.get("iscrowd", 0)]
    crowd = len(d["annotations"]) - len(anns)
    n = len(anns)
    print(f"== {path.split('/')[-1]}")
    print(f"images: {len(d['images']):,}  categories: {len(d['categories'])}  "
          f"instances (non-crowd): {n:,}  crowd: {crowd:,}")

    area = [a["area"] for a in anns]
    print("-- COCO bins, mask area (official definition)")
    for label, lo, hi in [("< 8^2", 0, 8**2), ("< 16^2", 0, 16**2), ("< 32^2 (small)", 0, 32**2),
                          ("32^2-96^2 (medium)", 32**2, 96**2), (">= 96^2 (large)", 96**2, math.inf)]:
        print(f"  {label:<20}{pct(sum(lo <= x < hi for x in area), n)}")

    size = [math.sqrt(a["bbox"][2] * a["bbox"][3]) for a in anns]
    print("-- AI-TOD bins, box size sqrt(w*h) in px")
    for label, lo, hi in [("< 2", 0, 2), ("2-8 very tiny", 2, 8), ("8-16 tiny", 8, 16),
                          ("16-32 small", 16, 32), ("32-64 medium", 32, 64), ("> 64", 64, math.inf)]:
        print(f"  {label:<20}{pct(sum(lo <= x < hi for x in size), n)}")
    print(f"  {'< 16 (tiny or less)':<20}{pct(sum(x < 16 for x in size), n)}")
    print(f"  {'< 32':<20}{pct(sum(x < 32 for x in size), n)}")
    print(f"  median box size: {statistics.median(size):.1f} px, mean: {statistics.mean(size):.1f} px")

    w = [im["width"] for im in d["images"]]
    h = [im["height"] for im in d["images"]]
    longest = [max(a, b) for a, b in zip(w, h)]
    print(f"-- resolution: longest side min {min(longest)}, median {statistics.median(longest):.0f}, "
          f"max {max(longest)}; share with longest side == 640: "
          f"{100 * sum(x == 640 for x in longest) / len(longest):.1f}%")
    print()


for p in sys.argv[1:]:
    report(p)
