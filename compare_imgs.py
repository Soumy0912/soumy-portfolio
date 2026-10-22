from PIL import Image

def compare_tiny(p1, p2):
    im1 = Image.open(p1).resize((32, 32)).convert('RGB')
    im2 = Image.open(p2).resize((32, 32)).convert('RGB')
    diff = 0
    for i in range(32):
        for j in range(32):
            px1 = im1.getpixel((i, j))
            px2 = im2.getpixel((i, j))
            diff += sum(abs(a - b) for a, b in zip(px1, px2))
    return diff / (32 * 32 * 3)

assets = [
    r"C:\Users\SHREE RAM\.gemini\antigravity\scratch\soumy-portfolio\assets\dance-1.jpg",
    r"C:\Users\SHREE RAM\.gemini\antigravity\scratch\soumy-portfolio\assets\dance-2.jpg",
    r"C:\Users\SHREE RAM\.gemini\antigravity\scratch\soumy-portfolio\assets\dance-3.jpg"
]

dl_files = [f"Image ({i}).jpg" for i in range(5, 11)]

for a in assets:
    a_name = a.split('\\')[-1]
    print(f"\nComparing {a_name}:")
    for d in dl_files:
        p = f"C:\\Users\\SHREE RAM\\Downloads\\{d}"
        diff = compare_tiny(a, p)
        print(f"   with {d}: diff = {diff:.2f}")
