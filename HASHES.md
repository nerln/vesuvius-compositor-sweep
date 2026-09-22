# Impronte del braccio di controllo di L1 — prese il 22/09/2026 16:35

Tutto misurato su questa macchina, niente copiato.

## Binario
- `vc_render_tifxyz`, costruito da **origin/main `d285029ab6b62bfacf12cdb41bd4653867db73c0`**
  (22/09), che contiene #1528 (fusa il 10/09 a `dc82d83c03bb`) e **non** contiene la nostra
  #1807, quindi nessun avviso su `--cache-gb`.
- sha256: `d813ddb1703a0ca569ced24867dcb9b66e50426692ebeb4ed7201af4da70f3f3`
- Costruito in 28 s in incrementale nella copia `pr-worktrees/pr1797` riportata a
  `origin/main` (il ramo `pr-1797` resta salvato: #1797 è chiusa dal suo autore).

## Checkpoint
- `scrollprize/ink_9um`, `hybrid_3d2d-seed43/step-060000.pth`, 132 MB
- sha256: `bf229faf754da3f1fc3026a3f9a9649341aeb3feb7bc89099cad31c55525d270`

## Mesh (braccio fine, già nel frame della scansione, nessuna trasformata)
`PHerc0139/segments/20250108000004-w029_2025010827/mesh/20250108000004-on-20260102150214-2.399um.tifxyz`
- `meta.json` `1f4c793ba0755e6fb05aa9219f320c68aff66aefc3b8bfea6a3f60a0e098b762` — scale 0,05, cioè passo 20 voxel
- `x.tif` `9f6bd997d436e042da6c40775c98bc31a0a22550ae77fc3699cdfcbe45a3c758`
- `y.tif` `7696c60bb67bf8ac93c0ba61021d1bdd6bdb8b9216a99c9e25d9631d19858db3`
- `z.tif` `f188a1303564ec30e04e68d8b066b372e57ad9557c7e28ed5ca13f007a3468f6`
- griglia 1404 x 1444 celle

## Etichette (dal repo di kadenpool, non ricalcolate da noi)
- `fine_labels_on_render.npz` `5111b5322b7d4bcc7312d527533c72fbf3349b14404bcecca386d6aa385def3b`
  — `V` (validazione) = **177.635** pixel, misurato da me sul file
- `coarse_labels_on_render.npz` `b8105ff31e10a9bcea19da8ba32d92d7187e0f138819e9caff964e0fd799e9ac`
  — `V` = 178.146, cioè il braccio grossolano: non è il nostro

## Volume
`s3://vesuvius-challenge-open-data/PHerc0139/volumes/20260102150214-2.399um-0.2m-78keV-masked.zarr/`,
letto in streaming al livello 2 (`[19239 6628 6628]`, `ds_scale=0.25` → 9,596 µm per pixel).

## Il comando, verbatim
```
vc_render_tifxyz --volume <cache>/20260102150214.zarr \
  --remote-url s3://vesuvius-challenge-open-data/PHerc0139/volumes/20260102150214-2.399um-0.2m-78keV-masked.zarr/ \
  --segmentation <mesh>/fine.tifxyz --zarr-output controllo_max.zarr \
  --scale 1 --group-idx 2 --num-slices 101 --slice-step 1 --flip-normals \
  --cache-gb 2 --crop-x 1728 --crop-y 4800 --crop-width 2304 --crop-height 768
```
Le bandiere di render sono quelle che kadenpool documenta (`downstream/README.md:132-135`).
Il ritaglio viene dalla docstring di `downstream/register.py`: tela 768 x 2304, origine
(4800, 1728). **Nessun `--accum` e nessun `--composite-collapse`**, quindi il riduttore
predefinito `max` non viene mai applicato: è il braccio di controllo.

## Uscita
`controllo_max.zarr`, livello 0 = **(101, 768, 2304) uint8**, cioè esattamente la tela
attesa. Render in circa 5 minuti in streaming, non i 20 previsti.

## Bersagli della replica, presi da `downstream/results.json` (braccio `theirmesh`)
- `peak`: finestre **[40, 61]**, `auc_forward` = **0,8967176079750061`**,
  `share_on_ink_forward` = **0,7218625255573946**, `share_on_bg_forward` = 0,0938
- `n_val_px` = **177.635**
- registrazione attesa: sy 0,999, sx 1,0, ty −192, tx −192, ncc 0,8905

## Ambiente di punteggio
venv isolato su disco esterno con `--system-site-packages` (eredita torch 2.8.0, MPS
disponibile); aggiunti solo `zarr` 3.4.0, `pynrrd`, `albumentations`. L'ambiente di base
non è stato toccato: `import zarr` fuori dal venv fallisce ancora. Si cancella con
`rm -rf` di una sola cartella.
`SWEEP_BATCH=2`, `SWEEP_WORKERS=1`, come dichiarato nel G0.
