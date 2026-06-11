# 實驗圖完整說明

本文件描述資料包中的每一組實驗圖。Relative-depth 模型輸出圖的格式均為「左側原圖 + 50 px 白色分隔 + 右側深度可視化」。深度圖使用 `Spectral_r` colormap，顏色用於呈現相對深度結構，不可直接解讀為公尺。

## 1. 論文結果對照與總覽

### `figures/comparisons/da2k_paper_vs_local_overall.png`

比較 Depth Anything V2 ViT-S、ViT-B、ViT-L 在 DA-2K 的論文 Table 3 accuracy 與本地 RTX 3090 結果。兩組柱狀圖幾乎重合，三模型差異皆在 0.1 個百分點內，顯示定量復現成功。

### `figures/comparisons/da2k_paper_vs_local_per_scenario.png`

分別呈現三種模型在 Indoor、Outdoor、Non-real、Transparent、Adverse、Aerial、Underwater、Object 八類場景的 accuracy。論文 Appendix Table 14 與本地曲線高度一致，可檢查 overall score 之外的場景泛化能力。

### `figures/comparisons/model_scale_comparison.jpg`

使用 `demo01`、`demo05`、`demo10`、`demo15` 比較同一輸入在 ViT-S、ViT-B、ViT-L 下的 relative-depth 結果。重點觀察道路物件、線稿、室內邊界和樓梯欄杆等薄結構隨模型尺度的變化。

### `figures/comparisons/resolution_scaling_comparison.jpg`

比較 ViT-L 在輸入尺寸 518 與 1036 的結果。對應論文 Appendix Figure 11 的 test-time resolution scaling 現象；1036 在局部邊界與細線結構通常較清楚。

### `figures/comparisons/metric_depth_comparison.jpg`

上排為室內 `demo10`，下排為室外 `demo01`。每排依序顯示輸入、ViT-L relative depth、ViT-L metric depth，說明 affine-invariant relative output 與公尺尺度 metric output 的用途差異。

### `figures/comparisons/all_20_examples_vitl_overview.jpg`

20 個官方範例的總覽，每格上半部是輸入，下半部是 ViT-L relative-depth 結果。此圖集中展示模型對照片、繪畫、線稿、透明反射物、細結構與不利光線的泛化。

## 2. Relative-depth 全部影像

每列四個連結依序為輸入、ViT-S、ViT-B、ViT-L。三個輸出使用相同輸入尺寸 518，因此每列的文字說明同時適用於三個模型，模型間可比較邊界完整度與細節。

