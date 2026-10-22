import pptx
from pptx.util import Pt, Inches
from pptx.dml.color import RGBColor
import os
import shutil

TEMPLATE_PATH = r"C:\Users\SHREE RAM\Downloads\Green and Yellow Bold Playful Creative Portfolio Presentation.pptx"
OUTPUT_PATH = r"C:\Users\SHREE RAM\Downloads\SOUMY RAGHUVANSHI PORTFOLIO PRESENTATION.pptx"
SCRATCH_OUTPUT = r"C:\Users\SHREE RAM\.gemini\antigravity\scratch\soumy-portfolio\SOUMY RAGHUVANSHI PORTFOLIO PRESENTATION.pptx"

DL_DIR = r"C:\Users\SHREE RAM\Downloads"
ASSETS_DIR = r"C:\Users\SHREE RAM\.gemini\antigravity\scratch\soumy-portfolio\processed_assets"

# Palette definitions matching Green & Yellow template
COL_YELLOW = RGBColor(0xFF, 0xD2, 0x17)  # #FFD217
COL_GREEN = RGBColor(0x5B, 0x7E, 0x3C)   # #5B7E3C
COL_CREAM = RGBColor(0xFF, 0xFB, 0xE6)   # #FFFBE6
COL_DARK_GREEN = RGBColor(0x3B, 0x57, 0x24)

prs = pptx.Presentation(TEMPLATE_PATH)
print("Loaded template presentation with", len(prs.slides), "slides")

def update_text(shape, new_text, font_name=None, size_pt=None, color_rgb=None, bold=None):
    if not shape.has_text_frame:
        return
    tf = shape.text_frame
    if not tf.paragraphs:
        return
    p0 = tf.paragraphs[0]
    # Record original formatting
    f_name = font_name or (p0.runs[0].font.name if p0.runs and p0.runs[0].font.name else None)
    f_size = Pt(size_pt) if size_pt else (p0.runs[0].font.size if p0.runs and p0.runs[0].font.size else None)
    f_col = color_rgb or (p0.runs[0].font.color.rgb if p0.runs and p0.runs[0].font.color and p0.runs[0].font.color.type == pptx.enum.dml.MSO_COLOR_TYPE.RGB else None)
    f_bold = bold if bold is not None else (p0.runs[0].font.bold if p0.runs else None)
    
    lines = new_text.split('\n')
    # Clear existing text
    p0.text = lines[0]
    if p0.runs:
        r = p0.runs[0]
        if f_name: r.font.name = f_name
        if f_size: r.font.size = f_size
        if f_col: r.font.color.rgb = f_col
        if f_bold is not None: r.font.bold = f_bold
        
    for line in lines[1:]:
        p = tf.add_paragraph()
        p.text = line
        if p.runs:
            r = p.runs[0]
            if f_name: r.font.name = f_name
            if f_size: r.font.size = f_size
            if f_col: r.font.color.rgb = f_col
            if f_bold is not None: r.font.bold = f_bold

def replace_group_pic_blob(group_shape, slide, img_path):
    with open(img_path, 'rb') as f:
        data = f.read()
    for sub in group_shape.shapes:
        if sub.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE:
            rId = sub._element.blipFill.blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
            part = slide.part.related_part(rId)
            part._blob = data
            print(f"Replaced image in {group_shape.name} -> {part.partname} with {os.path.basename(img_path)} ({len(data)} bytes)")
            return True
    return False

# ==========================================================
# SLIDE 1: COVER
# ==========================================================
print("\n--- Processing Slide 1 (Cover) ---")
s1 = prs.slides[0]
# Shape 1: 'portfolio' (Gulfs Display)
# Shape 3: 'Margarita Perez' -> 'Soumy Raghuvanshi'
update_text(s1.shapes[3], "Soumy Raghuvanshi", font_name="Signature", size_pt=145, color_rgb=COL_GREEN)
# Shape 4: Subtitle paragraph
s1_subtitle = "Full Stack Developer & AI Explorer · NMIMS MPSTME\nB.Tech Information Technology | UI/UX & Systems Architecture\nPresented to Dr. Deepti Barhate | Portfolio 2026"
update_text(s1.shapes[4], s1_subtitle, font_name="FF Providence Sans", size_pt=18, color_rgb=COL_GREEN)

