# Environment

The experiments were executed locally on:

| Item | Value |
|---|---|
| GPU | NVIDIA GeForce RTX 3090 |
| VRAM | 24576 MiB |
| NVIDIA driver | 590.48.01 |
| Conda environment | `DL` |
| Python | 3.10.19 |
| PyTorch | 2.5.1 |
| Torchvision | 0.20.1 |
| PyTorch CUDA runtime | 12.1 |
| OpenCV | 4.13.0 |
| NumPy | 2.2.6 |
| Matplotlib | 3.10.8 |
| Open3D | 0.19.0 |
| xFormers | unavailable; official code used its standard attention fallback |

Official repository:

- URL: https://github.com/DepthAnything/Depth-Anything-V2
- Commit: `a561b849ebae10a6f5ef49e26c83cbbcd36c71bf`

The checkpoint files are intentionally not duplicated inside this package because they total several gigabytes. Their SHA-256 hashes are recorded in `checkpoint_manifest.sha256`. The DA-2K archive hash is recorded in `dataset_manifest.sha256`.
