import os

import cv2
import numpy as np


PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.environ.get(
    "DEPTH_ANYTHING_REPO",
    os.path.join(PACKAGE_ROOT, "source_code", "Depth-Anything-V2"),
)
EXAMPLES = ["demo01", "demo05", "demo10", "demo15"]
MODELS = [("Small", "vits_518"), ("Base", "vitb_518"), ("Large", "vitl_518")]


def labeled_cell(label, image, width=360, height=240, label_height=36):
    image = cv2.resize(image, (width, height))
    canvas = np.full((height + label_height, width, 3), 255, np.uint8)
    canvas[label_height:] = image
    cv2.putText(canvas, label, (12, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (20, 20, 20), 2, cv2.LINE_AA)
    return canvas


def main():
    out_dir = os.path.join(ROOT, "outputs_inference")
    rows = []

    for example in EXAMPLES:
        raw_path = os.path.join(ROOT, "assets", "examples", f"{example}.jpg")
        raw = cv2.imread(raw_path)
        if raw is None:
            raise FileNotFoundError(raw_path)

        cells = [labeled_cell("Input", raw)]
        for label, folder in MODELS:
            output_path = os.path.join(out_dir, folder, f"{example}.png")
            combined = cv2.imread(output_path)
            if combined is None:
                raise FileNotFoundError(output_path)

            # run.py outputs [raw image | 50px white separator | depth visualization].
            depth = combined[:, raw.shape[1] + 50 :]
            cells.append(labeled_cell(label, depth))

        rows.append(cv2.hconcat(cells))

    sheet = cv2.vconcat(rows)
    os.makedirs(out_dir, exist_ok=True)
    output_path = os.path.join(out_dir, "model_scale_comparison.jpg")
    cv2.imwrite(output_path, sheet)
    print(output_path)


if __name__ == "__main__":
    main()
