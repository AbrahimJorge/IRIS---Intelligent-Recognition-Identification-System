import tkinter as tk

class ResultPanel:
    def __init__(self, root):
        self.root = root
        self.panel = tk.Toplevel(self.root)
        self.panel.overrideredirect(True)
        self.panel.attributes('-topmost', True)
        self.panel.geometry("300x50+200+100") 
        self.panel.configure(bg="#282828")
        
        self.panel_drag_x = 0
        self.panel_drag_y = 0
        self.panel.bind("<ButtonPress-1>", self.on_panel_press)
        self.panel.bind("<B1-Motion>", self.on_panel_drag)

        self.colors_frame = tk.Frame(self.panel, bg="#282828")
        self.colors_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.reset_empty()
        self.panel.withdraw()

    def on_panel_press(self, event):
        self.panel_drag_x = event.x
        self.panel_drag_y = event.y

    def on_panel_drag(self, event):
        delta_x = event.x - self.panel_drag_x
        delta_y = event.y - self.panel_drag_y
        x = self.panel.winfo_x() + delta_x
        y = self.panel.winfo_y() + delta_y
        self.panel.geometry(f"+{x}+{y}")

    def show(self):
        self.panel.deiconify()

    def hide(self):
        self.panel.withdraw()
        self.reset_empty()

    def reset_empty(self):
        for widget in self.colors_frame.winfo_children():
            widget.destroy()
        empty_lbl = tk.Label(self.colors_frame, text="Select an area...", 
                                  bg="#282828", fg="gray", font=("Arial", 11, "italic"))
        empty_lbl.pack(pady=10)
        
        px = self.panel.winfo_x()
        py = self.panel.winfo_y()

        if px <= 0 and py <= 0:
            px, py = 200, 100
        self.panel.geometry(f"300x50+{px}+{py}")

    def update_colors(self, colors):
        for widget in self.colors_frame.winfo_children():
            widget.destroy()

        for c in colors:
            b, g, r = c["bgr"]
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            
            row = tk.Frame(self.colors_frame, bg="#282828")
            row.pack(fill=tk.X, pady=3)
            
            color_box = tk.Label(row, bg=hex_color, width=4, height=1)
            color_box.pack(side=tk.LEFT, padx=(0, 10))
            
            if len(colors) == 1:
                text = f"{c['label']}"
            else:
                text = f"{c['label']} - {c['pct']:.1f}%"
                
            color_label = tk.Label(row, text=text, bg="#282828", fg="white", font=("Arial", 10, "bold"))
            color_label.pack(side=tk.LEFT)

        new_height = 20 + (len(colors) * 32)
        px = self.panel.winfo_x()
        py = self.panel.winfo_y()
        self.panel.geometry(f"300x{new_height}+{px}+{py}")

    def destroy(self):
        self.panel.destroy()
