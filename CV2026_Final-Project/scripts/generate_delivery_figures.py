import json
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
import open3d as o3d


PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.join(PROJECT, "source_code", "Depth-Anything-V2")
OUT = os.path.join(PROJECT, "delivery_generated_figures")


def ensure_out():
    os.makedirs(OUT, exist_ok=True)


def labeled(image, text, width, height, label_height=34):
    image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    canvas = np.full((height + label_height, width, 3), 255, dtype=np.uint8)
    canvas[label_height:] = image
    cv2.putText(canvas, text, (10, 23), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (20, 20, 20), 2, cv2.LINE_AA)
    return canvas


def crop_depth_from_combined(path, raw_width):
    combined = cv2.imread(path)
    if combined is None:
        raise FileNotFoundError(path)
    return combined[:, raw_width + 50 :]


def make_all_examples_overview():
    rows = []
    for row_idx in range(4):
        cells = []
        for col_idx in range(5):
            index = row_idx * 5 + col_idx + 1
            name = f"demo{index:02d}"
            raw_path = os.path.join(REPO, "assets", "examples", f"{name}.jpg")
            output_path = os.path.join(REPO, "outputs_inference", "vitl_518", f"{name}.png")
            raw = cv2.imread(raw_path)
            if raw is None:
                raise FileNotFoundError(raw_path)
            depth = crop_depth_from_combined(output_path, raw.shape[1])
            raw_small = cv2.resize(raw, (250, 145), interpolation=cv2.INTER_AREA)
            depth_small = cv2.resize(depth, (250, 145), interpolation=cv2.INTER_AREA)
            pair = cv2.vconcat([raw_small, depth_small])
            cells.append(labeled(pair, name, 250, 290))
        rows.append(cv2.hconcat(cells))
    overview = cv2.vconcat(rows)
    path = os.path.join(OUT, "all_20_examples_vitl_overview.jpg")
    cv2.imwrite(path, overview)
    return path


def make_da2k_charts():
    models = ["ViT-S", "ViT-B", "ViT-L"]
    paper = np.array([95.3, 97.0, 97.1])
    local = np.array([95.21, 97.05, 97.10])

    x = np.arange(len(models))
    width = 0.34
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x - width / 2, paper, width, label="Paper Table 3", color="#4878a8")
    ax.bar(x + width / 2, local, width, label="Local RTX 3090", color="#e27c43")
    ax.set_ylim(90, 100)
    ax.set_ylabel("DA-2K accuracy (%)")
    ax.set_xticks(x, models)
    ax.set_title("Depth Anything V2 DA-2K Reproduction")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    for xpos, value in zip(x - width / 2, paper):
        ax.text(xpos, value + 0.12, f"{value:.1f}", ha="center", fontsize=9)
    for xpos, value in zip(x + width / 2, local):
        ax.text(xpos, value + 0.12, f"{value:.2f}", ha="center", fontsize=9)
    fig.tight_layout()
    overall_path = os.path.join(OUT, "da2k_paper_vs_local_overall.png")
    fig.savefig(overall_path, dpi=180)
    plt.close(fig)

    scenarios = [
        "Indoor",
        "Outdoor",
        "Non-real",
        "Transparent",
        "Adverse",
        "Aerial",
        "Underwater",
        "Object",
    ]
    paper_scene = {
        "ViT-S": [92.9, 93.0, 98.4, 94.4, 95.7, 96.4, 99.2, 96.6],
        "ViT-B": [96.2, 94.8, 98.7, 96.3, 96.7, 99.0, 100.0, 97.3],
        "ViT-L": [96.4, 93.9, 99.0, 96.3, 97.3, 99.5, 99.2, 98.0],
    }
    local_scene = {
        "ViT-S": [92.62, 93.31, 98.35, 94.39, 95.12, 96.39, 99.15, 97.30],
        "ViT-B": [96.43, 94.77, 98.68, 96.26, 96.65, 99.48, 100.0, 97.30],
        "ViT-L": [96.19, 94.48, 99.01, 96.26, 97.26, 99.48, 99.15, 97.97],
    }

    fig, axes = plt.subplots(3, 1, figsize=(12, 12), sharex=True)
    sx = np.arange(len(scenarios))
    for ax, model in zip(axes, models):
        ax.plot(sx, paper_scene[model], marker="o", linewidth=2, label="Paper Appendix Table 14")
        ax.plot(sx, local_scene[model], marker="s", linewidth=2, label="Local")
        ax.set_ylim(89, 101)
        ax.set_ylabel("Accuracy (%)")
        ax.set_title(model)
        ax.grid(alpha=0.25)
        ax.legend(loc="lower right")
    axes[-1].set_xticks(sx, scenarios, rotation=20, ha="right")
    fig.suptitle("DA-2K Per-scenario Reproduction", fontsize=15)
    fig.tight_layout()
    scene_path = os.path.join(OUT, "da2k_paper_vs_local_per_scenario.png")
    fig.savefig(scene_path, dpi=180)
    plt.close(fig)

    result_json = {
        "overall": {"paper": dict(zip(models, paper.tolist())), "local": dict(zip(models, local.tolist()))},
        "per_scenario": {
            model: {
                scenario: {"paper": p, "local": l}
                for scenario, p, l in zip(scenarios, paper_scene[model], local_scene[model])
            }
            for model in models
        },
    }
    with open(os.path.join(OUT, "da2k_results.json"), "w") as f:
        json.dump(result_json, f, indent=2)
    return overall_path, scene_path


