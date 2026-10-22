import pptx
from pptx.util import Pt, Inches
from pptx.dml.color import RGBColor
import os
import shutil
import zipfile
import tempfile
import xml.etree.ElementTree as ET

TEMPLATE_PATH = r"C:\Users\SHREE RAM\Downloads\Green and Yellow Bold Playful Creative Portfolio Presentation.pptx"
REFERENCE_PATH = r"C:\Users\SHREE RAM\Downloads\SOHAM DALAL PORTFOLIO 1.pptx"
FINAL_OUTPUT_PATH = r"C:\Users\SHREE RAM\Downloads\SOUMY RAGHUVANSHI PORTFOLIO 1.pptx"
ALT_OUTPUT_PATH = r"C:\Users\SHREE RAM\Downloads\SOUMY RAGHUVANSHI PORTFOLIO PRESENTATION (Reference Typography).pptx"
LOCKED_PATH = r"C:\Users\SHREE RAM\Downloads\SOUMY RAGHUVANSHI PORTFOLIO PRESENTATION.pptx"
SCRATCH_OUTPUT_PATH = r"C:\Users\SHREE RAM\.gemini\antigravity\scratch\soumy-portfolio\SOUMY RAGHUVANSHI PORTFOLIO 1.pptx"

DL_DIR = r"C:\Users\SHREE RAM\Downloads"
ASSETS_DIR = r"C:\Users\SHREE RAM\.gemini\antigravity\scratch\soumy-portfolio\processed_assets"

# Reference Fonts exactly from SOHAM DALAL PORTFOLIO 1:
FONT_HEADLINE_BOLD = "Bebas Neue Bold"
FONT_HEADLINE_REG = "Bebas Neue"
FONT_SCRIPT = "Brittany"
FONT_BODY = "Poppins"

# Color Palette matching Green & Yellow template
COL_YELLOW = RGBColor(0xFF, 0xD2, 0x17)      # #FFD217
COL_GREEN = RGBColor(0x5B, 0x7E, 0x3C)       # #5B7E3C
COL_CREAM = RGBColor(0xFF, 0xFB, 0xE6)       # #FFFBE6
COL_DARK_GREEN = RGBColor(0x3B, 0x57, 0x24)  # #3B5724
COL_MUTED_GREEN = RGBColor(0x48, 0x67, 0x2C)

prs = pptx.Presentation(TEMPLATE_PATH)
print("Loaded Green & Yellow template:", len(prs.slides), "slides")

def update_text(shape, new_text, font_name, size_pt, color_rgb, bold=None):
    if not shape.has_text_frame:
        return
    tf = shape.text_frame
    tf.word_wrap = True
    lines = new_text.split('\n')
    
    p0 = tf.paragraphs[0]
    p0.text = lines[0]
    if p0.runs:
        r = p0.runs[0]
        r.font.name = font_name
        r.font.size = Pt(size_pt)
        r.font.color.rgb = color_rgb
        if bold is not None:
            r.font.bold = bold
            
    # Remove extra paragraphs if any originally existed beyond lines
    while len(tf.paragraphs) > 1:
        p_extra = tf.paragraphs[-1]
        p_extra._p.getparent().remove(p_extra._p)
        
    for line in lines[1:]:
        p = tf.add_paragraph()
        p.text = line
        if p.runs:
            r = p.runs[0]
            r.font.name = font_name
            r.font.size = Pt(size_pt)
            r.font.color.rgb = color_rgb
            if bold is not None:
                r.font.bold = bold

