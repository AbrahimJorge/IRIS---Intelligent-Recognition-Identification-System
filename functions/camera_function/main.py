import cv2
import numpy as np
import imutils
from database.github_database import ColorDataset
from constants.camera_constants import WINDOW_WIDTH, H_TOLERANCE, SV_TOLERANCE
from functions.camera_function.app.result_panel import ResultPanel

class CameraAnalyzerApp:
    def __init__(self, root_tk):
        self.dataset = ColorDataset()
        self.root_tk = root_tk
        self.panel_tk = None
        self.camera = None
        self.kernel = np.ones((9, 9), np.uint8)
        
        self.current_frame = None
        self.current_hsv = None
        self.lower_hsv_limit = None
        self.upper_hsv_limit = None
        
        self.is_running = False
        self.window_name = "RGB Frame - IRIS Camera"

    def mouse_click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.current_frame is not None and self.current_hsv is not None:
                b, g, r = int(self.current_frame[y, x][0]), int(self.current_frame[y, x][1]), int(self.current_frame[y, x][2])
                h, s, v = int(self.current_hsv[y, x][0]), int(self.current_hsv[y, x][1]), int(self.current_hsv[y, x][2])
                
                tracked_color_name = self.dataset.get_closest_color_name(r, g, b)
                tracked_bgr_color = (b, g, r)

                self.lower_hsv_limit = np.array([
                    max(0, h - H_TOLERANCE), 
                    max(50, s - SV_TOLERANCE), 
                    max(50, v - SV_TOLERANCE)
                ], dtype=np.uint8)
                
                self.upper_hsv_limit = np.array([
                    min(179, h + H_TOLERANCE), 
                    min(255, s + SV_TOLERANCE), 
                    min(255, v + SV_TOLERANCE)
                ], dtype=np.uint8)

                if self.panel_tk:
                    self.panel_tk.update_colors([{
                        "bgr": tracked_bgr_color, 
                        "label": tracked_color_name
                    }])
                    self.panel_tk.show()

    def start(self):
        if self.is_running:
            return
        
        if not self.dataset.is_loaded:
            if not self.dataset.load():
                print("Error loading colors database.")
                return

        self.panel_tk = ResultPanel(self.root_tk)
        self.camera = cv2.VideoCapture(0)
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.mouse_click)
        
        self.is_running = True
        self.update_frame()

    def update_frame(self):
        if not self.is_running:
            return

        ret, frame = self.camera.read()
        if ret:
            frame = imutils.resize(frame, width=WINDOW_WIDTH)
            self.current_frame = frame.copy()
            self.current_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            if self.lower_hsv_limit is not None and self.upper_hsv_limit is not None:
                mask = cv2.inRange(self.current_hsv, self.lower_hsv_limit, self.upper_hsv_limit)
                mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel)
                mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.kernel)
                _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

            cv2.imshow(self.window_name, frame)
            
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE) < 1:
            self.stop()
            return
            
        if self.is_running:
            self.root_tk.after(10, self.update_frame)

    def stop(self):
        if not self.is_running:
            return
        self.is_running = False
        
        if self.camera:
            self.camera.release()
            self.camera = None
            
        try:
            cv2.destroyWindow(self.window_name)
        except Exception:
            pass
            
        if self.panel_tk:
            self.panel_tk.destroy()
            self.panel_tk = None