# ==========================================================
# SLIDE 2: INTRODUCTION / WELCOME
# ==========================================================
print("\n--- Processing Slide 2 (Introduction) ---")
s2 = prs.slides[1]
# Shape 1: 'introduction'
update_text(s2.shapes[1], "welcome", font_name="Gulfs Display", size_pt=185, color_rgb=COL_CREAM)
# Shape 3 (Top text block): Statement of Intent
s2_top = "Showcase readiness not just as a full-stack engineer and machine learning builder, but as a disciplined creator who understands user journeys, visual balance, ergonomic system interfaces, and performance."
update_text(s2.shapes[3], s2_top, font_name="FF Providence Sans", size_pt=20, color_rgb=COL_CREAM)
# Shape 2 (Bottom text block): Context
s2_bottom = "B.Tech Information Technology at NMIMS MPSTME. From architecting 20+ production REST APIs and cloud-edge task offloading algorithms to trilingual civic accessibility and stage dance performance, I explore every challenge with rhythm, discipline, and persistence."
update_text(s2.shapes[2], s2_bottom, font_name="FF Providence Sans", size_pt=19, color_rgb=COL_CREAM)
# Shape 4 (Group 6): Picture 7 -> Soumy's Portrait
replace_group_pic_blob(s2.shapes[4], s2, os.path.join(DL_DIR, "Image (5).jpg"))

# ==========================================================
# SLIDE 3: ABOUT ME / HELLO I'M SOUMY
# ==========================================================
print("\n--- Processing Slide 3 (About Me) ---")
s3 = prs.slides[2]
# Shape 3: 'Hello'
# Shape 4: 'i’m Margarita' -> "i’m Soumy"
update_text(s3.shapes[4], "i’m Soumy", font_name="Signature", size_pt=156, color_rgb=COL_GREEN)
# Shape 1 (Top text):
s3_top = "A builder, engineer, and performer who believes technology is most transformative when driven by genuine curiosity."
update_text(s3.shapes[1], s3_top, font_name="FF Providence Sans", size_pt=20, color_rgb=COL_GREEN)
# Shape 2 (Narrative paragraph):
s3_narrative = "Pursuing B.Tech in IT at NMIMS MPSTME Shirpur. Driven by scalable backend microservices, time-series predictive modeling, and clean UI/UX heuristics. Whether optimizing API response times or executing synchronized partner lifts with Dance Dukes crew, passion and precision drive everything I build."
update_text(s3.shapes[2], s3_narrative, font_name="FF Providence Sans", size_pt=19, color_rgb=COL_GREEN)
# Shape 5 (Group 7): Picture 8 -> Kalsubai Summit Photo
replace_group_pic_blob(s3.shapes[5], s3, os.path.join(DL_DIR, "Image (10).jpg"))

# ==========================================================
# SLIDE 4: FOUNDATION / 3 PILLARS
# ==========================================================
print("\n--- Processing Slide 4 (Foundation & Pillars) ---")
s4 = prs.slides[3]
# Shape 1: 'education' -> 'foundation'
update_text(s4.shapes[1], "foundation", font_name="Gulfs Display", size_pt=185, color_rgb=COL_YELLOW)

# Column 1 (Left): Academic Rigor
update_text(s4.shapes[2], "NMIMS MPSTME", font_name="Signature", size_pt=34, color_rgb=COL_GREEN)
update_text(s4.shapes[3], "B.Tech Information Technology (2023–2027) at Shirpur Campus. Comprehensive coursework in Data Structures & Algorithms, OS, Computer Networks, and Distributed Computing.", font_name="FF Providence Sans", size_pt=17, color_rgb=COL_GREEN)
replace_group_pic_blob(s4.shapes[8], s4, os.path.join(DL_DIR, "Image (9).jpg"))