def add_nav_anchors(slide, page_num, col_text, col_accent):
    # Top-Left: SOUMY RAGHUVANSHI / creative portfolio
    tx_box = slide.shapes.add_textbox(Inches(1.12), Inches(0.65), Inches(5.0), Inches(0.45))
    tf = tx_box.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.text = "creative portfolio"
    if p.runs:
        p.runs[0].font.name = FONT_HEADLINE_BOLD
        p.runs[0].font.size = Pt(28)
        p.runs[0].font.color.rgb = col_text
        p.runs[0].font.bold = True
        
    # Top-Right: Page XX of 10
    tx_page = slide.shapes.add_textbox(Inches(16.5), Inches(0.65), Inches(2.4), Inches(0.45))
    tf_page = tx_page.text_frame
    tf_page.word_wrap = False
    p_page = tf_page.paragraphs[0]
    p_page.text = f"Page {page_num:02d} of 10"
    if p_page.runs:
        p_page.runs[0].font.name = FONT_BODY
        p_page.runs[0].font.size = Pt(18)
        p_page.runs[0].font.color.rgb = col_text

    # Bottom-Left: www.soumyraghuvanshi.dev
    tx_url = slide.shapes.add_textbox(Inches(1.12), Inches(10.2), Inches(5.0), Inches(0.4))
    tf_url = tx_url.text_frame
    tf_url.word_wrap = False
    p_url = tf_url.paragraphs[0]
    p_url.text = "www.soumyraghuvanshi.dev"
    if p_url.runs:
        p_url.runs[0].font.name = FONT_BODY
        p_url.runs[0].font.size = Pt(18)
        p_url.runs[0].font.color.rgb = col_text

def replace_group_pic_blob(group_shape, slide, img_path):
    with open(img_path, 'rb') as f:
        data = f.read()
    for sub in group_shape.shapes:
        if sub.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE:
            rId = sub._element.blipFill.blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
            part = slide.part.related_part(rId)
            part._blob = data
            print(f"Replaced image in {group_shape.name} with {os.path.basename(img_path)}")
            return True
    return False

# ==========================================================
# SLIDE 1: COVER
# ==========================================================
print("\n--- Styling Slide 1 ---")
s1 = prs.slides[0]
# Shape 1: 'portfolio' -> Bebas Neue Bold (205 pt, Yellow)
update_text(s1.shapes[1], "PORTFOLIO", FONT_HEADLINE_BOLD, 205, COL_YELLOW, bold=True)

# Group 4 subshape 1: 'creative' -> Brittany (140 pt, Green)
for sub in s1.shapes[2].shapes:
    if sub.has_text_frame:
        update_text(sub, "creative", FONT_SCRIPT, 140, COL_GREEN)

# Shape 3: 'Margarita Perez' -> 'BY SOUMY RAGHUVANSHI' in Bebas Neue Bold (52 pt)
update_text(s1.shapes[3], "BY SOUMY RAGHUVANSHI", FONT_HEADLINE_BOLD, 52, COL_GREEN, bold=True)

# Shape 4: Subtitle lines in Bebas Neue & Poppins
s1_sub = "UI/UX Portfolio & Engineering Architecture\nPresented to Dr. Deepti Barhate | NMIMS MPSTME 2026\nwww.soumyraghuvanshi.dev"
update_text(s1.shapes[4], s1_sub, FONT_BODY, 19, COL_GREEN)

# ==========================================================
# SLIDE 2: WELCOME / INTRO
# ==========================================================
print("\n--- Styling Slide 2 ---")
s2 = prs.slides[1]
# Shape 1: 'welcome to the presentation' -> Bebas Neue Bold (120 pt, Cream)
update_text(s2.shapes[1], "THE CREATIVE PRESENTATION", FONT_HEADLINE_BOLD, 100, COL_CREAM, bold=True)

# Shape 3 (Top text block): Statement of Intent -> Poppins (24 pt, Cream)
s2_top = "Showcase readiness not just as a full-stack engineer and machine learning builder, but as a disciplined creator who understands user journeys, visual balance, ergonomic system interfaces, and performance."
update_text(s2.shapes[3], s2_top, FONT_BODY, 22, COL_CREAM)

