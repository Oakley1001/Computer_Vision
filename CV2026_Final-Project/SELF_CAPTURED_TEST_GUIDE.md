# Self-captured Image Stress Test Guide

## Overview

本文件說明自行拍攝影像壓力測試實驗。此實驗使用在未受控制拍攝條件下蒐集的真實世界手機照片，評估 Depth Anything V2 的表現。不同於官方範例影像，這些影像主要用來測試模型面對實際真實世界挑戰時的穩健性。

## Motivation

Depth Anything V2 官方釋出的範例影像通常經過仔細挑選，且大多具有良好的光照條件。為了更完整地評估模型在真實世界中的適用性，我們額外蒐集了在多種挑戰條件下拍攝的手機照片。此壓力測試主要檢視模型在以下情況下的表現：

1. 光照條件不理想，例如低光源、強烈陽光與眩光
2. 相機與光照條件造成影像偽影，例如過曝、反射與鏡頭光斑
3. 場景中包含具挑戰性的表面，例如反射或透明材質
4. 深度範圍變化很大，例如從近距離物體到遠方戶外區域
5. 場景複雜度高，例如雜亂街景、繁忙都市環境與遮擋情況

## Test Cases by Category

### Category 1: Close-up Object-scale Scene

* **Images:** 近距離市場或物體尺度場景，包含前景物體與背景元素
* **Challenge:** 將近處物體與雜亂背景區域分離
* **Model Behavior:** 通常會將前景物體預測為較近，並將背景結構預測為較遠
* **Limitations:** 小型物體、雜亂元素與部分遮擋可能會降低局部深度準確性

### Category 2: Urban Street and Object-scale Scenes

* **Images:** 都市街道、建築物、車輛、巷弄與行人尺度環境
* **Challenge:** 透過透視、物體尺度與遮擋關係推論整體場景布局
* **Model Behavior:** 能捕捉消失方向、建築布局，以及前景與背景的排序
* **Limitations:** 細長結構、樹木、陰影與複雜遮擋可能會被過度平滑

### Category 3: Low-light and Long-range Night Scenes

* **Images:** 夜間城市景觀、遠方建築、天際線區域與人工光源
* **Challenge:** 夜間幾何線索較弱，且深度範圍非常大
* **Model Behavior:** 能產生大致由近到遠的場景結構
* **Limitations:** 遠方區域可能被壓縮到相近的深度範圍中，且紋理與邊界清晰度有限

### Category 4: Low-light Large-scale Outdoor Scenes

* **Images:** 低光源條件下的大尺度戶外場景，例如港口、郵輪甲板、海岸或開放戶外場景
* **Challenge:** 大面積黑暗區域具有弱紋理與有限視覺資訊
* **Model Behavior:** 能推論大致的前景與背景關係
* **Limitations:** 黑暗區域可能產生較平滑的深度圖，遠方背景細節也較不可靠

### Category 5: Strong Illumination, Glare, and Backlit Scenes

* **Images:** 強烈陽光、眩光、過曝區域、水面反射與逆光場景
* **Challenge:** 照明偽影可能與真實場景幾何產生衝突
* **Model Behavior:** 即使存在照明偽影，仍能捕捉主要場景布局
* **Limitations:** 亮區、陰影與反射可能被誤解為局部深度變化

### Category 6: Reflective, Transparent, and Through-window Scenes

* **Images:** 窗景、玻璃表面、反射場景與透窗影像
* **Challenge:** 反射與透明會混合來自不同深度的視覺資訊
* **Model Behavior:** 能產生視覺上合理的深度圖
* **Limitations:** 由於反射與玻璃本身具有歧義，實際物理表面的深度可能與預測結果不一致

### Category 7: Large-scale Outdoor and Distant Scenes

* **Images:** 海岸場景、港口景觀、船隻、遠方島嶼、海洋與地平線區域
* **Challenge:** 在非常大的距離範圍中呈現前景到背景的廣泛轉換
* **Model Behavior:** 能合理捕捉整體深度排序
* **Limitations:** 遠方區域通常相對平滑，細緻的遠距深度變化有限

## Key Observations

### Strengths

1. **Foreground-background Ordering:** 模型在多數範例中能可靠地區分近處與遠處區域。
2. **Global Scene Layout:** 模型能捕捉消失線、透視關係與主要場景結構。
3. **Semantic Understanding:** 模型能有效運用物體形狀、遮擋關係與尺度線索。
4. **Generalization:** 模型能在多樣化的真實世界手機影像中產生合理結果。

### Limitations

1. **Monocular Ambiguity:** 在缺乏額外幾何限制的情況下，模型無法完全解析真實深度。
2. **Low Texture and Blur:** 黑暗、平滑或弱紋理區域會降低局部深度可靠性。
3. **Illumination Artifacts:** 眩光、鏡頭光斑、過曝與強光會影響局部深度細節。
4. **Reflective and Transparent Surfaces:** 這些表面具有物理上的歧義，因此預測深度不一定符合真實幾何。
5. **Very Large Depth Ranges:** 遠方區域通常會被壓縮到相對一致的深度範圍。
6. **Thin Structures:** 電線桿、樹木、欄杆與其他細長結構仍然具有挑戰性。

## Interpretation

自行拍攝影像壓力測試顯示，**Depth Anything V2 在真實手機照片的整體場景理解上具有良好的泛化能力**。然而，這些結果應被解讀為：

* **Qualitative relative-depth estimates:** 定性的相對深度估計，而非定量的 3D 測量
* **Visually plausible predictions:** 基於模型學習到的語意先驗所產生的視覺合理預測
* **Foreground-background separation:** 適合用於前景與背景分離，以及整體場景布局理解
* **Metric 3D reconstruction:** 不適合用於反射或透明物體，以及遠距區域的精確 metric 3D 重建

## Experimental Setup

* **Camera:** 手機
* **Displayed Images:** 22 張自行拍攝照片
* **Model:** Depth Anything V2
* **Output:** 原始影像搭配彩色相對深度預測圖
* **Evaluation:** 定性視覺檢查
* **Ground-truth Depth:** 不提供

自行拍攝影像僅用於定性壓力測試。由於沒有 LiDAR、雙目立體視覺或 structure-from-motion 產生的真實深度標註，因此本實驗不使用數值深度誤差指標進行評估。相反地，我們主要關注預測深度圖是否能在真實世界手機攝影條件下，保留合理的前景—背景排序、整體場景布局與物體分離。

## Conclusion

自行拍攝影像壓力測試驗證了 Depth Anything V2 在開放世界應用中的**穩健性與實用性**，同時也確認了**單目深度估計的根本限制**。模型依賴學習到的語意先驗，因此能在多樣化場景中展現良好的泛化能力；然而，這仍無法完全克服單張影像深度預測中固有的幾何歧義。
