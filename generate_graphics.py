import os
from PIL import Image, ImageDraw, ImageFont

out_dir = r"C:\Users\SHREE RAM\.gemini\antigravity\scratch\soumy-portfolio\processed_assets"
os.makedirs(out_dir, exist_ok=True)

# Color Palette
BG_DARK = (15, 18, 14)
CARD_BG = (24, 30, 22)
BORDER_COL = (80, 110, 50)
GREEN_ACCENT = (91, 126, 60)
YELLOW_ACCENT = (255, 210, 23)
CREAM_TEXT = (255, 251, 230)
MUTED_TEXT = (180, 195, 170)
WHITE = (255, 255, 255)

def get_font(size, bold=False):
    # Try system fonts
    font_paths = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\calibrib.ttf" if bold else r"C:\Windows\Fonts\calibri.ttf"
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()

# 1. UI/UX Heuristics Graphic (Slide 5 large)
def make_ui_ux_graphic():
    w, h = 1400, 800
    im = Image.new('RGB', (w, h), BG_DARK)
    d = ImageDraw.Draw(im)
    
    # Outer frame
    d.rounded_rectangle([(30, 30), (w-30, h-30)], radius=24, fill=CARD_BG, outline=BORDER_COL, width=3)
    
    # Header Banner
    d.rounded_rectangle([(60, 60), (w-60, 150)], radius=16, fill=(35, 45, 30), outline=GREEN_ACCENT, width=2)
    d.text((90, 80), "UI / UX HEURISTICS & INTERACTION ARCHITECTURE", font=get_font(34, True), fill=YELLOW_ACCENT)
    d.text((90, 120), "Human-Centered Design Principles Applied to High-Performance Web Systems", font=get_font(20), fill=MUTED_TEXT)
    
    # 3 Columns
    col_w = (w - 180) // 3
    cards = [
        ("FITTS'S & HICK'S LAW", [
            ("Touch Targets", "48px ergonomic tap targets"),
            ("Choice Density", "Hierarchical menu filtering"),
            ("Nav Latency", "Zero-friction single-click routes"),
            ("Cognitive Load", "Chunked 3-part step forms")
        ], YELLOW_ACCENT),
        ("VISUAL HIERARCHY", [
            ("Display Scale", "Syne 800 for high impact"),
            ("Body Legibility", "Space Grotesk at 1.6 line-height"),
            ("Card Bounding", "Uniform aspect ratio grids"),
            ("Color Weight", "Strategic Green/Yellow focus")
        ], GREEN_ACCENT),
        ("AFFORDANCE & FEEDBACK", [
            ("Live Status", "Pulsing 2s green presence pill"),
            ("Toast Prompts", "Non-intrusive action feedback"),
            ("Web Audio", "Synthesized ambient feedback"),
            ("Modal Drawers", "Smooth cubic-bezier transitions")
        ], CREAM_TEXT)
    ]
    
    for i, (col_title, items, accent) in enumerate(cards):
        cx = 60 + i * (col_w + 30)
        cy = 180
        ch = h - 240
        d.rounded_rectangle([(cx, cy), (cx + col_w, cy + ch)], radius=18, fill=(28, 36, 26), outline=BORDER_COL, width=2)
        
        # Pill title
        d.rounded_rectangle([(cx + 20, cy + 20), (cx + col_w - 20, cy + 70)], radius=10, fill=(40, 52, 36))
        d.text((cx + 35, cy + 32), col_title, font=get_font(22, True), fill=accent)
        
        # Items
        for j, (lbl, desc) in enumerate(items):
            iy = cy + 95 + j * 110
            d.text((cx + 25, iy), f"• {lbl}", font=get_font(20, True), fill=WHITE)
            d.text((cx + 42, iy + 28), desc, font=get_font(18), fill=MUTED_TEXT)
            if j < len(items) - 1:
                d.line([(cx + 25, iy + 90), (cx + col_w - 25, iy + 90)], fill=(45, 58, 40), width=1)
                
    im.save(os.path.join(out_dir, "ui_ux_heuristics.png"), quality=95)
    print("Saved ui_ux_heuristics.png")

