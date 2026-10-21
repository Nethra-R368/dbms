import os
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def update_presentation():
    project_dir = os.path.dirname(__file__)
    uml_img = os.path.join(project_dir, "uml_diagram.png")
    schema_img = os.path.join(project_dir, "relational_schema.png")
    
    # We will update SmartHostel_Presentation (3).pptx and save clean final versions
    src_ppt = r"C:\Users\Nethra R\Downloads\SmartHostel_Presentation (3).pptx"
    if not os.path.exists(src_ppt):
        src_ppt = r"C:\Users\Nethra R\Downloads\SmartHostel_Presentation.pptx"

    prs = pptx.Presentation(src_ppt)
    blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[-1]

    # --- SLIDE: UML CLASS DIAGRAM ---
    slide_uml = prs.slides.add_slide(blank_layout)
    # Header box
    tb = slide_uml.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11), Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p_cat = tf.paragraphs[0]
    p_cat.text = "DATABASE DESIGN"
    p_cat.font.size = Pt(12)
    p_cat.font.bold = True
    p_cat.font.color.rgb = RGBColor(139, 92, 246)
    
    p_title = tf.add_paragraph()
    p_title.text = "UML Class Diagram — System Architecture & Multiplicities"
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(15, 23, 42)
    
    if os.path.exists(uml_img):
        slide_uml.shapes.add_picture(uml_img, Inches(0.8), Inches(1.3), width=Inches(11.7))

    # --- SLIDE: RELATIONAL SCHEMA ---
    slide_schema = prs.slides.add_slide(blank_layout)
    tb2 = slide_schema.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11), Inches(0.8))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2_cat = tf2.paragraphs[0]
    p2_cat.text = "DATABASE DESIGN"
    p2_cat.font.size = Pt(12)
    p2_cat.font.bold = True
    p2_cat.font.color.rgb = RGBColor(139, 92, 246)
    
    p2_title = tf2.add_paragraph()
    p2_title.text = "Relational Schema — 19 Core Tables & Referential Integrity"
    p2_title.font.size = Pt(22)
    p2_title.font.bold = True
    p2_title.font.color.rgb = RGBColor(15, 23, 42)

    if os.path.exists(schema_img):
        slide_schema.shapes.add_picture(schema_img, Inches(0.8), Inches(1.3), width=Inches(11.7))

    # --- SLIDE: ENTITY RELATIONSHIP (ER) MODELING ---
    slide_er = prs.slides.add_slide(blank_layout)
    tb_er = slide_er.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(6.5))
    tf_er = tb_er.text_frame
    tf_er.word_wrap = True

    p = tf_er.paragraphs[0]
    p.text = "DATABASE DESIGN & ENTITY RELATIONSHIP"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RGBColor(139, 92, 246)

    p = tf_er.add_paragraph()
    p.text = "Entity-Relationship (ER) Model — Entities, Attributes & Cardinalities"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = RGBColor(15, 23, 42)
    p.space_after = Pt(14)

    bullets_er = [
        ("Core Entities & Strong Types", "USERS, STUDENT, WARDEN, HOSTEL, ROOM, FEE_STRUCTURE, NOTICE, INVENTORY, MESS_MENU."),
        ("Weak & Temporal Junction Entities", "ROOM_ALLOCATION (associates Student to Room over time), STUDENT_FEE (instance bills), PAYMENT (settlement audit), INVENTORY_TRANSACTION (stock delta), ROOM_CHANGE_REQUEST."),
        ("Multiplicity & Participation", "• USERS to STUDENT / WARDEN: 1 : (0..1) optional total participation\n• HOSTEL to ROOM: 1 : N (mandatory existence)\n• STUDENT to ROOM_ALLOCATION: 1 : N (tracks residency history)\n• FEE_STRUCTURE to STUDENT_FEE: 1 : N rate billing\n• STUDENT_FEE to PAYMENT: 1 : N partial and full settlement logs"),
        ("Referential Integrity Rules", "• ON DELETE CASCADE: Purges child allocations, complaints, passes upon student exit.\n• ON DELETE SET NULL: Preserves historical records when wardens depart.\n• ON DELETE RESTRICT: Protects fee structures from deletion while active student dues exist.")
    ]

    for title, desc in bullets_er:
        p_b = tf_er.add_paragraph()
        p_b.text = f"• {title}: "
        p_b.font.bold = True
        p_b.font.size = Pt(14)
        p_b.font.color.rgb = RGBColor(15, 23, 42)
        
        # Add description
        p_desc = tf_er.add_paragraph()
        p_desc.text = f"   {desc}"
        p_desc.font.size = Pt(12.5)
        p_desc.font.color.rgb = RGBColor(51, 65, 85)
        p_desc.space_after = Pt(10)

    # --- SLIDE: NORMALIZATION JUSTIFICATION ---
    slide_norm = prs.slides.add_slide(blank_layout)
    tb_norm = slide_norm.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(6.5))
    tf_norm = tb_norm.text_frame
    tf_norm.word_wrap = True

    p = tf_norm.paragraphs[0]
    p.text = "DATABASE DESIGN & FORMAL VALIDATION"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RGBColor(139, 92, 246)

    p = tf_norm.add_paragraph()
    p.text = "Normalization Justification — Decomposition Proofs up to 3NF & BCNF"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = RGBColor(15, 23, 42)
    p.space_after = Pt(14)

    norm_steps = [
        ("1NF (First Normal Form)", "Eliminated all repeating groups and composite fields. Every column (e.g. fees, roommates) holds atomic scalar values with explicit unique primary keys."),
        ("2NF (Second Normal Form)", "Eliminated partial functional dependencies. In unnormalized allocations {StudentID, RoomID} -> HostelName, RoomCapacity; separated into independent relations STUDENT, ROOM, and ROOM_ALLOCATION so non-key attributes fully depend on the entire primary key."),
        ("3NF (Third Normal Form)", "Eliminated transitive dependencies (X -> Y and Y -> Z). Extracted fee tariffs into FEE_STRUCTURE (RoomType -> Fees) so tuition pricing does not transitively depend on individual Student records, preventing deletion anomalies."),
        ("BCNF (Boyce-Codd Normal Form)", "Every non-trivial functional dependency X -> Y has a candidate superkey for X. Surrogate keys (SERIAL PRIMARY KEY) and unique business keys ([UQ] roll_no, email, transaction_id) strictly enforce BCNF across all 19 schemas.")
    ]

    for title, desc in norm_steps:
        p_b = tf_norm.add_paragraph()
        p_b.text = f"• {title}: "
        p_b.font.bold = True
        p_b.font.size = Pt(14)
        p_b.font.color.rgb = RGBColor(15, 23, 42)
        
        p_desc = tf_norm.add_paragraph()
        p_desc.text = f"   {desc}"
        p_desc.font.size = Pt(12.5)
        p_desc.font.color.rgb = RGBColor(51, 65, 85)
        p_desc.space_after = Pt(10)

    # Save outputs
    out_local = os.path.join(project_dir, "SmartHostel_Final_Presentation.pptx")
    prs.save(out_local)
    
    downloads_out = r"C:\Users\Nethra R\Downloads\SmartHostel_Final_Presentation.pptx"
    prs.save(downloads_out)
    
    # Also overwrite the presentation in Downloads if requested
    try:
        prs.save(r"C:\Users\Nethra R\Downloads\SmartHostel_Presentation (3).pptx")
        print("Updated C:\\Users\\Nethra R\\Downloads\\SmartHostel_Presentation (3).pptx")
    except Exception as e:
        print("Could not overwrite open file:", e)

    print("Successfully generated final presentation at:")
    print(" -", out_local)
    print(" -", downloads_out)

if __name__ == "__main__":
    update_presentation()
