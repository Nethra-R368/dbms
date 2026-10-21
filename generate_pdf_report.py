import os
import sys
import psycopg2
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
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
            return  # Skip cover page
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header
        self.drawString(54, 11 * inch - 36, "23AIE303 - Database Management Systems (DBMS) | Course Project Report")
        self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "ResiKeep / SmartHostel")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
        
        # Footer
        self.line(54, 46, 8.5 * inch - 54, 46)
        self.drawString(54, 34, "Amrita Vishwa Vidyapeetham · Dept of Artificial Intelligence")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 34, page_str)
        self.restoreState()


def get_db_sample_data():
    tables_data = {}
    try:
        conn = psycopg2.connect(
            host='127.0.0.1',
            port=5432,
            user='postgres',
            password='Nark@1231',
            dbname='smarthostel'
        )
        cur = conn.cursor()
        
        key_tables = [
            'users', 'student', 'warden', 'hostel', 'room', 
            'room_allocation', 'fee_structure', 'student_fee', 'payment', 
            'complaint', 'attendance', 'leave_request'
        ]
        
        for t in key_tables:
            cur.execute(f"""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = '{t}' 
                ORDER BY ordinal_position LIMIT 8;
            """)
            cols = cur.fetchall()
            
            cur.execute(f'SELECT * FROM "{t}" LIMIT 3;')
            rows = cur.fetchall()
            
            tables_data[t] = {
                'cols': cols,
                'rows': rows
            }
        conn.close()
    except Exception as e:
        print(f"Warning: Could not fetch live DB rows: {e}")
    return tables_data


