"""Object-size and density statistics for aerial detection datasets.

Reads one annotation set in its native format, converts every object to a
common record, and prints (and optionally saves as JSON) the numbers we use to
compare datasets for tiny-object work.

Usage:
  python3 -I scripts/aerial_size_stats.py --format coco     --name AI-TOD-v2/val  ann.json [more.json ...]
  python3 -I scripts/aerial_size_stats.py --format visdrone --name VisDrone/val   annotations_dir [--sizes sizes.json]
  python3 -I scripts/aerial_size_stats.py --format dota     --name DOTA-v2/train  labelTxt_dir    [--sizes sizes.json]
  python3 -I scripts/aerial_size_stats.py --format xview    --name xView/train    xView_train.geojson
  python3 -I scripts/aerial_size_stats.py --format sodaa    --name SODA-A/train   annotations_dir
  add --json out.json to save the summary.

--sizes is an optional JSON mapping image file stem -> [width, height] for
formats whose labels do not store the image size (VisDrone, DOTA). Without it,
resolution and relative-size figures are skipped.

What is reported (crowd / ignore regions excluded and counted separately):
  - images, instances, categories, instances per category
  - box size s = sqrt(w*h) of the horizontal box, in pixels, at native
    resolution: mean, median, p10, p90
  - AI-TOD bins on s: <2, 2-8 very tiny, 8-16 tiny, 16-32 small, 32-64 medium,
    >64; share < 16 and < 32
  - COCO "small" by box area < 32^2 (COCO itself uses mask area; boxes are used
    here because aerial datasets have no masks)
  - for oriented boxes, the same size figures using sqrt(polygon area), and
    the share in SODA's area bins (eS <=144, rS <=400, gS <=1024, N <=2000 px^2)
  - objects per image (mean, median, max) and share of empty images
  - image resolution (min / median / max of the longest side)
  - relative size: s / sqrt(W*H)
  - CenterNet target check at native resolution, output stride --stride
    (default 4), using the official gaussian_radius (min_overlap 0.7) on the
    box size divided by the stride, rounded up, as in CenterNet's ctdet.py:
      * share of objects whose heatmap Gaussian has radius 0 (one positive cell)
      * share of objects whose centre falls in the same output cell as another
        object of the same image (they collapse to one heatmap peak)
    These are *native-resolution* figures: training at a different input size
    changes them.
"""
import argparse
import glob
import json
import math
import os
import statistics
import sys
from collections import Counter, defaultdict


# --------------------------------------------------------------------------- #
# Common record: dict(img, W, H, cls, x, y, w, h, poly_area, ignore)
#   x, y = top-left of the horizontal box; poly_area only for oriented boxes.
# --------------------------------------------------------------------------- #

def load_coco(paths, _sizes):
    recs, images = [], {}
    for p in paths:
        with open(p) as f:
            d = json.load(f)
        cats = {c["id"]: c["name"] for c in d["categories"]}
        for im in d["images"]:
            images[(p, im["id"])] = (im.get("width"), im.get("height"))
        for a in d["annotations"]:
            W, H = images.get((p, a["image_id"]), (None, None))
            x, y, w, h = a["bbox"]
            recs.append(dict(img=(p, a["image_id"]), W=W, H=H, cls=cats.get(a["category_id"], a["category_id"]),
                             x=x, y=y, w=w, h=h, poly_area=None,
                             ignore=bool(a.get("iscrowd", 0) or a.get("ignore", 0))))
    return recs, set(images)


VISDRONE_CLASSES = {0: "ignored-region", 1: "pedestrian", 2: "people", 3: "bicycle", 4: "car", 5: "van",
                    6: "truck", 7: "tricycle", 8: "awning-tricycle", 9: "bus", 10: "motor", 11: "others"}


def load_visdrone(paths, sizes):
    """VisDrone-DET txt: x,y,w,h,score,category,truncation,occlusion.
    category 0 = ignored region, 11 = others; score 0 marks ignored boxes."""
    recs, images = [], set()
    for d in paths:
        for fp in sorted(glob.glob(os.path.join(d, "*.txt"))):
            stem = os.path.splitext(os.path.basename(fp))[0]
            images.add(stem)
            W, H = sizes.get(stem, (None, None))
            with open(fp) as f:
                for line in f:
                    v = [t for t in line.strip().replace(",", " ").split() if t]
                    if len(v) < 6:
                        continue
                    x, y, w, h, score, cat = (float(v[0]), float(v[1]), float(v[2]), float(v[3]),
                                              int(v[4]), int(v[5]))
                    recs.append(dict(img=stem, W=W, H=H, cls=VISDRONE_CLASSES.get(cat, cat), x=x, y=y, w=w, h=h,
                                     poly_area=None, ignore=(cat in (0, 11) or score == 0)))
    return recs, images


