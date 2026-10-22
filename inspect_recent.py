import os
from PIL import Image

dl_dir = r"C:\Users\SHREE RAM\Downloads"
recent_files = ["Image (5).jpg", "Image (6).jpg", "Image (7).jpg", "Image (8).jpg", "Image (9).jpg", "Image (10).jpg", "Media.jpg", "Media (1).jpg", "Image (1).jpg", "WhatsApp Image 2026-07-27 at 11.57.17 PM.jpeg"]

for f in recent_files:
    p = os.path.join(dl_dir, f)
    if os.path.exists(p):
        im = Image.open(p)
        tiny = im.resize((1, 1))
        mean_rgb = tiny.getpixel((0, 0))
        print(f"{f:35s}: size={im.size}, mean_rgb={mean_rgb}")
