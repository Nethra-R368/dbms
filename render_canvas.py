import os
from PIL import Image, ImageDraw, ImageFont

def render_uml_png(output_path):
    width, height = 2400, 1600
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 36)
        font_hdr = ImageFont.truetype("arialbd.ttf", 20)
        font_body = ImageFont.truetype("courbd.ttf" if os.path.exists("C:/Windows/Fonts/courbd.ttf") else "arial.ttf", 16)
        font_card = ImageFont.truetype("arialbd.ttf", 18)
    except:
        font_title = font_hdr = font_body = font_card = ImageFont.load_default()

    # Draw Title
    draw.text((80, 40), "UML Diagram – SmartHostel System", fill=(15, 23, 42), font=font_title)

    def draw_box(x, y, w, h, title, items):
        # Card border and header
        draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=(30, 41, 59), width=2)
        draw.rectangle([x, y, x + w, y + 32], fill=(241, 245, 249), outline=(30, 41, 59), width=2)
        # Title
        bbox = draw.textbbox((0, 0), title, font=font_hdr)
        tw = bbox[2] - bbox[0]
        draw.text((x + (w - tw) // 2, y + 6), title, fill=(15, 23, 42), font=font_hdr)
        # Content
        cur_y = y + 42
        for line, tag in items:
            color = (15, 23, 42)
            if tag == "PK":
                color = (15, 23, 42)
            elif tag == "FK":
                color = (220, 38, 38)
            elif tag == "UQ":
                color = (22, 163, 74)
            draw.text((x + 12, cur_y), line, fill=color, font=font_body)
            cur_y += 24

    # Boxes Definitions
    # 1. USERS: x=1050, y=100, w=300, h=180
    draw_box(1050, 100, 300, 180, "USERS", [
        ("+ user_id : int (PK)", "PK"),
        ("+ username : varchar(50) (UQ)", "UQ"),
        ("+ password_hash : varchar(255)", "NORMAL"),
        ("+ role : varchar(20)", "NORMAL"),
        ("+ created_at : datetime", "NORMAL"),
    ])

    # 2. FEE_STRUCTURE: x=80, y=280, w=280, h=180
    draw_box(80, 280, 280, 180, "FEE_STRUCTURE", [
        ("+ fee_structure_id : int (PK)", "PK"),
        ("+ room_type : varchar(20)", "NORMAL"),
        ("+ academic_fee : decimal(10,2)", "NORMAL"),
        ("+ mess_fee : decimal(10,2)", "NORMAL"),
        ("+ caution_deposit : decimal(10,2)", "NORMAL"),
    ])

    # 3. STUDENT_FEE: x=80, y=520, w=280, h=230
    draw_box(80, 520, 280, 230, "STUDENT_FEE", [
        ("+ fee_id : int (PK)", "PK"),
        ("+ student_id : int (FK)", "FK"),
        ("+ fee_structure_id : int (FK)", "FK"),
        ("+ amount_due : decimal(10,2)", "NORMAL"),
        ("+ amount_paid : decimal(10,2)", "NORMAL"),
        ("+ due_date : date", "NORMAL"),
        ("+ status : varchar(20)", "NORMAL"),
    ])

    # 4. STUDENT: x=700, y=260, w=300, h=330
    draw_box(700, 260, 300, 330, "STUDENT", [
        ("+ student_id : int (PK)", "PK"),
        ("+ user_id : int (FK)", "FK"),
        ("+ roll_no : varchar(20) (UQ)", "UQ"),
        ("+ name : varchar(100)", "NORMAL"),
        ("+ email : varchar(100) (UQ)", "UQ"),
        ("+ phone : varchar(15)", "NORMAL"),
        ("+ department : varchar(100)", "NORMAL"),
        ("+ year : varchar(10)", "NORMAL"),
        ("+ gender : varchar(10)", "NORMAL"),
        ("+ date_of_birth : date", "NORMAL"),
        ("+ date_admission : date", "NORMAL"),
        ("+ status : varchar(20)", "NORMAL"),
    ])

    # 5. WARDEN: x=1250, y=260, w=260, h=200
    draw_box(1250, 260, 260, 200, "WARDEN", [
        ("+ warden_id : int (PK)", "PK"),
        ("+ user_id : int (FK)", "FK"),
        ("+ name : varchar(100)", "NORMAL"),
        ("+ email : varchar(100) (UQ)", "UQ"),
        ("+ phone : varchar(15)", "NORMAL"),
        ("+ created_at : datetime", "NORMAL"),
    ])

    # 6. NOTICE: x=1750, y=260, w=270, h=230
    draw_box(1750, 260, 270, 230, "NOTICE", [
        ("+ notice_id : int (PK)", "PK"),
        ("+ user_id : int (FK)", "FK"),
        ("+ title : varchar(200)", "NORMAL"),
        ("+ description : text", "NORMAL"),
        ("+ audience_type : varchar(50)", "NORMAL"),
        ("+ expiry_date : date", "NORMAL"),
        ("+ created_at : datetime", "NORMAL"),
    ])

    # 7. HOSTEL: x=1450, y=500, w=280, h=180
    draw_box(1450, 500, 280, 180, "HOSTEL", [
        ("+ hostel_id : int (PK)", "PK"),
        ("+ warden_id : int (FK)", "FK"),
        ("+ hostel_name : varchar(100) (UQ)", "UQ"),
        ("+ hostel_type : varchar(20)", "NORMAL"),
        ("+ capacity : int", "NORMAL"),
    ])

    # 8-12: The 5 Student Child Modules (Row at y=760)
    # COMPLAINT: x=400, y=760, w=220, h=270
    draw_box(400, 760, 220, 270, "COMPLAINT", [
        ("+ complaint_id : int (PK)", "PK"),
        ("+ student_id : int (FK)", "FK"),
        ("+ category : varchar(30)", "NORMAL"),
        ("+ description : text", "NORMAL"),
        ("+ priority : varchar(20)", "NORMAL"),
        ("+ created_at : datetime", "NORMAL"),
        ("+ status : varchar(20)", "NORMAL"),
        ("+ resolved_at : datetime", "NORMAL"),
        ("+ resolution : text", "NORMAL"),
    ])

    # VISITOR: x=650, y=760, w=220, h=270
    draw_box(650, 760, 220, 270, "VISITOR", [
        ("+ visitor_id : int (PK)", "PK"),
        ("+ student_id : int (FK)", "FK"),
        ("+ visitor_name : varchar(100)", "NORMAL"),
        ("+ relationship : varchar(50)", "NORMAL"),
        ("+ phone : varchar(15)", "NORMAL"),
        ("+ visit_date : date", "NORMAL"),
        ("+ entry_time : time", "NORMAL"),
        ("+ exit_time : time", "NORMAL"),
        ("+ status : varchar(20)", "NORMAL"),
    ])

    # LEAVE_REQUEST: x=900, y=760, w=230, h=290
    draw_box(900, 760, 230, 290, "LEAVE_REQUEST", [
        ("+ leave_id : int (PK)", "PK"),
        ("+ student_id : int (FK)", "FK"),
        ("+ pass_type : varchar(20)", "NORMAL"),
        ("+ from_date : date", "NORMAL"),
        ("+ to_date : date", "NORMAL"),
        ("+ reason : varchar(255)", "NORMAL"),
        ("+ destination : varchar(255)", "NORMAL"),
        ("+ emergency_contact : var(15)", "NORMAL"),
        ("+ status : varchar(20)", "NORMAL"),
        ("+ action_date : datetime", "NORMAL"),
    ])

    # ATTENDANCE: x=1160, y=760, w=230, h=250
    draw_box(1160, 760, 230, 250, "ATTENDANCE", [
        ("+ attendance_id : int (PK)", "PK"),
        ("+ student_id : int (FK)", "FK"),
        ("+ warden_id : int (FK)", "FK"),
        ("+ date : date", "NORMAL"),
        ("+ status : varchar(25)", "NORMAL"),
        ("+ emergency_contact : var(15)", "NORMAL"),
        ("+ remarks : text", "NORMAL"),
        ("+ action_date : datetime", "NORMAL"),
    ])

    # MESS_FEEDBACK: x=1420, y=760, w=220, h=250
    draw_box(1420, 760, 220, 250, "MESS_FEEDBACK", [
        ("+ feedback_id : int (PK)", "PK"),
        ("+ student_id : int (FK)", "FK"),
        ("+ warden_id : int (FK)", "FK"),
        ("+ date : date", "NORMAL"),
        ("+ food_quality : int", "NORMAL"),
        ("+ taste : int", "NORMAL"),
        ("+ cleanliness : int", "NORMAL"),
        ("+ comments : text", "NORMAL"),
    ])

    # 13-15: Hostel Child Modules (Row at y=760 on Right)
    # INVENTORY: x=1670, y=760, w=220, h=200
    draw_box(1670, 760, 220, 200, "INVENTORY", [
        ("+ item_id : int (PK)", "PK"),
        ("+ hostel_id : int (FK)", "FK"),
        ("+ item_name : varchar(100)", "NORMAL"),
        ("+ total_qty : int", "NORMAL"),
        ("+ occupied_qty : int", "NORMAL"),
        ("+ damaged_qty : int", "NORMAL"),
    ])

    # MESS_MENU: x=1920, y=760, w=220, h=200
    draw_box(1920, 760, 220, 200, "MESS_MENU", [
        ("+ menu_id : int (PK)", "PK"),
        ("+ hostel_id : int (FK)", "FK"),
        ("+ day_of_week : varchar(10)", "NORMAL"),
        ("+ breakfast : varchar(255)", "NORMAL"),
        ("+ lunch : varchar(255)", "NORMAL"),
        ("+ dinner : varchar(255)", "NORMAL"),
    ])

    # ROOM: x=2170, y=760, w=210, h=250
    draw_box(2170, 760, 210, 250, "ROOM", [
        ("+ room_id : int (PK)", "PK"),
        ("+ hostel_id : int (FK)", "FK"),
        ("+ room_number : varchar(20)", "NORMAL"),
        ("+ floor : varchar(10)", "NORMAL"),
        ("+ room_type : varchar(20)", "NORMAL"),
        ("+ capacity : int", "NORMAL"),
        ("+ occupied_count : int", "NORMAL"),
        ("+ status : varchar(20)", "NORMAL"),
    ])

    # 16-19: Bottom Entities (Row at y=1150 - 1300)
    # PAYMENT: x=80, y=1100, w=280, h=240
    draw_box(80, 1100, 280, 240, "PAYMENT", [
        ("+ payment_id : int (PK)", "PK"),
        ("+ fee_id : int (FK)", "FK"),
        ("+ amount : decimal(10,2)", "NORMAL"),
        ("+ payment_date : datetime", "NORMAL"),
        ("+ payment_method : varchar(50)", "NORMAL"),
        ("+ transaction_id : var(100) (UQ)", "UQ"),
        ("+ status : varchar(20)", "NORMAL"),
    ])

    # ROOM_ALLOCATION: x=650, y=1150, w=240, h=200
    draw_box(650, 1150, 240, 200, "ROOM_ALLOCATION", [
        ("+ allocation_id : int (PK)", "PK"),
        ("+ student_id : int (FK)", "FK"),
        ("+ room_id : int (FK)", "FK"),
        ("+ allocation_date : date", "NORMAL"),
        ("+ vacated_date : date", "NORMAL"),
        ("+ status : varchar(20)", "NORMAL"),
    ])

    # INVENTORY_TRANSACTION: x=1670, y=1050, w=230, h=200
    draw_box(1670, 1050, 230, 200, "INVENTORY_TRANSACTION", [
        ("+ transaction_id : int (PK)", "PK"),
        ("+ item_id : int (FK)", "FK"),
        ("+ transaction_type : varchar(20)", "NORMAL"),
        ("+ quantity : int", "NORMAL"),
        ("+ remarks : text", "NORMAL"),
        ("+ created_at : datetime", "NORMAL"),
    ])

    # ROOM_CHANGE_REQUEST: x=2150, y=1100, w=230, h=220
    draw_box(2150, 1100, 230, 220, "ROOM_CHANGE_REQUEST", [
        ("+ request_id : int (PK)", "PK"),
        ("+ student_id : int (FK)", "FK"),
        ("+ current_room : int (FK)", "FK"),
        ("+ requested_room : int (FK)", "FK"),
        ("+ reason : varchar(255)", "NORMAL"),
        ("+ status : varchar(20)", "NORMAL"),
        ("+ action_date : datetime", "NORMAL"),
    ])

    # ================= DRAW ORTHOGONAL CONNECTORS =================
    line_col = (51, 65, 85)
    lw = 2

    def draw_wire(pts):
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i+1]], fill=line_col, width=lw)

    # 1. USERS -> STUDENT
    draw_wire([(1100, 280), (1100, 220), (850, 220), (850, 260)])
    draw.text((1080, 230), "1", fill=line_col, font=font_card)
    draw.text((820, 235), "0..1", fill=line_col, font=font_card)

    # 2. USERS -> WARDEN
    draw_wire([(1250, 280), (1250, 220), (1350, 220), (1350, 260)])
    draw.text((1230, 230), "1", fill=line_col, font=font_card)
    draw.text((1355, 235), "0..1", fill=line_col, font=font_card)

    # 3. USERS -> NOTICE
    draw_wire([(1350, 180), (1885, 180), (1885, 260)])
    draw.text((1365, 155), "1", fill=line_col, font=font_card)
    draw.text((1895, 235), "N", fill=line_col, font=font_card)

    # 4. WARDEN -> HOSTEL
    draw_wire([(1380, 460), (1380, 480), (1550, 480), (1550, 500)])
    draw.text((1360, 465), "1", fill=line_col, font=font_card)
    draw.text((1560, 475), "N", fill=line_col, font=font_card)

    # 5. FEE_STRUCTURE -> STUDENT_FEE
    draw_wire([(220, 460), (220, 520)])
    draw.text((230, 470), "1", fill=line_col, font=font_card)
    draw.text((230, 495), "N", fill=line_col, font=font_card)

    # 6. STUDENT -> STUDENT_FEE
    draw_wire([(700, 420), (360, 420), (360, 550)])
    draw.text((670, 395), "1", fill=line_col, font=font_card)
    draw.text((370, 525), "N", fill=line_col, font=font_card)

    # 7. STUDENT_FEE -> PAYMENT
    draw_wire([(220, 750), (220, 1100)])
    draw.text((230, 770), "1", fill=line_col, font=font_card)
    draw.text((230, 1070), "N", fill=line_col, font=font_card)

    # 8. STUDENT -> 5 MODULES (Horizontal distribution bus at y=680)
    draw_wire([(850, 590), (850, 680)])
    draw.text((860, 600), "1", fill=line_col, font=font_card)
    # Bus line
    draw_wire([(510, 680), (1530, 680)])
    # Drops:
    draw_wire([(510, 680), (510, 760)]) # COMPLAINT
    draw.text((520, 730), "N", fill=line_col, font=font_card)
    draw_wire([(760, 680), (760, 760)]) # VISITOR
    draw.text((770, 730), "N", fill=line_col, font=font_card)
    draw_wire([(1015, 680), (1015, 760)]) # LEAVE_REQUEST
    draw.text((1025, 730), "N", fill=line_col, font=font_card)
    draw_wire([(1275, 680), (1275, 760)]) # ATTENDANCE
    draw.text((1285, 730), "N", fill=line_col, font=font_card)
    draw_wire([(1530, 680), (1530, 760)]) # MESS_FEEDBACK
    draw.text((1540, 730), "N", fill=line_col, font=font_card)

    # 9. STUDENT -> ROOM_ALLOCATION
    draw_wire([(770, 590), (770, 1150)])
    draw.text((745, 610), "1", fill=line_col, font=font_card)
    draw.text((745, 1120), "1", fill=line_col, font=font_card)

    # 10. HOSTEL -> 3 MODULES (Bus at y=720)
    draw_wire([(1590, 680), (1590, 720)])
    draw.text((1600, 685), "1", fill=line_col, font=font_card)
    draw_wire([(1780, 720), (2275, 720)])
    # Drops:
    draw_wire([(1780, 720), (1780, 760)]) # INVENTORY
    draw.text((1790, 735), "N", fill=line_col, font=font_card)
    draw_wire([(2030, 720), (2030, 760)]) # MESS_MENU
    draw.text((2040, 735), "N", fill=line_col, font=font_card)
    draw_wire([(2275, 720), (2275, 760)]) # ROOM
    draw.text((2285, 735), "N", fill=line_col, font=font_card)

    # 11. INVENTORY -> INVENTORY_TRANSACTION
    draw_wire([(1780, 960), (1780, 1050)])
    draw.text((1790, 980), "1", fill=line_col, font=font_card)
    draw.text((1790, 1025), "N", fill=line_col, font=font_card)

    # 12. ROOM -> ROOM_ALLOCATION
    draw_wire([(2170, 950), (1400, 950), (1400, 1250), (890, 1250)])
    draw.text((2140, 925), "1", fill=line_col, font=font_card)
    draw.text((905, 1225), "N", fill=line_col, font=font_card)

    # 13. ROOM -> ROOM_CHANGE_REQUEST
    draw_wire([(2230, 1010), (2230, 1100)])
    draw.text((2175, 1050), "current_room (N)", fill=(71, 85, 105), font=font_card)
    draw_wire([(2320, 1010), (2320, 1100)])
    draw.text((2330, 1050), "requested_room (1)", fill=(71, 85, 105), font=font_card)

    img.save(output_path, "PNG")
    print("Clean PNG saved to:", output_path)