def _poly_area(pts):
    a = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        a += x1 * y2 - x2 * y1
    return abs(a) / 2


def _from_poly(pts, img, W, H, cls, ignore):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return dict(img=img, W=W, H=H, cls=cls, x=min(xs), y=min(ys), w=max(xs) - min(xs), h=max(ys) - min(ys),
                poly_area=_poly_area(pts), ignore=ignore)


def load_dota(paths, sizes):
    """DOTA labelTxt: optional 'imagesource:' / 'gsd:' header, then
    x1 y1 x2 y2 x3 y3 x4 y4 class difficult. Difficult objects are kept
    (DOTA evaluates them as ignore) but flagged."""
    recs, images = [], set()
    for d in paths:
        for fp in sorted(glob.glob(os.path.join(d, "*.txt"))):
            stem = os.path.splitext(os.path.basename(fp))[0]
            images.add(stem)
            W, H = sizes.get(stem, (None, None))
            with open(fp) as f:
                for line in f:
                    v = line.split()
                    if len(v) < 9 or ":" in v[0]:
                        continue
                    pts = [(float(v[i]), float(v[i + 1])) for i in range(0, 8, 2)]
                    r = _from_poly(pts, stem, W, H, v[8], ignore=False)
                    r["difficult"] = len(v) > 9 and v[9] == "1"
                    recs.append(r)
    return recs, images


# xView type_id -> one of the 60 official classes; -1 = not one of the 60
# (ignored). Mapping and names from Ultralytics' xView.yaml.
XVIEW_CLASS2INDEX = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, -1, 3, -1, 4, 5, 6, 7, 8, -1, 9, 10, 11,
                     12, 13, 14, 15, -1, -1, 16, 17, 18, 19, 20, 21, 22, -1, 23, 24, 25, -1, 26, 27, -1, 28, -1,
                     29, 30, 31, 32, 33, 34, 35, 36, 37, -1, 38, 39, 40, 41, 42, 43, 44, 45, -1, -1, -1, -1, 46,
                     47, 48, 49, -1, 50, 51, -1, 52, -1, -1, -1, 53, 54, -1, 55, -1, -1, 56, -1, 57, -1, 58, 59]
XVIEW_NAMES = ["Fixed-wing Aircraft", "Small Aircraft", "Cargo Plane", "Helicopter", "Passenger Vehicle", "Small Car",
               "Bus", "Pickup Truck", "Utility Truck", "Truck", "Cargo Truck", "Truck w/Box", "Truck Tractor",
               "Trailer", "Truck w/Flatbed", "Truck w/Liquid", "Crane Truck", "Railway Vehicle", "Passenger Car",
               "Cargo Car", "Flat Car", "Tank car", "Locomotive", "Maritime Vessel", "Motorboat", "Sailboat",
               "Tugboat", "Barge", "Fishing Vessel", "Ferry", "Yacht", "Container Ship", "Oil Tanker",
               "Engineering Vehicle", "Tower crane", "Container Crane", "Reach Stacker", "Straddle Carrier",
               "Mobile Crane", "Dump Truck", "Haul Truck", "Scraper/Tractor", "Front loader/Bulldozer", "Excavator",
               "Cement Mixer", "Ground Grader", "Hut/Tent", "Shed", "Building", "Aircraft Hangar",
               "Damaged Building", "Facility", "Construction Site", "Vehicle Lot", "Helipad", "Storage Tank",
               "Shipping container lot", "Shipping Container", "Pylon", "Tower"]


def load_xview(paths, _sizes):
    """xView geojson: properties.bounds_imcoords = 'x1,y1,x2,y2', type_id, image_id.
    type_ids outside the 60 official classes are counted as ignored. Image
    sizes are not in the labels, so boxes are not clipped to the image.
    Checked on xView_train.geojson (Nov 2026)."""
    recs, images = [], set()
    for p in paths:
        with open(p) as f:
            d = json.load(f)
        for ft in d["features"]:
            pr = ft["properties"]
            x1, y1, x2, y2 = [float(t) for t in pr["bounds_imcoords"].split(",")]
            images.add(pr["image_id"])
            t = int(pr["type_id"])
            k = XVIEW_CLASS2INDEX[t] if 0 <= t < len(XVIEW_CLASS2INDEX) else -1
            recs.append(dict(img=pr["image_id"], W=None, H=None,
                             cls=XVIEW_NAMES[k] if k >= 0 else f"type_{t}", x=x1, y=y1,
                             w=x2 - x1, h=y2 - y1, poly_area=None, ignore=k < 0))
    return recs, images


