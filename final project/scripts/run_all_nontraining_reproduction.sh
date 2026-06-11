#!/usr/bin/env bash
set -euo pipefail

PACKAGE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REPO_DIR="$PACKAGE_DIR/source_code/Depth-Anything-V2"
METRIC_DIR="$REPO_DIR/metric_depth"

cd "$PACKAGE_DIR"

conda run -n DL python scripts/evaluate_da2k.py --encoder vits | tee logs/da2k_vits.log
conda run -n DL python scripts/evaluate_da2k.py --encoder vitb | tee logs/da2k_vitb.log
conda run -n DL python scripts/evaluate_da2k.py --encoder vitl | tee logs/da2k_vitl.log

cd "$REPO_DIR"

conda run -n DL python run.py --encoder vits --img-path assets/examples --outdir outputs_inference/vits_518
conda run -n DL python run.py --encoder vitb --img-path assets/examples --outdir outputs_inference/vitb_518
conda run -n DL python run.py --encoder vitl --img-path assets/examples --outdir outputs_inference/vitl_518

conda run -n DL python run.py \
  --encoder vitl \
  --input-size 1036 \
  --img-path "$PACKAGE_DIR/scripts/resolution_examples.txt" \
  --outdir outputs_resolution/vitl_1036

conda run -n DL python run_video.py \
  --encoder vits \
  --video-path assets/examples_video \
  --outdir outputs_video/vits_518

cd "$PACKAGE_DIR"
conda run -n DL python scripts/make_inference_contact_sheet.py
conda run -n DL python scripts/make_resolution_contact_sheet.py

cd "$METRIC_DIR"

conda run -n DL python run.py \
  --encoder vitl \
  --load-from checkpoints/depth_anything_v2_metric_hypersim_vitl.pth \
  --max-depth 20 \
  --img-path ../assets/examples/demo10.jpg \
  --outdir outputs_metric/hypersim_vitl_demo \
  --save-numpy

conda run -n DL python run.py \
  --encoder vitl \
  --load-from checkpoints/depth_anything_v2_metric_vkitti_vitl.pth \
  --max-depth 80 \
  --img-path ../assets/examples/demo01.jpg \
  --outdir outputs_metric/vkitti_vitl_demo \
  --save-numpy

conda run -n DL python depth_to_pointcloud.py \
  --encoder vits \
  --load-from checkpoints/depth_anything_v2_metric_hypersim_vits.pth \
  --max-depth 20 \
  --img-path ../assets/examples/demo10.jpg \
  --outdir outputs_pointcloud/hypersim_vits_demo \
  --focal-length-x 470.4 \
  --focal-length-y 470.4