def render_schema_png(output_path):
    width, height = 2200, 1700
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 36)
        font_legend = ImageFont.truetype("arialbd.ttf", 20)
        font_body = ImageFont.truetype("courbd.ttf" if os.path.exists("C:/Windows/Fonts/courbd.ttf") else "arial.ttf", 19)
        font_hdr = ImageFont.truetype("arialbd.ttf", 22)
    except:
        font_title = font_legend = font_body = font_hdr = ImageFont.load_default()

    # Outer border
    draw.rectangle([40, 40, width - 40, height - 40], fill="white", outline=(139, 92, 246), width=4)

    # Header
    draw.text((width // 2 - 500, 80), "RELATIONAL SCHEMA – HOSTEL MANAGEMENT SYSTEM", fill=(15, 23, 42), font=font_title)
    draw.text((width // 2 - 400, 135), "Notation: Underlined = Primary Key | (FK) = Foreign Key | [UQ] = Unique Constraint", fill=(51, 65, 85), font=font_legend)
    draw.line([(80, 175), (width - 80, 175)], fill=(226, 232, 240), width=2)

    schema_lines = [
        "1.  USERS( User_ID, Username [UQ], Password_Hash, Role, Created_At )",
        "2.  STUDENT( Student_ID, User_ID (FK), Roll_No [UQ], Name, Email [UQ], Phone, Department, Year, Gender, Date_Of_Birth, Date_Admission, Status )",
        "3.  WARDEN( Warden_ID, User_ID (FK), Name, Email [UQ], Phone, Created_At )",
        "4.  NOTICE( Notice_ID, User_ID (FK), Title, Description, Audience_Type, Expiry_Date, Created_At )",
        "5.  FEE_STRUCTURE( Fee_Structure_ID, Room_Type, Academic_Fee, Mess_Fee, Caution_Deposit )",
        "6.  STUDENT_FEE( Fee_ID, Student_ID (FK), Fee_Structure_ID (FK), Amount_Due, Amount_Paid, Due_Date, Status )",
        "7.  COMPLAINT( Complaint_ID, Student_ID (FK), Category, Description, Priority, Created_At, Status, Resolved_At, Resolution )",
        "8.  VISITOR( Visitor_ID, Student_ID (FK), Visitor_Name, Relationship, Phone, Visit_Date, Entry_Time, Exit_Time, Status )",
        "9.  LEAVE_REQUEST( Leave_ID, Student_ID (FK), Pass_Type, From_Date, To_Date, Reason, Destination, Emergency_Contact, Status, Action_Date )",
        "10. ATTENDANCE( Attendance_ID, Student_ID (FK), Warden_ID (FK), Date, Status, Emergency_Contact, Remarks, Action_Date )",
        "11. MESS_FEEDBACK( Feedback_ID, Student_ID (FK), Warden_ID (FK), Date, Food_Quality, Taste, Cleanliness, Comments )",
        "12. HOSTEL( Hostel_ID, Warden_ID (FK), Hostel_Name [UQ], Hostel_Type, Capacity )",
        "13. INVENTORY( Item_ID, Hostel_ID (FK), Item_Name, Total_Qty, Occupied_Qty, Damaged_Qty )",
        "14. MESS_MENU( Menu_ID, Hostel_ID (FK), Day_Of_Week, Breakfast, Lunch, Dinner )",
        "15. ROOM( Room_ID, Hostel_ID (FK), Room_Number, Floor, Room_Type, Capacity, Occupied_Count, Status )",
        "16. ROOM_ALLOCATION( Allocation_ID, Student_ID (FK), Room_ID (FK), Allocation_Date, Vacated_Date, Status )",
        "17. INVENTORY_TRANSACTION( Transaction_ID, Item_ID (FK), Transaction_Type, Quantity, Remarks, Created_At )",
        "18. ROOM_CHANGE_REQUEST( Request_ID, Student_ID (FK), Current_Room (FK), Requested_Room (FK), Reason, Status, Action_Date )",
        "19. PAYMENT( Payment_ID, Fee_ID (FK), Amount, Payment_Date, Payment_Method, Transaction_ID [UQ], Status )"
    ]

    cur_y = 210
    for line in schema_lines:
        draw.text((90, cur_y), line, fill=(30, 41, 59), font=font_body)
        cur_y += 45

    draw.line([(80, cur_y + 10), (width - 80, cur_y + 10)], fill=(203, 213, 225), width=2)
    cur_y += 35

    draw.text((90, cur_y), "FOREIGN KEY REFERENCES:", fill=(15, 23, 42), font=font_hdr)
    cur_y += 45

    fk_lines = [
        "STUDENT.User_ID -> USERS.User_ID  |  WARDEN.User_ID -> USERS.User_ID  |  NOTICE.User_ID -> USERS.User_ID",
        "STUDENT_FEE.Student_ID -> STUDENT.Student_ID  |  STUDENT_FEE.Fee_Structure_ID -> FEE_STRUCTURE.Fee_Structure_ID",
        "COMPLAINT.Student_ID -> STUDENT.Student_ID  |  VISITOR.Student_ID -> STUDENT.Student_ID  |  LEAVE_REQUEST.Student_ID -> STUDENT.Student_ID",
        "ATTENDANCE.Student_ID -> STUDENT.Student_ID  |  ATTENDANCE.Warden_ID -> WARDEN.Warden_ID",
        "MESS_FEEDBACK.Student_ID -> STUDENT.Student_ID  |  MESS_FEEDBACK.Warden_ID -> WARDEN.Warden_ID",
        "HOSTEL.Warden_ID -> WARDEN.Warden_ID  |  INVENTORY.Hostel_ID -> HOSTEL.Hostel_ID  |  MESS_MENU.Hostel_ID -> HOSTEL.Hostel_ID",
        "ROOM.Hostel_ID -> HOSTEL.Hostel_ID  |  ROOM_ALLOCATION.Student_ID -> STUDENT.Student_ID  |  ROOM_ALLOCATION.Room_ID -> ROOM.Room_ID",
        "INVENTORY_TRANSACTION.Item_ID -> INVENTORY.Item_ID  |  ROOM_CHANGE_REQUEST.Student_ID -> STUDENT.Student_ID",
        "ROOM_CHANGE_REQUEST.Current_Room -> ROOM.Room_ID  |  ROOM_CHANGE_REQUEST.Requested_Room -> ROOM.Room_ID",
        "PAYMENT.Fee_ID -> STUDENT_FEE.Fee_ID"
    ]

    for line in fk_lines:
        draw.text((90, cur_y), line, fill=(51, 65, 85), font=font_body)
        cur_y += 40

    img.save(output_path, "PNG")
    print("Schema PNG saved to:", output_path)

if __name__ == "__main__":
    out_dir = os.path.dirname(__file__)
    render_uml_png(os.path.join(out_dir, "uml_diagram.png"))
    render_schema_png(os.path.join(out_dir, "relational_schema.png"))
