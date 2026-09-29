from pathlib import Path

IMAGE_PATH = Path("images") / "kermet.png"
MAX_WIDTH = 900

STATE = {
    "mode": "rect",
    "drawing": False,
    "start": None,
    "cur": None,
    "selection": None,  
    "result": None,
}
