# 完整實驗命令

以下命令記錄本次實驗的實際設定。資料包內已包含 `source_code/Depth-Anything-V2` source snapshot；執行前需依官方 README 將 checkpoint 與 DA-2K 放到對應目錄，其 hash 見 `config/`。

```bash
PROJECT=/path/to/DepthAnythingV2_nontraining_experiments_package
REPO=$PROJECT/source_code/Depth-Anything-V2
```

## DA-2K

```bash
cd "$PROJECT"
conda run -n DL python scripts/evaluate_da2k.py --encoder vits | tee logs/da2k_vits.log
conda run -n DL python scripts/evaluate_da2k.py --encoder vitb | tee logs/da2k_vitb.log
conda run -n DL python scripts/evaluate_da2k.py --encoder vitl | tee logs/da2k_vitl.log
```

共同參數：`--input-size 518`、完整 1033 張標註影像、2068 個 point pairs。

## 20 張 relative-depth images

```bash
cd "$REPO"
conda run -n DL python run.py --encoder vits --input-size 518 \
  --img-path assets/examples --outdir outputs_inference/vits_518
conda run -n DL python run.py --encoder vitb --input-size 518 \
  --img-path assets/examples --outdir outputs_inference/vitb_518
conda run -n DL python run.py --encoder vitl --input-size 518 \
  --img-path assets/examples --outdir outputs_inference/vitl_518
```

官方 `run.py` 預設會保存原圖、50 px 分隔與 colored depth；沒有使用 `--pred-only` 或 `--grayscale`。

## Resolution scaling

```bash
cd "$REPO"
conda run -n DL python run.py \
  --encoder vitl \
  --input-size 1036 \
  --img-path "$PROJECT/scripts/resolution_examples.txt" \
  --outdir outputs_resolution/vitl_1036
```

`resolution_examples.txt` 包含四個相對於 repository root 的路徑：`demo01.jpg`、`demo05.jpg`、`demo10.jpg`、`demo15.jpg`。

## Video inference

```bash
cd "$REPO"
conda run -n DL python run_video.py \
  --encoder vits \
  --input-size 518 \
  --video-path assets/examples_video \
  --outdir outputs_video/vits_518
```

## Indoor metric depth

```bash
cd "$REPO/metric_depth"
conda run -n DL python run.py \
  --encoder vitl \
  --load-from checkpoints/depth_anything_v2_metric_hypersim_vitl.pth \
  --max-depth 20 \
  --img-path ../assets/examples/demo10.jpg \
  --outdir outputs_metric/hypersim_vitl_demo \
  --save-numpy
```

## Outdoor metric depth

```bash
cd "$REPO/metric_depth"
conda run -n DL python run.py \
  --encoder vitl \
  --load-from checkpoints/depth_anything_v2_metric_vkitti_vitl.pth \
  --max-depth 80 \
  --img-path ../assets/examples/demo01.jpg \
  --outdir outputs_metric/vkitti_vitl_demo \
  --save-numpy
```

## Point cloud

```bash
cd "$REPO/metric_depth"
conda run -n DL python depth_to_pointcloud.py \
  --encoder vits \
  --load-from checkpoints/depth_anything_v2_metric_hypersim_vits.pth \
  --max-depth 20 \
  --img-path ../assets/examples/demo10.jpg \
  --outdir outputs_pointcloud/hypersim_vits_demo \
  --focal-length-x 470.4 \
  --focal-length-y 470.4
```

ViT-L point-cloud 嘗試因官方 script 採用原圖高度作為 inference size，在 RTX 3090 24 GB 發生 CUDA OOM；本資料包保存成功的 ViT-S 點雲。

## 製作報告圖

```bash
cd "$PROJECT"
conda run -n DL python scripts/make_inference_contact_sheet.py
conda run -n DL python scripts/make_resolution_contact_sheet.py
conda run -n DL python scripts/generate_delivery_figures.py
```

`scripts/run_all_nontraining_reproduction.sh` 保存上述主要流程的批次版本，會自動以資料包根目錄作為 `PROJECT_DIR`。
