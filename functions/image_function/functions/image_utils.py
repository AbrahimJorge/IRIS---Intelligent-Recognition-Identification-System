import cv2
import numpy as np
from collections import Counter

def create_mask(mode, p0, p1, shape):
    h, w = shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)

    if mode == "rect":
        x0, x1 = sorted((int(p0[0]), int(p1[0])))
        y0, y1 = sorted((int(p0[1]), int(p1[1])))
        x0, x1 = max(0, x0), min(w - 1, x1)
        y0, y1 = max(0, y0), min(h - 1, y1)
        if x1 > x0 and y1 > y0:
            mask[y0:y1 + 1, x0:x1 + 1] = 255
    else:  
        cx, cy = int(p0[0]), int(p0[1])
        r = int(round(np.hypot(p1[0] - p0[0], p1[1] - p0[1])))
        if r > 0:
            cv2.circle(mask, (cx, cy), r, 255, thickness=-1)
    return mask

def analyze_region(img, mask, dataset, min_pixels=20):
    ys, xs = np.where(mask == 255)
    if len(xs) < min_pixels:
        return None

    pixels_bgr = img[ys, xs].astype(np.int32)
    pixels_rgb = pixels_bgr[:, ::-1]

    distances, indices = dataset.query(pixels_rgb)
    if indices is None:
        return None
        
    labels = dataset.names[indices]
    
    total = len(labels)
    counter = Counter(labels)

    colors = []
    for label, count in counter.most_common(5): 
        sel = labels == label
        mean_bgr = pixels_bgr[sel].mean(axis=0).astype(int)
        colors.append({
            "label": label,
            "count": int(count),
            "pct": count / total * 100.0,
            "bgr": (int(mean_bgr[0]), int(mean_bgr[1]), int(mean_bgr[2])),
        })

    return {"total": total, "colors": colors}
