# tiny-object-detection

Research on detecting tiny objects in images.

We study how well existing object detectors handle tiny objects (a few pixels
across), starting from point-based detectors such as CenterNet. We benchmark
them on three datasets, then try to improve them. The full project context,
goals and open questions are in [CLAUDE.md](CLAUDE.md). Read it first; it is
also what Claude uses as its instructions in this repo.

## Repository layout

| Path | What goes there |
|---|---|
| `CLAUDE.md` | Shared project context and working rules |
| `docs/datasets/` | Dataset research: one file per dataset choice, plus the final decision in `selection.md` |
| `docs/` | Other research notes and decisions (e.g. `model-selection.md`) |
| `scripts/` | Analysis and helper scripts |
| `data/`, `checkpoints/`, `outputs/` | Datasets, model weights and experiment outputs. **Not tracked by git** |

## How we work

- Tasks are GitHub issues in this repository.
- Work on a branch named `<type>/<short-topic>` (`docs`, `feat`, `fix` or
  `exp`), never directly on `main`.
- Open a pull request into `main`, and get another contributor to review it
  before merging. Reference the issue with `refs #N`.
- Never commit datasets, annotations or weights; put them in `data/`,
  `checkpoints/` or `outputs/`.

## Scripts

`scripts/coco_size_stats.py` reports object size shares for any COCO-format
annotation file, in AI-TOD size bins (box size) and COCO size bins (mask area):

```bash
python3 scripts/coco_size_stats.py data/coco/annotations/instances_val2017.json
```
