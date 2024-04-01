from pathlib import Path
import os

base = Path(__file__).resolve().parent.parent
print(os.path.join(base, 'templates'))