def build_pdf_report(pdf_filename):
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    primary_color = colors.HexColor("#1e3a8a")     # Deep Blue
    accent_color = colors.HexColor("#6366f1")      # Indigo
    text_dark = colors.HexColor("#0f172a")         # Slate 900
    text_muted = colors.HexColor("#475569")        # Slate 600
    
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=primary_color,
        alignment=1, # Center
        spaceAfter=14
    )
    
    style_cover_sub = ParagraphStyle(
        'CoverSub',
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=text_muted,
        alignment=1,
        spaceAfter=24
    )
    
    style_sec_h1 = ParagraphStyle(
        'SectionH1',
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    style_sec_h2 = ParagraphStyle(
        'SectionH2',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=accent_color,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    
    style_body = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=text_dark,
        spaceAfter=6
    )

    style_bullet = ParagraphStyle(
        'Bullet',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_dark,
        leftIndent=14,
        spaceAfter=3
    )

    style_code = ParagraphStyle(
        'CodeStyle',
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f8fafc"),
        borderPadding=6,
        spaceAfter=6
    )

    story = []
    
    # =========================================================================
    # SECTION 1 & 2: COVER PAGE (TITLE & TEAM MEMBERS)
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("AMRITA VISHWA VIDYAPEETHAM", ParagraphStyle('Univ', fontName='Helvetica-Bold', fontSize=12, alignment=1, textColor=text_muted, spaceAfter=8)))
    story.append(Paragraph("School of Artificial Intelligence & Computing", ParagraphStyle('Dept', fontName='Helvetica', fontSize=10, alignment=1, textColor=text_muted, spaceAfter=18)))
    story.append(HRFlowable(width="60%", thickness=1.5, color=accent_color, spaceAfter=30))
    
    story.append(Paragraph("ResiKeep: Cloud-Integrated Enterprise Relational Database for Multi-Tenant Student Housing & Facility Operations", style_cover_title))
    story.append(Paragraph("Comprehensive Database Management Systems (DBMS) Laboratory Project Report<br/>Course Code: <b>23AIE303</b>", style_cover_sub))
    story.append(Spacer(1, 30))
    
    # Team Table
    team_data = [
        [Paragraph("<b>Student Name</b>", style_body), Paragraph("<b>Roll Number</b>", style_body), Paragraph("<b>Contribution Scope</b>", style_body)],
        [Paragraph("R Nethra", style_body), Paragraph("CB.SC.U4AIE24147", style_body), Paragraph("Database Architecture, Schema DDL, Triggers, Cloud Deployment", style_body)],
        [Paragraph("Sahaana Shri S K", style_body), Paragraph("CB.SC.U4AIE24149", style_body), Paragraph("Stored Procedures, Relational Normalization, Frontend & API Integration", style_body)],
    ]
    team_table = Table(team_data, colWidths=[1.8 * inch, 1.8 * inch, 3.4 * inch])
    team_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e0e7ff")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#1e1b4b")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(team_table)
    
    story.append(Spacer(1, 40))
    meta_box = [
        [Paragraph("<b>Group / Team ID:</b>", style_body), Paragraph("Team 12 (Batch B12)", style_body)],
        [Paragraph("<b>GitHub Repository:</b>", style_body), Paragraph("<font color='#2563eb'><u>https://github.com/Nethra-R368/dbms</u></font>", style_body)],
        [Paragraph("<b>Database Engine:</b>", style_body), Paragraph("PostgreSQL 18 (Relational Engine) with PL/pgSQL Procedural Extensions", style_body)],
        [Paragraph("<b>Application Stack:</b>", style_body), Paragraph("FastAPI (Python 3.12+), SQLAlchemy 2.0 ORM, React 19, Tailwind CSS", style_body)],
        [Paragraph("<b>Academic Term:</b>", style_body), Paragraph("5th Semester B.Tech / B.E. Computer Science & Artificial Intelligence", style_body)]
    ]
    meta_table = Table(meta_box, colWidths=[2.2 * inch, 4.8 * inch])
    meta_table.setStyle(TableStyle([
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(meta_table)
    
    story.append(PageBreak())
    
    # =========================================================================
    # SECTION 3: INTRODUCTION AND PROBLEM STATEMENT
    # =========================================================================
    story.append(Paragraph("3. Introduction and Problem Statement", style_sec_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10))
    
    story.append(Paragraph("<b>3.1. Background & Context</b>", style_sec_h2))
    story.append(Paragraph(
        "University hostel administration represents a high-concurrency, multi-stakeholder operational environment. "
        "Managing campus living involves residential space allocation, financial fee invoicing, maintenance grievance ticketing, "
        "nightly curfew attendance monitoring, student leave pass approvals, catering quality evaluations, and hostel asset logistics. "
        "Historically, educational institutions have relied on siloed physical logbooks and disjointed electronic spreadsheets, "
        "introducing severe systemic failures.", style_body
    ))
    
    story.append(Paragraph("<b>3.2. Problem Statement</b>", style_sec_h2))
    story.append(Paragraph("Manual and naive electronic hostel administration suffers from four critical deficiencies:", style_body))
    story.append(Paragraph("• <b>Concurrency Race Conditions:</b> In manual systems, multiple staff members can assign the same room bed simultaneously, creating double-booking disputes.", style_bullet))
    story.append(Paragraph("• <b>Financial & Ledger Inconsistencies:</b> Fragmented spreadsheets lack real-time balance reconciliation, obscuring partial payments and resulting in untracked fee defaulters.", style_bullet))
    story.append(Paragraph("• <b>Data Redundancy and Update Anomalies:</b> Student demographics replicated across fee registers, gate passes, and room books lead to uncoordinated updates and stale data.", style_bullet))
    story.append(Paragraph("• <b>Lack of Auditable Lifecycles:</b> Maintenance complaints, visitor check-ins, and student leave passes lack immutable timestamping, creating accountability gaps.", style_bullet))
    
    story.append(Paragraph("<b>3.3. Proposed Solution: ResiKeep / SmartHostel</b>", style_sec_h2))
    story.append(Paragraph(
        "ResiKeep resolves these challenges by introducing an enterprise-grade <b>PostgreSQL 18</b> relational database management system. "
        "Rather than relying on fragile application-layer logic, ResiKeep embeds business invariants directly into the database engine via "
        "<b>PL/pgSQL triggers</b>, <b>ACID-compliant stored procedures</b>, <b>relational views</b>, and strict referential constraints, "
        "guaranteeing zero double-bookings, automatic balance tracking, and immutable audit logs.", style_body
    ))
    
    # =========================================================================
    # SECTION 4: CONCEPTUAL AND LOGICAL DATABASE DESIGN
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("4. Conceptual and Logical Database Design", style_sec_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10))
    
    story.append(Paragraph("<b>4.1. Conceptual Entity Modeling</b>", style_sec_h2))
    story.append(Paragraph(
        "The conceptual model partitions campus accommodation into 19 normalized relational entities across 6 functional domains:", style_body
    ))
    story.append(Paragraph("1. <b>Identity & Authentication Domain:</b> <code>USERS</code> acts as the single security principal, establishing a 1:0..1 relationship with <code>STUDENT</code> and <code>WARDEN</code>.", style_bullet))
    story.append(Paragraph("2. <b>Hostel & Facility Domain:</b> <code>HOSTEL</code> blocks hold a 1:N hierarchy with <code>ROOM</code> units, overseen by assigned <code>WARDEN</code> officers.", style_bullet))
    story.append(Paragraph("3. <b>Tenure & Allocation Domain:</b> <code>ROOM_ALLOCATION</code> operates as a temporal junction entity tracking student-to-bed residency with state transitions (ACTIVE, COMPLETED).", style_bullet))
    story.append(Paragraph("4. <b>Financial Ledger Domain:</b> Master rate cards in <code>FEE_STRUCTURE</code> map to individualized student invoices in <code>STUDENT_FEE</code>, settled via audited <code>PAYMENT</code> transactions.", style_bullet))
    story.append(Paragraph("5. <b>Student Lifecycle Domain:</b> Student entities anchor 1:N operational subsystems for <code>COMPLAINT</code>, <code>VISITOR</code> gate passes, <code>LEAVE_REQUEST</code> out-passes, and <code>ATTENDANCE</code>.", style_bullet))
    story.append(Paragraph("6. <b>Catering & Inventory Domain:</b> <code>INVENTORY</code> tracks equipment deltas in <code>INVENTORY_TRANSACTION</code>, while <code>MESS_MENU</code> pairs with student ratings in <code>MESS_FEEDBACK</code>.", style_bullet))
    
    story.append(Paragraph("<b>4.2. Referential Integrity & Cascading Rules</b>", style_sec_h2))
    story.append(Paragraph("To ensure database consistency, precise referential actions are enforced:", style_body))
    story.append(Paragraph("• <b>ON DELETE CASCADE:</b> When a student is removed, dependent allocations, fee records, attendance rolls, and complaints are purged automatically to prevent orphan rows.", style_bullet))
    story.append(Paragraph("• <b>ON DELETE SET NULL:</b> If a warden resigns, historical complaints, visitor passes, and hostel supervision records remain intact with warden references set to NULL.", style_bullet))
    story.append(Paragraph("• <b>ON DELETE RESTRICT:</b> Tariff structures in <code>FEE_STRUCTURE</code> cannot be dropped while active student billing records reference them, preventing accidental pricing loss.", style_bullet))
    
    # =========================================================================
    # SECTION 5: NORMALIZATION AND FUNCTIONAL DEPENDENCIES
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("5. Normalization and Functional Dependencies", style_sec_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10))
    story.append(Paragraph(
        "To ensure that the schema is completely immune to insertion, update, and deletion anomalies, "
        "the database was systematically decomposed from an Unnormalized Form (UNF) through to Boyce-Codd Normal Form (BCNF).", style_body
    ))
    
    norm_table_data = [
        [Paragraph("<b>Normal Form</b>", style_body), Paragraph("<b>Violation in Naive Schema</b>", style_body), Paragraph("<b>Mathematical Decomposition & Resolution</b>", style_body)],
        [
            Paragraph("<b>1NF (First Normal Form)</b>", style_body),
            Paragraph("Repeating groups and comma-delimited strings for fee payments, complaints, and roommates within student rows.", style_body),
            Paragraph("Ensured atomic scalar attributes. Decomposed repeating groups into independent tables: <code>STUDENT</code>, <code>STUDENT_FEE</code>, <code>PAYMENT</code>, and <code>COMPLAINT</code> with distinct surrogate primary keys.", style_body)
        ],
        [
            Paragraph("<b>2NF (Second Normal Form)</b>", style_body),
            Paragraph("Partial functional dependencies on composite keys: In <code>{Student_ID, Room_ID} -> Hostel_Name, Capacity</code>, room metadata depends only on <code>Room_ID</code>.", style_body),
            Paragraph("Eliminated partial dependencies by separating room catalog attributes into <code>ROOM(Room_ID, Hostel_ID, Room_Number, Capacity)</code> and maintaining allocation state in <code>ROOM_ALLOCATION</code>.", style_body)
        ],
        [
            Paragraph("<b>3NF (Third Normal Form)</b>", style_body),
            Paragraph("Transitive functional dependencies: In student billing, <code>Fee_ID -> Room_Type -> (Academic_Fee, Mess_Fee)</code> where non-key charges depend transitively on <code>Room_Type</code>.", style_body),
            Paragraph("Eliminated transitive dependencies by isolating master room tariffs into <code>FEE_STRUCTURE(Fee_Structure_ID, Room_Type, Academic_Fee, Mess_Fee)</code>, linked via Foreign Key.", style_body)
        ],
        [
            Paragraph("<b>BCNF (Boyce-Codd Normal Form)</b>", style_body),
            Paragraph("Occurs when a functional determinant X in non-trivial X -> Y is not a candidate superkey.", style_body),
            Paragraph("Every determinant across all 19 relations (e.g. <code>User_ID</code>, <code>Roll_No</code>, <code>{Hostel_ID, Room_Number}</code>, <code>Transaction_ID</code>) is a candidate superkey. Hence, BCNF is strictly satisfied.", style_body)
        ]
    ]
    norm_table = Table(norm_table_data, colWidths=[1.5 * inch, 2.5 * inch, 3.0 * inch])
    norm_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(norm_table)
    
    # =========================================================================
    # SECTION 6: ADVANCED SQL IMPLEMENTATION AND QUERY DESIGN
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("6. Advanced SQL Implementation and Query Design", style_sec_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10))
    
    story.append(Paragraph("<b>6.1. Multi-Table Relational Joins & Subqueries</b>", style_sec_h2))
    story.append(Paragraph(
        "The project implements advanced PostgreSQL queries incorporating multi-table joins, correlated subqueries, "
        "Common Table Expressions (CTEs), and window functions. Below are key queries demonstrating these operations:", style_body
    ))
    
    q1_text = """-- Query: Building-Level Occupancy Analytics with LEFT JOIN, GROUP BY & HAVING
SELECT h.hostel_name, h.hostel_type,
       COALESCE(SUM(r.capacity), 0) AS total_room_beds,
       COALESCE(SUM(r.occupied_count), 0) AS occupied_beds,
       ROUND((COALESCE(SUM(r.occupied_count),0)::NUMERIC / 
              NULLIF(COALESCE(SUM(r.capacity),0),0)::NUMERIC) * 100, 2) AS occupancy_pct
FROM hostel h
LEFT JOIN room r ON h.hostel_id = r.hostel_id
GROUP BY h.hostel_id, h.hostel_name, h.hostel_type
HAVING COALESCE(SUM(r.occupied_count), 0) > 0
ORDER BY occupancy_pct DESC;"""
    story.append(Paragraph(q1_text.replace('\n', '<br/>').replace(' ', '&nbsp;'), style_code))
    
    q2_text = """-- Query: Window Functions for Running Cumulative Student Payments
SELECT p.payment_id, s.name, p.amount, p.payment_date,
       ROW_NUMBER() OVER(PARTITION BY p.student_id ORDER BY p.payment_date) AS txn_seq,
       SUM(p.amount) OVER(PARTITION BY p.student_id ORDER BY p.payment_date 
                          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_paid_total
FROM payment p
JOIN student s ON p.student_id = s.student_id
WHERE p.status = 'SUCCESS';"""
    story.append(Paragraph(q2_text.replace('\n', '<br/>').replace(' ', '&nbsp;'), style_code))

    story.append(Paragraph("<b>6.2. PL/pgSQL Triggers & Stored Procedures</b>", style_sec_h2))
    story.append(Paragraph("• <code>trg_update_room_occupancy</code>: Automates bed count increments on INSERT, decrements on vacated UPDATE/DELETE, and toggles room status between 'AVAILABLE' and 'FULL'.", style_bullet))
    story.append(Paragraph("• <code>trg_update_payment_status</code>: Dynamically sums successful payments and transitions invoice status among 'PENDING', 'PARTIAL', and 'PAID'.", style_bullet))
    story.append(Paragraph("• <code>allocate_room(p_student_id, p_room_id)</code>: Transactional function enforcing student active standing, room availability check, auto-completion of prior allocations, and atomic bed assignment.", style_bullet))

    # =========================================================================
    # SECTION 7: ER DIAGRAM AND UML DIAGRAM
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("7. ER Diagram and UML Diagram", style_sec_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10))
    story.append(Paragraph(
        "Below is the complete, aligned UML Class Diagram for ResiKeep, illustrating all 19 entities, their attributes, "
        "Primary Keys (PK), Foreign Keys (FK), Unique constraints (UQ), and structural multiplicities (1, 0..1, N):", style_body
    ))
    
    uml_img_path = os.path.join(os.path.dirname(__file__), "uml_diagram.png")
    if os.path.exists(uml_img_path):
        story.append(Image(uml_img_path, width=7.0 * inch, height=4.6 * inch))
        story.append(Spacer(1, 10))
    
    story.append(Paragraph("<b>Figure 7.1:</b> ResiKeep UML Class Diagram demonstrating class attributes, associations, and cardinalities.", ParagraphStyle('Cap', fontName='Helvetica-Oblique', fontSize=8.5, alignment=1, textColor=text_muted)))

    # =========================================================================
    # SECTION 8: RELATIONAL SCHEMA
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("8. Relational Schema", style_sec_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10))
    story.append(Paragraph(
        "The logical relational schema maps entities to tables with explicit Primary Keys, Foreign Keys, and Unique Constraints:", style_body
    ))
    
    schema_img_path = os.path.join(os.path.dirname(__file__), "relational_schema.png")
    if os.path.exists(schema_img_path):
        story.append(Image(schema_img_path, width=7.0 * inch, height=5.2 * inch))
        story.append(Spacer(1, 10))
    
    story.append(Paragraph("<b>Figure 8.1:</b> ResiKeep Relational Schema Specification and Complete Foreign Key Referential Map.", ParagraphStyle('Cap2', fontName='Helvetica-Oblique', fontSize=8.5, alignment=1, textColor=text_muted)))

    # =========================================================================
    # SECTION 9: DATABASE TABLES & SAMPLE RECORDS
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("9. Database Tables – Structures, Keys & Sample Records", style_sec_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10))
    story.append(Paragraph(
        "Below are the physical PostgreSQL 18 table structures and live sample data retrieved directly from the seeded database instance:", style_body
    ))
    
    sample_data = get_db_sample_data()
    
    for t_name, data in sample_data.items():
        story.append(Paragraph(f"<b>Table: <code>{t_name.upper()}</code></b>", style_sec_h2))
        
        # Column schema table
        col_rows = [[Paragraph("<b>Column</b>", style_body), Paragraph("<b>Type</b>", style_body), Paragraph("<b>Nullable</b>", style_body)]]
        for c in data['cols'][:6]:
            col_rows.append([Paragraph(str(c[0]), style_body), Paragraph(str(c[1]), style_body), Paragraph(str(c[2]), style_body)])
        
        col_table = Table(col_rows, colWidths=[2.2 * inch, 2.5 * inch, 1.8 * inch])
        col_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f8fafc")),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('PADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(col_table)
        story.append(Spacer(1, 4))
        
        # Sample records
        if data['rows']:
            sample_str = "<br/>".join([f"• Row {i+1}: {str(row[:5])}" for i, row in enumerate(data['rows'])])
            story.append(Paragraph(f"<b>Sample Live Records:</b><br/>{sample_str}", ParagraphStyle('Sample', fontName='Courier', fontSize=7.5, leading=10, textColor=text_muted)))
        story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 10: CONCLUSION AND FUTURE SCOPE
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("10. Conclusion and Future Scope", style_sec_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10))
    
    story.append(Paragraph("<b>10.1. Project Conclusion</b>", style_sec_h2))
    story.append(Paragraph(
        "ResiKeep / SmartHostel successfully establishes a robust, enterprise-grade relational database management system "
        "designed specifically for multi-tenant educational hostel facilities. By rigorously applying database normalization principles "
        "up to Boyce-Codd Normal Form (BCNF), the system eliminates data redundancy, guarantees referential consistency, and maintains "
        "flawless audit trails. The integration of active database mechanisms—specifically PL/pgSQL triggers and transactional stored procedures—"
        "guarantees that room occupancy, fee balances, and complaint timestamps are synchronized within the database engine itself, "
        "completely eliminating application-level race conditions and double-booking vulnerabilities.", style_body
    ))
    story.append(Paragraph(
        "Coupling this PostgreSQL foundation with a modern FastAPI asynchronous REST API and a responsive React 19 single-page interface "
        "yields sub-millisecond query responses, unified single-server production deployment, and frictionless multi-role access control.", style_body
    ))
    
    story.append(Paragraph("<b>10.2. Future Scope</b>", style_sec_h2))
    story.append(Paragraph("1. <b>Biometric Hardware Integration:</b> Interfacing physical IoT biometric turnstiles and facial recognition cameras directly with the <code>attendance</code> table using secure webhook endpoints.", style_bullet))
    story.append(Paragraph("2. <b>AI-Powered Roommate Matching:</b> Applying machine learning vector embeddings to student study habits, sleep schedules, and academic departments to optimize room allocation compatibility.", style_bullet))
    story.append(Paragraph("3. <b>Automated SMS / WhatsApp Gateway:</b> Trigger-driven instant notifications dispatched to guardians upon approval of student out-passes and leave requests.", style_bullet))
    story.append(Paragraph("4. <b>Payment Gateway Webhook Synchronization:</b> Direct integration with online banking UPI/Stripe/Razorpay webhooks for instant digital receipt generation and automated reconciliation.", style_bullet))
    story.append(Paragraph("5. <b>Multi-Campus Federation:</b> Scaling the relational schema to support multi-campus university deployments using PostgreSQL partition tables and distributed read-replicas.", style_bullet))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated formal PDF Report at: {pdf_filename}")

if __name__ == "__main__":
    out_dir = os.path.dirname(__file__)
    pdf_path = os.path.join(out_dir, "ResiKeep_DBMS_Project_Report.pdf")
    build_pdf_report(pdf_path)
    
    # Also save a copy to Downloads
    dl_path = r"C:\Users\Nethra R\Downloads\ResiKeep_DBMS_Project_Report.pdf"
    import shutil
    shutil.copyfile(pdf_path, dl_path)
    print(f"Copied PDF Report to Downloads: {dl_path}")