def load_sodaa(paths, _sizes):
    """SODA-A: one JSON per image with 'images' (width/height) and
    'annotations' holding a 'poly' of x, y pairs (4 corners for most objects). Category names from 'categories'.
    Category "ignore" (id 9) marks ignore regions. Checked on the official
    SODA-A annotation files (Nov 2026)."""
    recs, images = [], set()
    files = []
    for d in paths:
        files += sorted(glob.glob(os.path.join(d, "*.json"))) if os.path.isdir(d) else [d]
    for fp in files:
        with open(fp) as f:
            d = json.load(f)
        im = d["images"] if isinstance(d["images"], dict) else d["images"][0]
        W, H = im.get("width"), im.get("height")
        stem = os.path.splitext(os.path.basename(fp))[0]
        images.add(stem)
        cats = {c["id"]: c["name"] for c in d.get("categories", [])}
        for a in d["annotations"]:
            v = a["poly"]  # usually 4 corners; objects cut by the image border and ignore regions have more
            pts = [(float(v[i]), float(v[i + 1])) for i in range(0, len(v) - 1, 2)]
            name = cats.get(a["category_id"], a["category_id"])
            recs.append(_from_poly(pts, stem, W, H, name,
                                   ignore=bool(name == "ignore" or a.get("ignore", 0) or a.get("iscrowd", 0))))
    return recs, images


LOADERS = dict(coco=load_coco, visdrone=load_visdrone, dota=load_dota, xview=load_xview, sodaa=load_sodaa)


# --------------------------------------------------------------------------- #
# CenterNet target check (official formula, CenterNet src/lib/utils/image.py)
# --------------------------------------------------------------------------- #

def gaussian_radius(height, width, min_overlap=0.7):
    b1 = height + width
    c1 = width * height * (1 - min_overlap) / (1 + min_overlap)
    r1 = (b1 + math.sqrt(b1 ** 2 - 4 * c1)) / 2
    b2 = 2 * (height + width)
    c2 = (1 - min_overlap) * width * height
    r2 = (b2 + math.sqrt(b2 ** 2 - 16 * c2)) / 2
    a3 = 4 * min_overlap
    b3 = -2 * min_overlap * (height + width)
    c3 = (min_overlap - 1) * width * height
    r3 = (b3 + math.sqrt(b3 ** 2 - 4 * a3 * c3)) / 2
    return min(r1, r2, r3)


# --------------------------------------------------------------------------- #

def q(xs, p):
    xs = sorted(xs)
    if not xs:
        return float("nan")
    k = (len(xs) - 1) * p
    lo, hi = math.floor(k), math.ceil(k)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def bins(sizes):
    n = len(sizes)
    out = {}
    for label, lo, hi in [("<2", 0, 2), ("2-8 very tiny", 2, 8), ("8-16 tiny", 8, 16), ("16-32 small", 16, 32),
                          ("32-64 medium", 32, 64), (">=64", 64, math.inf)]:
        out[label] = sum(lo <= s < hi for s in sizes) / n
    out["<16"] = sum(s < 16 for s in sizes) / n
    out["<32"] = sum(s < 32 for s in sizes) / n
    return out


