# Every command, verbatim

Binary: `vc_render_tifxyz` built from `origin/main d285029ab6b62bfacf12cdb41bd4653867db73c0`.
Scorer: `register.py` / `sweep.py` from `kadenpool/scroll-lineup`, `downstream/`, unmodified.

## Control (kadenpool's documented flags, no accumulation)

```
vc_render_tifxyz \
  --volume cache/20260102150214.zarr \
  --remote-url s3://vesuvius-challenge-open-data/PHerc0139/volumes/20260102150214-2.399um-0.2m-78keV-masked.zarr/ \
  --segmentation mesh/fine.tifxyz \
  --zarr-output controllo_max.zarr \
  --scale 1 --group-idx 2 --num-slices 101 --slice-step 1 --flip-normals \
  --cache-gb 2 --crop-x 1728 --crop-y 4800 --crop-width 2304 --crop-height 768
```

Mesh: `PHerc0139/segments/20250108000004-w029_2025010827/mesh/20250108000004-on-20260102150214-2.399um.tifxyz`
(already in the 2.399 µm frame, no transform). Level 2 is 9.596 µm per pixel and per layer.
Crop from `downstream/register.py`: canvas 768 × 2304, origin (4800, 1728).

## The three accumulated arms

Identical, plus:

```
  --accum 0.5 --accum-type max      # or mean, or median
```

`--accum 0.5` with `--slice-step 1` gives 2 samples per slice. The tool prints
`Accumulation: 2 samples/slice at step 0.5000 (<reducer>)`.

## Scoring, identical for all four

```
SWEEP_BATCH=2 SWEEP_WORKERS=1 python sweep.py \
  <arm>.zarr fine_labels_on_render.npz <workdir> \
  hybrid_3d2d-seed43/step-060000.pth <villa>/vesuvius/src 40
```

Window start 40 is the peak window [40,61] reported for this mesh in
`downstream/results.json`. Labels: `downstream/mesh_choice/fine_labels_on_render.npz`,
field `V` = 177,635 validation pixels.
