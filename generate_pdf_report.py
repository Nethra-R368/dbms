import os
import sys
import psycopg2
from decimal import Decimal
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and display total page count: 'Page X of Y'
    along with formal academic running headers and footers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress headers and footers on the formal cover page
        
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Running Top Header
        self.drawString(45, 11 * inch - 32, "23AIE303: Database Management Systems (DBMS) | Project Report")
        self.drawRightString(8.5 * inch - 45, 11 * inch - 32, "ResiKeep / SmartHostel - Team 12")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.75)
        self.line(45, 11 * inch - 36, 8.5 * inch - 45, 11 * inch - 36)
        
        # Running Bottom Footer
        self.line(45, 42, 8.5 * inch - 45, 42)
        self.setFont("Helvetica", 8)
        self.drawString(45, 30, "Amrita Vishwa Vidyapeetham · School of Artificial Intelligence & Computing")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 45, 30, page_str)
        self.restoreState()


def format_cell_value(val):
    if val is None:
        return "NULL"
    if isinstance(val, (datetime.date, datetime.datetime)):
        return val.strftime("%Y-%m-%d")
    if isinstance(val, Decimal):
        return f"{val:,.2f}"
    val_str = str(val).strip()
    if len(val_str) > 28:
        return val_str[:25] + "..."
    return val_str


def fetch_database_metadata():
    """
    Connects to the active local PostgreSQL database and extracts column schemas
    and clean live sample rows for all core tables.
    """
    tables_order = [
        ("users", "Authentication & Role-Based Access Control (Admin, Warden, Student, Accountant)"),
        ("student", "Core Student Demographic, Academic, and Status Registry"),
        ("warden", "Hostel Supervisors & Residence Officers Directory"),
        ("hostel", "Residential Accommodation Blocks (Boys, Girls, Co-Ed)"),
        ("room", "Physical Room Inventory, Capacities, and Dynamic Occupancy Status"),
        ("room_allocation", "Temporal Student Bed Allocation Ledger with Status Tracking"),
        ("fee_structure", "Standard Academic, Mess, and Caution Tariff Rate Cards"),
        ("student_fee", "Student Invoiced Fee Ledgers, Balances, and Dues"),
        ("payment", "Financial Receipts, Audit Codes, and Transaction Logs"),
        ("complaint", "Student Grievance Ticketing, Categorization, and Resolution Lifecycle"),
        ("attendance", "Nightly Curfew Verification and Attendance Tracking"),
        ("leave_request", "Student Out-Pass Approvals and Emergency Contact Authorizations"),
        ("visitor", "External Campus Guest Check-In and Check-Out Auditing"),
        ("mess_menu", "Weekly Meal Schedules across Hostel Kitchens"),
        ("mess_feedback", "Nutritional, Cleanliness, and Taste Evaluation Ledger"),
        ("inventory", "Hostel Operational Equipment and Asset Directory"),
        ("inventory_transaction", "Asset Delta Logs (Procurement, Maintenance, Write-Offs)"),
        ("notice", "Administrative Broadcast Announcements with Role-Targeted Visibility"),
        ("room_change_request", "Student Bed Transfer Applications & Warden Approvals")
    ]
    
    db_data = []
    try:
        conn = psycopg2.connect(
            host='127.0.0.1',
            port=5432,
            user='postgres',
            password='Nark@1231',
            dbname='smarthostel'
        )
        cur = conn.cursor()
        
        for table_name, description in tables_order:
            # Query column definitions
            cur.execute(f"""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = '{table_name}'
                ORDER BY ordinal_position;
            """)
            cols = cur.fetchall()
            
            # Query sample rows
            cur.execute(f'SELECT * FROM "{table_name}" LIMIT 3;')
            rows = cur.fetchall()
            
            col_names = [c[0] for c in cols]
            
            db_data.append({
                "name": table_name,
                "desc": description,
                "cols": cols,
                "col_names": col_names,
                "rows": rows
            })
            
        conn.close()
    except Exception as e:
        print(f"Database query note: {e}")
    return db_data