# Shape 2 (Bottom text block): Context -> Poppins (20 pt, Cream)
s2_bottom = "B.Tech Information Technology at NMIMS MPSTME. From architecting 20+ production REST APIs and predictive ML forecasting engines to competitive stage dance choreography and mountain expeditions, I explore every challenge with rhythm, discipline, and persistence."
update_text(s2.shapes[2], s2_bottom, FONT_BODY, 20, COL_CREAM)

# Picture -> Soumy Portrait
replace_group_pic_blob(s2.shapes[4], s2, os.path.join(DL_DIR, "Image (5).jpg"))
add_nav_anchors(s2, 2, COL_CREAM, COL_YELLOW)

# ==========================================================
# SLIDE 3: ABOUT ME / HELLO
# ==========================================================
print("\n--- Styling Slide 3 ---")
s3 = prs.slides[2]
# Shape 3: 'Hello' -> Bebas Neue Bold (140 pt, Yellow)
update_text(s3.shapes[3], "ABOUT ME", FONT_HEADLINE_BOLD, 130, COL_YELLOW, bold=True)

# Shape 4: 'i’m Margarita' -> 'introduce' in Brittany (110 pt, Green)
update_text(s3.shapes[4], "introduce", FONT_SCRIPT, 110, COL_GREEN)

# Shape 1 (Top text): Poppins (22 pt, Green)
s3_top = "A builder, engineer, and performer who believes technology is most transformative when driven by genuine curiosity."
update_text(s3.shapes[1], s3_top, FONT_BODY, 22, COL_GREEN, bold=True)

# Shape 2 (Narrative paragraph): Poppins (19 pt, Green)
s3_narrative = "Pursuing B.Tech in IT at NMIMS MPSTME Shirpur. Driven by scalable backend microservices, time-series predictive modeling, and clean UI/UX heuristics. Whether optimizing API response times or executing synchronized partner lifts with Dance Dukes crew, passion and precision drive everything I build."
update_text(s3.shapes[2], s3_narrative, FONT_BODY, 19, COL_GREEN)

# Picture -> Kalsubai Summit Photo
replace_group_pic_blob(s3.shapes[5], s3, os.path.join(DL_DIR, "Image (10).jpg"))
add_nav_anchors(s3, 3, COL_GREEN, COL_DARK_GREEN)

# ==========================================================
# SLIDE 4: FOUNDATION / 3 PILLARS
# ==========================================================
print("\n--- Styling Slide 4 ---")
s4 = prs.slides[3]
# Shape 1: 'education' -> Bebas Neue Bold (160 pt, Yellow)
update_text(s4.shapes[1], "FOUNDATION", FONT_HEADLINE_BOLD, 150, COL_YELLOW, bold=True)

# Column 1 (Left): NMIMS MPSTME
update_text(s4.shapes[2], "NMIMS MPSTME", FONT_HEADLINE_BOLD, 36, COL_GREEN, bold=True)
update_text(s4.shapes[3], "B.Tech Information Technology (2023–2027) at Shirpur Campus. Comprehensive engineering curriculum in Data Structures, OS, Computer Networks, and Distributed Systems.", FONT_BODY, 17, COL_GREEN)
replace_group_pic_blob(s4.shapes[8], s4, os.path.join(DL_DIR, "Image (9).jpg"))

# Column 2 (Middle): Innovation Sprints
update_text(s4.shapes[4], "INNOVATION SPRINTS", FONT_HEADLINE_BOLD, 36, COL_GREEN, bold=True)
update_text(s4.shapes[6], "NMIMS 24-Hour Innovation Hackathon & competitive hack sprints. Collaborative 36-hour rapid prototyping, software architecture pitching, and high-velocity delivery.", FONT_BODY, 17, COL_GREEN)
replace_group_pic_blob(s4.shapes[9], s4, os.path.join(ASSETS_DIR, "hackathon_stage.jpg"))

