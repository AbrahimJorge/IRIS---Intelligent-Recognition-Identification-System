import tkinter as tk
from mss import mss
import numpy as np
import cv2
from pynput import mouse
from screeninfo import get_monitors
from functions.screen_function.functions.shared_functions import analyze_region

class CroppedMode:
    def __init__(self, root, shared_panel):
        self.root = root
        self.shared_panel = shared_panel
        self.active = False

        monitor = get_monitors()[0]
        self.sw = monitor.width
        self.sh = monitor.height

        self.overlay = tk.Toplevel(self.root)
        self.overlay.overrideredirect(True)
        self.overlay.attributes('-topmost', True)
        self.overlay.geometry(f"{self.sw}x{self.sh}+0+0")
        self.overlay.wm_attributes("-transparentcolor", "black")

        self.canvas = tk.Canvas(self.overlay, width=self.sw, height=self.sh, bg="black", highlightthickness=0)
        self.canvas.pack()
        self.rect_id = None 

        self.overlay.withdraw()

        self.mouse_start_x = 0
        self.mouse_start_y = 0
        self.mouse_cur_x = 0
        self.mouse_cur_y = 0
        self.is_drawing_rect = False

        self.listener = mouse.Listener(on_click=self.on_global_click, on_move=self.on_global_move)

    def activate(self):
        self.active = True
        self.shared_panel.show()
        self.overlay.deiconify()
        self.update_drawing_loop()
        if not self.listener.is_alive():
            self.listener = mouse.Listener(on_click=self.on_global_click, on_move=self.on_global_move)
            self.listener.start()

    def deactivate(self):
        self.active = False
        self.shared_panel.hide()
        self.overlay.withdraw()
        if self.rect_id is not None:
            self.canvas.delete(self.rect_id)
            self.rect_id = None
        
        if self.listener.is_alive():
            self.listener.stop()

    def cleanup(self):
        self.deactivate()
        self.overlay.destroy()

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
                self.mouse_start_x = int(x)
                self.mouse_start_y = int(y)
                self.mouse_cur_x = int(x)
                self.mouse_cur_y = int(y)
                self.is_drawing_rect = True
            else:
                self.is_drawing_rect = False
                end_x, end_y = int(x), int(y)
                x1, x2 = sorted([self.mouse_start_x, end_x])
                y1, y2 = sorted([self.mouse_start_y, end_y])
                w, h = x2 - x1, y2 - y1

                if self.rect_id is not None:
                    self.canvas.delete(self.rect_id)
                    self.rect_id = None
                    self.overlay.update() 

                if w > 5 and h > 5:
                    self.root.after(50, self.capture_and_analyze, x1, y1, w, h)

    def on_global_move(self, x, y):
        if self.is_drawing_rect and self.active:
            self.mouse_cur_x = int(x)
            self.mouse_cur_y = int(y)

    def update_drawing_loop(self):
        if not self.active: return

        if self.is_drawing_rect:
            if self.rect_id is None:
                self.rect_id = self.canvas.create_rectangle(
                    self.mouse_start_x, self.mouse_start_y, 
                    self.mouse_cur_x, self.mouse_cur_y, 
                    outline="#00FF00", width=2, dash=(4, 2)
                )
            else:
                self.canvas.coords(
                    self.rect_id, 
                    self.mouse_start_x, self.mouse_start_y, 
                    self.mouse_cur_x, self.mouse_cur_y
                )
        else:
            if self.rect_id is not None:
                self.canvas.delete(self.rect_id)
                self.rect_id = None
        
        self.root.after(16, self.update_drawing_loop)

    def capture_and_analyze(self, x, y, w, h):
        region = {"top": y, "left": x, "width": w, "height": h}
        
        with mss() as sct:
            screenshot = sct.grab(region)
            img = np.array(screenshot)
            img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            result = analyze_region(img_bgr, min_pixels=10, top_n=8)
            
            if result:
                self.shared_panel.update_colors(result["colors"])
