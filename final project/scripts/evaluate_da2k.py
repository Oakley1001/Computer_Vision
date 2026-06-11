import argparse
import json
import os
import sys
from collections import defaultdict

import cv2
import torch


MODEL_CONFIGS = {
    "vits": {"encoder": "vits", "features": 64, "out_channels": [48, 96, 192, 384]},
    "vitb": {"encoder": "vitb", "features": 128, "out_channels": [96, 192, 384, 768]},
    "vitl": {"encoder": "vitl", "features": 256, "out_channels": [256, 512, 1024, 1024]},
}


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate Depth Anything V2 on DA-2K relative-depth pairs.")
    parser.add_argument("--repo", default="source_code/Depth-Anything-V2", help="Path to official Depth-Anything-V2 repo.")
    parser.add_argument("--da2k-root", default="source_code/Depth-Anything-V2/data/DA-2K/DA-2K", help="Path to extracted DA-2K folder.")
    parser.add_argument("--encoder", default="vits", choices=MODEL_CONFIGS.keys())
    parser.add_argument("--checkpoint", default=None, help="Checkpoint path. Defaults to repo/checkpoints/depth_anything_v2_<encoder>.pth")
    parser.add_argument("--input-size", type=int, default=518)
    parser.add_argument("--limit", type=int, default=0, help="Evaluate only first N annotated images. 0 means all.")
    parser.add_argument("--scene-type", default="", choices=["", "indoor", "outdoor", "non_real", "transparent_reflective", "adverse_style", "aerial", "underwater", "object"])
    return parser.parse_args()


def load_model(repo, encoder, checkpoint):
    sys.path.insert(0, os.path.abspath(repo))
    from depth_anything_v2.dpt import DepthAnythingV2

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = DepthAnythingV2(**MODEL_CONFIGS[encoder])
    if checkpoint is None:
        checkpoint = os.path.join(repo, "checkpoints", f"depth_anything_v2_{encoder}.pth")
    model.load_state_dict(torch.load(checkpoint, map_location="cpu"))
    return model.to(device).eval()


def scene_from_path(path):
    parts = path.split("/")
    return parts[1] if len(parts) > 1 and parts[0] == "images" else "unknown"


def main():
    args = parse_args()
    model = load_model(args.repo, args.encoder, args.checkpoint)

    annotation_path = os.path.join(args.da2k_root, "annotations.json")
    with open(annotation_path, "r") as f:
        annotations = json.load(f)

    rows = list(annotations.items())
    if args.scene_type:
        rows = [(p, pairs) for p, pairs in rows if f"/{args.scene_type}/" in p]
    if args.limit:
        rows = rows[: args.limit]

    total = 0
    correct = 0
    per_scene = defaultdict(lambda: [0, 0])

    for idx, (rel_image_path, pairs) in enumerate(rows, 1):
        image_path = os.path.join(args.da2k_root, rel_image_path)
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(image_path)

        pred = model.infer_image(image, args.input_size)
        scene = scene_from_path(rel_image_path)

        for pair in pairs:
            p1_h, p1_w = pair["point1"]
            p2_h, p2_w = pair["point2"]

            # Depth Anything V2's relative model predicts affine-invariant inverse depth:
            # larger response means closer to the camera.
            is_correct = pred[p1_h, p1_w] > pred[p2_h, p2_w]
            correct += int(is_correct)
            total += 1
            per_scene[scene][0] += int(is_correct)
            per_scene[scene][1] += 1

        if idx % 50 == 0:
            print(f"processed {idx}/{len(rows)} images, pairs={total}, acc={100 * correct / total:.2f}")

    print("\nDA-2K accuracy")
    print(f"encoder: {args.encoder}")
    print(f"images: {len(rows)}")
    print(f"pairs: {total}")
    print(f"mean: {100 * correct / total:.2f}")
    for scene in sorted(per_scene):
        s_correct, s_total = per_scene[scene]
        print(f"{scene}: {100 * s_correct / s_total:.2f} ({s_correct}/{s_total})")


if __name__ == "__main__":
    main()