| ID | 場景與觀察重點 | 輸入 | ViT-S | ViT-B | ViT-L |
|---|---|---|---|---|---|
| demo01 | 都市街景，包含車輛、行人、樹木與建築的多層前後關係；觀察道路遠近與物件遮擋。 | [input](figures/relative_depth/input/demo01.jpg) | [S](figures/relative_depth/vits_518/demo01.png) | [B](figures/relative_depth/vitb_518/demo01.png) | [L](figures/relative_depth/vitl_518/demo01.png) |
| demo02 | 向日葵田，花瓣、莖與大量重疊細線；觀察薄結構與密集前景。 | [input](figures/relative_depth/input/demo02.jpg) | [S](figures/relative_depth/vits_518/demo02.png) | [B](figures/relative_depth/vitb_518/demo02.png) | [L](figures/relative_depth/vitl_518/demo02.png) |
| demo03 | 風格化瓶罐靜物，缺少真實照片紋理；觀察 non-real image 的形狀與遮擋理解。 | [input](figures/relative_depth/input/demo03.jpg) | [S](figures/relative_depth/vits_518/demo03.png) | [B](figures/relative_depth/vitb_518/demo03.png) | [L](figures/relative_depth/vitl_518/demo03.png) |
| demo04 | 苔蘚上的透明反光玻璃球；觀察透明、反射表面和球體輪廓。 | [input](figures/relative_depth/input/demo04.jpg) | [S](figures/relative_depth/vits_518/demo04.png) | [B](figures/relative_depth/vitb_518/demo04.png) | [L](figures/relative_depth/vitl_518/demo04.png) |
| demo05 | 房間、床與櫃子的黑白線稿；觀察模型是否能在幾乎沒有色彩與材質時恢復空間。 | [input](figures/relative_depth/input/demo05.jpg) | [S](figures/relative_depth/vits_518/demo05.png) | [B](figures/relative_depth/vitb_518/demo05.png) | [L](figures/relative_depth/vitl_518/demo05.png) |
| demo06 | 鋼構橋梁，具有重複樑柱與大量細長構件；觀察幾何重複與薄結構。 | [input](figures/relative_depth/input/demo06.jpg) | [S](figures/relative_depth/vits_518/demo06.png) | [B](figures/relative_depth/vitb_518/demo06.png) | [L](figures/relative_depth/vitl_518/demo06.png) |
| demo07 | 籃球與籃框，包含網線和圓形球體；觀察細網線、物件邊界及前後關係。 | [input](figures/relative_depth/input/demo07.jpg) | [S](figures/relative_depth/vits_518/demo07.png) | [B](figures/relative_depth/vitb_518/demo07.png) | [L](figures/relative_depth/vitl_518/demo07.png) |
| demo08 | 腳踏車輪與密集輪輻；觀察極細線條是否保持完整且不與背景混合。 | [input](figures/relative_depth/input/demo08.jpg) | [S](figures/relative_depth/vits_518/demo08.png) | [B](figures/relative_depth/vitb_518/demo08.png) | [L](figures/relative_depth/vitl_518/demo08.png) |
| demo09 | 樹木、山景與天空的繪畫；觀察非真實風格下的遠近層次。 | [input](figures/relative_depth/input/demo09.jpg) | [S](figures/relative_depth/vits_518/demo09.png) | [B](figures/relative_depth/vitb_518/demo09.png) | [L](figures/relative_depth/vitl_518/demo09.png) |
| demo10 | 有窗戶、桌面與反射材質的室內空間；觀察房間幾何、桌緣和窗框。 | [input](figures/relative_depth/input/demo10.jpg) | [S](figures/relative_depth/vits_518/demo10.png) | [B](figures/relative_depth/vitb_518/demo10.png) | [L](figures/relative_depth/vitl_518/demo10.png) |
| demo11 | 多隻貓互相遮擋；觀察多物件分離、輪廓與相近深度。 | [input](figures/relative_depth/input/demo11.jpg) | [S](figures/relative_depth/vits_518/demo11.png) | [B](figures/relative_depth/vitb_518/demo11.png) | [L](figures/relative_depth/vitl_518/demo11.png) |
| demo12 | 花朵近拍，花瓣層層重疊且景深明顯；觀察局部曲面與細緻邊界。 | [input](figures/relative_depth/input/demo12.jpg) | [S](figures/relative_depth/vits_518/demo12.png) | [B](figures/relative_depth/vitb_518/demo12.png) | [L](figures/relative_depth/vitl_518/demo12.png) |
| demo13 | 展示櫃中的碗盤器物；觀察多個相似物件、層架與反射表面。 | [input](figures/relative_depth/input/demo13.jpg) | [S](figures/relative_depth/vits_518/demo13.png) | [B](figures/relative_depth/vitb_518/demo13.png) | [L](figures/relative_depth/vitl_518/demo13.png) |
| demo14 | 透明與反光玻璃瓶；觀察模型面對透明材質時是否仍能辨識瓶身與背景。 | [input](figures/relative_depth/input/demo14.jpg) | [S](figures/relative_depth/vits_518/demo14.png) | [B](figures/relative_depth/vitb_518/demo14.png) | [L](figures/relative_depth/vitl_518/demo14.png) |
| demo15 | 裝飾繁複的室內樓梯；觀察欄杆、階梯邊緣與深遠空間。 | [input](figures/relative_depth/input/demo15.jpg) | [S](figures/relative_depth/vits_518/demo15.png) | [B](figures/relative_depth/vitb_518/demo15.png) | [L](figures/relative_depth/vitl_518/demo15.png) |
| demo16 | 逆光街景與騎車人物；觀察 adverse lighting 下的主體、道路和背景分層。 | [input](figures/relative_depth/input/demo16.jpg) | [S](figures/relative_depth/vits_518/demo16.png) | [B](figures/relative_depth/vitb_518/demo16.png) | [L](figures/relative_depth/vitl_518/demo16.png) |
| demo17 | 單色水墨山水；觀察低紋理、非攝影影像中的山體與空間層次。 | [input](figures/relative_depth/input/demo17.jpg) | [S](figures/relative_depth/vits_518/demo17.png) | [B](figures/relative_depth/vitb_518/demo17.png) | [L](figures/relative_depth/vitl_518/demo17.png) |
| demo18 | 動物主題繪畫；觀察筆觸與非真實材質下的主體輪廓。 | [input](figures/relative_depth/input/demo18.jpg) | [S](figures/relative_depth/vits_518/demo18.png) | [B](figures/relative_depth/vitb_518/demo18.png) | [L](figures/relative_depth/vitl_518/demo18.png) |
| demo19 | 印象派風景畫；觀察模糊筆觸中的前景、中景與背景分離。 | [input](figures/relative_depth/input/demo19.jpg) | [S](figures/relative_depth/vits_518/demo19.png) | [B](figures/relative_depth/vitb_518/demo19.png) | [L](figures/relative_depth/vitl_518/demo19.png) |
| demo20 | 抽象或繪畫風格的人物群像；觀察不規則外觀下的人物分離與相對深度。 | [input](figures/relative_depth/input/demo20.jpg) | [S](figures/relative_depth/vits_518/demo20.png) | [B](figures/relative_depth/vitb_518/demo20.png) | [L](figures/relative_depth/vitl_518/demo20.png) |

