import os
import datetime
from PIL import Image

dl_dir = r"C:\Users\SHREE RAM\Downloads"
imgs = [f for f in os.listdir(dl_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
for f in sorted(imgs):
    p = os.path.join(dl_dir, f)
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(p))
    im = Image.open(p)
    print(f"{f:35s} | {mtime.strftime('%Y-%m-%d %H:%M')} | {im.size} | {im.format}")
