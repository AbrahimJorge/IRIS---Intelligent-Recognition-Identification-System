import tkinter as tk
from tkinter import font as tkfont
from database.github_database import ColorDataset
from functions.camera_function.main import CameraAnalyzerApp as CameraApp
from functions.image_function.main import ImageAnalyzerApp as ImageApp
from functions.screen_function.main import ScreenAnalyzerApp as ScreenApp

class IRISApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IRIS")
        self.root.geometry("360x640")
        self.root.configure(bg="#1E1E1E")
        self.root.resizable(False, False)

        self.dataset = ColorDataset()
        self.dataset.load()
        
        self.camera_app = CameraApp(self.root)
        self.image_app = ImageApp(self.root)
        self.screen_app = ScreenApp(self.root)
        
        self.active_module = None
        
        self.setup_ui()
        
    def setup_ui(self):
        title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        self.title_lbl = tk.Label(self.root, text="IRIS", font=title_font, bg="#1E1E1E", fg="#FFFFFF")
        self.title_lbl.pack(pady=40)
        
        status_font = tkfont.Font(family="Helvetica", size=12)
        self.status_lbl = tk.Label(self.root, text="Select a feature", font=status_font, bg="#1E1E1E", fg="#AAAAAA")
        self.status_lbl.pack(pady=20)
        
        nav_frame = tk.Frame(self.root, bg="#2D2D2D")
        nav_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=0)
        
        btn_font = tkfont.Font(family="Helvetica", size=10, weight="bold")
        
        self.btn_camera = tk.Button(nav_frame, text="Camera", font=btn_font, bg="#333333", fg="white", 
                                    relief=tk.FLAT, command=self.toggle_camera)
        self.btn_camera.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=15)
        
        self.btn_image = tk.Button(nav_frame, text="Image", font=btn_font, bg="#333333", fg="white", 
                                   relief=tk.FLAT, command=self.toggle_image)
        self.btn_image.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=15)
        
        self.btn_screen = tk.Button(nav_frame, text="Screen", font=btn_font, bg="#333333", fg="white", 
                                    relief=tk.FLAT, command=self.toggle_screen)
        self.btn_screen.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=15)
        
    def reset_buttons(self):
        self.btn_camera.configure(bg="#333333")
        self.btn_image.configure(bg="#333333")
        self.btn_screen.configure(bg="#333333")

    def toggle_camera(self):
        if self.active_module == "camera":
            self.camera_app.stop()
            self.active_module = None
            self.reset_buttons()
            self.status_lbl.configure(text="Select a feature")
        else:
            self.stop_all()
            self.active_module = "camera"
            self.btn_camera.configure(bg="#4CAF50")
            self.status_lbl.configure(text="Camera Activated")
            self.camera_app.start()

    def toggle_image(self):
        if self.active_module == "image":
            self.image_app.stop()
            self.active_module = None
            self.reset_buttons()
            self.status_lbl.configure(text="Select a feature")
        else:
            self.stop_all()
            self.active_module = "image"
            self.btn_image.configure(bg="#4CAF50")
            self.status_lbl.configure(text="Image Activated")
            self.image_app.start()

            if not self.image_app.is_running:
                self.active_module = None
                self.reset_buttons()
                self.status_lbl.configure(text="Select a feature")

    def toggle_screen(self):
        if self.active_module == "screen":
            self.screen_app.stop()
            self.active_module = None
            self.reset_buttons()
            self.status_lbl.configure(text="Select a feature")
        else:
            self.stop_all()
            self.active_module = "screen"
            self.btn_screen.configure(bg="#4CAF50")
            self.status_lbl.configure(text="Screen Activated")
            self.screen_app.start()

    def stop_all(self):
        self.camera_app.stop()
        self.image_app.stop()
        self.screen_app.stop()
        self.reset_buttons()
        self.active_module = None

    def on_closing(self):
        self.stop_all()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = IRISApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
