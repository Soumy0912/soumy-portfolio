import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile(r"C:\Users\SHREE RAM\Downloads\SOHAM DALAL PORTFOLIO 1.pptx", "r") as z:
    pres_xml = z.read("ppt/presentation.xml").decode("utf-8")
    rels_xml = z.read("ppt/_rels/presentation.xml.rels").decode("utf-8")
    
    print("=== SOHAM DALAL PRESENTATION.XML EMBEDDED FONTS ===")
    root = ET.fromstring(pres_xml)
    for elem in root.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}embeddedFont'):
        font_elem = elem.find('{http://schemas.openxmlformats.org/presentationml/2006/main}font')
        type_face = font_elem.attrib.get('typeface') if font_elem is not None else None
        print("Embedded font typeface:", type_face)
        for child in elem:
            print("   sub element:", child.tag, child.attrib)

print("\n=== SOHAM DALAL PRESENTATION.XML.RELS FONT RELATIONSHIPS ===")
root_rels = ET.fromstring(rels_xml)
for rel in root_rels.iter('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
    if 'font' in rel.attrib.get('Type', '').lower() or 'font' in rel.attrib.get('Target', '').lower():
        print("Rel:", rel.attrib)
