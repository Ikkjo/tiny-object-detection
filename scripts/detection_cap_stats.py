"""How many objects a detector can never find because it keeps too few boxes.

Most detectors keep at most N detections per image (MMDetection's CenterNet
and the official CenterNet code keep 100 by default, MMDetection's DINO keeps
300 of its 900 queries, the AI-TOD evaluation counts up to 1500). In an image
with more than N objects, at least (objects - N) of them can't be detected,
whatever the model does. Some code also caps the objects used for training
(the official CenterNet code keeps the first 128 per image). This script
counts, for each cap N, how many images have more than N objects and what
share of all objects lies beyond the cap. Counts are per full image; training
on crops changes them.

Crowd boxes (iscrowd = 1) are left out, as in the evaluation.

Usage:
  python3 -I scripts/detection_cap_stats.py ann.json [--caps 100 128 300 900 1500]
  add --json out.json to save the numbers.
"""
import argparse
import collections
import json


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("ann", help="COCO-format annotation file")
    parser.add_argument("--caps", type=int, nargs="+", default=[100, 128, 300, 900, 1500])
    parser.add_argument("--json", help="save the summary to this file")
    args = parser.parse_args()

    with open(args.ann) as f:
        data = json.load(f)
    counts = collections.Counter(
        a["image_id"] for a in data["annotations"] if not a.get("iscrowd", 0)
    )
    n_images = len(data["images"])
    n_objects = sum(counts.values())

    summary = {"annotation_file": args.ann, "images": n_images,
               "objects": n_objects, "max_objects_per_image": max(counts.values()),
               "caps": []}
    print(f"{args.ann}: {n_images} images, {n_objects} objects, "
          f"max {summary['max_objects_per_image']} per image")
    for cap in args.caps:
        over = [c for c in counts.values() if c > cap]
        missed = sum(c - cap for c in over)
        row = {"cap": cap, "images_over_cap": len(over),
               "images_over_cap_share": len(over) / n_images,
               "objects_beyond_cap": missed,
               "objects_beyond_cap_share": missed / n_objects}
        summary["caps"].append(row)
        print(f"  cap {cap:>5}: {len(over):>5} images over the cap "
              f"({row['images_over_cap_share']:.2%}), {missed:>6} objects beyond it "
              f"({row['objects_beyond_cap_share']:.2%})")
    if args.json:
        with open(args.json, "w") as f:
            json.dump(summary, f, indent=2)


if __name__ == "__main__":
    main()
