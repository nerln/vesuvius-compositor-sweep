#!/usr/bin/env python3
"""Recompute every number in README.md from data/*.json. No network, no model, no renders.

    python3 reproduce.py

Exits 1 if any README claim does not match the scorer output.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARMS = [("control", "controllo"), ("max", "accum_max"),
        ("mean", "accum_mean"), ("median", "accum_median")]
THRESHOLD = 0.010                      # fixed in G0.md before any render
PUBLISHED_AUC = 0.8967176079750061     # kadenpool, downstream/results.json, arm "theirmesh"
PUBLISHED_INK = 0.7218625255573946
PUBLISHED_NVAL = 177635

rows, fail = {}, []
for name, f in ARMS:
    p = os.path.join(HERE, "data", f + ".json")
    d = json.load(open(p))
    rows[name] = (d["rows"][0], d["n_val_px"])

base = rows["control"][0]["auc_forward"]
print(f"{'arm':9} {'AUC fwd':>11} {'vs control':>11} {'ink found':>10} {'bg as ink':>10} {'AUC rev':>9}")
for name, _ in ARMS:
    r, _ = rows[name]
    d = "" if name == "control" else f"{r['auc_forward'] - base:+.4f}"
    print(f"{name:9} {r['auc_forward']:11.6f} {d:>11} "
          f"{r['share_on_ink_forward']*100:9.2f}% {r['share_on_bg_forward']*100:9.2f}% "
          f"{r['auc_reverse']:9.4f}")

print(f"\nvalidation pixels, all arms: {set(n for _, n in rows.values())}")
for name, _ in ARMS:
    if rows[name][1] != PUBLISHED_NVAL:
        fail.append(f"{name}: n_val_px {rows[name][1]} != {PUBLISHED_NVAL}")

d_repl = abs(base - PUBLISHED_AUC)
print(f"\nreplication: control {base:.6f} vs published {PUBLISHED_AUC:.7f} -> {d_repl:.7f}")
print(f"             ink share {rows['control'][0]['share_on_ink_forward']:.6f} "
      f"vs published {PUBLISHED_INK:.6f}")
if d_repl > 0.005:
    fail.append(f"replication off by {d_repl:.6f}, G0 rule 1 allows 0.005")

print(f"\nthreshold fixed in G0 before any render: {THRESHOLD}")
for name, _ in ARMS[1:]:
    delta = rows[name][0]["auc_forward"] - base
    verdict = "at/over the margin" if abs(delta) >= THRESHOLD else "indistinguishable"
    print(f"  {name:7} {delta:+.4f}  -> {verdict}")
    if name in ("mean", "median") and abs(delta) >= THRESHOLD:
        fail.append(f"README calls {name} indistinguishable, but |{delta:.4f}| >= {THRESHOLD}")
    if name == "max" and abs(delta) < THRESHOLD:
        fail.append(f"README puts max at the margin, but |{delta:.4f}| < {THRESHOLD}")
if rows["max"][0]["auc_forward"] >= base:
    fail.append("README says max is worse than the control; the data disagrees")

print()
if fail:
    print("MISMATCH:"); [print("  -", f) for f in fail]; sys.exit(1)
print("Every README claim matches data/. OK")
