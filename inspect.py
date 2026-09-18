import argparse
from pathlib import Path

import cv2


def classify_contour(area, perimeter):
    if perimeter == 0:
        return "unknown"
    circularity = 4 * 3.141592653589793 * area / (perimeter * perimeter)
    if circularity > 0.82:
        return "circle-like"
    if circularity > 0.55:
        return "rounded/irregular"
    return "angular"


def inspect_image(input_path, output_path=None):
    image = cv2.imread(str(input_path))
    if image is None:
        raise FileNotFoundError(f"Could not read image: {input_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 75, 150)

    contours, _ = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    findings = []
    annotated = image.copy()

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 100:
            continue

        perimeter = cv2.arcLength(contour, True)
        x, y, w, h = cv2.boundingRect(contour)
        shape = classify_contour(area, perimeter)

        findings.append({
            "area": round(area, 2),
            "perimeter": round(perimeter, 2),
            "bbox": [x, y, w, h],
            "shape": shape,
        })
        cv2.rectangle(annotated, (x, y), (x + w, y + h), (255, 255, 255), 2)

    findings.sort(key=lambda item: item["area"], reverse=True)

    if output_path:
        cv2.imwrite(str(output_path), annotated)

    return findings


def main():
    parser = argparse.ArgumentParser(description="Inspect contours in an image.")
    parser.add_argument("image", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    findings = inspect_image(args.image, args.output)
    for i, item in enumerate(findings, 1):
        print(f"#{i}: {item}")


if __name__ == "__main__":
    main()