# Column 3 (Right): Dance Dukes Crew
update_text(s4.shapes[5], "DANCE DUKES CREW", FONT_HEADLINE_BOLD, 36, COL_GREEN, bold=True)
update_text(s4.shapes[7], "Core Dancer & Performer at NMIMS MPSTME. Demanding intense spatial awareness, split-second partner synchronization, stamina, and graceful composure under dynamic stage lights.", FONT_BODY, 17, COL_GREEN)
replace_group_pic_blob(s4.shapes[10], s4, os.path.join(DL_DIR, "Image (8).jpg"))
add_nav_anchors(s4, 4, COL_GREEN, COL_DARK_GREEN)

# ==========================================================
# SLIDE 5: UI/UX HEURISTICS
# ==========================================================
print("\n--- Styling Slide 5 ---")
s5 = prs.slides[4]
# Shape 1: 'Areas of' -> Bebas Neue Bold (130 pt, Cream)
update_text(s5.shapes[1], "AREAS OF", FONT_HEADLINE_BOLD, 120, COL_CREAM, bold=True)

# Shape 7: 'Expertise' -> 'Heuristics' in Brittany (110 pt, Green)
update_text(s5.shapes[7], "Heuristics", FONT_SCRIPT, 110, COL_GREEN)

# Shape 3: Heading 1 -> Bebas Neue Bold (32 pt, Cream)
update_text(s5.shapes[3], "COGNITIVE ERGONOMICS", FONT_HEADLINE_BOLD, 32, COL_CREAM, bold=True)
update_text(s5.shapes[6], "Applying Hick's Law and Miller's Rule to minimize choice paralysis across dashboards. Strict typographic scales in Space Grotesk ensure instantaneous visual hierarchy.", FONT_BODY, 18, COL_CREAM)

# Shape 2: Heading 2 -> Bebas Neue Bold (32 pt, Cream)
update_text(s5.shapes[2], "AFFORDANCE & FEEDBACK", FONT_HEADLINE_BOLD, 32, COL_CREAM, bold=True)
update_text(s5.shapes[4], "Fitts's Law applied to primary touch targets and CTA placements. Real-time feedback with pulsing live status indicators, clipboard toasts, and synthesized Web Audio cues.", FONT_BODY, 18, COL_CREAM)

# Shape 5 (Right Column summary): Poppins (18 pt, Cream)
update_text(s5.shapes[5], "Uniform 8pt bounding box grid, consistent card aspect ratios, accessible WCAG contrast, and semantic role tags creating a cohesive, delightful user experience.", FONT_BODY, 18, COL_CREAM)

replace_group_pic_blob(s5.shapes[8], s5, os.path.join(ASSETS_DIR, "ui_ux_heuristics.png"))
replace_group_pic_blob(s5.shapes[9], s5, os.path.join(ASSETS_DIR, "tech_badge.png"))
add_nav_anchors(s5, 5, COL_CREAM, COL_YELLOW)

# ==========================================================
# SLIDE 6: WORK EXPERIENCE
# ==========================================================
print("\n--- Styling Slide 6 ---")
s6 = prs.slides[5]
# Shape 8: 'experiance' -> Bebas Neue Bold (160 pt, Yellow)
update_text(s6.shapes[8], "EXPERIENCE", FONT_HEADLINE_BOLD, 150, COL_YELLOW, bold=True)

# Left Box (Salford & Co. -> Parkhya Solutions)
update_text(s6.shapes[5], "PARKHYA SOLUTIONS", FONT_HEADLINE_BOLD, 34, COL_YELLOW, bold=True)
update_text(s6.shapes[7], "MERN Stack Developer Intern (June–July 2026, Indore). Engineered scalable backend microservices and 20+ secure REST APIs. Integrated JWT authentication, RBAC authorization, and Cloudinary asset pipelines.", FONT_BODY, 18, COL_YELLOW)
replace_group_pic_blob(s6.shapes[3], s6, os.path.join(ASSETS_DIR, "hackathon_table.jpg"))

