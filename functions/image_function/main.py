import cv2
import numpy as np
from tkinter import filedialog

from constants.image_constants import MAX_WIDTH
from database.github_database import ColorDataset
from functions.image_function.functions.image_utils import create_mask, analyze_region
from functions.image_function.app.result_panel import build_results_panel

class ImageAnalyzerApp:
    def __init__(self, root_tk):
        self.dataset = ColorDataset()
        self.root_tk = root_tk
        self.is_running = False
        self.window_name = "Color Analyzer (1=rect 2=circle l=clear q=quit)"
        
        self.img = None
        self.display = None
        
        self.state = {
            "mode": "rect",
            "drawing": False,
            "start": None,
            "cur": None,
            "selection": None,  
            "result": None,
        }

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        )
        return file_path

    def start(self):
        if self.is_running:
            return
            
        if not self.dataset.is_loaded:
            if not self.dataset.load():
                print("Error loading colors database.")
                return

        image_path = self.select_image()
        if not image_path:
            return

        self.img = cv2.imread(image_path)
        if self.img is None:
            print(f"Could not open image: {image_path}")
            return

        if MAX_WIDTH and self.img.shape[1] > MAX_WIDTH:
            scale = MAX_WIDTH / self.img.shape[1]
            self.img = cv2.resize(self.img, (MAX_WIDTH, int(self.img.shape[0] * scale)))

        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.on_mouse)
        
        self.is_running = True
        self.update_frame()

    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.state["drawing"] = True
            self.state["start"] = (x, y)
            self.state["cur"] = (x, y)
            self.state["selection"] = None
            
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.state["drawing"]:
                self.state["cur"] = (x, y)
                
        elif event == cv2.EVENT_LBUTTONUP:
            self.state["drawing"] = False
            self.state["cur"] = (x, y)
            self.state["selection"] = (self.state["mode"], self.state["start"], self.state["cur"])
            self.run_analysis()

    def run_analysis(self):
        if not self.state["selection"]:
            return
        
        mode, p0, p1 = self.state["selection"]
        mask = create_mask(mode, p0, p1, self.img.shape)
        result = analyze_region(self.img, mask, self.dataset)
        self.state["result"] = result
        
        if result is None:
            return
        
        panel = build_results_panel(result)
        cv2.imshow("Result", panel)

    def update_frame(self):
        if not self.is_running:
            return

        self.display = self.img.copy()
        active = None
        
        if self.state["drawing"] and self.state["start"] and self.state["cur"]:
            active = (self.state["mode"], self.state["start"], self.state["cur"])
        elif self.state["selection"]:
            active = self.state["selection"]

        if active:
            mode, p0, p1 = active
            if mode == "rect":
                cv2.rectangle(self.display, p0, p1, (95, 208, 95), 2)
            else:
                r = int(round(np.hypot(p1[0] - p0[0], p1[1] - p0[1])))
                cv2.circle(self.display, p0, r, (95, 208, 95), 2)

        cv2.imshow(self.window_name, self.display)
        
        key = cv2.waitKey(20) & 0xFF
        
        if key == ord('1'):
            self.state["mode"] = "rect"
        elif key == ord('2'):
            self.state["mode"] = "circle"
        elif key == ord('l'):
            self.state["selection"] = None
            self.state["result"] = None
            try:
                cv2.destroyWindow("Result")
            except:
                pass
        
        if key in (27, ord('q')) or cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE) < 1:
            self.stop()
            return
            
        if self.is_running:
            self.root_tk.after(20, self.update_frame)

    def stop(self):
        if not self.is_running:
            return
        self.is_running = False
        
        try:
            cv2.destroyWindow(self.window_name)
            cv2.destroyWindow("Result")
        except Exception:
            pass