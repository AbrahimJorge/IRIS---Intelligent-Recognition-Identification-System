import cv2
import numpy as np

def build_results_panel(result, width=380, row_h=46):
    n = len(result["colors"])
    panel = np.full((row_h * n + 20, width, 3), 28, dtype=np.uint8)

    for i, c in enumerate(result["colors"]):
        y0 = 10 + i * row_h
        cv2.rectangle(panel, (10, y0), (56, y0 + row_h - 12), c["bgr"], -1)
        cv2.rectangle(panel, (10, y0), (56, y0 + row_h - 12), (90, 90, 90), 1)
        text = f'{c["label"]}  -  {c["pct"]:.1f}%'
        cv2.putText(
            panel, text, (66, y0 + (row_h - 12) // 2 + 6),
            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (235, 235, 235), 1, cv2.LINE_AA
        )

    return panel