# Right Box (Studio Shodwe -> Payments & Systems)
update_text(s6.shapes[4], "PAYMENT & CLOUD PIPELINES", FONT_HEADLINE_BOLD, 34, COL_YELLOW, bold=True)
update_text(s6.shapes[6], "Architected Razorpay payment gateway webhook integration, automated transaction reconciliation, optimized MongoDB indexing, and established containerized microservice deployments.", FONT_BODY, 18, COL_YELLOW)
replace_group_pic_blob(s6.shapes[2], s6, os.path.join(ASSETS_DIR, "car_rental_architecture.png"))

replace_group_pic_blob(s6.shapes[1], s6, os.path.join(DL_DIR, "Image (5).jpg"))
add_nav_anchors(s6, 6, COL_YELLOW, COL_CREAM)

# ==========================================================
# SLIDE 7: PROJECT 1 - DEMAND FORECASTING AI
# ==========================================================
print("\n--- Styling Slide 7 ---")
s7 = prs.slides[6]
# Shape 1: 'project 1' -> Bebas Neue Bold (160 pt, Yellow)
update_text(s7.shapes[1], "PROJECT 1", FONT_HEADLINE_BOLD, 150, COL_YELLOW, bold=True)

# Shape 4: 'SALFORD & CO.' -> 'DEMAND FORECASTING AI'
update_text(s7.shapes[4], "DEMAND FORECASTING AI", FONT_HEADLINE_BOLD, 38, COL_YELLOW, bold=True)

# Descriptions in Poppins
s7_desc1 = "A predictive machine learning engine designed to eliminate perishable food waste and stockouts for food businesses. Evaluates historical sales against external factors: weather forecasts, temperature shifts, holidays, and weekly customer footfall."
update_text(s7.shapes[2], s7_desc1, FONT_BODY, 18, COL_YELLOW)

s7_desc2 = "Engineered using Python, Facebook Prophet, and XGBoost regression models with Pandas data pipelines. Achieved robust multi-horizon demand forecasting, mitigating perishable inventory shortages by over 30%."
update_text(s7.shapes[3], s7_desc2, FONT_BODY, 18, COL_YELLOW)

replace_group_pic_blob(s7.shapes[5], s7, os.path.join(ASSETS_DIR, "food_demand_ml.png"))
replace_group_pic_blob(s7.shapes[6], s7, os.path.join(ASSETS_DIR, "tech_badge.png"))
add_nav_anchors(s7, 7, COL_YELLOW, COL_CREAM)

# ==========================================================
# SLIDE 8: PROJECT 2 - CAR RENTAL BACKEND
# ==========================================================
print("\n--- Styling Slide 8 ---")
s8 = prs.slides[7]
# Shape 2: 'project 2' -> Bebas Neue Bold (160 pt, Cream)
update_text(s8.shapes[2], "PROJECT 2", FONT_HEADLINE_BOLD, 150, COL_CREAM, bold=True)

# Shape 3: Heading -> Bebas Neue Bold (36 pt, Cream)
update_text(s8.shapes[3], "CAR RENTAL BACKEND ENGINE", FONT_HEADLINE_BOLD, 36, COL_CREAM, bold=True)

# Description -> Poppins (18 pt, Cream)
s8_desc = "Full-featured RESTful backend architecture powering multi-tenant vehicle rentals. Features 20+ production endpoints, JWT authorization, RBAC role guard middleware, automated Cloudinary documentation transforms, and Razorpay webhook checkout flows."
update_text(s8.shapes[1], s8_desc, FONT_BODY, 18, COL_CREAM)

replace_group_pic_blob(s8.shapes[4], s8, os.path.join(ASSETS_DIR, "car_rental_architecture.png"))
replace_group_pic_blob(s8.shapes[5], s8, os.path.join(ASSETS_DIR, "hackathon_stage.jpg"))
replace_group_pic_blob(s8.shapes[6], s8, os.path.join(ASSETS_DIR, "hackathon_table.jpg"))
add_nav_anchors(s8, 8, COL_CREAM, COL_YELLOW)

