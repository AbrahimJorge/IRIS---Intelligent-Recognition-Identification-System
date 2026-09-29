import tkinter as tk
from functions.screen_function.app.click_function import ClickMode
from functions.screen_function.app.cropped_function import CroppedMode
from functions.screen_function.app.result_panel import ResultPanel

class ScreenAnalyzerApp:
    def __init__(self, parent_tk):
        self.parent_tk = parent_tk
        self.is_running = False
        
        self.root = None
        self.options_win = None
        self.shared_panel = None
        self.click_mode = None
        self.cropped_mode = None
        
        self.is_menu_open = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.is_dragging_btn = False

    def start(self):
        if self.is_running:
            return
            
        self.is_running = True
        
        self.root = tk.Toplevel(self.parent_tk)
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.geometry("80x80+100+100") 
        self.root.configure(bg="#282828")

        self.shared_panel = ResultPanel(self.root)

        self.click_mode = ClickMode(self.root, self.shared_panel)
        self.cropped_mode = CroppedMode(self.root, self.shared_panel)

        self.btn_power = tk.Label(self.root, text="🎨\nON", bg="#333333", fg="white", 
                                  font=("Arial", 10, "bold"), cursor="hand2")
        self.btn_power.pack(fill=tk.BOTH, expand=True)

        self.btn_power.bind("<ButtonPress-1>", self.on_btn_press)
        self.btn_power.bind("<B1-Motion>", self.on_btn_drag)
        self.btn_power.bind("<ButtonRelease-1>", self.on_btn_release)
        self.btn_power.bind("<ButtonPress-3>", lambda e: self.stop())

        self.options_win = tk.Toplevel(self.root)
        self.options_win.overrideredirect(True)
        self.options_win.attributes('-topmost', True)
        self.options_win.configure(bg="magenta")
        self.options_win.wm_attributes("-transparentcolor", "magenta")
        self.options_win.withdraw()
        
        self.click_mode.options_win = self.options_win
        self.cropped_mode.options_win = self.options_win

        self.btn_click = tk.Button(self.options_win, text="Click", bg="#444444", fg="white",
                                   font=("Arial", 10, "bold"), cursor="hand2", command=self.activate_click)
        self.btn_click.place(x=0, y=0, width=80, height=80)

        self.btn_cropped = tk.Button(self.options_win, text="Cropped", bg="#444444", fg="white",
                                     font=("Arial", 10, "bold"), cursor="hand2", command=self.activate_cropped)
        self.btn_cropped.place(x=90, y=0, width=80, height=80)

    def update_options_position(self):
        if not self.root: return
        x = self.root.winfo_x() + self.root.winfo_width() + 10
        y = self.root.winfo_y()
        self.options_win.geometry(f"170x80+{x}+{y}")

    def on_btn_press(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.is_dragging_btn = False

    def on_btn_drag(self, event):
        delta_x = event.x - self.drag_start_x
        delta_y = event.y - self.drag_start_y
        x = self.root.winfo_x() + delta_x
        y = self.root.winfo_y() + delta_y
        self.root.geometry(f"+{x}+{y}")
        if self.is_menu_open:
            self.update_options_position()
        self.is_dragging_btn = True

    def on_btn_release(self, event):
        if not self.is_dragging_btn:
            self.toggle_menu()

    def toggle_menu(self):
        self.is_menu_open = not self.is_menu_open
        if self.is_menu_open:
            self.btn_power.config(bg="#d9534f")
            self.update_options_position()
            self.options_win.deiconify()
        else:
            self.btn_power.config(bg="#333333")
            self.options_win.withdraw()
            self.click_mode.deactivate()
            self.cropped_mode.deactivate()
            self.reset_buttons()

    def reset_buttons(self):
        self.btn_click.config(bg="#444444", text="Click")
        self.btn_cropped.config(bg="#444444", text="Cropped")

    def activate_click(self):
        self.reset_buttons()
        self.btn_click.config(bg="#5cb85c", text="ACTIVE")
        self.cropped_mode.deactivate()
        self.click_mode.activate()

    def activate_cropped(self):
        self.reset_buttons()
        self.btn_cropped.config(bg="#5cb85c", text="ACTIVE")
        self.click_mode.deactivate()
        self.cropped_mode.activate()

    def stop(self):
        if not self.is_running:
            return
        self.is_running = False
        self.is_menu_open = False
        
        if self.click_mode:
            self.click_mode.cleanup()
        if self.cropped_mode:
            self.cropped_mode.cleanup()
        if self.shared_panel:
            self.shared_panel.destroy()
        if self.options_win:
            self.options_win.destroy()
        if self.root:
            self.root.destroy()