def make_metric_depth_comparison():
    cases = [
        (
            "Indoor / Hypersim ViT-L / max depth 20m",
            "demo10",
            os.path.join(REPO, "metric_depth", "outputs_metric", "hypersim_vitl_demo", "demo10.png"),
        ),
        (
            "Outdoor / VKITTI ViT-L / max depth 80m",
            "demo01",
            os.path.join(REPO, "metric_depth", "outputs_metric", "vkitti_vitl_demo", "demo01.png"),
        ),
    ]
    rows = []
    for title, name, metric_path in cases:
        raw_path = os.path.join(REPO, "assets", "examples", f"{name}.jpg")
        relative_path = os.path.join(REPO, "outputs_inference", "vitl_518", f"{name}.png")
        raw = cv2.imread(raw_path)
        if raw is None:
            raise FileNotFoundError(raw_path)
        relative = crop_depth_from_combined(relative_path, raw.shape[1])
        metric = crop_depth_from_combined(metric_path, raw.shape[1])
        rows.append(
            cv2.hconcat(
                [
                    labeled(raw, f"{title}: input", 420, 280),
                    labeled(relative, "Relative depth ViT-L", 420, 280),
                    labeled(metric, "Metric depth visualization", 420, 280),
                ]
            )
        )
    sheet = cv2.vconcat(rows)
    path = os.path.join(OUT, "metric_depth_comparison.jpg")
    cv2.imwrite(path, sheet)
    return path


def make_video_keyframes():
    video_dir = os.path.join(REPO, "outputs_video", "vits_518")
    rows = []
    for filename in ["ferris_wheel.mp4", "basketball.mp4"]:
        path = os.path.join(video_dir, filename)
        cap = cv2.VideoCapture(path)
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frames = []
        for ratio in [0.2, 0.5, 0.8]:
            frame_idx = max(0, min(total - 1, int(total * ratio)))
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ok, frame = cap.read()
            if not ok:
                raise RuntimeError(f"Cannot read frame {frame_idx} from {path}")
            frames.append(labeled(frame, f"{filename}: frame {frame_idx}", 520, 292))
        cap.release()
        rows.append(cv2.hconcat(frames))
    sheet = cv2.vconcat(rows)
    output = os.path.join(OUT, "video_inference_keyframes.jpg")
    cv2.imwrite(output, sheet)
    return output


def make_pointcloud_render():
    ply_path = os.path.join(
        REPO,
        "metric_depth",
        "outputs_pointcloud",
        "hypersim_vits_demo",
        "demo10.ply",
    )
    pcd = o3d.io.read_point_cloud(ply_path)
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    if len(points) > 90000:
        ids = np.linspace(0, len(points) - 1, 90000, dtype=np.int64)
        points = points[ids]
        colors = colors[ids]

    finite = np.isfinite(points).all(axis=1)
    points = points[finite]
    colors = colors[finite]
    center = np.median(points, axis=0)
    points = points - center
    distance = np.linalg.norm(points, axis=1)
    keep = distance < np.percentile(distance, 98)
    points = points[keep]
    colors = colors[keep]

    background = "#101417"
    colors = np.clip(colors * 1.35, 0, 1)
    fig = plt.figure(figsize=(12, 5), facecolor=background)
    views = [(18, -75, "Front-oblique view"), (28, 25, "Side-oblique view")]
    for index, (elev, azim, title) in enumerate(views, 1):
        ax = fig.add_subplot(1, 2, index, projection="3d")
        ax.set_facecolor(background)
        ax.scatter(points[:, 0], -points[:, 1], points[:, 2], c=colors, s=0.35, linewidths=0)
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(title, color="white")
        ax.set_axis_off()
        ax.set_box_aspect((1.3, 1.0, 0.8))
    fig.suptitle("Metric-depth Point Cloud (Hypersim ViT-S, demo10)", color="white")
    fig.tight_layout()
    path = os.path.join(OUT, "pointcloud_demo10_render.png")
    fig.savefig(path, dpi=180, facecolor=background)
    plt.close(fig)
    return path


def make_metric_statistics():
    files = {
        "Hypersim ViT-L demo10": os.path.join(
            REPO,
            "metric_depth",
            "outputs_metric",
            "hypersim_vitl_demo",
            "demo10_raw_depth_meter.npy",
        ),
        "VKITTI ViT-L demo01": os.path.join(
            REPO,
            "metric_depth",
            "outputs_metric",
            "vkitti_vitl_demo",
            "demo01_raw_depth_meter.npy",
        ),
    }
    stats = {}
    for name, path in files.items():
        depth = np.load(path)
        finite = depth[np.isfinite(depth)]
        stats[name] = {
            "shape": list(depth.shape),
            "min_m": float(finite.min()),
            "max_m": float(finite.max()),
            "mean_m": float(finite.mean()),
            "median_m": float(np.median(finite)),
            "p05_m": float(np.percentile(finite, 5)),
            "p95_m": float(np.percentile(finite, 95)),
        }
    with open(os.path.join(OUT, "metric_depth_statistics.json"), "w") as f:
        json.dump(stats, f, indent=2)
    return stats


def main():
    ensure_out()
    generated = [
        make_all_examples_overview(),
        *make_da2k_charts(),
        make_metric_depth_comparison(),
        make_video_keyframes(),
        make_pointcloud_render(),
    ]
    stats = make_metric_statistics()
    print("Generated:")
    for path in generated:
        print(path)
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