# ==========================================================
# SLIDE 9: MOMENTS & DANCE DUKES
# ==========================================================
print("\n--- Styling Slide 9 ---")
s9 = prs.slides[8]
# Shape 3: 'project 3' -> 'MOMENTS' in Bebas Neue Bold (160 pt, Yellow)
update_text(s9.shapes[3], "MOMENTS", FONT_HEADLINE_BOLD, 150, COL_YELLOW, bold=True)

s9_dance = "DANCE DUKES CREW: Performer & Core Dancer at NMIMS MPSTME. High-energy stage drama, acrobatic partner lifts, and vibrant Gujarati folk & Garba routines. Building absolute spatial awareness, mutual trust, and precision under stadium concert lights."
update_text(s9.shapes[2], s9_dance, FONT_BODY, 18, COL_YELLOW)

s9_summit = "KALSUBAI SUMMIT EXPEDITION: Conquering Maharashtra's highest peak (1,646m / 5,400 ft) in the Sahyadris. Scaling midnight cliffside iron ladders and rocky ridges to catch the sunrise above the clouds — teaching grit, endurance, and quiet resilience."
update_text(s9.shapes[1], s9_summit, FONT_BODY, 18, COL_YELLOW)

replace_group_pic_blob(s9.shapes[4], s9, os.path.join(DL_DIR, "Image (6).jpg"))
replace_group_pic_blob(s9.shapes[5], s9, os.path.join(DL_DIR, "Image (7).jpg"))
replace_group_pic_blob(s9.shapes[6], s9, os.path.join(DL_DIR, "Image (8).jpg"))
add_nav_anchors(s9, 9, COL_YELLOW, COL_CREAM)

# ==========================================================
# SLIDE 10: CONNECT / LETS WORK TOGETHER
# ==========================================================
print("\n--- Styling Slide 10 ---")
s10 = prs.slides[9]
# Shape 1: 'lets work' -> Bebas Neue Bold (220 pt, Yellow)
update_text(s10.shapes[1], "LETS WORK", FONT_HEADLINE_BOLD, 220, COL_YELLOW, bold=True)

# Shape 5: 'together' -> Brittany (280 pt, Green)
update_text(s10.shapes[5], "together", FONT_SCRIPT, 280, COL_GREEN)

# Contact links in Poppins (24 pt, Yellow)
update_text(s10.shapes[2], "soumy.raghuvanshi@example.com", FONT_BODY, 24, COL_YELLOW, bold=True)
update_text(s10.shapes[3], "linkedin.com/in/soumy-raghuvanshi", FONT_BODY, 24, COL_YELLOW, bold=True)
update_text(s10.shapes[4], "+91 7247055152 · Indore & Shirpur", FONT_BODY, 24, COL_YELLOW, bold=True)

replace_group_pic_blob(s10.shapes[6], s10, os.path.join(DL_DIR, "Image (2).jpg"))
add_nav_anchors(s10, 10, COL_YELLOW, COL_GREEN)

# Save intermediate pptx
temp_pptx = r"C:\Users\SHREE RAM\.gemini\antigravity\scratch\soumy-portfolio\temp_styled.pptx"
prs.save(temp_pptx)
print("Saved intermediate styled PPTX to:", temp_pptx)

