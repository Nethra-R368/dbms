import os

def create_uml_svg():
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1150" width="100%" height="100%" style="background-color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <defs>
    <style>
      .cls-title { font-size: 28px; font-weight: bold; fill: #1e293b; }
      .box { fill: #ffffff; stroke: #334155; stroke-width: 1.5; rx: 4; ry: 4; }
      .box-header { fill: #f8fafc; stroke: #334155; stroke-width: 1.5; }
      .header-text { font-size: 13px; font-weight: bold; fill: #0f172a; text-anchor: middle; }
      .attr-text { font-size: 11px; fill: #1e293b; font-family: 'Consolas', 'Courier New', monospace; }
      .pk { font-weight: bold; fill: #0f172a; }
      .fk { fill: #dc2626; font-weight: 600; }
      .uq { fill: #16a34a; font-weight: 600; }
      .line { stroke: #334155; stroke-width: 1.5; fill: none; }
      .cardinality { font-size: 11px; font-weight: bold; fill: #0f172a; }
    </style>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#334155" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="50" y="50" class="cls-title">UML Diagram – SmartHostel System</text>

  <!-- ================= ROW 1: USERS ================= -->
  <!-- USERS (x: 650, y: 70, w: 200, h: 100) -->
  <rect x="650" y="70" width="200" height="105" class="box" />
  <rect x="650" y="70" width="200" height="24" class="box-header" />
  <text x="750" y="87" class="header-text">USERS</text>
  <text x="660" y="110" class="attr-text"><tspan class="pk">+ user_id : int (PK)</tspan></text>
  <text x="660" y="126" class="attr-text">+ username : varchar(50) <tspan class="uq">(UQ)</tspan></text>
  <text x="660" y="142" class="attr-text">+ password_hash : varchar(255)</text>
  <text x="660" y="158" class="attr-text">+ role : varchar(20)</text>
  <text x="660" y="171" class="attr-text">+ created_at : datetime</text>

  <!-- ================= ROW 2: STUDENT, WARDEN, NOTICE ================= -->
  <!-- STUDENT (x: 420, y: 190, w: 180, h: 200) -->
  <rect x="420" y="190" width="180" height="210" class="box" />
  <rect x="420" y="190" width="180" height="24" class="box-header" />
  <text x="510" y="207" class="header-text">STUDENT</text>
  <text x="428" y="230" class="attr-text"><tspan class="pk">+ student_id : int (PK)</tspan></text>
  <text x="428" y="246" class="attr-text">+ user_id : int <tspan class="fk">(FK)</tspan></text>
  <text x="428" y="262" class="attr-text">+ roll_no : varchar(20) <tspan class="uq">(UQ)</tspan></text>
  <text x="428" y="278" class="attr-text">+ name : varchar(100)</text>
  <text x="428" y="294" class="attr-text">+ email : varchar(100) <tspan class="uq">(UQ)</tspan></text>
  <text x="428" y="310" class="attr-text">+ phone : varchar(15)</text>
  <text x="428" y="326" class="attr-text">+ department : varchar(100)</text>
  <text x="428" y="342" class="attr-text">+ year : varchar(10)</text>
  <text x="428" y="358" class="attr-text">+ gender : varchar(10)</text>
  <text x="428" y="374" class="attr-text">+ date_of_birth : date</text>
  <text x="428" y="390" class="attr-text">+ date_admission : date</text>
  <text x="428" y="398" class="attr-text">+ status : varchar(20)</text>

  <!-- WARDEN (x: 770, y: 195, w: 170, h: 125) -->
  <rect x="770" y="195" width="170" height="125" class="box" />
  <rect x="770" y="195" width="170" height="24" class="box-header" />
  <text x="855" y="212" class="header-text">WARDEN</text>
  <text x="778" y="235" class="attr-text"><tspan class="pk">+ warden_id : int (PK)</tspan></text>
  <text x="778" y="251" class="attr-text">+ user_id : int <tspan class="fk">(FK)</tspan></text>
  <text x="778" y="267" class="attr-text">+ name : varchar(100)</text>
  <text x="778" y="283" class="attr-text">+ email : varchar(100) <tspan class="uq">(UQ)</tspan></text>
  <text x="778" y="299" class="attr-text">+ phone : varchar(15)</text>
  <text x="778" y="315" class="attr-text">+ created_at : datetime</text>

  <!-- NOTICE (x: 1020, y: 195, w: 170, h: 135) -->
  <rect x="1020" y="195" width="170" height="135" class="box" />
  <rect x="1020" y="195" width="170" height="24" class="box-header" />
  <text x="1105" y="212" class="header-text">NOTICE</text>
  <text x="1028" y="235" class="attr-text"><tspan class="pk">+ notice_id : int (PK)</tspan></text>
  <text x="1028" y="251" class="attr-text">+ user_id : int <tspan class="fk">(FK)</tspan></text>
  <text x="1028" y="267" class="attr-text">+ title : varchar(200)</text>
  <text x="1028" y="283" class="attr-text">+ description : text</text>
  <text x="1028" y="299" class="attr-text">+ audience_type : varchar(50)</text>
  <text x="1028" y="315" class="attr-text">+ expiry_date : date</text>
  <text x="1028" y="327" class="attr-text">+ created_at : datetime</text>

  <!-- FEE_STRUCTURE (x: 160, y: 220, w: 170, h: 110) -->
  <rect x="160" y="220" width="170" height="110" class="box" />
  <rect x="160" y="220" width="170" height="24" class="box-header" />
  <text x="245" y="237" class="header-text">FEE_STRUCTURE</text>
  <text x="168" y="260" class="attr-text"><tspan class="pk">+ fee_structure_id : int (PK)</tspan></text>
  <text x="168" y="276" class="attr-text">+ room_type : varchar(20)</text>
  <text x="168" y="292" class="attr-text">+ academic_fee : decimal(10,2)</text>
  <text x="168" y="308" class="attr-text">+ mess_fee : decimal(10,2)</text>
  <text x="168" y="324" class="attr-text">+ caution_deposit : decimal(10,2)</text>

  <!-- STUDENT_FEE (x: 160, y: 375, w: 175, h: 140) -->
  <rect x="160" y="375" width="175" height="140" class="box" />
  <rect x="160" y="375" width="175" height="24" class="box-header" />
  <text x="247" y="392" class="header-text">STUDENT_FEE</text>
  <text x="168" y="415" class="attr-text"><tspan class="pk">+ fee_id : int (PK)</tspan></text>
  <text x="168" y="431" class="attr-text">+ student_id : int <tspan class="fk">(FK)</tspan></text>
  <text x="168" y="447" class="attr-text">+ fee_structure_id : int <tspan class="fk">(FK)</tspan></text>
  <text x="168" y="463" class="attr-text">+ amount_due : decimal(10,2)</text>
  <text x="168" y="479" class="attr-text">+ amount_paid : decimal(10,2)</text>
  <text x="168" y="495" class="attr-text">+ due_date : date</text>
  <text x="168" y="511" class="attr-text">+ status : varchar(20)</text>

  <!-- HOSTEL (x: 870, y: 345, w: 175, h: 110) -->
  <rect x="870" y="345" width="175" height="110" class="box" />
  <rect x="870" y="345" width="175" height="24" class="box-header" />
  <text x="957" y="362" class="header-text">HOSTEL</text>
  <text x="878" y="385" class="attr-text"><tspan class="pk">+ hostel_id : int (PK)</tspan></text>
  <text x="878" y="401" class="attr-text">+ warden_id : int <tspan class="fk">(FK)</tspan></text>
  <text x="878" y="417" class="attr-text">+ hostel_name : varchar(100) <tspan class="uq">(UQ)</tspan></text>
  <text x="878" y="433" class="attr-text">+ hostel_type : varchar(20)</text>
  <text x="878" y="449" class="attr-text">+ capacity : int</text>

  <!-- ================= ROW 3: STUDENT SUBSIDIARIES ================= -->
  <!-- COMPLAINT (x: 120, y: 560, w: 145, h: 175) -->
  <rect x="120" y="560" width="145" height="175" class="box" />
  <rect x="120" y="560" width="145" height="24" class="box-header" />
  <text x="192" y="577" class="header-text">COMPLAINT</text>
  <text x="128" y="600" class="attr-text"><tspan class="pk">+ complaint_id : int (PK)</tspan></text>
  <text x="128" y="616" class="attr-text">+ student_id : int <tspan class="fk">(FK)</tspan></text>
  <text x="128" y="632" class="attr-text">+ category : varchar(30)</text>
  <text x="128" y="648" class="attr-text">+ description : text</text>
  <text x="128" y="664" class="attr-text">+ priority : varchar(20)</text>
  <text x="128" y="680" class="attr-text">+ created_at : datetime</text>
  <text x="128" y="696" class="attr-text">+ status : varchar(20)</text>
  <text x="128" y="712" class="attr-text">+ resolved_at : datetime</text>
  <text x="128" y="728" class="attr-text">+ resolution : text</text>

  <!-- VISITOR (x: 275, y: 560, w: 140, h: 175) -->
  <rect x="275" y="560" width="140" height="175" class="box" />
  <rect x="275" y="560" width="140" height="24" class="box-header" />
  <text x="345" y="577" class="header-text">VISITOR</text>
  <text x="283" y="600" class="attr-text"><tspan class="pk">+ visitor_id : int (PK)</tspan></text>
  <text x="283" y="616" class="attr-text">+ student_id : int <tspan class="fk">(FK)</tspan></text>
  <text x="283" y="632" class="attr-text">+ visitor_name : varchar(100)</text>
  <text x="283" y="648" class="attr-text">+ relationship : varchar(50)</text>
  <text x="283" y="664" class="attr-text">+ phone : varchar(15)</text>
  <text x="283" y="680" class="attr-text">+ visit_date : date</text>
  <text x="283" y="696" class="attr-text">+ entry_time : time</text>
  <text x="283" y="712" class="attr-text">+ exit_time : time</text>
  <text x="283" y="728" class="attr-text">+ status : varchar(20)</text>

  <!-- LEAVE_REQUEST (x: 425, y: 560, w: 155, h: 185) -->
  <rect x="425" y="560" width="155" height="185" class="box" />
  <rect x="425" y="560" width="155" height="24" class="box-header" />
  <text x="502" y="577" class="header-text">LEAVE_REQUEST</text>
  <text x="433" y="600" class="attr-text"><tspan class="pk">+ leave_id : int (PK)</tspan></text>
  <text x="433" y="616" class="attr-text">+ student_id : int <tspan class="fk">(FK)</tspan></text>
  <text x="433" y="632" class="attr-text">+ pass_type : varchar(20)</text>
  <text x="433" y="648" class="attr-text">+ from_date : date</text>
  <text x="433" y="664" class="attr-text">+ to_date : date</text>
  <text x="433" y="680" class="attr-text">+ reason : varchar(255)</text>
  <text x="433" y="696" class="attr-text">+ destination : varchar(255)</text>
  <text x="433" y="712" class="attr-text">+ emergency_contact : var(15)</text>
  <text x="433" y="728" class="attr-text">+ status : varchar(20)</text>
  <text x="433" y="741" class="attr-text">+ action_date : datetime</text>

  <!-- ATTENDANCE (x: 590, y: 560, w: 145, h: 160) -->
  <rect x="590" y="560" width="145" height="160" class="box" />
  <rect x="590" y="560" width="145" height="24" class="box-header" />
  <text x="662" y="577" class="header-text">ATTENDANCE</text>
  <text x="598" y="600" class="attr-text"><tspan class="pk">+ attendance_id : int (PK)</tspan></text>
  <text x="598" y="616" class="attr-text">+ student_id : int <tspan class="fk">(FK)</tspan></text>
  <text x="598" y="632" class="attr-text">+ warden_id : int <tspan class="fk">(FK)</tspan></text>
  <text x="598" y="648" class="attr-text">+ date : date</text>
  <text x="598" y="664" class="attr-text">+ status : varchar(25)</text>
  <text x="598" y="680" class="attr-text">+ emergency_contact : var(15)</text>
  <text x="598" y="696" class="attr-text">+ remarks : text</text>
  <text x="598" y="712" class="attr-text">+ action_date : datetime</text>

  <!-- MESS_FEEDBACK (x: 745, y: 560, w: 135, h: 160) -->
  <rect x="745" y="560" width="135" height="160" class="box" />
  <rect x="745" y="560" width="135" height="24" class="box-header" />
  <text x="812" y="577" class="header-text">MESS_FEEDBACK</text>
  <text x="753" y="600" class="attr-text"><tspan class="pk">+ feedback_id : int (PK)</tspan></text>
  <text x="753" y="616" class="attr-text">+ student_id : int <tspan class="fk">(FK)</tspan></text>
  <text x="753" y="632" class="attr-text">+ warden_id : int <tspan class="fk">(FK)</tspan></text>
  <text x="753" y="648" class="attr-text">+ date : date</text>
  <text x="753" y="664" class="attr-text">+ food_quality : int</text>
  <text x="753" y="680" class="attr-text">+ taste : int</text>
  <text x="753" y="696" class="attr-text">+ cleanliness : int</text>
  <text x="753" y="712" class="attr-text">+ comments : text</text>

  <!-- ================= HOSTEL SUBSIDIARIES ================= -->
  <!-- INVENTORY (x: 900, y: 560, w: 140, h: 125) -->
  <rect x="900" y="560" width="140" height="125" class="box" />
  <rect x="900" y="560" width="140" height="24" class="box-header" />
  <text x="970" y="577" class="header-text">INVENTORY</text>
  <text x="908" y="600" class="attr-text"><tspan class="pk">+ item_id : int (PK)</tspan></text>
  <text x="908" y="616" class="attr-text">+ hostel_id : int <tspan class="fk">(FK)</tspan></text>
  <text x="908" y="632" class="attr-text">+ item_name : varchar(100)</text>
  <text x="908" y="648" class="attr-text">+ total_qty : int</text>
  <text x="908" y="664" class="attr-text">+ occupied_qty : int</text>
  <text x="908" y="680" class="attr-text">+ damaged_qty : int</text>

  <!-- MESS_MENU (x: 1050, y: 560, w: 135, h: 125) -->
  <rect x="1050" y="560" width="135" height="125" class="box" />
  <rect x="1050" y="560" width="135" height="24" class="box-header" />
  <text x="1117" y="577" class="header-text">MESS_MENU</text>
  <text x="1058" y="600" class="attr-text"><tspan class="pk">+ menu_id : int (PK)</tspan></text>
  <text x="1058" y="616" class="attr-text">+ hostel_id : int <tspan class="fk">(FK)</tspan></text>
  <text x="1058" y="632" class="attr-text">+ day_of_week : varchar(10)</text>
  <text x="1058" y="648" class="attr-text">+ breakfast : varchar(255)</text>
  <text x="1058" y="664" class="attr-text">+ lunch : varchar(255)</text>
  <text x="1058" y="680" class="attr-text">+ dinner : varchar(255)</text>

  <!-- ROOM (x: 1200, y: 560, w: 140, h: 155) -->
  <rect x="1200" y="560" width="140" height="155" class="box" />
  <rect x="1200" y="560" width="140" height="24" class="box-header" />
  <text x="1270" y="577" class="header-text">ROOM</text>
  <text x="1208" y="600" class="attr-text"><tspan class="pk">+ room_id : int (PK)</tspan></text>
  <text x="1208" y="616" class="attr-text">+ hostel_id : int <tspan class="fk">(FK)</tspan></text>
  <text x="1208" y="632" class="attr-text">+ room_number : varchar(20)</text>
  <text x="1208" y="648" class="attr-text">+ floor : varchar(10)</text>
  <text x="1208" y="664" class="attr-text">+ room_type : varchar(20)</text>
  <text x="1208" y="680" class="attr-text">+ capacity : int</text>
  <text x="1208" y="696" class="attr-text">+ occupied_count : int</text>
  <text x="1208" y="708" class="attr-text">+ status : varchar(20)</text>

  <!-- ================= ROW 4: BOTTOM NODES ================= -->
  <!-- ROOM_ALLOCATION (x: 280, y: 790, w: 145, h: 125) -->
  <rect x="280" y="790" width="145" height="125" class="box" />
  <rect x="280" y="790" width="145" height="24" class="box-header" />
  <text x="352" y="807" class="header-text">ROOM_ALLOCATION</text>
  <text x="288" y="830" class="attr-text"><tspan class="pk">+ allocation_id : int (PK)</tspan></text>
  <text x="288" y="846" class="attr-text">+ student_id : int <tspan class="fk">(FK)</tspan></text>
  <text x="288" y="862" class="attr-text">+ room_id : int <tspan class="fk">(FK)</tspan></text>
  <text x="288" y="878" class="attr-text">+ allocation_date : date</text>
  <text x="288" y="894" class="attr-text">+ vacated_date : date</text>
  <text x="288" y="907" class="attr-text">+ status : varchar(20)</text>

  <!-- PAYMENT (x: 450, y: 880, w: 165, h: 145) -->
  <rect x="450" y="880" width="165" height="145" class="box" />
  <rect x="450" y="880" width="165" height="24" class="box-header" />
  <text x="532" y="897" class="header-text">PAYMENT</text>
  <text x="458" y="920" class="attr-text"><tspan class="pk">+ payment_id : int (PK)</tspan></text>
  <text x="458" y="936" class="attr-text">+ fee_id : int <tspan class="fk">(FK)</tspan></text>
  <text x="458" y="952" class="attr-text">+ amount : decimal(10,2)</text>
  <text x="458" y="968" class="attr-text">+ payment_date : datetime</text>
  <text x="458" y="984" class="attr-text">+ payment_method : varchar(50)</text>
  <text x="458" y="1000" class="attr-text">+ transaction_id : var(100) <tspan class="uq">(UQ)</tspan></text>
  <text x="458" y="1016" class="attr-text">+ status : varchar(20)</text>

  <!-- INVENTORY_TRANSACTION (x: 880, y: 750, w: 160, h: 125) -->
  <rect x="880" y="750" width="160" height="125" class="box" />
  <rect x="880" y="750" width="160" height="24" class="box-header" />
  <text x="960" y="767" class="header-text">INVENTORY_TRANSACTION</text>
  <text x="888" y="790" class="attr-text"><tspan class="pk">+ transaction_id : int (PK)</tspan></text>
  <text x="888" y="806" class="attr-text">+ item_id : int <tspan class="fk">(FK)</tspan></text>
  <text x="888" y="822" class="attr-text">+ transaction_type : varchar(20)</text>
  <text x="888" y="838" class="attr-text">+ quantity : int</text>
  <text x="888" y="854" class="attr-text">+ remarks : text</text>
  <text x="888" y="870" class="attr-text">+ created_at : datetime</text>

  <!-- ROOM_CHANGE_REQUEST (x: 1190, y: 760, w: 155, h: 140) -->
  <rect x="1190" y="760" width="155" height="140" class="box" />
  <rect x="1190" y="760" width="155" height="24" class="box-header" />
  <text x="1267" y="777" class="header-text">ROOM_CHANGE_REQUEST</text>
  <text x="1198" y="800" class="attr-text"><tspan class="pk">+ request_id : int (PK)</tspan></text>
  <text x="1198" y="816" class="attr-text">+ student_id : int <tspan class="fk">(FK)</tspan></text>
  <text x="1198" y="832" class="attr-text">+ current_room : int <tspan class="fk">(FK)</tspan></text>
  <text x="1198" y="848" class="attr-text">+ requested_room : int <tspan class="fk">(FK)</tspan></text>
  <text x="1198" y="864" class="attr-text">+ reason : varchar(255)</text>
  <text x="1198" y="880" class="attr-text">+ status : varchar(20)</text>
  <text x="1198" y="894" class="attr-text">+ action_date : datetime</text>

  <!-- ================= CONNECTING LINES & CARDINALITIES ================= -->
  <!-- USERS -> STUDENT -->
  <path d="M 690 175 L 690 185 L 530 185 L 530 190" class="line" />
  <text x="695" y="183" class="cardinality">1</text>
  <text x="535" y="185" class="cardinality">0..1</text>

  <!-- USERS -> WARDEN -->
  <path d="M 790 175 L 790 185 L 830 185 L 830 195" class="line" />
  <text x="778" y="185" class="cardinality">1</text>
  <text x="835" y="190" class="cardinality">0..1</text>

  <!-- USERS -> NOTICE -->
  <path d="M 850 120 L 1090 120 L 1090 195" class="line" />
  <text x="855" y="115" class="cardinality">1</text>
  <text x="1095" y="190" class="cardinality">N</text>

  <!-- WARDEN -> HOSTEL -->
  <path d="M 855 320 L 855 380 L 870 380" class="line" />
  <text x="840" y="335" class="cardinality">1</text>
  <text x="858" y="375" class="cardinality">N</text>

  <!-- FEE_STRUCTURE -> STUDENT_FEE -->
  <path d="M 245 330 L 245 375" class="line" />
  <text x="250" y="345" class="cardinality">1</text>
  <text x="250" y="370" class="cardinality">N</text>

  <!-- STUDENT -> STUDENT_FEE -->
  <path d="M 420 370 L 335 390" class="line" />
  <text x="405" y="365" class="cardinality">1</text>
  <text x="340" y="385" class="cardinality">N</text>

  <!-- STUDENT_FEE -> PAYMENT -->
  <path d="M 230 515 L 230 920 L 450 920" class="line" />
  <text x="235" y="530" class="cardinality">1</text>
  <text x="435" y="915" class="cardinality">N</text>

  <!-- STUDENT -> COMPLAINT -->
  <path d="M 440 400 L 440 540 L 190 540 L 190 560" class="line" />
  <text x="445" y="415" class="cardinality">1</text>
  <text x="195" y="555" class="cardinality">N</text>

  <!-- STUDENT -> VISITOR -->
  <path d="M 460 400 L 460 540 L 345 540 L 345 560" class="line" />
  <text x="350" y="555" class="cardinality">N</text>

  <!-- STUDENT -> LEAVE_REQUEST -->
  <path d="M 490 400 L 490 560" class="line" />
  <text x="495" y="555" class="cardinality">N</text>

  <!-- STUDENT -> ATTENDANCE -->
  <path d="M 520 400 L 520 540 L 660 540 L 660 560" class="line" />
  <text x="665" y="555" class="cardinality">N</text>

  <!-- STUDENT -> MESS_FEEDBACK -->
  <path d="M 550 400 L 550 540 L 810 540 L 810 560" class="line" />
  <text x="815" y="555" class="cardinality">N</text>

  <!-- HOSTEL -> INVENTORY -->
  <path d="M 940 455 L 940 500 L 960 500 L 960 560" class="line" />
  <text x="945" y="470" class="cardinality">1</text>
  <text x="965" y="550" class="cardinality">N</text>

  <!-- HOSTEL -> MESS_MENU -->
  <path d="M 980 455 L 980 500 L 1100 500 L 1100 560" class="line" />
  <text x="1105" y="550" class="cardinality">N</text>

  <!-- HOSTEL -> ROOM -->
  <path d="M 1020 455 L 1020 500 L 1260 500 L 1260 560" class="line" />
  <text x="1265" y="550" class="cardinality">N</text>

  <!-- INVENTORY -> INVENTORY_TRANSACTION -->
  <path d="M 960 685 L 960 750" class="line" />
  <text x="965" y="700" class="cardinality">1</text>
  <text x="965" y="740" class="cardinality">N</text>

  <!-- STUDENT -> ROOM_ALLOCATION -->
  <path d="M 430 400 L 430 480 L 370 480 L 370 790" class="line" />
  <text x="375" y="780" class="cardinality">1</text>

  <!-- ROOM -> ROOM_ALLOCATION -->
  <path d="M 1200 660 L 680 660 L 680 840 L 425 840" class="line" />
  <text x="1180" y="655" class="cardinality">1</text>
  <text x="430" y="835" class="cardinality">N</text>

  <!-- ROOM -> ROOM_CHANGE_REQUEST (current & requested) -->
  <path d="M 1260 715 L 1260 760" class="line" />
  <text x="1265" y="730" class="cardinality">1</text>
  <text x="1265" y="750" class="cardinality">N</text>
</svg>"""
    return svg_content

def create_relational_schema_svg():
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1450 1120" width="100%" height="100%" style="background-color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <defs>
    <style>
      .card { fill: #ffffff; stroke: #8b5cf6; stroke-width: 2.5; rx: 8; ry: 8; }
      .title { font-size: 24px; font-weight: 800; fill: #0f172a; text-anchor: middle; letter-spacing: 0.5px; }
      .legend { font-size: 13px; font-weight: 600; fill: #334155; text-anchor: middle; }
      .legend-pk { text-decoration: underline; font-weight: bold; fill: #0f172a; }
      .legend-fk { fill: #dc2626; font-weight: bold; }
      .legend-uq { fill: #16a34a; font-weight: bold; }
      .schema-line { font-size: 13px; fill: #1e293b; font-family: 'Consolas', 'Courier New', monospace; }
      .tbl-name { font-weight: bold; fill: #0f172a; }
      .pk { text-decoration: underline; font-weight: bold; fill: #0f172a; }
      .fk { fill: #dc2626; font-weight: bold; }
      .uq { fill: #16a34a; font-weight: bold; }
      .section-hdr { font-size: 14px; font-weight: 800; fill: #0f172a; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; letter-spacing: 0.5px; }
      .ref-line { font-size: 11.5px; fill: #334155; font-family: 'Consolas', 'Courier New', monospace; }
    </style>
  </defs>

  <!-- Border Card -->
  <rect x="25" y="25" width="1400" height="1070" class="card" />

  <!-- Heading -->
  <text x="725" y="65" class="title">RELATIONAL SCHEMA – HOSTEL MANAGEMENT SYSTEM</text>
  <text x="725" y="95" class="legend">Notation: <tspan class="legend-pk">Underlined</tspan> = Primary Key | <tspan class="legend-fk">(FK)</tspan> = Foreign Key | <tspan class="legend-uq">[UQ]</tspan> = Unique Constraint</text>

  <!-- Line separator -->
  <line x1="50" y1="115" x2="1400" y2="115" stroke="#e2e8f0" stroke-width="1.5" />

  <!-- Schema 1 to 19 -->
  <text x="60" y="145" class="schema-line">1.  <tspan class="tbl-name">USERS</tspan>( <tspan class="pk">User_ID</tspan>, Username <tspan class="uq">[UQ]</tspan>, Password_Hash, Role, Created_At )</text>
  <text x="60" y="175" class="schema-line">2.  <tspan class="tbl-name">STUDENT</tspan>( <tspan class="pk">Student_ID</tspan>, <tspan class="fk">User_ID (FK)</tspan>, Roll_No <tspan class="uq">[UQ]</tspan>, Name, Email <tspan class="uq">[UQ]</tspan>, Phone, Department, Year, Gender, Date_Of_Birth, Date_Admission, Status )</text>
  <text x="60" y="205" class="schema-line">3.  <tspan class="tbl-name">WARDEN</tspan>( <tspan class="pk">Warden_ID</tspan>, <tspan class="fk">User_ID (FK)</tspan>, Name, Email <tspan class="uq">[UQ]</tspan>, Phone, Created_At )</text>
  <text x="60" y="235" class="schema-line">4.  <tspan class="tbl-name">NOTICE</tspan>( <tspan class="pk">Notice_ID</tspan>, <tspan class="fk">User_ID (FK)</tspan>, Title, Description, Audience_Type, Expiry_Date, Created_At )</text>
  <text x="60" y="265" class="schema-line">5.  <tspan class="tbl-name">FEE_STRUCTURE</tspan>( <tspan class="pk">Fee_Structure_ID</tspan>, Room_Type, Academic_Fee, Mess_Fee, Caution_Deposit )</text>
  <text x="60" y="295" class="schema-line">6.  <tspan class="tbl-name">STUDENT_FEE</tspan>( <tspan class="pk">Fee_ID</tspan>, <tspan class="fk">Student_ID (FK)</tspan>, <tspan class="fk">Fee_Structure_ID (FK)</tspan>, Amount_Due, Amount_Paid, Due_Date, Status )</text>
  <text x="60" y="325" class="schema-line">7.  <tspan class="tbl-name">COMPLAINT</tspan>( <tspan class="pk">Complaint_ID</tspan>, <tspan class="fk">Student_ID (FK)</tspan>, Category, Description, Priority, Created_At, Status, Resolved_At, Resolution )</text>
  <text x="60" y="355" class="schema-line">8.  <tspan class="tbl-name">VISITOR</tspan>( <tspan class="pk">Visitor_ID</tspan>, <tspan class="fk">Student_ID (FK)</tspan>, Visitor_Name, Relationship, Phone, Visit_Date, Entry_Time, Exit_Time, Status )</text>
  <text x="60" y="385" class="schema-line">9.  <tspan class="tbl-name">LEAVE_REQUEST</tspan>( <tspan class="pk">Leave_ID</tspan>, <tspan class="fk">Student_ID (FK)</tspan>, Pass_Type, From_Date, To_Date, Reason, Destination, Emergency_Contact, Status, Action_Date )</text>
  <text x="60" y="415" class="schema-line">10. <tspan class="tbl-name">ATTENDANCE</tspan>( <tspan class="pk">Attendance_ID</tspan>, <tspan class="fk">Student_ID (FK)</tspan>, <tspan class="fk">Warden_ID (FK)</tspan>, Date, Status, Emergency_Contact, Remarks, Action_Date )</text>
  <text x="60" y="445" class="schema-line">11. <tspan class="tbl-name">MESS_FEEDBACK</tspan>( <tspan class="pk">Feedback_ID</tspan>, <tspan class="fk">Student_ID (FK)</tspan>, <tspan class="fk">Warden_ID (FK)</tspan>, Date, Food_Quality, Taste, Cleanliness, Comments )</text>
  <text x="60" y="475" class="schema-line">12. <tspan class="tbl-name">HOSTEL</tspan>( <tspan class="pk">Hostel_ID</tspan>, <tspan class="fk">Warden_ID (FK)</tspan>, Hostel_Name <tspan class="uq">[UQ]</tspan>, Hostel_Type, Capacity )</text>
  <text x="60" y="505" class="schema-line">13. <tspan class="tbl-name">INVENTORY</tspan>( <tspan class="pk">Item_ID</tspan>, <tspan class="fk">Hostel_ID (FK)</tspan>, Item_Name, Total_Qty, Occupied_Qty, Damaged_Qty )</text>
  <text x="60" y="535" class="schema-line">14. <tspan class="tbl-name">MESS_MENU</tspan>( <tspan class="pk">Menu_ID</tspan>, <tspan class="fk">Hostel_ID (FK)</tspan>, Day_Of_Week, Breakfast, Lunch, Dinner )</text>
  <text x="60" y="565" class="schema-line">15. <tspan class="tbl-name">ROOM</tspan>( <tspan class="pk">Room_ID</tspan>, <tspan class="fk">Hostel_ID (FK)</tspan>, Room_Number, Floor, Room_Type, Capacity, Occupied_Count, Status )</text>
  <text x="60" y="595" class="schema-line">16. <tspan class="tbl-name">ROOM_ALLOCATION</tspan>( <tspan class="pk">Allocation_ID</tspan>, <tspan class="fk">Student_ID (FK)</tspan>, <tspan class="fk">Room_ID (FK)</tspan>, Allocation_Date, Vacated_Date, Status )</text>
  <text x="60" y="625" class="schema-line">17. <tspan class="tbl-name">INVENTORY_TRANSACTION</tspan>( <tspan class="pk">Transaction_ID</tspan>, <tspan class="fk">Item_ID (FK)</tspan>, Transaction_Type, Quantity, Remarks, Created_At )</text>
  <text x="60" y="655" class="schema-line">18. <tspan class="tbl-name">ROOM_CHANGE_REQUEST</tspan>( <tspan class="pk">Request_ID</tspan>, <tspan class="fk">Student_ID (FK)</tspan>, <tspan class="fk">Current_Room (FK)</tspan>, <tspan class="fk">Requested_Room (FK)</tspan>, Reason, Status, Action_Date )</text>
  <text x="60" y="685" class="schema-line">19. <tspan class="tbl-name">PAYMENT</tspan>( <tspan class="pk">Payment_ID</tspan>, <tspan class="fk">Fee_ID (FK)</tspan>, Amount, Payment_Date, Payment_Method, Transaction_ID <tspan class="uq">[UQ]</tspan>, Status )</text>

  <!-- Line separator -->
  <line x1="50" y1="720" x2="1400" y2="720" stroke="#cbd5e1" stroke-width="1.5" />

  <!-- Foreign Key References -->
  <text x="60" y="750" class="section-hdr">FOREIGN KEY REFERENCES:</text>
  
  <text x="60" y="780" class="ref-line">STUDENT.User_ID &#8594; USERS.User_ID  |  WARDEN.User_ID &#8594; USERS.User_ID  |  NOTICE.User_ID &#8594; USERS.User_ID</text>
  <text x="60" y="810" class="ref-line">STUDENT_FEE.Student_ID &#8594; STUDENT.Student_ID  |  STUDENT_FEE.Fee_Structure_ID &#8594; FEE_STRUCTURE.Fee_Structure_ID</text>
  <text x="60" y="840" class="ref-line">COMPLAINT.Student_ID &#8594; STUDENT.Student_ID  |  VISITOR.Student_ID &#8594; STUDENT.Student_ID  |  LEAVE_REQUEST.Student_ID &#8594; STUDENT.Student_ID</text>
  <text x="60" y="870" class="ref-line">ATTENDANCE.Student_ID &#8594; STUDENT.Student_ID  |  ATTENDANCE.Warden_ID &#8594; WARDEN.Warden_ID</text>
  <text x="60" y="900" class="ref-line">MESS_FEEDBACK.Student_ID &#8594; STUDENT.Student_ID  |  MESS_FEEDBACK.Warden_ID &#8594; WARDEN.Warden_ID</text>
  <text x="60" y="930" class="ref-line">HOSTEL.Warden_ID &#8594; WARDEN.Warden_ID  |  INVENTORY.Hostel_ID &#8594; HOSTEL.Hostel_ID  |  MESS_MENU.Hostel_ID &#8594; HOSTEL.Hostel_ID</text>
  <text x="60" y="960" class="ref-line">ROOM.Hostel_ID &#8594; HOSTEL.Hostel_ID  |  ROOM_ALLOCATION.Student_ID &#8594; STUDENT.Student_ID  |  ROOM_ALLOCATION.Room_ID &#8594; ROOM.Room_ID</text>
  <text x="60" y="990" class="ref-line">INVENTORY_TRANSACTION.Item_ID &#8594; INVENTORY.Item_ID  |  ROOM_CHANGE_REQUEST.Student_ID &#8594; STUDENT.Student_ID</text>
  <text x="60" y="1020" class="ref-line">ROOM_CHANGE_REQUEST.Current_Room &#8594; ROOM.Room_ID  |  ROOM_CHANGE_REQUEST.Requested_Room &#8594; ROOM.Room_ID</text>
  <text x="60" y="1050" class="ref-line">PAYMENT.Fee_ID &#8594; STUDENT_FEE.Fee_ID</text>
</svg>"""
    return svg_content

if __name__ == "__main__":
    out_dir = os.path.dirname(__file__)
    with open(os.path.join(out_dir, "uml_diagram.svg"), "w", encoding="utf-8") as f:
        f.write(create_uml_svg())
    with open(os.path.join(out_dir, "relational_schema.svg"), "w", encoding="utf-8") as f:
        f.write(create_relational_schema_svg())
    print("Successfully generated uml_diagram.svg and relational_schema.svg!")
