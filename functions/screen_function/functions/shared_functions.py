import pandas as pd
from collections import Counter
from database.github_database import ColorDataset

def analyze_region(img_bgr, min_pixels=1, top_n=1):
    pixels_bgr = img_bgr.reshape(-1, 3)
    
    if len(pixels_bgr) < min_pixels: return None

    pixels_rgb = pixels_bgr[:, ::-1] 

    dataset = ColorDataset()
    if not dataset.is_loaded:
        dataset.load()

    distances, indices = dataset.query(pixels_rgb)
    if indices is None:
        return None
        
    labels = dataset.names[indices]
    
    total = len(labels)
    counter = Counter(labels)

    colors = []
    for label, count in counter.most_common(top_n):
        sel = labels == label
        mean_bgr = pixels_bgr[sel].mean(axis=0).astype(int)
        
        colors.append({
            "label": label,
            "count": int(count),
            "pct": count / total * 100.0,
            "bgr": (int(mean_bgr[0]), int(mean_bgr[1]), int(mean_bgr[2])),
        })

    return {"total": total, "colors": colors}
