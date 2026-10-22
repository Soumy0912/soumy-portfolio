import zipfile
import tempfile
import os
import shutil
import xml.etree.ElementTree as ET

def inject_fonts_safe(source_pptx, target_pptx, output_pptx):
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
    
    # Copy all font files from source
    for f in os.listdir(src_fonts_dir):
        shutil.copy2(os.path.join(src_fonts_dir, f), os.path.join(tgt_fonts_dir, f))
    print(f"Copied {len(os.listdir(src_fonts_dir))} font files to target.")

    # Read source rels to map old rId to font target
    src_rels_path = os.path.join(source_extract, "ppt", "_rels", "presentation.xml.rels")
    with open(src_rels_path, 'r', encoding='utf-8') as f:
        src_rels_root = ET.fromstring(f.read())
        
    old_rid_to_target = {}
    for rel in src_rels_root:
        if 'font' in rel.attrib.get('Type', '').lower() or 'font' in rel.attrib.get('Target', '').lower():
            old_rid_to_target[rel.attrib.get('Id')] = rel.attrib.get('Target')
            
    # Read target rels to find existing rIds
    tgt_rels_path = os.path.join(target_extract, "ppt", "_rels", "presentation.xml.rels")
    with open(tgt_rels_path, 'r', encoding='utf-8') as f:
        tgt_rels_root = ET.fromstring(f.read())
        
    # Remove any existing font relationships in target
    to_remove = []
    for rel in tgt_rels_root:
        if 'font' in rel.attrib.get('Type', '').lower() or 'font' in rel.attrib.get('Target', '').lower():
            to_remove.append(rel)
    for r in to_remove:
        tgt_rels_root.remove(r)
        
    # Find max existing rId integer
    max_id = 0
    for rel in tgt_rels_root:
        rid_str = rel.attrib.get('Id', '')
        if rid_str.startswith('rId'):
            try:
                num = int(rid_str[3:])
                if num > max_id:
                    max_id = num
            except:
                pass
                
    start_id = max(max_id + 1, 50)
    print(f"Assigning new font rIds starting at rId{start_id}")
    
    old_rid_to_new_rid = {}
    rel_ns = 'http://schemas.openxmlformats.org/package/2006/relationships'
    font_type = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/font'
    
    for old_rid, target in old_rid_to_target.items():
        new_rid = f"rId{start_id}"
        start_id += 1
        old_rid_to_new_rid[old_rid] = new_rid
        
        # Add new Relationship element
        new_rel = ET.Element(f'{{{rel_ns}}}Relationship', {
            'Id': new_rid,
            'Type': font_type,
            'Target': target
        })
        tgt_rels_root.append(new_rel)
        print(f"Mapped {old_rid} -> {new_rid} ({target})")

    ET.register_namespace('', rel_ns)
    tree_rels = ET.ElementTree(tgt_rels_root)
    tree_rels.write(tgt_rels_path, encoding='utf-8', xml_declaration=True)
    
    # Now read source presentation.xml and update rIds in embeddedFontLst
    src_pres_path = os.path.join(source_extract, "ppt", "presentation.xml")
    with open(src_pres_path, 'r', encoding='utf-8') as f:
        src_pres_root = ET.fromstring(f.read())
        
    font_lst = src_pres_root.find('{http://schemas.openxmlformats.org/presentationml/2006/main}embeddedFontLst')
    
    # Update r:id attributes in font_lst
    r_ns_attr = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
    for elem in font_lst.iter():
        if r_ns_attr in elem.attrib:
            old_r = elem.attrib[r_ns_attr]
            if old_r in old_rid_to_new_rid:
                elem.attrib[r_ns_attr] = old_rid_to_new_rid[old_r]
                
    # Update target presentation.xml
    tgt_pres_path = os.path.join(target_extract, "ppt", "presentation.xml")
    with open(tgt_pres_path, 'r', encoding='utf-8') as f:
        tgt_pres_root = ET.fromstring(f.read())
        
    existing_lst = tgt_pres_root.find('{http://schemas.openxmlformats.org/presentationml/2006/main}embeddedFontLst')
    if existing_lst is not None:
        tgt_pres_root.remove(existing_lst)
    tgt_pres_root.append(font_lst)
    
    ET.register_namespace('p', 'http://schemas.openxmlformats.org/presentationml/2006/main')
    ET.register_namespace('a', 'http://schemas.openxmlformats.org/drawingml/2006/main')
    ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
    
    tree_pres = ET.ElementTree(tgt_pres_root)
    tree_pres.write(tgt_pres_path, encoding='utf-8', xml_declaration=True)
    
    # Repack zip
    with zipfile.ZipFile(output_pptx, 'w', zipfile.ZIP_DEFLATED) as z_out:
        for root_dir, dirs, files in os.walk(target_extract):
            for file in files:
                full_p = os.path.join(root_dir, file)
                rel_p = os.path.relpath(full_p, target_extract)
                z_out.write(full_p, rel_p)
                
    shutil.rmtree(temp_dir)
    print("Safe injection finished successfully:", output_pptx)

inject_fonts_safe(
    r"C:\Users\SHREE RAM\Downloads\SOHAM DALAL PORTFOLIO 1.pptx",
    r"C:\Users\SHREE RAM\.gemini\antigravity\scratch\soumy-portfolio\temp_styled.pptx",
    r"C:\Users\SHREE RAM\Downloads\SOUMY RAGHUVANSHI PORTFOLIO 1.pptx"
)
shutil.copy2(
    r"C:\Users\SHREE RAM\Downloads\SOUMY RAGHUVANSHI PORTFOLIO 1.pptx",
    r"C:\Users\SHREE RAM\Downloads\SOUMY RAGHUVANSHI PORTFOLIO PRESENTATION (Reference Typography).pptx"
)
shutil.copy2(
    r"C:\Users\SHREE RAM\Downloads\SOUMY RAGHUVANSHI PORTFOLIO 1.pptx",
    r"C:\Users\SHREE RAM\.gemini\antigravity\scratch\soumy-portfolio\SOUMY RAGHUVANSHI PORTFOLIO 1.pptx"
)
print("Copied to all output destinations!")
