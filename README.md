# No reducer improves ink reading on this segment, and `max` costs 0.010 AUC

Four arms, one variable: the `--accum-type` reducer in `vc_render_tifxyz`. Measured on
PHerc0139 segment `20250108000004-w029_2025010827`, scored with kadenpool's own harness
([scroll-lineup](https://github.com/kadenpool/scroll-lineup), `downstream/`), against the
Challenge's published ink labels. Context: [ScrollPrize/villa#1845](https://github.com/ScrollPrize/villa/issues/1845).

## The result

| arm | AUC forward | vs control | labelled ink found | background called ink | AUC reverse |
|---|---|---|---|---|---|
| control (no `--accum`) | **0.896687** | — | 72.21% | 9.37% | 0.5165 |
| max | 0.886627 | **−0.0101** | 71.14% | 9.20% | 0.4068 |
| mean | 0.895313 | −0.0014 | 71.80% | 7.91% | 0.4649 |
| median | 0.893082 | −0.0036 | 71.27% | 7.87% | 0.4627 |

Decision threshold **0.010 AUC**, fixed in [G0.md](G0.md) before any render — the size
#1845 itself treats as real. `mean` and `median` fall under it: indistinguishable. `max` is
the only arm at the margin, and in the wrong direction.

## Why the control matters

The control reproduces kadenpool's published number for the same mesh: **0.896687 against
0.8967176**, on the same **177,635** validation pixels, ink share 72.21% against 72.19%.
Different machine, `vc_render_tifxyz` rebuilt from `main@d285029a`, and `SWEEP_BATCH=2`
instead of 8 — a difference he had already measured himself (0.9123 vs 0.912). Without that
agreement, nothing below would mean anything.

## Two observations, not explanations

- Reverse-direction AUC drops in all three accumulated arms (0.5165 → 0.41–0.46). Reverse
  should be noise near 0.5. We do not know why, and do not guess here.
- `mean` and `median` lower background-called-ink (9.37% → ~7.9%) without moving AUC: fewer
  false positives at the same ranking.

## What is excluded, and why

`alpha` and `beerlambert` are not comparable arms: they imply composite mode on their own
(`vc_render_tifxyz.cpp:1204-1206`) and emit **one** collapsed image instead of
`--num-slices`, so the model's 21-layer windows cannot be formed.

## Limits

One segment, one checkpoint (`ink_9um` `hybrid_3d2d-seed43/step-060000`), one `--accum`
value (0.5, two samples per slice). The segment is in the checkpoint's training set, which
lifts absolute AUC but not the comparison between arms.

## Re-running it

[COMANDI.md](COMANDI.md) has every command verbatim; [HASHES.md](HASHES.md) has the sha256
of the binary, checkpoint, mesh and labels; `data/` has the raw scorer output; `log/` the
render logs. Renders are not committed (~180 MB each).

AI-assisted (Claude Code), human-directed.
