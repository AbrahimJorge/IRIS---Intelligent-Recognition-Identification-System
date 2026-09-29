import pandas as pd
from scipy.spatial import KDTree
import ssl

URL = "https://raw.githubusercontent.com/codebrainz/color-names/master/output/colors.csv"

class ColorDataset:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ColorDataset, cls).__new__(cls)
            cls._instance.tree = None
            cls._instance.names = None
            cls._instance.is_loaded = False
        return cls._instance

    def load(self):
        if self.is_loaded:
            return True
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            df = pd.read_csv(URL, names=['Name', 'Hex', 'R', 'G', 'B'])
            self.names = df['Name'].values
            self.tree = KDTree(df[['R', 'G', 'B']].values)
            self.is_loaded = True
            print("Dataset loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return False

    def get_closest_color_name(self, r, g, b):
        if not self.tree:
            return "Unknown"
        _, index = self.tree.query((r, g, b))
        return self.names[index]
    
    def query(self, pixels_rgb):
        if not self.tree:
            return None, None
        return self.tree.query(pixels_rgb)