## 3. Resolution scaling 全部影像

以下四張圖均為 ViT-L、輸入尺寸 1036 的完整輸出，可與同 ID 的 `figures/relative_depth/vitl_518/` 圖比較。

| 圖檔 | 說明 |
|---|---|
| [`demo01.png`](figures/resolution/vitl_1036/demo01.png) | 都市街景。觀察車輛、行人、樹枝與建築邊緣在提高解析度後的完整度。 |
| [`demo05.png`](figures/resolution/vitl_1036/demo05.png) | 室內線稿。觀察床架、櫃體與牆面線條是否更連續。 |
| [`demo10.png`](figures/resolution/vitl_1036/demo10.png) | 室內房間。觀察窗框、桌緣與細小物件的邊界。 |
| [`demo15.png`](figures/resolution/vitl_1036/demo15.png) | 樓梯場景。觀察欄杆與階梯等高頻薄結構。 |

## 4. Metric-depth 全部影像

### `figures/metric_depth/demo10.png`

Hypersim ViT-L 室內 metric-depth 結果，最大深度設定 20 m。左側為室內原圖，右側為公尺尺度深度的色彩可視化；原始每像素浮點公尺值保存在 `raw_results/metric_depth/demo10_raw_depth_meter.npy`。

### `figures/metric_depth/demo01.png`

Virtual KITTI 2 ViT-L 室外 metric-depth 結果，最大深度設定 80 m。左側為街景原圖，右側為 metric-depth 可視化；原始值保存在 `raw_results/metric_depth/demo01_raw_depth_meter.npy`。

## 5. Video 圖與影片

### `figures/video/video_inference_keyframes.jpg`

從 `ferris_wheel.mp4` 與 `basketball.mp4` 的輸出各取 20%、50%、80% 時間位置的三個 frame。每個 frame 左半是原始影片，右半是 ViT-S relative-depth，供快速檢查不同時間點均有有效輸出。

### `videos/ferris_wheel.mp4`

摩天輪場景的完整 inference 影片。重點是輪架與纜線等細長結構，以及天空背景和主體的分離。

### `videos/basketball.mp4`

籃球動態場景的完整 inference 影片。重點是人物、球、地面與背景的逐幀相對深度；本實驗沒有額外 temporal smoothing。

## 6. Point-cloud 圖

### `figures/pointcloud/pointcloud_demo10_render.png`

以 Hypersim ViT-S metric depth 和原圖 RGB 建立 `demo10` 彩色點雲的兩個斜視角預覽。圖中可見房間平面與桌面等 3D 結構；邊緣散點來自單張深度估計、遮擋邊界和相機內參近似。

完整可旋轉點雲是 `raw_results/pointcloud/demo10.ply`，可用 Open3D、CloudCompare 或 MeshLab 開啟。