# Column 2 (Middle): Technical Sprints
update_text(s4.shapes[4], "Innovation Sprints", font_name="Signature", size_pt=34, color_rgb=COL_GREEN)
update_text(s4.shapes[6], "NMIMS 24-Hour Innovation Hackathon & competitive hack sprints. Collaborative 36-hour rapid prototyping, software architecture pitching, and high-velocity team delivery.", font_name="FF Providence Sans", size_pt=17, color_rgb=COL_GREEN)
replace_group_pic_blob(s4.shapes[9], s4, os.path.join(ASSETS_DIR, "hackathon_stage.jpg"))

# Column 3 (Right): Dance Discipline
update_text(s4.shapes[5], "Dance Dukes Crew", font_name="Signature", size_pt=34, color_rgb=COL_GREEN)
update_text(s4.shapes[7], "Core Dancer & Performer. Demanding intense spatial awareness, split-second partner synchronization, stamina, and graceful composure under dynamic stage concert lights.", font_name="FF Providence Sans", size_pt=17, color_rgb=COL_GREEN)
replace_group_pic_blob(s4.shapes[10], s4, os.path.join(DL_DIR, "Image (8).jpg"))

# ==========================================================
# SLIDE 5: UI/UX PRINCIPLES & HEURISTICS
# ==========================================================
print("\n--- Processing Slide 5 (UI/UX Principles) ---")
s5 = prs.slides[4]
# Shape 1: 'Areas of'
# Shape 7: 'Expertise' -> 'Heuristics'
update_text(s5.shapes[7], "Heuristics", font_name="Signature", size_pt=145, color_rgb=COL_GREEN)

# Shape 3: Heading 1
update_text(s5.shapes[3], "COGNITIVE ERGONOMICS", font_name="FF Providence Sans Bold", size_pt=26, color_rgb=COL_CREAM, bold=True)
update_text(s5.shapes[6], "Applying Hick's Law and Miller's Rule to minimize choice paralysis across dashboards. Strict typographic scales in Space Grotesk ensure instantaneous visual hierarchy.", font_name="FF Providence Sans", size_pt=18, color_rgb=COL_CREAM)

# Shape 2: Heading 2
update_text(s5.shapes[2], "AFFORDANCE & FEEDBACK", font_name="FF Providence Sans Bold", size_pt=26, color_rgb=COL_CREAM, bold=True)
update_text(s5.shapes[4], "Fitts's Law applied to primary touch targets and CTA placements. Real-time feedback with pulsing live status indicators, clipboard toasts, and synthesized Web Audio cues.", font_name="FF Providence Sans", size_pt=18, color_rgb=COL_CREAM)

# Shape 5 (Right Column summary):
update_text(s5.shapes[5], "Uniform 8pt bounding box grid, consistent card aspect ratios, accessible WCAG contrast, and semantic role tags creating a cohesive, delightful user experience.", font_name="FF Providence Sans", size_pt=18, color_rgb=COL_CREAM)

# Images: Group 10 (Large) -> ui_ux_heuristics.png; Group 12 (Small) -> tech_badge.png
replace_group_pic_blob(s5.shapes[8], s5, os.path.join(ASSETS_DIR, "ui_ux_heuristics.png"))
replace_group_pic_blob(s5.shapes[9], s5, os.path.join(ASSETS_DIR, "tech_badge.png"))

# ==========================================================
# SLIDE 6: WORK EXPERIENCE & INTERNSHIP
# ==========================================================
print("\n--- Processing Slide 6 (Experience) ---")
s6 = prs.slides[5]
# Shape 8: 'experiance' -> 'experience'
update_text(s6.shapes[8], "experience", font_name="Gulfs Display", size_pt=185, color_rgb=COL_YELLOW)