def summarise(name, recs, images, stride):
    valid = [r for r in recs if not r["ignore"] and r["w"] > 0 and r["h"] > 0]
    ign = len(recs) - len(valid)
    n = len(valid)
    S = {"name": name, "images": len(images), "instances": n, "ignored_or_crowd": ign}
    if n == 0:
        return S
    size = [math.sqrt(r["w"] * r["h"]) for r in valid]
    S["box_size_px"] = dict(mean=statistics.mean(size), median=statistics.median(size), p10=q(size, .1),
                            p90=q(size, .9), min=min(size), max=max(size))
    S["box_size_bins"] = bins(size)
    S["coco_small_by_box_area"] = sum(r["w"] * r["h"] < 32 ** 2 for r in valid) / n
    poly = [math.sqrt(r["poly_area"]) for r in valid if r["poly_area"]]
    if poly:
        S["obb_size_px"] = dict(mean=statistics.mean(poly), median=statistics.median(poly))
        S["obb_size_bins"] = bins(poly)
        pa = [r["poly_area"] for r in valid if r["poly_area"]]
        S["soda_area_bins"] = {lab: sum(lo < a <= hi for a in pa) / len(pa) for lab, lo, hi in
                               [("eS (0,144]", 0, 144), ("rS (144,400]", 144, 400), ("gS (400,1024]", 400, 1024),
                                ("N (1024,2000]", 1024, 2000), (">2000", 2000, math.inf)]}
    if any("difficult" in r for r in valid):
        S["difficult"] = sum(r.get("difficult", False) for r in valid)

    cls = Counter(r["cls"] for r in valid)
    by_cls = defaultdict(list)
    for r, s in zip(valid, size):
        by_cls[r["cls"]].append(s)
    S["classes"] = {str(c): dict(count=k, share=k / n, median_px=statistics.median(by_cls[c]),
                                 under16=sum(s < 16 for s in by_cls[c]) / k)
                    for c, k in cls.most_common()}

    per_img = Counter(r["img"] for r in valid)
    counts = [per_img.get(i, 0) for i in images] if images else list(per_img.values())
    S["objects_per_image"] = dict(mean=statistics.mean(counts), median=statistics.median(counts),
                                  max=max(counts), empty_share=sum(c == 0 for c in counts) / len(counts))

    whs = {}
    for r in valid:
        if r["W"] and r["H"]:
            whs[r["img"]] = (r["W"], r["H"])
    if whs:
        longest = [max(w, h) for w, h in whs.values()]
        S["resolution_longest_side"] = dict(min=min(longest), median=statistics.median(longest),
                                            max=max(longest), distinct_sizes=len(set(whs.values())))
        rel = [math.sqrt(r["w"] * r["h"]) / math.sqrt(r["W"] * r["H"]) for r in valid if r["W"] and r["H"]]
        S["relative_size_median"] = statistics.median(rel)

    r0 = 0
    cells = Counter()
    for r in valid:
        if max(0, int(gaussian_radius(math.ceil(r["h"] / stride), math.ceil(r["w"] / stride)))) == 0:
            r0 += 1
        cells[(r["img"], int((r["x"] + r["w"] / 2) // stride), int((r["y"] + r["h"] / 2) // stride))] += 1
    S[f"centernet_stride{stride}"] = dict(radius0_share=r0 / n,
                                          centre_collision_share=sum(c for c in cells.values() if c > 1) / n)
    return S


def show(S):
    print(f"== {S['name']}")
    print(f"images {S['images']:,}  instances {S['instances']:,}  ignored/crowd {S['ignored_or_crowd']:,}")
    if not S["instances"]:
        return
    b = S["box_size_px"]
    print(f"box size sqrt(wh): mean {b['mean']:.1f}  median {b['median']:.1f}  p10 {b['p10']:.1f}  "
          f"p90 {b['p90']:.1f}  (min {b['min']:.1f}, max {b['max']:.0f})")
    print("  bins: " + "  ".join(f"{k} {100 * v:.1f}%" for k, v in S["box_size_bins"].items()))
    print(f"  COCO small by box area: {100 * S['coco_small_by_box_area']:.1f}%")
    if "obb_size_px" in S:
        print(f"oriented size sqrt(poly area): mean {S['obb_size_px']['mean']:.1f}  "
              f"median {S['obb_size_px']['median']:.1f}")
        print("  bins: " + "  ".join(f"{k} {100 * v:.1f}%" for k, v in S["obb_size_bins"].items()))
        print("  SODA area bins (polygon area, px^2): " +
              "  ".join(f"{k} {100 * v:.1f}%" for k, v in S["soda_area_bins"].items()))
    o = S["objects_per_image"]
    print(f"objects/image: mean {o['mean']:.1f}  median {o['median']:.0f}  max {o['max']:,}  "
          f"empty images {100 * o['empty_share']:.1f}%")
    if "resolution_longest_side" in S:
        r = S["resolution_longest_side"]
        print(f"resolution longest side: min {r['min']}  median {r['median']:.0f}  max {r['max']}  "
              f"({r['distinct_sizes']} distinct sizes); relative size median {S['relative_size_median']:.4f}")
    for k, v in S.items():
        if k.startswith("centernet"):
            print(f"{k}: radius-0 {100 * v['radius0_share']:.1f}%  centre collisions "
                  f"{100 * v['centre_collision_share']:.1f}%")
    print("classes (count, share, median px, share <16):")
    for c, v in S["classes"].items():
        print(f"  {c:<22}{v['count']:>9,}  {100 * v['share']:5.1f}%  {v['median_px']:6.1f}  {100 * v['under16']:5.1f}%")
    print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--format", required=True, choices=sorted(LOADERS))
    ap.add_argument("--name", required=True)
    ap.add_argument("--sizes")
    ap.add_argument("--stride", type=int, default=4)
    ap.add_argument("--json")
    ap.add_argument("paths", nargs="+")
    a = ap.parse_args()
    sizes = {}
    if a.sizes:
        with open(a.sizes) as f:
            sizes = {k: tuple(v) for k, v in json.load(f).items()}
    recs, images = LOADERS[a.format](a.paths, sizes)
    S = summarise(a.name, recs, images, a.stride)
    show(S)
    if a.json:
        with open(a.json, "w") as f:
            json.dump(S, f, indent=1)


if __name__ == "__main__":
    sys.exit(main())