def generate_project_report_pdf(pdf_filepath):
    doc = SimpleDocTemplate(
        pdf_filepath,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=45,
        bottomMargin=45
    )
    
    styles = getSampleStyleSheet()
    
    primary_color = colors.HexColor("#1e3a8a")     # Deep Corporate Navy
    secondary_color = colors.HexColor("#3b82f6")   # Royal Blue
    accent_color = colors.HexColor("#4f46e5")      # Indigo
    text_dark = colors.HexColor("#0f172a")         # Dark Slate
    text_muted = colors.HexColor("#475569")        # Muted Slate
    border_color = colors.HexColor("#cbd5e1")      # Border Slate
    bg_light = colors.HexColor("#f8fafc")          # Off-white Slate
    
    style_cover_univ = ParagraphStyle(
        'CoverUniv',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=primary_color,
        alignment=1,
        spaceAfter=4
    )
    style_cover_school = ParagraphStyle(
        'CoverSchool',
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=text_muted,
        alignment=1,
        spaceAfter=20
    )
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=23,
        leading=28,
        textColor=primary_color,
        alignment=1,
        spaceAfter=14
    )
    style_cover_subtitle = ParagraphStyle(
        'CoverSub',
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=text_dark,
        alignment=1,
        spaceAfter=25
    )
    
    style_sec_h1 = ParagraphStyle(
        'SecH1',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    style_sec_h2 = ParagraphStyle(
        'SecH2',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=accent_color,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    style_body = ParagraphStyle(
        'BodyDark',
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=text_dark,
        spaceAfter=5
    )
    style_body_bold = ParagraphStyle(
        'BodyBold',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13.5,
        textColor=text_dark
    )
    style_bullet = ParagraphStyle(
        'BulletDark',
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=text_dark,
        leftIndent=14,
        spaceAfter=3
    )
    style_code = ParagraphStyle(
        'CodeSnippet',
        fontName='Courier',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#1e293b"),
        backColor=bg_light,
        borderPadding=5,
        spaceAfter=6
    )
    style_caption = ParagraphStyle(
        'FigCaption',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        alignment=1,
        textColor=primary_color,
        spaceAfter=8
    )

    story = []
    
    # =========================================================================
    # SECTION 1 & 2: PROJECT TITLE & TEAM MEMBERS (FORMAL TITLE PAGE)
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("AMRITA VISHWA VIDYAPEETHAM", style_cover_univ))
    story.append(Paragraph("School of Artificial Intelligence & Computing · Department of AI", style_cover_school))
    story.append(HRFlowable(width="75%", thickness=2, color=secondary_color, spaceAfter=26))
    
    story.append(Paragraph("ResiKeep: Cloud-Integrated Enterprise Relational Database for Multi-Tenant Student Housing & Facility Operations", style_cover_title))
    story.append(Paragraph("<b>Course Code:</b> 23AIE303 — Database Management Systems (DBMS)<br/>Comprehensive Laboratory Evaluation & Technical Report", style_cover_subtitle))
    story.append(Spacer(1, 15))
    
    # Team Members Table
    team_headers = [Paragraph("<b>Team Member</b>", style_body_bold), Paragraph("<b>Roll Number</b>", style_body_bold), Paragraph("<b>Assigned Contribution Matrix</b>", style_body_bold)]
    team_r1 = [
        Paragraph("<b>R Nethra</b>", style_body),
        Paragraph("CB.SC.U4AIE24147", style_body),
        Paragraph("Database Architecture, PostgreSQL DDL Schema, PL/pgSQL Triggers, Foreign Key Constraints, Cloud Deployment Pipeline", style_body)
    ]
    team_r2 = [
        Paragraph("<b>Sahaana Shri S K</b>", style_body),
        Paragraph("CB.SC.U4AIE24149", style_body),
        Paragraph("Relational Normalization (1NF–BCNF), Transactional Stored Procedures, FastAPI REST API Endpoints, Frontend Integration", style_body)
    ]
    
    team_tbl = Table([team_headers, team_r1, team_r2], colWidths=[1.8 * inch, 1.8 * inch, 3.6 * inch])
    team_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e0e7ff")),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(team_tbl)
    
    story.append(Spacer(1, 28))
    
    # Project Metadata Summary Box
    meta_data = [
        [Paragraph("<b>Academic Batch & Group:</b>", style_body_bold), Paragraph("Batch B12 · Team 12", style_body)],
        [Paragraph("<b>Official GitHub Repository:</b>", style_body_bold), Paragraph("<font color='#1d4ed8'><u>https://github.com/Nethra-R368/dbms</u></font>", style_body)],
        [Paragraph("<b>Database Engine:</b>", style_body_bold), Paragraph("PostgreSQL 18 (Relational Engine) with PL/pgSQL Procedural Extensions", style_body)],
        [Paragraph("<b>Application Stack:</b>", style_body_bold), Paragraph("FastAPI (Python 3.12+), SQLAlchemy 2.0 ORM, React 19, Tailwind CSS, Vite", style_body)],
        [Paragraph("<b>Hosting & Deployment:</b>", style_body_bold), Paragraph("Local Windows Service, Single-Server Unified SPA, Live HTTPS Public Tunnel", style_body)],
        [Paragraph("<b>Evaluation Standard:</b>", style_body_bold), Paragraph("23AIE303 DBMS Laboratory Assessment (Project Presentation, Report & Viva)", style_body)]
    ]
    meta_tbl = Table(meta_data, colWidths=[2.2 * inch, 5.0 * inch])
    meta_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_light),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_tbl)
    
    story.append(PageBreak())
    
    # =========================================================================
    # SECTION 3: INTRODUCTION AND PROBLEM STATEMENT
    # =========================================================================
    story.append(Paragraph("3. Introduction and Problem Statement", style_sec_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))
    
    story.append(Paragraph("3.1. Project Context & Background", style_sec_h2))
    story.append(Paragraph(
        "University hostel accommodation represents a high-density, multi-stakeholder operational ecosystem. "
        "Modern campus residential management encompasses diverse mission-critical workflows: residential bed "
        "and room inventory management, financial fee invoicing and receipt reconciliation, maintenance grievance "
        "ticketing, nightly biometric curfew tracking, student out-pass approvals, catering feedback aggregation, "
        "and institutional asset logistics. Historically, educational institutions have operated these subsystems through "
        "fragmented paper logbooks and disjointed spreadsheet files. These obsolete workflows fail to maintain "
        "data integrity, lack auditability, and introduce severe administrative delays.", style_body
    ))
    
    story.append(Paragraph("3.2. Problem Statement", style_sec_h2))
    story.append(Paragraph("Manual and naive software solutions suffer from four fundamental systemic deficiencies:", style_body))
    story.append(Paragraph("• <b>Concurrency Race Conditions & Double-Bookings:</b> In the absence of transactional isolation, multiple wardens allocating rooms simultaneously can assign the same bed to different students, causing severe accommodation conflicts.", style_bullet))
    story.append(Paragraph("• <b>Financial Ledger Inconsistencies:</b> Fragmented spreadsheets obscure partial payments, miscalculate late penalty fees, and prevent real-time reconciliation against university accounts ledgers.", style_bullet))
    story.append(Paragraph("• <b>Severe Data Redundancy & Update Anomalies:</b> Student demographics replicated across separate registers lead to conflicting, stale, or orphaned records upon student status updates or departures.", style_bullet))
    story.append(Paragraph("• <b>Accountability & Audit Gaps:</b> Maintenance complaints, emergency out-passes, and campus visitor logs lack immutable server timestamping, leaving no verifiable audit trail.", style_bullet))
    
    story.append(Paragraph("3.3. System Objectives & Proposed Solution", style_sec_h2))
    story.append(Paragraph(
        "<b>ResiKeep / SmartHostel</b> resolves these systemic vulnerabilities by implementing an enterprise-grade "
        "<b>PostgreSQL 18</b> relational database management system. Rather than delegating business rules exclusively "
        "to application code, ResiKeep enforces invariants directly within the relational engine using:", style_body
    ))
    story.append(Paragraph("• <b>Active Database Triggers:</b> PL/pgSQL triggers automatically maintain room occupancy counts and dynamically update student invoice statuses upon receipt of payments.", style_bullet))
    story.append(Paragraph("• <b>ACID-Compliant Stored Procedures:</b> Atomic stored functions (<code>allocate_room</code>, <code>vacate_room</code>) isolate room assignment operations, guaranteeing zero double-bookings.", style_bullet))
    story.append(Paragraph("• <b>Strict Domain & Referential Constraints:</b> Cascading rules (<code>ON DELETE CASCADE</code>, <code>RESTRICT</code>) and table check constraints preserve database invariants at all times.", style_bullet))
    story.append(Paragraph("• <b>Role-Based Access Control (RBAC):</b> Cryptographically secured JWT authentication segregates administrative, warden, student, and accountant privileges.", style_bullet))
    
    # =========================================================================
    # SECTION 4: CONCEPTUAL AND LOGICAL DATABASE DESIGN
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("4. Conceptual and Logical Database Design", style_sec_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))
    
    story.append(Paragraph("4.1. Conceptual Entity Modeling across 6 Business Domains", style_sec_h2))
    story.append(Paragraph(
        "The conceptual architecture partitions the university housing ecosystem into 19 distinct normalized entities "
        "spanning six interconnected functional domains:", style_body
    ))
    story.append(Paragraph("1. <b>Identity & RBAC Domain:</b> <code>USERS</code> anchors authentication, linking in a 1:0..1 relationship to <code>STUDENT</code> and <code>WARDEN</code> profiles.", style_bullet))
    story.append(Paragraph("2. <b>Hostel & Facility Domain:</b> <code>HOSTEL</code> blocks hold a 1:N hierarchy of <code>ROOM</code> units, supervised by assigned <code>WARDEN</code> officers.", style_bullet))
    story.append(Paragraph("3. <b>Tenure & Allocation Domain:</b> <code>ROOM_ALLOCATION</code> tracks student residency with state transitions (<code>ACTIVE</code>, <code>COMPLETED</code>), while <code>ROOM_CHANGE_REQUEST</code> manages internal transfers.", style_bullet))
    story.append(Paragraph("4. <b>Financial Ledger Domain:</b> Master rate cards in <code>FEE_STRUCTURE</code> instantiate individualized student balances in <code>STUDENT_FEE</code>, settled via audited <code>PAYMENT</code> transactions.", style_bullet))
    story.append(Paragraph("5. <b>Student Lifecycle Domain:</b> Encompasses <code>COMPLAINT</code> ticketing, <code>VISITOR</code> gate passes, <code>LEAVE_REQUEST</code> out-passes, and daily <code>ATTENDANCE</code> logs.", style_bullet))
    story.append(Paragraph("6. <b>Catering & Inventory Domain:</b> <code>INVENTORY</code> tracks equipment deltas in <code>INVENTORY_TRANSACTION</code>, while <code>MESS_MENU</code> pairs with student ratings in <code>MESS_FEEDBACK</code>.", style_bullet))
    
    story.append(Paragraph("4.2. Referential Integrity & Cascading Strategies", style_sec_h2))
    story.append(Paragraph("• <b>ON DELETE CASCADE:</b> When a student is removed, dependent allocations, fees, attendance rolls, and complaints are purged automatically to eliminate orphaned records.", style_bullet))
    story.append(Paragraph("• <b>ON DELETE SET NULL:</b> If a warden profile is archived, historical complaint logs and hostel supervision records remain intact with warden references set to NULL.", style_bullet))
    story.append(Paragraph("• <b>ON DELETE RESTRICT:</b> Tariff tiers in <code>FEE_STRUCTURE</code> cannot be deleted while active student fee records reference them, preventing pricing history corruption.", style_bullet))

    story.append(PageBreak())
    
    # =========================================================================
    # SECTION 5: NORMALIZATION AND FUNCTIONAL DEPENDENCIES
    # =========================================================================
    story.append(Paragraph("5. Normalization and Functional Dependencies", style_sec_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))
    story.append(Paragraph(
        "To guarantee that the relational schema is completely immune to insertion, update, and deletion anomalies, "
        "the database was systematically decomposed from an Unnormalized Form (UNF) through to Boyce-Codd Normal Form (BCNF).", style_body
    ))
    
    norm_headers = [Paragraph("<b>Normal Form</b>", style_body_bold), Paragraph("<b>Violation in Naive Schema</b>", style_body_bold), Paragraph("<b>Mathematical Decomposition & Resolution</b>", style_body_bold)]
    norm_r1 = [
        Paragraph("<b>1NF<br/>(First Normal Form)</b>", style_body),
        Paragraph("Repeating groups and comma-delimited strings for fee payments, complaints, and roommates within student rows.", style_body),
        Paragraph("Enforced atomic scalar domains. Decomposed multi-valued fields into distinct tables: <code>STUDENT</code>, <code>STUDENT_FEE</code>, <code>PAYMENT</code>, and <code>COMPLAINT</code> with surrogate primary keys.", style_body)
    ]
    norm_r2 = [
        Paragraph("<b>2NF<br/>(Second Normal Form)</b>", style_body),
        Paragraph("Partial functional dependencies on composite candidate keys: In <code>{Student_ID, Room_ID} -> Hostel_Name, Capacity</code>, room attributes depend only on <code>Room_ID</code>.", style_body),
        Paragraph("Eliminated partial dependencies by separating room catalog attributes into <code>ROOM(Room_ID, Hostel_ID, Room_Number, Capacity)</code> and maintaining allocation state in <code>ROOM_ALLOCATION</code>.", style_body)
    ]
    norm_r3 = [
        Paragraph("<b>3NF<br/>(Third Normal Form)</b>", style_body),
        Paragraph("Transitive functional dependencies: In student billing, <code>Fee_ID -> Room_Type -> (Academic_Fee, Mess_Fee)</code> where non-key charges depend transitively on <code>Room_Type</code>.", style_body),
        Paragraph("Eliminated transitive dependencies by isolating master room tariffs into <code>FEE_STRUCTURE(Fee_Structure_ID, Room_Type, Academic_Fee, Mess_Fee)</code>, linked via Foreign Key.", style_body)
    ]
    norm_r4 = [
        Paragraph("<b>BCNF<br/>(Boyce-Codd Normal Form)</b>", style_body),
        Paragraph("Occurs when a functional determinant X in non-trivial X -> Y is not a candidate superkey.", style_body),
        Paragraph("Every functional determinant across all 19 relations (e.g. <code>User_ID</code>, <code>Roll_No</code>, <code>{Hostel_ID, Room_Number}</code>, <code>Transaction_ID</code>) is a candidate superkey. Hence, BCNF is strictly satisfied.", style_body)
    ]
    
    norm_tbl = Table([norm_headers, norm_r1, norm_r2, norm_r3, norm_r4], colWidths=[1.2 * inch, 2.7 * inch, 3.3 * inch])
    norm_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(norm_tbl)
    
    # =========================================================================
    # SECTION 6: ADVANCED SQL IMPLEMENTATION AND QUERY DESIGN
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("6. Advanced SQL Implementation and Query Design", style_sec_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))
    
    story.append(Paragraph("6.1. Analytical Queries: Aggregations, Joins & Window Functions", style_sec_h2))
    story.append(Paragraph(
        "Below are representative queries demonstrating multi-table relational joins, conditional aggregations, "
        "and analytical window functions implemented in the production system:", style_body
    ))
    
    q1_code = """-- Query 1: Hostel-Level Real-Time Occupancy Analytics with GROUP BY & HAVING
SELECT h.hostel_name, h.hostel_type,
       COALESCE(SUM(r.capacity), 0) AS total_beds,
       COALESCE(SUM(r.occupied_count), 0) AS occupied_beds,
       ROUND((COALESCE(SUM(r.occupied_count),0)::NUMERIC / 
              NULLIF(COALESCE(SUM(r.capacity),0),0)::NUMERIC) * 100, 2) AS occupancy_pct
FROM hostel h
LEFT JOIN room r ON h.hostel_id = r.hostel_id
GROUP BY h.hostel_id, h.hostel_name, h.hostel_type
HAVING COALESCE(SUM(r.occupied_count), 0) > 0
ORDER BY occupancy_pct DESC;"""
    story.append(Paragraph(q1_code.replace('\n', '<br/>').replace(' ', '&nbsp;'), style_code))
    
    q2_code = """-- Query 2: Running Cumulative Student Fee Payment Totals via Window Functions
SELECT p.payment_id, s.roll_no, s.name, p.amount, p.payment_date,
       ROW_NUMBER() OVER(PARTITION BY p.fee_id ORDER BY p.payment_date) AS installment_idx,
       SUM(p.amount) OVER(PARTITION BY p.fee_id ORDER BY p.payment_date 
                          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_paid
FROM payment p
JOIN student_fee sf ON p.fee_id = sf.fee_id
JOIN student s ON sf.student_id = s.student_id
WHERE p.status = 'SUCCESS';"""
    story.append(Paragraph(q2_code.replace('\n', '<br/>').replace(' ', '&nbsp;'), style_code))

    story.append(Paragraph("6.2. Active Database Automation: Triggers & Stored Procedures", style_sec_h2))
    story.append(Paragraph("• <code>trg_update_room_occupancy</code>: Fires on <code>room_allocation</code> INSERT/UPDATE/DELETE. Increments/decrements <code>room.occupied_count</code> and automatically toggles status between <code>AVAILABLE</code> and <code>FULL</code>.", style_bullet))
    story.append(Paragraph("• <code>trg_update_payment_status</code>: Fires on <code>payment</code> INSERT/UPDATE. Dynamically sums successful payments and transitions <code>student_fee.status</code> among <code>PENDING</code>, <code>PARTIAL</code>, and <code>PAID</code>.", style_bullet))
    story.append(Paragraph("• <code>allocate_room(p_student_id, p_room_id)</code>: Transactional stored function that verifies student active standing, checks bed availability, automatically closes prior allocations, and atomically assigns the student.", style_bullet))

    story.append(PageBreak())
    
    # =========================================================================
    # SECTION 7: ER DIAGRAM AND UML DIAGRAM
    # =========================================================================
    story.append(Paragraph("7. ER Diagram and UML Diagram", style_sec_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))
    story.append(Paragraph(
        "Below is the comprehensive, aligned <b>UML Class Diagram</b> for the ResiKeep / SmartHostel management system. "
        "It visualizes all 19 relational entities, defining their class attributes, data types, primary keys (PK), "
        "foreign keys (FK), unique constraints (UQ), and exact structural multiplicities (1, 0..1, N):", style_body
    ))
    story.append(Spacer(1, 4))
    
    uml_img_path = os.path.join(os.path.dirname(__file__), "uml_diagram.png")
    if os.path.exists(uml_img_path):
        # Printable width is 7.2 inches, height scaled proportionally
        story.append(Image(uml_img_path, width=7.2 * inch, height=4.05 * inch))
        story.append(Spacer(1, 6))
    
    story.append(Paragraph("<b>Figure 7.1:</b> ResiKeep Complete UML Class Diagram demonstrating 19 entity structures, attribute domains, and relational associations.", style_caption))
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("<b>Entity Cardinality & Multiplicity Breakdown:</b>", style_sec_h2))
    story.append(Paragraph("• <code>USERS (1) —— (0..1) STUDENT</code>: One-to-optional-one user login linkage for authenticated students.", style_bullet))
    story.append(Paragraph("• <code>USERS (1) —— (0..1) WARDEN</code>: One-to-optional-one user login linkage for assigned residential officers.", style_bullet))
    story.append(Paragraph("• <code>HOSTEL (1) —— (N) ROOM</code>: One hostel block contains multiple residential rooms.", style_bullet))
    story.append(Paragraph("• <code>STUDENT (1) —— (N) ROOM_ALLOCATION —— (1) ROOM</code>: Many-to-many relationship mediated by the allocation ledger.", style_bullet))
    story.append(Paragraph("• <code>STUDENT_FEE (1) —— (N) PAYMENT</code>: One student invoice may receive multiple partial installments.", style_bullet))

    story.append(PageBreak())
    
    # =========================================================================
    # SECTION 8: RELATIONAL SCHEMA
    # =========================================================================
    story.append(Paragraph("8. Relational Schema", style_sec_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))
    story.append(Paragraph(
        "The relational schema translates the conceptual UML model into formal relational database specifications. "
        "Each relation is defined with underlined Primary Keys, Foreign Keys (FK), and Unique constraints [UQ]:", style_body
    ))
    story.append(Spacer(1, 4))
    
    schema_img_path = os.path.join(os.path.dirname(__file__), "relational_schema.png")
    if os.path.exists(schema_img_path):
        story.append(Image(schema_img_path, width=7.2 * inch, height=4.75 * inch))
        story.append(Spacer(1, 6))
        
    story.append(Paragraph("<b>Figure 8.1:</b> ResiKeep Relational Schema Specification and Complete Foreign Key Referential Integrity Map.", style_caption))
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("<b>Foreign Key Referential Map Summary:</b>", style_sec_h2))
    story.append(Paragraph("• <code>STUDENT.User_ID → USERS.User_ID</code> | <code>WARDEN.User_ID → USERS.User_ID</code> | <code>NOTICE.User_ID → USERS.User_ID</code>", style_bullet))
    story.append(Paragraph("• <code>ROOM.Hostel_ID → HOSTEL.Hostel_ID</code> | <code>ROOM_ALLOCATION.Student_ID → STUDENT.Student_ID</code> | <code>ROOM_ALLOCATION.Room_ID → ROOM.Room_ID</code>", style_bullet))
    story.append(Paragraph("• <code>STUDENT_FEE.Student_ID → STUDENT.Student_ID</code> | <code>STUDENT_FEE.Fee_Structure_ID → FEE_STRUCTURE.Fee_Structure_ID</code>", style_bullet))
    story.append(Paragraph("• <code>PAYMENT.Fee_ID → STUDENT_FEE.Fee_ID</code> | <code>COMPLAINT.Student_ID → STUDENT.Student_ID</code> | <code>ATTENDANCE.Student_ID → STUDENT.Student_ID</code>", style_bullet))

    story.append(PageBreak())
    
    # =========================================================================
    # SECTION 9: DATABASE TABLES – STRUCTURES, KEYS & SAMPLE RECORDS
    # =========================================================================
    story.append(Paragraph("9. Database Tables – Structures, Keys & Sample Records", style_sec_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))
    story.append(Paragraph(
        "This section documents the physical PostgreSQL 18 table structures, attribute definitions, "
        "data types, constraints, and live sample records extracted directly from the seeded operational database:", style_body
    ))
    story.append(Spacer(1, 4))
    
    db_tables_data = fetch_database_metadata()
    
    for t_idx, t_info in enumerate(db_tables_data):
        t_block = []
        t_block.append(Paragraph(f"<b>Table 9.{t_idx+1}: <code>{t_info['name'].upper()}</code></b> — <i>{t_info['desc']}</i>", style_sec_h2))
        
        # Schema Table
        col_header = [Paragraph("<b>Attribute</b>", style_body_bold), Paragraph("<b>Data Type</b>", style_body_bold), Paragraph("<b>Nullable</b>", style_body_bold), Paragraph("<b>Constraint / Key</b>", style_body_bold)]
        col_rows = [col_header]
        
        for c in t_info['cols']:
            c_name = c[0]
            c_type = c[1]
            c_null = c[2]
            
            c_role = "—"
            if c_name.endswith("_id") and (c_name.startswith(t_info['name']) or c_name == 'id' or c_name == f"{t_info['name']}_id"):
                c_role = "<b>PK</b>"
            elif c_name.endswith("_id"):
                c_role = "<b>FK</b>"
            elif c_name in ('roll_no', 'email', 'username', 'transaction_id', 'hostel_name'):
                c_role = "<b>UQ</b>"
            
            col_rows.append([
                Paragraph(f"<code>{c_name}</code>", style_body),
                Paragraph(f"<font color='#475569'>{c_type}</font>", style_body),
                Paragraph(f"<font color='#475569'>{c_null}</font>", style_body),
                Paragraph(c_role, style_body)
            ])
            
        c_table = Table(col_rows, colWidths=[2.2 * inch, 2.3 * inch, 1.2 * inch, 1.5 * inch])
        c_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
            ('GRID', (0,0), (-1,-1), 0.5, border_color),
            ('PADDING', (0,0), (-1,-1), 3),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        t_block.append(c_table)
        t_block.append(Spacer(1, 4))
        
        # Sample Records Table
        if t_info['rows']:
            sample_cols = t_info['col_names'][:5]
            s_header = [Paragraph(f"<b>{c}</b>", style_body_bold) for c in sample_cols]
            s_rows = [s_header]
            for r in t_info['rows']:
                s_rows.append([Paragraph(format_cell_value(val), style_body) for val in r[:5]])
                
            sample_col_w = 7.2 * inch / len(sample_cols)
            s_table = Table(s_rows, colWidths=[sample_col_w] * len(sample_cols))
            s_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f8fafc")),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
                ('PADDING', (0,0), (-1,-1), 2.5),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))
            t_block.append(Paragraph("<b>Live Sample Data:</b>", ParagraphStyle('SubSub', fontName='Helvetica-Bold', fontSize=8, textColor=text_muted)))
            t_block.append(s_table)
            
        t_block.append(Spacer(1, 10))
        story.append(KeepTogether(t_block))
        
        # Group tables into sensible multi-page batches
        if (t_idx + 1) in (4, 9, 14):
            story.append(PageBreak())

    # =========================================================================
    # SECTION 10: CONCLUSION AND FUTURE SCOPE
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("10. Conclusion and Future Scope", style_sec_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))
    
    story.append(Paragraph("10.1. Project Conclusion", style_sec_h2))
    story.append(Paragraph(
        "<b>ResiKeep / SmartHostel</b> successfully establishes a robust, enterprise-grade relational database management "
        "system specifically engineered for multi-tenant educational hostel facilities. By rigorously applying database "
        "normalization principles up to <b>Boyce-Codd Normal Form (BCNF)</b>, the system completely eliminates redundant data "
        "storage, prevents update anomalies, and enforces referential consistency across all operational workflows.", style_body
    ))
    story.append(Paragraph(
        "The core innovation of the project lies in its active database implementation. By deploying server-side <b>PL/pgSQL triggers</b> "
        "and <b>transactional stored procedures</b>, operations such as room allocation concurrency locking, dynamic fee status updates, "
        "and resolution timestamp tracking occur with strict <b>ACID</b> compliance inside the PostgreSQL engine itself. "
        "Coupling this database foundation with a high-throughput FastAPI asynchronous REST backend and an intuitive React 19 web portal "
        "delivers sub-millisecond query responses, unified single-server deployment capability, and secure role-based access control.", style_body
    ))
    
    story.append(Paragraph("10.2. Future Scope & System Roadmap", style_sec_h2))
    story.append(Paragraph("1. <b>IoT Biometric Turnstile Hardware Integration:</b> Interfacing physical RFID turnstiles and facial recognition sensors directly with the <code>attendance</code> table using secure HMAC-authenticated webhook endpoints.", style_bullet))
    story.append(Paragraph("2. <b>AI-Powered Roommate Compatibility Matching:</b> Applying machine learning vector embeddings to student study habits, sleep schedules, and academic departments to optimize room allocation compatibility.", style_bullet))
    story.append(Paragraph("3. <b>Automated SMS / WhatsApp Guardian Gateways:</b> Trigger-driven instant notifications dispatched to parents and guardians upon approval of student out-passes and overnight leave requests.", style_bullet))
    story.append(Paragraph("4. <b>Payment Gateway Webhook Synchronization:</b> Direct integration with online banking UPI/Stripe/Razorpay webhooks for instant digital receipt generation and automated ledger reconciliation.", style_bullet))
    story.append(Paragraph("5. <b>Multi-Campus Database Federation:</b> Scaling the relational schema to support multi-campus university deployments using PostgreSQL declarative table partitioning and distributed read-replicas.", style_bullet))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"ReportLab: Successfully generated formal PDF Report at: {pdf_filepath}")


if __name__ == "__main__":
    out_dir = os.path.dirname(__file__)
    pdf_path = os.path.join(out_dir, "ResiKeep_DBMS_Project_Report.pdf")
    generate_project_report_pdf(pdf_path)
    
    # Also synchronize to user's root Downloads directory
    dl_path = r"C:\Users\Nethra R\Downloads\ResiKeep_DBMS_Project_Report.pdf"
    import shutil
    shutil.copyfile(pdf_path, dl_path)
    print(f"Copied final PDF to Downloads: {dl_path}")