# Left Box (Salford & Co. -> Parkhya Solutions)
update_text(s6.shapes[5], "PARKHYA SOLUTIONS", font_name="FF Providence Sans Bold", size_pt=28, color_rgb=COL_YELLOW, bold=True)
update_text(s6.shapes[7], "MERN Stack Developer Intern (June–July 2026, Indore). Engineered scalable backend microservices and 20+ secure REST APIs. Integrated JWT authentication, RBAC authorization, and Cloudinary asset pipelines.", font_name="FF Providence Sans", size_pt=18, color_rgb=COL_YELLOW)
replace_group_pic_blob(s6.shapes[3], s6, os.path.join(ASSETS_DIR, "hackathon_table.jpg"))

# Right Box (Studio Shodwe -> Payments & Systems)
update_text(s6.shapes[4], "PAYMENT & CLOUD PIPELINES", font_name="FF Providence Sans Bold", size_pt=28, color_rgb=COL_YELLOW, bold=True)
update_text(s6.shapes[6], "Architected Razorpay payment gateway webhook integration, automated transaction reconciliation, optimized MongoDB indexing, and established containerized microservice deployments.", font_name="FF Providence Sans", size_pt=18, color_rgb=COL_YELLOW)
replace_group_pic_blob(s6.shapes[2], s6, os.path.join(ASSETS_DIR, "car_rental_architecture.png"))

# Center Image (Group 3) -> Developer portrait
replace_group_pic_blob(s6.shapes[1], s6, os.path.join(DL_DIR, "Image (5).jpg"))

# ==========================================================
# SLIDE 7: PROJECT 1 - DEMAND FORECASTING AI
# ==========================================================
print("\n--- Processing Slide 7 (Project 1) ---")
s7 = prs.slides[6]
# Shape 1: 'project 1'
# Shape 4: 'SALFORD & CO.' -> 'DEMAND FORECASTING AI'
update_text(s7.shapes[4], "DEMAND FORECASTING AI", font_name="FF Providence Sans Bold", size_pt=30, color_rgb=COL_YELLOW, bold=True)
# Shape 2: Description Left
s7_desc1 = "A predictive machine learning engine designed to eliminate perishable food waste and stockouts for food businesses. Evaluates historical sales against external factors: weather forecasts, temperature shifts, holidays, and weekly customer footfall."
update_text(s7.shapes[2], s7_desc1, font_name="FF Providence Sans", size_pt=18, color_rgb=COL_YELLOW)
# Shape 3: Description Right
s7_desc2 = "Engineered using Python, Facebook Prophet, and XGBoost regression models with Pandas data pipelines. Achieved robust multi-horizon demand forecasting, mitigating perishable inventory shortages by over 30%."
update_text(s7.shapes[3], s7_desc2, font_name="FF Providence Sans", size_pt=18, color_rgb=COL_YELLOW)
# Group 7 (Large image) -> food_demand_ml.png
replace_group_pic_blob(s7.shapes[5], s7, os.path.join(ASSETS_DIR, "food_demand_ml.png"))
# Group 9 (Badge) -> tech_badge.png
replace_group_pic_blob(s7.shapes[6], s7, os.path.join(ASSETS_DIR, "tech_badge.png"))

# ==========================================================
# SLIDE 8: PROJECT 2 - CAR RENTAL BACKEND
# ==========================================================
print("\n--- Processing Slide 8 (Project 2) ---")
s8 = prs.slides[7]
# Shape 2: 'project 2'
# Shape 3: 'THYNK UNLIMITED' -> 'CAR RENTAL BACKEND ENGINE'
update_text(s8.shapes[3], "CAR RENTAL BACKEND ENGINE", font_name="FF Providence Sans Bold", size_pt=28, color_rgb=COL_CREAM, bold=True)
# Shape 1: Description
s8_desc = "Full-featured RESTful backend architecture powering multi-tenant vehicle rentals. Features 20+ production endpoints, JWT authorization, RBAC role guard middleware, automated Cloudinary documentation transforms, and Razorpay webhook checkout flows."
update_text(s8.shapes[1], s8_desc, font_name="FF Providence Sans", size_pt=18, color_rgb=COL_CREAM)
# Group 6 (Left), Group 8 (Center), Group 10 (Right)
replace_group_pic_blob(s8.shapes[4], s8, os.path.join(ASSETS_DIR, "car_rental_architecture.png"))
replace_group_pic_blob(s8.shapes[5], s8, os.path.join(ASSETS_DIR, "hackathon_stage.jpg"))
replace_group_pic_blob(s8.shapes[6], s8, os.path.join(ASSETS_DIR, "hackathon_table.jpg"))

