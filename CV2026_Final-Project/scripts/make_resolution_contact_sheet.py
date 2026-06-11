import os

import cv2
import numpy as np


PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.environ.get(
    "DEPTH_ANYTHING_REPO",
    os.path.join(PACKAGE_ROOT, "source_code", "Depth-Anything-V2"),
)
EXAMPLES = ["demo01", "demo05", "demo10", "demo15"]


def labeled_cell(label, image, width=420, height=280, label_height=36):
    image = cv2.resize(image, (width, height))
    canvas = np.full((height + label_height, width, 3), 255, np.uint8)
    canvas[label_height:] = image
    cv2.putText(canvas, label, (12, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (20, 20, 20), 2, cv2.LINE_AA)
    return canvas


def depth_part(output_path, raw_width):
    combined = cv2.imread(output_path)
    if combined is None:
        raise FileNotFoundError(output_path)
    return combined[:, raw_width + 50 :]


def main():
    out_dir = os.path.join(ROOT, "outputs_resolution")
    rows = []

    for example in EXAMPLES:
        raw_path = os.path.join(ROOT, "assets", "examples", f"{example}.jpg")
        raw = cv2.imread(raw_path)
        if raw is None:
            raise FileNotFoundError(raw_path)

        depth_518 = depth_part(os.path.join(ROOT, "outputs_inference", "vitl_518", f"{example}.png"), raw.shape[1])
        depth_1036 = depth_part(os.path.join(ROOT, "outputs_resolution", "vitl_1036", f"{example}.png"), raw.shape[1])

        row = cv2.hconcat([
            labeled_cell("Input", raw),
            labeled_cell("ViT-L 518", depth_518),
            labeled_cell("ViT-L 1036", depth_1036),
        ])
        rows.append(row)

    sheet = cv2.vconcat(rows)
    os.makedirs(out_dir, exist_ok=True)
    output_path = os.path.join(out_dir, "resolution_scaling_comparison.jpg")
    cv2.imwrite(output_path, sheet)
    print(output_path)


if __name__ == "__main__":
    main()