# 2. Food Demand ML Architecture (Slide 7)
def make_food_demand_graphic():
    w, h = 1200, 1000
    im = Image.new('RGB', (w, h), BG_DARK)
    d = ImageDraw.Draw(im)
    
    d.rounded_rectangle([(20, 20), (w-20, h-20)], radius=24, fill=CARD_BG, outline=BORDER_COL, width=3)
    
    # Title
    d.text((50, 50), "DEMAND FORECASTING ARCHITECTURE", font=get_font(36, True), fill=YELLOW_ACCENT)
    d.text((50, 100), "Time-Series Machine Learning Engine · Python | Prophet | XGBoost", font=get_font(22), fill=MUTED_TEXT)
    
    # Diagram Stages
    stages = [
        ("1. DATA INGESTION & CLEANING", "Restaurant sales history (CSV/SQL), POS registers, daily footfall records"),
        ("2. EXTERNAL FEATURE ENRICHMENT", "Real-time weather API, local temperature trends, holidays, weekend multipliers"),
        ("3. DUAL-MODEL FORECASTING PIPELINE", "Facebook Prophet (seasonality, holiday spikes) + XGBoost Regressor (residual regression)"),
        ("4. ACTIONABLE INVENTORY METRICS", "Automated reorder triggers, 30% reduction in food waste, eliminated stockouts")
    ]
    
    for i, (st, desc) in enumerate(stages):
        sy = 160 + i * 155
        d.rounded_rectangle([(50, sy), (w-50, sy + 125)], radius=16, fill=(32, 42, 30), outline=GREEN_ACCENT, width=2)
        # Badge
        d.rounded_rectangle([(70, sy + 18), (120, sy + 68)], radius=8, fill=YELLOW_ACCENT)
        d.text((88, sy + 25), str(i+1), font=get_font(30, True), fill=(20, 25, 15))
        d.text((140, sy + 25), st, font=get_font(24, True), fill=WHITE)
        d.text((140, sy + 65), desc, font=get_font(18), fill=MUTED_TEXT)
        
        if i < len(stages) - 1:
            # Arrow
            d.line([(w//2, sy + 125), (w//2, sy + 155)], fill=YELLOW_ACCENT, width=3)
            d.polygon([(w//2 - 8, sy + 148), (w//2 + 8, sy + 148), (w//2, sy + 155)], fill=YELLOW_ACCENT)
            
    # Model comparison summary box at bottom
    by = 800
    d.rounded_rectangle([(50, by), (w-50, by + 150)], radius=16, fill=(20, 26, 18), outline=BORDER_COL, width=2)
    d.text((80, by + 25), "MODEL PERFORMANCE METRICS", font=get_font(22, True), fill=YELLOW_ACCENT)
    d.text((80, by + 65), "• XGBoost RMSE: 12.4% vs 24.8% baseline", font=get_font(19), fill=WHITE)
    d.text((80, by + 100), "• Prophet Multi-Seasonality: Weekly + Annual Cyclical Fit", font=get_font(19), fill=MUTED_TEXT)
    d.text((650, by + 65), "• Target: Perishable Produce & Dairy Supply", font=get_font(19), fill=WHITE)
    d.text((650, by + 100), "• Deployment: FastAPI microservice wrapper", font=get_font(19), fill=MUTED_TEXT)

    im.save(os.path.join(out_dir, "food_demand_ml.png"), quality=95)
    print("Saved food_demand_ml.png")

# 3. Car Rental Backend Architecture (Slide 8)
def make_car_rental_graphic():
    w, h = 1000, 1000
    im = Image.new('RGB', (w, h), BG_DARK)
    d = ImageDraw.Draw(im)
    
    d.rounded_rectangle([(20, 20), (w-20, h-20)], radius=24, fill=CARD_BG, outline=BORDER_COL, width=3)
    
    d.text((50, 50), "CAR RENTAL BACKEND ENGINE", font=get_font(34, True), fill=YELLOW_ACCENT)
    d.text((50, 95), "Scalable RESTful API Architecture · Node.js | Express | MongoDB", font=get_font(20), fill=MUTED_TEXT)
    
    modules = [
        ("AUTHENTICATION & RBAC", "JWT Token generation, bcrypt password hashing, role guard middleware (Admin / Agent / User)", YELLOW_ACCENT),
        ("VEHICLE FLEET INVENTORY", "Real-time car availability indexing, booking slot lockouts, price tier calculations", GREEN_ACCENT),
        ("PAYMENTS & RAZORPAY", "Payment order creation, HMAC-SHA256 signature verification, webhook processing", YELLOW_ACCENT),
        ("CLOUDINARY ASSET PIPELINE", "Vehicle document scans, driver license validation, automated thumbnail transform", GREEN_ACCENT),
        ("20+ REST PRODUCTION APIS", "Thoroughly tested via Postman suites with high throughput and error handling", CREAM_TEXT)
    ]
    
    for i, (m_title, m_desc, acc) in enumerate(modules):
        my = 150 + i * 160
        d.rounded_rectangle([(50, my), (w-50, my + 135)], radius=16, fill=(30, 38, 28), outline=BORDER_COL, width=2)
        d.text((80, my + 25), m_title, font=get_font(22, True), fill=acc)
        d.text((80, my + 68), m_desc, font=get_font(17), fill=MUTED_TEXT)
        
    im.save(os.path.join(out_dir, "car_rental_architecture.png"), quality=95)
    print("Saved car_rental_architecture.png")

# 4. Tech Badges for Slide 5 & 7
def make_badges():
    # Slide 5 small badge
    im = Image.new('RGB', (600, 300), CARD_BG)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([(10, 10), (590, 290)], radius=18, fill=(30, 40, 28), outline=BORDER_COL, width=2)
    d.text((35, 35), "TECH STACK HIGHLIGHT", font=get_font(22, True), fill=YELLOW_ACCENT)
    d.text((35, 80), "• Full Stack: Node.js, Express, MongoDB", font=get_font(18), fill=WHITE)
    d.text((35, 120), "• Machine Learning: Python, Prophet, XGBoost", font=get_font(18), fill=MUTED_TEXT)
    d.text((35, 160), "• Analytics: Power BI, DAX, Power Query", font=get_font(18), fill=WHITE)
    d.text((35, 200), "• Cloud: Cloudinary, Razorpay, Firebase", font=get_font(18), fill=MUTED_TEXT)
    im.save(os.path.join(out_dir, "tech_badge.png"), quality=95)
    print("Saved tech_badge.png")

make_ui_ux_graphic()
make_food_demand_graphic()
make_car_rental_graphic()
make_badges()
