# Vision Inspector

Small computer-vision experiments for inspecting images with classical OpenCV techniques.

## Pipeline

```
image → grayscale → blur → Canny edges → contours → measurements
```

## Features

- Canny edge detection
- Contour extraction
- Bounding boxes
- Area and perimeter measurements
- Simple shape classification
- Optional annotated output image

The project focuses on understanding the image-processing pipeline before reaching for a deep-learning detector.

## Run

```bash
pip install -r requirements.txt
python inspect.py path/to/image.jpg --output annotated.jpg
```

## Scope

This is an experimental inspection tool, not a production object detector. It is intentionally based on deterministic classical CV operations so each stage can be inspected.
