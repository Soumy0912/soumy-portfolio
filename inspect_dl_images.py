import os
from PIL import Image

download_dir = r"C:\Users\SHREE RAM\Downloads"
for f in sorted(os.listdir(download_dir)):
    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        p = os.path.join(download_dir, f)
        try:
            im = Image.open(p)
            print(f"{f:45s} : {im.size[0]}x{im.size[1]} ({im.format}, mode={im.mode})")
        except Exception as e:
            print(f"{f:45s} : Error {e}")