# Inject Embedded Fonts from Reference PPTX
def inject_fonts_from_reference(source_pptx, target_pptx, output_pptx):
    temp_dir = tempfile.mkdtemp()
    target_extract = os.path.join(temp_dir, "target")
    source_extract = os.path.join(temp_dir, "source")
    
    with zipfile.ZipFile(source_pptx, 'r') as z:
        z.extractall(source_extract)
    with zipfile.ZipFile(target_pptx, 'r') as z:
        z.extractall(target_extract)
        
    src_fonts_dir = os.path.join(source_extract, "ppt", "fonts")
    tgt_fonts_dir = os.path.join(target_extract, "ppt", "fonts")
    os.makedirs(tgt_fonts_dir, exist_ok=True)
    for f in os.listdir(src_fonts_dir):
        shutil.copy2(os.path.join(src_fonts_dir, f), os.path.join(tgt_fonts_dir, f))

    with open(os.path.join(source_extract, "ppt", "presentation.xml"), 'r', encoding='utf-8') as f:
        src_pres_xml = f.read()
    with open(os.path.join(source_extract, "ppt", "_rels", "presentation.xml.rels"), 'r', encoding='utf-8') as f:
        src_rels_xml = f.read()
        
    src_root = ET.fromstring(src_pres_xml)
    font_lst = src_root.find('{http://schemas.openxmlformats.org/presentationml/2006/main}embeddedFontLst')
    
    tgt_pres_path = os.path.join(target_extract, "ppt", "presentation.xml")
    with open(tgt_pres_path, 'r', encoding='utf-8') as f:
        tgt_pres_xml = f.read()
    tgt_root = ET.fromstring(tgt_pres_xml)
    
    existing_font_lst = tgt_root.find('{http://schemas.openxmlformats.org/presentationml/2006/main}embeddedFontLst')
    if existing_font_lst is not None:
        tgt_root.remove(existing_font_lst)
        
    if font_lst is not None:
        tgt_root.append(font_lst)
        
    ET.register_namespace('p', 'http://schemas.openxmlformats.org/presentationml/2006/main')
    ET.register_namespace('a', 'http://schemas.openxmlformats.org/drawingml/2006/main')
    ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
    
    tree = ET.ElementTree(tgt_root)
    tree.write(tgt_pres_path, encoding='utf-8', xml_declaration=True)
    
    src_rels_root = ET.fromstring(src_rels_xml)
    tgt_rels_path = os.path.join(target_extract, "ppt", "_rels", "presentation.xml.rels")
    with open(tgt_rels_path, 'r', encoding='utf-8') as f:
        tgt_rels_xml = f.read()
    tgt_rels_root = ET.fromstring(tgt_rels_xml)
    
    existing_rids = {r.attrib.get('Id') for r in tgt_rels_root.iter('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship')}
    
    for rel in src_rels_root.iter('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
        if 'font' in rel.attrib.get('Type', '').lower() or 'font' in rel.attrib.get('Target', '').lower():
            tgt_rels_root.append(rel)
            
    ET.register_namespace('', 'http://schemas.openxmlformats.org/package/2006/relationships')
    tree_rels = ET.ElementTree(tgt_rels_root)
    tree_rels.write(tgt_rels_path, encoding='utf-8', xml_declaration=True)
    
    with zipfile.ZipFile(output_pptx, 'w', zipfile.ZIP_DEFLATED) as z_out:
        for root_dir, dirs, files in os.walk(target_extract):
            for file in files:
                full_p = os.path.join(root_dir, file)
                rel_p = os.path.relpath(full_p, target_extract)
                z_out.write(full_p, rel_p)
                
    shutil.rmtree(temp_dir)
    print("Embedded fonts successfully into final presentation:", output_pptx)

inject_fonts_from_reference(REFERENCE_PATH, temp_pptx, FINAL_OUTPUT_PATH)
shutil.copy2(FINAL_OUTPUT_PATH, ALT_OUTPUT_PATH)
shutil.copy2(FINAL_OUTPUT_PATH, SCRATCH_OUTPUT_PATH)
try:
    shutil.copy2(FINAL_OUTPUT_PATH, LOCKED_PATH)
    print("Also updated locked path successfully!")
except Exception as e:
    print("Could not update locked path (likely open in PowerPoint):", e)

print("Updated destinations successfully:")
print("  -", FINAL_OUTPUT_PATH)
print("  -", ALT_OUTPUT_PATH)
print("  -", SCRATCH_OUTPUT_PATH)
