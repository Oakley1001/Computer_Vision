# Inference 資料與重要數據說明

## 1. 屬於 Inference 的資料

以下資料都是使用官方預訓練模型直接進行推論，不包含重新訓練模型。

### Relative-depth 影像推論

位置：`figures/relative_depth/`

- 20 張官方測試影像
- ViT-S、ViT-B、ViT-L 三種模型的深度預測
- 用於觀察模型大小對深度邊界與細節的影響

### Resolution scaling

位置：`figures/resolution/`

- 比較 ViT-L 在輸入尺寸 518 與 1036 的結果
- 用於觀察提高測試解析度是否能改善細線、欄杆和物件邊界

### Metric-depth 推論

位置：

- `figures/metric_depth/`
- `raw_results/metric_depth/`

內容包含：

- Hypersim 室內 metric-depth 結果
- Virtual KITTI 2 室外 metric-depth 結果
- `.npy` 檔案保存每個 pixel 的原始公尺深度預測值

### Video inference

位置：

- `videos/`
- `figures/video/`

包含兩支官方影片的逐幀 relative-depth 推論，以及用於快速檢查結果的關鍵幀圖。

### Point-cloud inference

位置：

- `raw_results/pointcloud/demo10.ply`
- `figures/pointcloud/pointcloud_demo10_render.png`

使用 metric-depth 預測與 RGB 影像建立彩色 3D 點雲。

上述 inference 資料主要屬於**定性結果**，適合觀察：

- 物件邊界是否完整
- 欄杆、輪輻和枝葉等薄結構
- 透明與反射物體
- 不同模型大小的差異
- 不同輸入解析度的差異
- 模型對照片、線稿和繪畫的泛化能力

## 2. 最重要的定量數據：DA-2K

DA-2K 是本專案中最重要的實驗，因為它具有 ground-truth relative-depth point pairs，可以直接和論文結果比較。

| 模型 | 論文結果 | 本地結果 | 差異 |
|---|---:|---:|---:|
| ViT-S | 95.30% | 95.21% | -0.09 pp |
| ViT-B | 97.00% | 97.05% | +0.05 pp |
| ViT-L | 97.10% | 97.10% | 0.00 pp |

三種模型與論文 Table 3 的差異都在 0.1 個百分點內，因此可以視為成功重現論文結果。

這組數據應放在期末報告的主要實驗結果中。

相關檔案：

- `figures/comparisons/da2k_paper_vs_local_overall.png`
- `figures/comparisons/da2k_paper_vs_local_per_scenario.png`
- `raw_results/da2k_results.json`
- `logs/da2k_vits.log`
- `logs/da2k_vitb.log`
- `logs/da2k_vitl.log`

## 3. 次重要數據

### DA-2K 八種場景準確率

除了 overall accuracy，也可以比較以下八種場景：

- Indoor
- Outdoor
- Non-real
- Transparent
- Adverse
- Aerial
- Underwater
- Object

這些結果適合分析模型在不同影像類型與困難環境下的泛化能力。

### 模型大小與執行時間

| 模型 | 20 張影像完整執行時間 |
|---|---:|
| ViT-S | 8.30 秒 |
| ViT-B | 9.64 秒 |
| ViT-L | 14.57 秒 |

這些時間包含：

- Conda 啟動
- 載入 checkpoint
- 影像讀寫
- 模型 inference
- 深度圖可視化

因此不能直接與論文中的純 GPU latency 比較，只適合比較本地三種模型的完整執行成本。

### Resolution scaling

比較 ViT-L 在輸入尺寸 518 與 1036 的結果。

這項實驗沒有 ground truth，因此主要進行定性分析。可以觀察：

- 欄杆與細線是否更完整
- 物件邊界是否更清楚
- 室內結構是否更細緻
- 提高解析度所增加的運算成本

### Metric-depth 預測

| 設定 | 平均深度 | 中位數 | 預測範圍 |
|---|---:|---:|---:|
| Hypersim ViT-L 室內 | 3.6437 m | 3.7514 m | 0.8345–12.4208 m |
| VKITTI ViT-L 室外 | 34.3118 m | 33.7906 m | 4.9448–79.3470 m |

這些數值描述模型預測出的深度分布。由於測試圖沒有 ground-truth depth，因此不能將平均深度或預測範圍解讀為 accuracy。

## 4. 報告撰寫重點

期末報告應以 **DA-2K accuracy** 作為主要定量結果，因為它能直接對照論文。

其他 inference 結果則用來支持以下分析：

1. 模型大小對細節與執行時間的影響
2. 提高輸入解析度對預測銳利度的影響
3. 模型對照片、線稿、繪畫和透明物體的泛化能力
4. Relative depth、metric depth、影片和 3D 點雲等應用能力

簡單來說：

> DA-2K 是本專案最重要的定量實驗；其他 inference 圖像與影片則是定性結果，用來展示模型的細節、泛化能力與實際應用。
