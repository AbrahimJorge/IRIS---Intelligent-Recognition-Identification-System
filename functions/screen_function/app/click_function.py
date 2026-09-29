import tkinter as tk
from mss import mss
import numpy as np
import cv2
from pynput import mouse
from functions.screen_function.functions.shared_functions import analyze_region

class ClickMode:
    def __init__(self, root, shared_panel):
        self.root = root
        self.shared_panel = shared_panel
        self.active = False
        
        self.listener = mouse.Listener(on_click=self.on_global_click)

    def activate(self):
        self.active = True
        self.shared_panel.show()
        if not self.listener.is_alive():
            self.listener = mouse.Listener(on_click=self.on_global_click)
            self.listener.start()

    def deactivate(self):
        self.active = False
        self.shared_panel.hide()
        if self.listener.is_alive():
            self.listener.stop()

    def cleanup(self):
        self.deactivate()

    def on_global_click(self, x, y, button, pressed):
        if not self.active: return
            
        if button == mouse.Button.left:
            bx, by = self.root.winfo_rootx(), self.root.winfo_rooty()
            bw, bh = self.root.winfo_width(), self.root.winfo_height()
            px, py = self.shared_panel.panel.winfo_rootx(), self.shared_panel.panel.winfo_rooty()
            pw, ph = self.shared_panel.panel.winfo_width(), self.shared_panel.panel.winfo_height()
            
            ox, oy = -1000, -1000
            ow, oh = 0, 0
            if hasattr(self, 'options_win') and self.options_win.state() != 'withdrawn':
                ox, oy = self.options_win.winfo_rootx(), self.options_win.winfo_rooty()
                ow, oh = self.options_win.winfo_width(), self.options_win.winfo_height()
            
            if (bx <= x <= bx + bw and by <= y <= by + bh) or \
               (px <= x <= px + pw and py <= y <= py + ph) or \
               (ox <= x <= ox + ow and oy <= y <= oy + oh): 
                return

            if pressed:
                self.root.after(10, self.capture_and_analyze, int(x), int(y))

    def capture_and_analyze(self, x, y):
        region = {"top": y, "left": x, "width": 1, "height": 1}
        
        with mss() as sct:
            screenshot = sct.grab(region)
            img = np.array(screenshot)
            img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            result = analyze_region(img_bgr, min_pixels=1, top_n=1)
            
            if result:
                self.shared_panel.update_colors(result["colors"])