# ==========================================================
# SLIDE 9: MOMENTS & DANCE DUKES
# ==========================================================
print("\n--- Processing Slide 9 (Moments Beyond Code) ---")
s9 = prs.slides[8]
# Shape 3: 'project 3' -> 'moments'
update_text(s9.shapes[3], "moments", font_name="Gulfs Display", size_pt=185, color_rgb=COL_YELLOW)
# Shape 2 (Left text): Dance Dukes
s9_dance = "DANCE DUKES CREW: Performer & Core Dancer at NMIMS MPSTME. High-energy stage drama, acrobatic partner lifts, and vibrant Gujarati folk & Garba routines. Building absolute spatial awareness, mutual trust, and precision under stadium concert lights."
update_text(s9.shapes[2], s9_dance, font_name="FF Providence Sans", size_pt=18, color_rgb=COL_YELLOW)
# Shape 1 (Right text): Kalsubai Peak
s9_summit = "KALSUBAI SUMMIT EXPEDITION: Conquering Maharashtra's highest peak (1,646m / 5,400 ft) in the Sahyadris. Scaling midnight cliffside iron ladders and rocky ridges to catch the sunrise above the clouds — teaching grit, endurance, and quiet resilience."
update_text(s9.shapes[1], s9_summit, font_name="FF Providence Sans", size_pt=18, color_rgb=COL_YELLOW)
# Pictures:
# Group 6 -> Dance 1 (Stage Drama sash)
replace_group_pic_blob(s9.shapes[4], s9, os.path.join(DL_DIR, "Image (6).jpg"))
# Group 8 -> Dance 3 (Live Concert Synchrony)
replace_group_pic_blob(s9.shapes[5], s9, os.path.join(DL_DIR, "Image (7).jpg"))
# Group 10 -> Dance 2 (Acrobatic Lift)
replace_group_pic_blob(s9.shapes[6], s9, os.path.join(DL_DIR, "Image (8).jpg"))

# ==========================================================
# SLIDE 10: CONNECT / LETS WORK TOGETHER
# ==========================================================
print("\n--- Processing Slide 10 (Connect) ---")
s10 = prs.slides[9]
# Shape 1: 'lets work'
# Shape 5: 'together'
# Shape 2: Email
update_text(s10.shapes[2], "soumy.raghuvanshi@example.com", font_name="FF Providence Sans Bold", size_pt=22, color_rgb=COL_YELLOW, bold=True)
# Shape 3: LinkedIn / Web
update_text(s10.shapes[3], "linkedin.com/in/soumy-raghuvanshi", font_name="FF Providence Sans Bold", size_pt=22, color_rgb=COL_YELLOW, bold=True)
# Shape 4: Phone & Location
update_text(s10.shapes[4], "+91 7247055152 · Indore & Shirpur", font_name="FF Providence Sans Bold", size_pt=22, color_rgb=COL_YELLOW, bold=True)
# Group 8 (Picture 9) -> Soumy's Handwritten Signature!
replace_group_pic_blob(s10.shapes[6], s10, os.path.join(DL_DIR, "Image (2).jpg"))

# ==========================================================
# SAVE PRESENTATION
# ==========================================================
prs.save(OUTPUT_PATH)
prs.save(SCRATCH_OUTPUT)
print(f"\nSUCCESS! Presentation saved to:\n  {OUTPUT_PATH}\n  {SCRATCH_OUTPUT}")
