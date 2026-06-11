#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../source_code/Depth-Anything-V2"

conda run -n DL python run.py \
  --encoder vits \
  --img-path assets/examples \
  --outdir outputs_inference/vits_518

conda run -n DL python run.py \
  --encoder vitb \
  --img-path assets/examples \
  --outdir outputs_inference/vitb_518

conda run -n DL python run.py \
  --encoder vitl \
  --img-path assets/examples \
  --outdir outputs_inference/vitl_518

cd ../..
conda run -n DL python scripts/make_inference_contact_sheet.py
