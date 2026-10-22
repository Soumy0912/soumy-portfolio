import zipfile
import tempfile
import os
import shutil
import xml.etree.ElementTree as ET

def inject_fonts_from_reference(source_pptx, target_pptx, output_pptx):
    temp_dir = tempfile.mkdtemp()
    target_extract = os.path.join(temp_dir, "target")
    source_extract = os.path.join(temp_dir, "source")
    
    with zipfile.ZipFile(source_pptx, 'r') as z:
        z.extractall(source_extract)
    with zipfile.ZipFile(target_pptx, 'r') as z:
        z.extractall(target_extract)
        
    # Copy all ppt/fonts from source to target
    src_fonts_dir = os.path.join(source_extract, "ppt", "fonts")
    tgt_fonts_dir = os.path.join(target_extract, "ppt", "fonts")
    os.makedirs(tgt_fonts_dir, exist_ok=True)
    for f in os.listdir(src_fonts_dir):
        shutil.copy2(os.path.join(src_fonts_dir, f), os.path.join(tgt_fonts_dir, f))
    print(f"Copied {len(os.listdir(src_fonts_dir))} font files.")

    # Read source presentation.xml and presentation.xml.rels
    with open(os.path.join(source_extract, "ppt", "presentation.xml"), 'r', encoding='utf-8') as f:
        src_pres_xml = f.read()
    with open(os.path.join(source_extract, "ppt", "_rels", "presentation.xml.rels"), 'r', encoding='utf-8') as f:
        src_rels_xml = f.read()
        
    # Extract embeddedFontLst from source
    src_root = ET.fromstring(src_pres_xml)
    font_lst = src_root.find('{http://schemas.openxmlformats.org/presentationml/2006/main}embeddedFontLst')
    
    # Read target presentation.xml
    tgt_pres_path = os.path.join(target_extract, "ppt", "presentation.xml")
    with open(tgt_pres_path, 'r', encoding='utf-8') as f:
        tgt_pres_xml = f.read()
    tgt_root = ET.fromstring(tgt_pres_xml)
    
    # Remove existing embeddedFontLst in target if any
    existing_font_lst = tgt_root.find('{http://schemas.openxmlformats.org/presentationml/2006/main}embeddedFontLst')
    if existing_font_lst is not None:
        tgt_root.remove(existing_font_lst)
        
    # Append font_lst from source
    if font_lst is not None:
        tgt_root.append(font_lst)
        
    ET.register_namespace('p', 'http://schemas.openxmlformats.org/presentationml/2006/main')
    ET.register_namespace('a', 'http://schemas.openxmlformats.org/drawingml/2006/main')
    ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
    
    tree = ET.ElementTree(tgt_root)
    tree.write(tgt_pres_path, encoding='utf-8', xml_declaration=True)
    
    # Now merge font relationships into target presentation.xml.rels
    src_rels_root = ET.fromstring(src_rels_xml)
    tgt_rels_path = os.path.join(target_extract, "ppt", "_rels", "presentation.xml.rels")
    with open(tgt_rels_path, 'r', encoding='utf-8') as f:
        tgt_rels_xml = f.read()
    tgt_rels_root = ET.fromstring(tgt_rels_xml)
    
    # Collect existing relationship IDs
    existing_rids = {r.attrib.get('Id') for r in tgt_rels_root.iter('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship')}
    
    # Add font relationships from source
    for rel in src_rels_root.iter('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
        if 'font' in rel.attrib.get('Type', '').lower() or 'font' in rel.attrib.get('Target', '').lower():
            r_id = rel.attrib.get('Id')
            # If r_id already exists in target (e.g. for a slide), we can re-map or if target already used that rId
            tgt_rels_root.append(rel)
            print(f"Added font relationship {r_id} -> {rel.attrib.get('Target')}")
            
    ET.register_namespace('', 'http://schemas.openxmlformats.org/package/2006/relationships')
    tree_rels = ET.ElementTree(tgt_rels_root)
    tree_rels.write(tgt_rels_path, encoding='utf-8', xml_declaration=True)
    
    # Zip back into output_pptx
    with zipfile.ZipFile(output_pptx, 'w', zipfile.ZIP_DEFLATED) as z_out:
        for root_dir, dirs, files in os.walk(target_extract):
            for file in files:
                full_p = os.path.join(root_dir, file)
                rel_p = os.path.relpath(full_p, target_extract)
                z_out.write(full_p, rel_p)
                
    shutil.rmtree(temp_dir)
    print("Injected fonts successfully and created:", output_pptx)

inject_fonts_from_reference(
    r"C:\Users\SHREE RAM\Downloads\SOHAM DALAL PORTFOLIO 1.pptx",
    r"C:\Users\SHREE RAM\Downloads\SOUMY RAGHUVANSHI PORTFOLIO PRESENTATION.pptx",
    r"C:\Users\SHREE RAM\.gemini\antigravity\scratch\soumy-portfolio\test_font_inject.pptx"
)
