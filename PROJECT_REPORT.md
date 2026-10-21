# SmartHostel: Comprehensive Database Management System (DBMS) Project Report
**Course:** Database Management Systems (DBMS)  
**Academic Project:** 5th Semester B.Tech / B.E. Computer Science & Engineering  
**Project Repository:** [https://github.com/Nethra-R368/dbms](https://github.com/Nethra-R368/dbms)  
**Tech Stack:** PostgreSQL 18, PL/pgSQL, FastAPI (Python 3.12+), SQLAlchemy 2.0 ORM, React 19, Vite, Tailwind CSS, REST APIs, JWT Security  

---

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Problem Statement & System Objectives](#2-problem-statement--system-objectives)
3. [System Architecture & Layered Design](#3-system-architecture--layered-design)
4. [Deep Dive: Database Management System (DBMS) Architecture](#4-deep-dive-database-management-system-dbms-architecture)
   - 4.1. [Conceptual Modeling & Entity-Relationship (ER) Design](#41-conceptual-modeling--entity-relationship-er-design)
   - 4.2. [Relational Schema & Detailed Data Dictionary (21 Tables)](#42-relational-schema--detailed-data-dictionary-21-tables)
   - 4.3. [Database Normalization Analysis & Mathematical Proofs (1NF to BCNF)](#43-database-normalization-analysis--mathematical-proofs-1nf-to-bcnf)
   - 4.4. [Relational Database Views (Virtual Tables)](#44-relational-database-views-virtual-tables)
   - 4.5. [Database Triggers & Business Logic Automation (PL/pgSQL)](#45-database-triggers--business-logic-automation-plpgsql)
   - 4.6. [Stored Procedures, Functions & ACID Transaction Integrity](#46-stored-procedures-functions--acid-transaction-integrity)
   - 4.7. [Indexing Strategies & Query Performance Optimization](#47-indexing-strategies--query-performance-optimization)
   - 4.8. [Database Security, Referential Integrity & Access Control](#48-database-security-referential-integrity--access-control)
5. [Backend Architecture & REST API Implementation](#5-backend-architecture--rest-api-implementation)
6. [Frontend Architecture & Role-Based Portals](#6-frontend-architecture--role-based-portals)
7. [Testing, Verification & Concurrency Validation](#7-testing-verification--concurrency-validation)
8. [End-to-End Deployment Lifecycle](#8-end-to-end-deployment-lifecycle)
   - 8.1. [Local Development Setup](#81-local-development-setup)
   - 8.2. [Automated Single-Server Unified Production Build](#82-automated-single-server-unified-production-build)
   - 8.3. [Public HTTPS Tunnel Deployment](#83-public-https-tunnel-deployment)
   - 8.4. [Enterprise Cloud Deployment (Azure Database for PostgreSQL & AWS RDS)](#84-enterprise-cloud-deployment-azure-database-for-postgresql--aws-rds)
9. [Repository Organization & File Manifest](#9-repository-organization--file-manifest)
10. [Conclusion & Future Enhancements](#10-conclusion--future-enhancements)

---

## 1. Executive Summary

**SmartHostel** is an enterprise-grade, relational-database-driven web application designed to automate, streamline, and audit the end-to-end operational lifecycle of university hostel accommodations. Built specifically to demonstrate advanced concepts in **Database Management Systems (DBMS)**, the application addresses real-world challenges such as concurrent room allocation races, fee discrepancy tracking, automated student attendance reconciliation, complaint escalation auditing, visitor gate-pass issuance, and mess feedback aggregation.

The cornerstone of the system is a highly normalized **PostgreSQL 18** relational database engine operating under the **Third Normal Form (3NF)** and **Boyce-Codd Normal Form (BCNF)**. Rather than delegating business rules exclusively to application code, SmartHostel embeds core business invariants directly into the database engine using:
- **PL/pgSQL Triggers** for real-time room capacity tracking and ledger payment calculations.
- **Stored Procedures / PL/pgSQL Functions** guaranteeing **ACID** (Atomicity, Consistency, Isolation, Durability) transaction semantics during student room assignment and vacate cycles.
- **Relational Views** for consolidated operational reporting without performance-degrading duplicate data storage.
- **B-Tree & Partial Secondary Indexes** for rapid query filtering and low-latency joins.

Complementing the robust database engine is an asynchronous, high-throughput backend written in **FastAPI (Python)** using **SQLAlchemy 2.0 ORM** and **Pydantic** data validation, alongside an ultra-responsive client application built with **React 19**, **Vite**, and **Tailwind CSS**.

---

## 2. Problem Statement & System Objectives

### 2.1. Traditional Hostel Management Challenges
1. **Manual Record Keeping & Data Redundancy**: Paper logbooks and disjointed spreadsheets suffer from severe update, insertion, and deletion anomalies.
2. **Double-Booking & Race Conditions**: In manual or naive electronic systems, multiple staff members can assign the same room bed simultaneously, causing student disputes.
3. **Financial Inconsistencies**: Manual fee collection often leads to untracked partial payments, late fee calculation mistakes, and lack of real-time balance reconciliation.
4. **Delayed Complaint Resolution**: Students have no visibility into maintenance requests, while wardens lack categorized dashboards to prioritize urgent issues (electrical, plumbing, security).
5. **Security & Gate Pass Gaps**: Inability to quickly verify student leave requests, emergency contacts, and external visitor check-in/check-out logs.

### 2.2. SmartHostel Core Objectives
- **Zero Double-Bookings**: Guaranteed at the database level via atomic stored procedures and table-level constraints.
- **Automated Financial Reconciliation**: Trigger-driven fee ledger synchronization upon verified transaction insertion.
- **Role-Based Access Control (RBAC)**: Strict separation of concerns across four primary user personas: **Administrator**, **Warden**, **Student**, and **Accountant**.
- **Auditable Lifecycle Tracking**: Timestamped logs for complaint resolution, leave passes, visitor checkouts, and room transfers.
- **Seamless Deployment**: Multi-environment support spanning local development, single-binary unified serving, and cloud infrastructure (Azure PostgreSQL & AWS RDS).

---

## 3. System Architecture & Layered Design

SmartHostel follows a modern **3-Tier Enterprise Architecture**:

```mermaid
graph TD
    subgraph Client Tier [Presentation Tier - React 19 + Vite + Tailwind CSS]
        UI_Admin[Admin Dashboard]
        UI_Warden[Warden Console]
        UI_Student[Student Portal]
        UI_Accountant[Accountant Ledger]
    end

    subgraph App Tier [Application & API Tier - FastAPI + Uvicorn]
        AuthRouter["/api/auth (JWT Authentication & RBAC)"]
        StudentRouter["/api/student (Profile, Roommates, Leaves, Complaints)"]
        WardenRouter["/api/warden (Allocations, Attendance, Approvals)"]
        AcctRouter["/api/accountant (Fee Structures, Payments, Defaulters)"]
        AdminRouter["/api/admin (Hostels, Rooms, Wardens, Inventory, Notices)"]
        CommonRouter["/api/common (Public & Shared Catalogs)"]
        ORM[SQLAlchemy 2.0 ORM & Connection Pool]
    end

    subgraph Database Tier [Database Engine Tier - PostgreSQL 18]
        Tables[(21 Relational Tables)]
        Views[(Database Views: available_rooms, hostel_occupancy, pending_fees, complaint_summary)]
        Triggers[(PL/pgSQL Triggers: trg_update_room_occupancy, trg_update_payment_status, trg_complaint_resolution)]
        Procedures[(Stored Procedures: allocate_room, vacate_room)]
        Indexes[(B-Tree & Partial Secondary Indexes)]
    end

    Client Tier -->|REST HTTP / JSON + Bearer JWT| App Tier
    App Tier -->|Parameterized SQL Queries & Connection Pooling| Database Tier
```

---

## 4. Deep Dive: Database Management System (DBMS) Architecture

### 4.1. Conceptual Modeling & Entity-Relationship (ER) Design

The database schema models complex interactions between residential real estate, educational personnel, financial transactions, maintenance ticketing, and inventory logistics.

#### Key Entities:
1. **User**: Authentication credentials and RBAC authorization identity (`ADMIN`, `WARDEN`, `STUDENT`, `ACCOUNTANT`).
2. **Hostel**: Physical residential building with defined capacity and dedicated warden supervision.
3. **Room**: Individual dwelling units inside a hostel, categorized by layout (`SINGLE`, `DOUBLE`, `TRIPLE`, `COMMON`).
4. **Student**: University resident with academic roll number, department, year, and contact metadata.
5. **Warden**: Administrative supervisory personnel assigned to manage hostels, approve leaves, and oversee facilities.
6. **Room Allocation**: Temporal junction entity tracking student-to-room tenure (`ACTIVE`, `COMPLETED`, `CANCELLED`).
7. **Fee Structure & Student Fee**: Financial templates and individualized student payment obligations.
8. **Payment**: Audited monetary transactions linked directly to specific student fees.
9. **Complaint**: Maintenance and welfare tickets with status lifecycle (`NEW` $\to$ `ASSIGNED` $\to$ `IN_PROGRESS` $\to$ `RESOLVED`).
10. **Leave Request**: Digital out-pass and home-pass applications with warden sign-off.
11. **Visitor**: Gate registry for campus visitors with check-in and check-out timestamps.
12. **Attendance**: Daily morning/evening residential presence rolls.
13. **Inventory & Transaction**: Hostel furniture, fixtures, and amenity stock management.
14. **Mess Menu & Feedback**: Weekly food planning and student rating system.

#### Mermaid Entity-Relationship Diagram:

```mermaid
erDiagram
    USERS ||--o| STUDENT : "has profile"
    USERS ||--o| WARDEN : "has profile"
    USERS ||--o{ NOTICE : "authors"

    WARDEN ||--o{ HOSTEL : "supervises"
    WARDEN ||--o{ COMPLAINT : "resolves"
    WARDEN ||--o{ LEAVE_REQUEST : "approves"
    WARDEN ||--o{ VISITOR : "authorizes"
    WARDEN ||--o{ ATTENDANCE : "marks"

    HOSTEL ||--|{ ROOM : "contains"
    HOSTEL ||--o{ INVENTORY : "stores"
    HOSTEL ||--o{ MESS_MENU : "serves"

    ROOM ||--o{ ROOM_ALLOCATION : "assigned to"
    STUDENT ||--o{ ROOM_ALLOCATION : "occupies"

    FEE_STRUCTURE ||--o{ STUDENT_FEE : "defines rate for"
    STUDENT ||--o{ STUDENT_FEE : "billed with"
    STUDENT_FEE ||--o{ PAYMENT : "settled by"
    STUDENT ||--o{ PAYMENT : "executes"

    STUDENT ||--o{ COMPLAINT : "files"
    STUDENT ||--o{ LEAVE_REQUEST : "submits"
    STUDENT ||--o{ ROOM_CHANGE_REQUEST : "requests"
    STUDENT ||--o{ VISITOR : "receives"
    STUDENT ||--o{ ATTENDANCE : "recorded in"
    STUDENT ||--o{ MESS_FEEDBACK : "submits"

    INVENTORY ||--o{ INVENTORY_TRANSACTION : "logged in"
```

---

### 4.2. Relational Schema & Detailed Data Dictionary (21 Tables)

The schema utilizes strict PostgreSQL data types, non-null assertions, foreign keys with explicit referential integrity triggers, and domain-level `CHECK` constraints.

#### 1. `users` (Authentication & Security Principal)
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `user_id` | `SERIAL` | `PRIMARY KEY` | Unique surrogate key for user account |
| `username` | `VARCHAR(50)` | `UNIQUE`, `NOT NULL` | Unique login identifier |
| `password_hash` | `VARCHAR(255)` | `NOT NULL` | Bcrypt salt-hashed password string |
| `role` | `VARCHAR(20)` | `NOT NULL`, `CHECK (role IN ('ADMIN', 'WARDEN', 'STUDENT', 'ACCOUNTANT'))` | System RBAC authorization role |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Account registration timestamp |

#### 2. `warden` (Hostel Administrative Officers)
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `warden_id` | `SERIAL` | `PRIMARY KEY` | Unique warden identifier |
| `user_id` | `INT` | `REFERENCES users(user_id) ON DELETE CASCADE` | Linked authentication account |
| `name` | `VARCHAR(100)` | `NOT NULL` | Full name of warden |
| `email` | `VARCHAR(100)` | `UNIQUE`, `NOT NULL` | Institutional email address |
| `phone` | `VARCHAR(15)` | — | Contact telephone number |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Profile creation timestamp |

#### 3. `hostel` (Residential Hostel Blocks)
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `hostel_id` | `SERIAL` | `PRIMARY KEY` | Unique hostel identifier |
| `hostel_name` | `VARCHAR(100)` | `UNIQUE`, `NOT NULL` | Unique building title |
| `hostel_type` | `VARCHAR(20)` | `CHECK (hostel_type IN ('BOYS', 'GIRLS', 'COED'))` | Demographic classification |
| `capacity` | `INT` | `NOT NULL`, `CHECK (capacity > 0)` | Maximum resident capacity |
| `warden_id` | `INT` | `REFERENCES warden(warden_id) ON DELETE SET NULL` | Assigned chief supervisor |

#### 4. `room` (Living Units & Capacity Management)
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `room_id` | `SERIAL` | `PRIMARY KEY` | Unique room identifier |
| `hostel_id` | `INT` | `REFERENCES hostel(hostel_id) ON DELETE CASCADE` | Parent hostel building |
| `room_number` | `VARCHAR(20)` | `NOT NULL` | Room designation (e.g., 'A-101') |
| `floor` | `INT` | `NOT NULL` | Floor index (0 for Ground, 1, 2, etc.) |
| `room_type` | `VARCHAR(30)` | `CHECK (room_type IN ('SINGLE', 'DOUBLE', 'TRIPLE', 'COMMON'))` | Bed layout category |
| `capacity` | `INT` | `NOT NULL` | Number of allowable beds |
| `occupied_count` | `INT` | `DEFAULT 0`, `CHECK (occupied_count >= 0 AND occupied_count <= capacity)` | Real-time occupants |
| `status` | `VARCHAR(20)` | `DEFAULT 'AVAILABLE'`, `CHECK (status IN ('AVAILABLE', 'FULL', 'MAINTENANCE'))` | Availability state |
*Constraint:* `UNIQUE(hostel_id, room_number)` prevents duplicate room numbering within the same hostel.

#### 5. `student` (Hostel Residents)
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `student_id` | `SERIAL` | `PRIMARY KEY` | Unique student surrogate key |
| `user_id` | `INT` | `REFERENCES users(user_id) ON DELETE CASCADE` | Linked authentication account |
| `roll_no` | `VARCHAR(20)` | `UNIQUE`, `NOT NULL` | University registration number |
| `name` | `VARCHAR(100)` | `NOT NULL` | Full student name |
| `email` | `VARCHAR(100)` | `UNIQUE`, `NOT NULL` | Contact email address |
| `phone` | `VARCHAR(15)` | — | Student phone number |
| `department` | `VARCHAR(100)` | — | Academic engineering department |
| `year` | `INT` | — | Current academic year (1-4) |
| `gender` | `VARCHAR(20)` | — | Demographic gender |
| `date_of_birth` | `DATE` | — | Birth date |
| `admission_date` | `DATE` | `DEFAULT CURRENT_DATE` | Hostel admission date |
| `status` | `VARCHAR(20)` | `DEFAULT 'ACTIVE'`, `CHECK (status IN ('ACTIVE', 'GRADUATED', 'SUSPENDED', 'LEFT'))` | Residency status |

#### 6. `room_allocation` (Temporal Resident Assignment)
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `allocation_id` | `SERIAL` | `PRIMARY KEY` | Unique allocation event key |
| `student_id` | `INT` | `REFERENCES student(student_id) ON DELETE CASCADE` | Allocated resident |
| `room_id` | `INT` | `REFERENCES room(room_id) ON DELETE CASCADE` | Allocated room bed |
| `allocation_date` | `DATE` | `DEFAULT CURRENT_DATE`, `NOT NULL` | Date accommodation initiated |
| `vacated_date` | `DATE` | `NULL` | Date student checked out |
| `status` | `VARCHAR(20)` | `DEFAULT 'ACTIVE'`, `CHECK (status IN ('ACTIVE', 'COMPLETED', 'CANCELLED'))` | Allocation lifecycle |

#### 7. `fee_structure` (Standardized Pricing Tariffs)
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `fee_structure_id` | `SERIAL` | `PRIMARY KEY` | Tariff rule key |
| `room_type` | `VARCHAR(30)` | `UNIQUE`, `NOT NULL` | Associated room classification |
| `academic_fee` | `NUMERIC(10,2)` | `NOT NULL` | Tuition and facilities room charge |
| `mess_fee` | `NUMERIC(10,2)` | `NOT NULL` | Mandatory meal package fee |
| `caution_deposit` | `NUMERIC(10,2)` | `NOT NULL` | Refundable security deposit |

#### 8. `student_fee` (Student Fee Invoices)
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `fee_id` | `SERIAL` | `PRIMARY KEY` | Bill invoice identifier |
| `student_id` | `INT` | `REFERENCES student(student_id) ON DELETE CASCADE` | Student debtor |
| `fee_structure_id` | `INT` | `REFERENCES fee_structure(fee_structure_id) ON DELETE RESTRICT` | Rate card applied |
| `amount_due` | `NUMERIC(10,2)` | `NOT NULL` | Total assessed charges |
| `amount_paid` | `NUMERIC(10,2)` | `DEFAULT 0.00` | Cumulative credited receipts |
| `due_date` | `DATE` | `NOT NULL` | Payment deadline |
| `status` | `VARCHAR(20)` | `DEFAULT 'PENDING'`, `CHECK (status IN ('PENDING', 'PARTIAL', 'PAID'))` | Settlement state |

#### 9. `payment` (Audited Financial Transactions)
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `payment_id` | `SERIAL` | `PRIMARY KEY` | Unique receipt key |
| `student_id` | `INT` | `REFERENCES student(student_id) ON DELETE CASCADE` | Paying resident |
| `fee_id` | `INT` | `REFERENCES student_fee(fee_id) ON DELETE CASCADE` | Invoice being settled |
| `amount` | `NUMERIC(10,2)` | `NOT NULL`, `CHECK (amount > 0)` | Payment quantum |
| `payment_date` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Transaction timestamp |
| `payment_method` | `VARCHAR(30)` | `CHECK (payment_method IN ('UPI', 'CARD', 'NET_BANKING', 'CASH'))` | Banking instrument |
| `transaction_id` | `VARCHAR(100)` | `UNIQUE`, `NOT NULL` | Bank/UPI gateway tracking reference |
| `status` | `VARCHAR(20)` | `DEFAULT 'SUCCESS'`, `CHECK (status IN ('SUCCESS', 'PENDING', 'FAILED'))` | Settlement outcome |

#### 10. `complaint` (Maintenance & Grievance Tickets)
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `complaint_id` | `SERIAL` | `PRIMARY KEY` | Unique ticket identifier |
| `student_id` | `INT` | `REFERENCES student(student_id) ON DELETE CASCADE` | Complainant student |
| `category` | `VARCHAR(30)` | `CHECK (category IN ('ELECTRICAL', 'PLUMBING', 'WIFI', 'CLEANING', 'FURNITURE', 'FOOD', 'SECURITY', 'OTHER'))` | Domain category |
| `description` | `TEXT` | `NOT NULL` | Problem detail |
| `priority` | `VARCHAR(20)` | `DEFAULT 'MEDIUM'`, `CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH'))` | Urgency tier |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Submission timestamp |
| `assigned_to` | `INT` | `REFERENCES warden(warden_id) ON DELETE SET NULL` | Assigned resolving staff |
| `status` | `VARCHAR(20)` | `DEFAULT 'NEW'`, `CHECK (status IN ('NEW', 'ASSIGNED', 'IN_PROGRESS', 'RESOLVED'))` | Progress milestone |
| `resolved_at` | `TIMESTAMP` | `NULL` | Automated timestamp of resolution |
| `resolution` | `TEXT` | `NULL` | Remedial actions documented |

#### 11. `visitor` (Campus Security Gate Logs)
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `visitor_id` | `SERIAL` | `PRIMARY KEY` | Gate pass identifier |
| `student_id` | `INT` | `REFERENCES student(student_id) ON DELETE CASCADE` | Host student visited |
| `visitor_name` | `VARCHAR(100)` | `NOT NULL` | Legal name of visitor |
| `relationship` | `VARCHAR(50)` | `NOT NULL` | Relationship (e.g., 'Parent') |
| `phone` | `VARCHAR(15)` | — | Visitor phone number |
| `visit_date` | `DATE` | `DEFAULT CURRENT_DATE` | Date of visit |
| `entry_time` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Check-in timestamp |
| `exit_time` | `TIMESTAMP` | `NULL` | Check-out timestamp |
| `approved_by` | `INT` | `REFERENCES warden(warden_id) ON DELETE SET NULL` | Authorizing warden |
| `status` | `VARCHAR(20)` | `DEFAULT 'APPROVED'`, `CHECK (status IN ('APPROVED', 'CHECKED_OUT', 'DENIED'))` | Pass state |

#### 12. `leave_request` (Student Out-Passes & Leaves)
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `leave_id` | `SERIAL` | `PRIMARY KEY` | Leave pass identifier |
| `student_id` | `INT` | `REFERENCES student(student_id) ON DELETE CASCADE` | Applicant student |
| `pass_type` | `VARCHAR(20)` | `CHECK (pass_type IN ('LEAVE', 'HOME_PASS', 'OUT_PASS'))` | Pass classification |
| `from_date` | `DATE` | `NOT NULL` | Departure date |
| `to_date` | `DATE` | `NOT NULL` | Expected return date |
| `reason` | `TEXT` | `NOT NULL` | Justification |
| `destination` | `TEXT` | `NOT NULL` | Travel destination address |
| `emergency_contact`| `VARCHAR(15)` | `NOT NULL` | Guardian contact number |
| `status` | `VARCHAR(20)` | `DEFAULT 'PENDING'`, `CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED'))` | Approval outcome |
| `action_by` | `INT` | `REFERENCES warden(warden_id) ON DELETE SET NULL` | Warden decision maker |
| `action_date` | `TIMESTAMP` | `NULL` | Timestamp of decision |

#### 13. `room_change_request` (Internal Relocation Requests)
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `request_id` | `SERIAL` | `PRIMARY KEY` | Transfer request key |
| `student_id` | `INT` | `REFERENCES student(student_id) ON DELETE CASCADE` | Transferring student |
| `current_room_id` | `INT` | `REFERENCES room(room_id) ON DELETE CASCADE` | Existing assigned room |
| `requested_room_id`| `INT` | `REFERENCES room(room_id) ON DELETE CASCADE` | Target desired room |
| `reason` | `TEXT` | `NOT NULL` | Relocation motive |
| `status` | `VARCHAR(20)` | `CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED'))` | Status |
| `action_by` | `INT` | `REFERENCES warden(warden_id) ON DELETE SET NULL` | Approving warden |
| `action_date` | `TIMESTAMP` | `NULL` | Decision timestamp |

#### 14. `attendance` (Daily Roll Call Auditing)
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `attendance_id` | `SERIAL` | `PRIMARY KEY` | Attendance entry key |
| `student_id` | `INT` | `REFERENCES student(student_id) ON DELETE CASCADE` | Target resident |
| `date` | `DATE` | `DEFAULT CURRENT_DATE` | Attendance date |
| `status` | `VARCHAR(20)` | `CHECK (status IN ('PRESENT', 'ABSENT', 'LEAVE'))` | Daily presence status |
| `marked_by` | `INT` | `REFERENCES warden(warden_id) ON DELETE SET NULL` | Recording warden |
*Constraint:* `UNIQUE(student_id, date)` ensures only one attendance entry exists per student per calendar date.

#### 15. `notice` (Campus Broadcast Bulletin)
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `notice_id` | `SERIAL` | `PRIMARY KEY` | Bulletin identifier |
| `title` | `VARCHAR(200)` | `NOT NULL` | Announcement headline |
| `description` | `TEXT` | `NOT NULL` | Full notice text |
| `audience` | `VARCHAR(30)` | `CHECK (audience IN ('ALL', 'STUDENTS', 'WARDENS', 'STAFF'))` | Target demographic |
| `expiry_date` | `DATE` | `NULL` | Deprecation date |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Publishing timestamp |
| `created_by` | `INT` | `REFERENCES users(user_id) ON DELETE SET NULL` | Author account |

#### 16. `inventory` & 17. `inventory_transaction` (Hostel Asset Control)
- `inventory`: Tracks asset stockpiles (`item_name`, `total_qty`, `occupied_qty`, `damaged_qty`) per hostel.
- `inventory_transaction`: Audit trail of quantity adjustments (`ADD`, `REMOVE`, `DAMAGE_REPORT`, `REPAIR_REPORT`).

#### 18. `mess_menu` & 19. `mess_feedback` (Catering Services)
- `mess_menu`: Weekly dining timetable (`day_of_week`, `breakfast`, `lunch`, `dinner`) with `UNIQUE(hostel_id, day_of_week)`.
- `mess_feedback`: Student dining evaluations with 1-to-5 Likert scores for `food_quality`, `taste`, and `cleanliness`.

#### 20. `department` & 21. `employee` (Institutional Organizational Entities)
- Academic faculties and staff rosters demonstrating cross-table relational joins with university personnel systems.

---

### 4.3. Database Normalization Analysis & Mathematical Proofs (1NF to BCNF)

To eliminate update, insertion, and deletion anomalies while conserving disk space and ensuring data integrity, the schema underwent rigorous normalization.

#### Unnormalized Form (UNF) Example:
Imagine a flat file recording student hostel registrations:
$$\text{Registration}(\underline{\text{RollNo}}, \text{Name}, \text{HostelName}, \text{RoomNo}, \text{RoomType}, \text{Beds}, \{\text{FeeType}, \text{Amount}, \text{DueDate}, \text{PaymentDate}, \text{TxnID}\})$$
- **Problem**: Repeating groups for fees and payments. If a student makes multiple payments, rows must be duplicated or arrays stored.

#### 1. First Normal Form (1NF) — Atomicity of Attributes
- **Rule**: Every column must contain only atomic (indivisible) values, and each record must be unique.
- **Action**: Removed all repeating groups by splitting fees and payments into distinct relational tables (`student_fee`, `payment`). Each cell holds a single scalar value.

#### 2. Second Normal Form (2NF) — Elimination of Partial Dependencies
- **Rule**: Must be in 1NF, and all non-key attributes must be fully functionally dependent on the entire primary key (no partial dependencies on a composite key).
- **Proof**: In the unnormalized allocation:
  $$\{\text{StudentID}, \text{RoomID}\} \to \text{HostelName}, \text{RoomCapacity}, \text{StudentName}$$
  Notice that $\text{RoomID} \to \text{HostelName}, \text{RoomCapacity}$ depends *only* on `RoomID`, not on `StudentID`. This is a partial dependency.
- **Action**: Decomposed into:
  - $\text{Student}(\underline{\text{StudentID}}, \text{Name}, \text{RollNo}, \dots)$
  - $\text{Room}(\underline{\text{RoomID}}, \text{HostelID}, \text{RoomNumber}, \text{Capacity}, \dots)$
  - $\text{RoomAllocation}(\underline{\text{AllocationID}}, \text{StudentID}, \text{RoomID}, \text{AllocationDate}, \text{Status})$
  Now, every non-key attribute depends entirely on the primary surrogate key.

#### 3. Third Normal Form (3NF) — Elimination of Transitive Dependencies
- **Rule**: Must be in 2NF, and no non-key attribute may be transitively dependent on the primary key ($X \to Y$ and $Y \to Z$ where $Z$ is not a candidate key).
- **Proof**: Consider student fee billing:
  $$\text{StudentID} \to \text{RoomType} \to (\text{AcademicFee}, \text{MessFee}, \text{CautionDeposit})$$
  Here, tuition charges depend on `RoomType`, which in turn depends on `StudentID`. If no student currently books a `TRIPLE` room, the pricing for a `TRIPLE` room would be lost (deletion anomaly).
- **Action**: Extracted pricing tariffs into an independent catalog:
  - $\text{FeeStructure}(\underline{\text{FeeStructureID}}, \text{RoomType}, \text{AcademicFee}, \text{MessFee}, \text{CautionDeposit})$
  - $\text{StudentFee}(\underline{\text{FeeID}}, \text{StudentID}, \text{FeeStructureID}, \text{AmountDue}, \text{DueDate}, \text{Status})$
  Transitive dependency eliminated.

#### 4. Boyce-Codd Normal Form (BCNF) — Determinant Form
- **Rule**: A relation is in BCNF if and only if for every non-trivial functional dependency $X \to Y$, $X$ is a superkey.
- **Proof**: In all SmartHostel relations, surrogate keys (`SERIAL PRIMARY KEY`) and natural alternate keys (`UNIQUE`) serve as strict superkeys for all attribute determinants. There are no overlapping composite candidate keys that determine subsets of one another. Hence, all tables satisfy BCNF.

---

### 4.4. Relational Database Views (Virtual Tables)

Database views provide pre-compiled, optimized abstractions for frequent analytical queries, shielding raw tables from direct client querying while reducing network bandwidth.

#### View 1: `available_rooms`
Allows wardens and students to instantaneously view vacant accommodations with vacancy counts:
```sql
CREATE OR REPLACE VIEW available_rooms AS
SELECT 
    r.room_id, 
    r.room_number, 
    r.floor, 
    r.room_type, 
    r.capacity, 
    r.occupied_count, 
    r.status, 
    h.hostel_name
FROM room r
JOIN hostel h ON r.hostel_id = h.hostel_id
WHERE r.status = 'AVAILABLE' AND r.occupied_count < r.capacity;
```

#### View 2: `hostel_occupancy`
Calculates real-time occupancy rates, total beds, and percentage utilization across all hostel blocks using SQL aggregations (`SUM`, `COALESCE`, `ROUND`, `CASE`):
```sql
CREATE OR REPLACE VIEW hostel_occupancy AS
SELECT 
    h.hostel_id, 
    h.hostel_name, 
    h.hostel_type,
    COALESCE(SUM(r.capacity), 0) AS total_capacity,
    COALESCE(SUM(r.occupied_count), 0) AS occupied_beds,
    COALESCE(SUM(r.capacity), 0) - COALESCE(SUM(r.occupied_count), 0) AS available_beds,
    CASE 
        WHEN COALESCE(SUM(r.capacity), 0) = 0 THEN 0.0
        ELSE ROUND((COALESCE(SUM(r.occupied_count), 0)::NUMERIC / COALESCE(SUM(r.capacity), 0)::NUMERIC) * 100, 2)
    END AS occupancy_percentage
FROM hostel h
LEFT JOIN room r ON h.hostel_id = r.hostel_id
GROUP BY h.hostel_id, h.hostel_name, h.hostel_type;
```

#### View 3: `pending_fees`
Enables the accountant to audit fee defaulters and compute dynamic remaining balances:
```sql
CREATE OR REPLACE VIEW pending_fees AS
SELECT 
    s.student_id, 
    s.roll_no, 
    s.name, 
    s.email, 
    s.phone,
    sf.fee_id, 
    sf.amount_due, 
    sf.amount_paid,
    (sf.amount_due - sf.amount_paid) AS balance_due,
    sf.due_date, 
    sf.status AS fee_status
FROM student s
JOIN student_fee sf ON s.student_id = sf.student_id
WHERE (sf.amount_due - sf.amount_paid) > 0;
```

#### View 4: `complaint_summary`
Aggregates maintenance backlogs by category and urgency for SLA compliance monitoring:
```sql
CREATE OR REPLACE VIEW complaint_summary AS
SELECT 
    category, 
    status, 
    priority, 
    COUNT(*) AS complaint_count
FROM complaint
GROUP BY category, status, priority;
```

---

### 4.5. Database Triggers & Business Logic Automation (PL/pgSQL)

SmartHostel harnesses active database rules (**ECA — Event-Condition-Action**) via PostgreSQL PL/pgSQL triggers to maintain continuous operational consistency.

#### Trigger 1: Real-Time Room Occupancy Synchronization
- **Trigger**: `trg_update_room_occupancy` on `room_allocation`
- **Hook**: `AFTER INSERT OR UPDATE OR DELETE FOR EACH ROW`
- **Functionality**:
  1. On **`INSERT`** of an active allocation: Increments `room.occupied_count` by 1.
  2. On **`UPDATE`**: Handles transitions between `ACTIVE` and `COMPLETED`/`CANCELLED`, or inter-room transfers, updating old and new rooms accordingly using `GREATEST(0, occupied_count - 1)`.
  3. On **`DELETE`**: Safely decrements the bed count.
  4. Automatically toggles `room.status` to `'FULL'` if `occupied_count >= capacity`, otherwise `'AVAILABLE'`.

```sql
CREATE OR REPLACE FUNCTION func_update_room_occupancy()
RETURNS TRIGGER AS $$
BEGIN
    -- Increment occupancy when a new active allocation is inserted
    IF (TG_OP = 'INSERT' AND NEW.status = 'ACTIVE') THEN
        UPDATE room 
        SET occupied_count = occupied_count + 1
        WHERE room_id = NEW.room_id;
    END IF;

    -- Adjust occupancy when an allocation status is changed
    IF (TG_OP = 'UPDATE') THEN
        IF (OLD.status = 'ACTIVE' AND NEW.status != 'ACTIVE') THEN
            UPDATE room 
            SET occupied_count = GREATEST(0, occupied_count - 1)
            WHERE room_id = OLD.room_id;
        ELSIF (OLD.status != 'ACTIVE' AND NEW.status = 'ACTIVE') THEN
            UPDATE room 
            SET occupied_count = occupied_count + 1
            WHERE room_id = NEW.room_id;
        ELSIF (OLD.room_id != NEW.room_id AND NEW.status = 'ACTIVE') THEN
            UPDATE room 
            SET occupied_count = GREATEST(0, occupied_count - 1)
            WHERE room_id = OLD.room_id;
            
            UPDATE room 
            SET occupied_count = occupied_count + 1
            WHERE room_id = NEW.room_id;
        END IF;
    END IF;

    -- Decrement occupancy when an active allocation is deleted
    IF (TG_OP = 'DELETE' AND OLD.status = 'ACTIVE') THEN
        UPDATE room 
        SET occupied_count = GREATEST(0, occupied_count - 1)
        WHERE room_id = OLD.room_id;
    END IF;

    -- Automatically toggle room availability state
    UPDATE room 
    SET status = CASE 
        WHEN occupied_count >= capacity THEN 'FULL'
        ELSE 'AVAILABLE'
    END
    WHERE room_id IN (COALESCE(NEW.room_id, OLD.room_id), COALESCE(OLD.room_id, NEW.room_id));

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_room_occupancy
AFTER INSERT OR UPDATE OR DELETE ON room_allocation
FOR EACH ROW EXECUTE FUNCTION func_update_room_occupancy();
```

#### Trigger 2: Automatic Financial Ledger Reconciliation
- **Trigger**: `trg_update_payment_status` on `payment`
- **Hook**: `AFTER INSERT OR UPDATE FOR EACH ROW`
- **Functionality**: Queries all successful receipts for the given `fee_id`, aggregates the total paid quantum, and dynamically updates `student_fee.amount_paid` and `student_fee.status` (`'PAID'`, `'PARTIAL'`, `'PENDING'`).

```sql
CREATE OR REPLACE FUNCTION func_update_payment_status()
RETURNS TRIGGER AS $$
DECLARE
    v_total_paid NUMERIC(10,2);
    v_due NUMERIC(10,2);
BEGIN
    SELECT COALESCE(SUM(amount), 0.00) INTO v_total_paid
    FROM payment
    WHERE fee_id = NEW.fee_id AND status = 'SUCCESS';

    SELECT amount_due INTO v_due
    FROM student_fee
    WHERE fee_id = NEW.fee_id;

    UPDATE student_fee
    SET amount_paid = v_total_paid,
        status = CASE
            WHEN v_total_paid >= v_due THEN 'PAID'
            WHEN v_total_paid > 0 THEN 'PARTIAL'
            ELSE 'PENDING'
        END
    WHERE fee_id = NEW.fee_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_payment_status
AFTER INSERT OR UPDATE ON payment
FOR EACH ROW EXECUTE FUNCTION func_update_payment_status();
```

#### Trigger 3: Complaint Lifecycle Timestamp Auditing
- **Trigger**: `trg_complaint_resolution` on `complaint`
- **Hook**: `BEFORE UPDATE FOR EACH ROW`
- **Functionality**: Automatically stamps the exact system timestamp `resolved_at := CURRENT_TIMESTAMP` the moment a ticket status transitions to `'RESOLVED'`. If reopened, sets `resolved_at := NULL`.

```sql
CREATE OR REPLACE FUNCTION func_complaint_resolution()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'RESOLVED' AND OLD.status != 'RESOLVED' THEN
        NEW.resolved_at := CURRENT_TIMESTAMP;
    ELSIF NEW.status != 'RESOLVED' THEN
        NEW.resolved_at := NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_complaint_resolution
BEFORE UPDATE ON complaint
FOR EACH ROW EXECUTE FUNCTION func_complaint_resolution();
```

---

### 4.6. Stored Procedures, Functions & ACID Transaction Integrity

In high-concurrency systems, multiple users might attempt to claim the last available bed in a room. To prevent overselling and guarantee **ACID** properties, SmartHostel executes room assignments inside PL/pgSQL transactional functions.

#### Stored Function: `allocate_room(p_student_id, p_room_id)`
```sql
CREATE OR REPLACE FUNCTION allocate_room(p_student_id INT, p_room_id INT)
RETURNS BOOLEAN AS $$
DECLARE
    v_capacity INT;
    v_occupied INT;
    v_room_status VARCHAR(20);
    v_student_status VARCHAR(20);
BEGIN
    -- 1. Verify student exists and is in ACTIVE standing
    SELECT status INTO v_student_status FROM student WHERE student_id = p_student_id;
    IF v_student_status IS NULL THEN
        RAISE EXCEPTION 'Student ID % not found.', p_student_id;
    END IF;
    IF v_student_status != 'ACTIVE' THEN
        RAISE EXCEPTION 'Student is not ACTIVE (current status: %), cannot allocate room.', v_student_status;
    END IF;

    -- 2. Inspect room capacity and maintenance status
    SELECT capacity, occupied_count, status INTO v_capacity, v_occupied, v_room_status
    FROM room
    WHERE room_id = p_room_id;

    IF v_capacity IS NULL THEN
        RAISE EXCEPTION 'Room ID % not found.', p_room_id;
    END IF;

    IF v_room_status = 'MAINTENANCE' THEN
        RAISE EXCEPTION 'Room is currently under maintenance.';
    END IF;

    IF v_occupied >= v_capacity THEN
        RAISE EXCEPTION 'Room is fully occupied (%/% beds).', v_occupied, v_capacity;
    END IF;

    -- 3. Seamlessly mark any prior active allocation as COMPLETED
    UPDATE room_allocation 
    SET status = 'COMPLETED', vacated_date = CURRENT_DATE 
    WHERE student_id = p_student_id AND status = 'ACTIVE';

    -- 4. Atomically insert new allocation (Invokes trg_update_room_occupancy)
    INSERT INTO room_allocation (student_id, room_id, allocation_date, status)
    VALUES (p_student_id, p_room_id, CURRENT_DATE, 'ACTIVE');

    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
```

#### Stored Function: `vacate_room(p_student_id)`
```sql
CREATE OR REPLACE FUNCTION vacate_room(p_student_id INT)
RETURNS BOOLEAN AS $$
DECLARE
    v_allocation_id INT;
BEGIN
    SELECT allocation_id INTO v_allocation_id
    FROM room_allocation
    WHERE student_id = p_student_id AND status = 'ACTIVE';

    IF v_allocation_id IS NULL THEN
        RAISE EXCEPTION 'No active room allocation found for this student.';
    END IF;

    UPDATE room_allocation
    SET status = 'COMPLETED',
        vacated_date = CURRENT_DATE
    WHERE allocation_id = v_allocation_id;

    RETURN TRUE;
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Vacating room failed: %', SQLERRM;
        RETURN FALSE;
END;
$$ LANGUAGE plpgsql;
```

#### Formal Evaluation of ACID Properties:
1. **Atomicity**: If an allocation fails midway (e.g., room occupied between check and insert), PostgreSQL's transactional engine aborts the transaction and issues an exception. Partial allocations cannot occur.
2. **Consistency**: Integrity rules (`occupied_count <= capacity`, foreign keys, enum checks) remain inviolate before and after every execution.
3. **Isolation**: Read Committed / Repeatable Read transaction isolation levels protect against dirty reads, unrepeatable reads, and phantom records during peak admissions.
4. **Durability**: PostgreSQL's **Write-Ahead Logging (WAL)** ensures committed room bookings survive server reboots or network interruptions.

---

### 4.7. Indexing Strategies & Query Performance Optimization

Without indexing, queries searching for a student by roll number or retrieving occupied beds require exhaustive Sequential Table Scans ($O(N)$ complexity). SmartHostel implements targeted **B-Tree** and **Partial Indexes**:

```sql
-- 1. Fast student lookup by institutional identifier
CREATE INDEX idx_student_rollno ON student(roll_no);

-- 2. Foreign key navigation index for building rooms
CREATE INDEX idx_room_hostel ON room(hostel_id);

-- 3. Filter index for room availability lookups
CREATE INDEX idx_room_status ON room(status);

-- 4. Partial Index: Indexes ONLY currently active allocations (Drastically reduces index tree size)
CREATE INDEX idx_allocation_student ON room_allocation(student_id) WHERE status = 'ACTIVE';

-- 5. Foreign key acceleration for financial ledger lookups
CREATE INDEX idx_payment_student ON payment(student_id);

-- 6. Ticket routing and triage filter
CREATE INDEX idx_complaint_status ON complaint(status);

-- 7. Time-series attendance date filtering
CREATE INDEX idx_attendance_date ON attendance(date);
```

**Optimization Impact:**
- **Student Lookup**: Time complexity drops from $O(N)$ sequential scan to $O(\log N)$ binary tree traversal.
- **Partial Indexing**: For 10,000 historical allocations with only 500 active, `idx_allocation_student WHERE status = 'ACTIVE'` indexes only 500 records, consuming 95% less disk and RAM while accelerating check-in joins.

---

### 4.8. Database Security, Referential Integrity & Access Control

1. **Foreign Key Integrity Cascades**:
   - `ON DELETE CASCADE`: Used where child existence depends entirely on the parent entity (e.g., deleting a student cascades to their complaints, attendance records, and leave requests).
   - `ON DELETE SET NULL`: Preserves historical audit records when personnel change (e.g., if a warden is deleted, `complaint.assigned_to` and `hostel.warden_id` are set to `NULL` rather than wiping out the hostel or maintenance history).
   - `ON DELETE RESTRICT`: Used in critical financial structures (`student_fee` $\to$ `fee_structure`) to prevent accidental deletion of tariff schedules while active student invoices exist.
2. **Password Cryptography**: Passwords are never stored in plaintext. They are salt-hashed using **Bcrypt** ($2^{12}$ hashing rounds), providing mathematical protection against rainbow table attacks.
3. **Protection Against SQL Injection**: The application utilizes **SQLAlchemy ORM** parameterized queries. SQL statements and parameters are transmitted to PostgreSQL separately, making injection attacks mathematically impossible.

---

## 5. Backend Architecture & REST API Implementation

The backend application layer is built using **FastAPI**, renowned for high execution speed (benchmarking on par with NodeJS and Go) and automated OpenAPI 3.0 (Swagger) interactive documentation.

### 5.1. Modular Router Architecture
The API routes are divided into six decoupled routers under `/api`:
- **`auth_router` (`/api/auth`)**:
  - `POST /login`: Validates credentials, verifies Bcrypt hash, and issues a signed JSON Web Token (JWT) containing `sub`, `role`, and expiration claims.
- **`student_router` (`/api/student`)**:
  - `GET /profile`: Retrieves detailed resident info.
  - `GET /roommates`: Performs a relational self-join to list other active residents in the same room.
  - `GET /fees` & `POST /pay-fee`: Inspects tuition invoices and records payments.
  - `GET /complaints` & `POST /complaints`: Submits maintenance tickets.
  - `GET /leaves` & `POST /leave-request`: Applies for residential out-passes.
  - `POST /room-change`: Requests room relocation.
- **`warden_router` (`/api/warden`)**:
  - `GET /dashboard-stats`: Returns block occupancy metrics and pending request counts.
  - `POST /allocate-room`: Assigns students to beds.
  - `POST /vacate-room`: Safely discharges a resident.
  - `GET /complaints` & `PUT /complaint/{id}`: Triages and marks maintenance tickets `RESOLVED`.
  - `GET /leaves` & `POST /leave-action`: Approves or rejects student leave requests.
  - `POST /attendance/mark`: Submits batch attendance entries.
  - `POST /visitors`: Issues gate passes for campus visitors.
- **`accountant_router` (`/api/accountant`)**:
  - `GET /fee-structures` & `POST /fee-structure`: Configures room rates.
  - `GET /all-fees`, `GET /all-payments`, & `GET /defaulters`: Audits institutional receivables.
- **`admin_router` (`/api/admin`)**:
  - Full CRUD control over hostels, rooms, wardens, students, inventory stock, and campus-wide notice broadcasts.
- **`common_router` (`/api/common`)**:
  - Shared endpoints for catalog listings (hostel lists, room catalogues, mess menus, notices).

### 5.2. Role-Based Access Control (RBAC) Dependency Injection
FastAPI dependencies verify the client's JWT and enforce role boundaries before executing database queries:
```python
class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: models.User = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for current user role"
            )
        return current_user
```

---

## 6. Frontend Architecture & Role-Based Portals

The frontend is an ultra-modern Single Page Application (SPA) developed with **React 19**, bundled via **Vite**, and styled with **Tailwind CSS** and **Lucide Icons**.

### 6.1. Interactive Portals by Role
1. **Student Portal**:
   - **My Profile & Room Card**: Displays hostel name, room number, floor, room type, and allocated date.
   - **Roommates Roster**: Automatically detects co-residents in the same room.
   - **Fees & Payment Center**: Lists pending, partial, and paid dues with an instant UPI / Card simulation payment modal.
   - **Grievance Box**: Ticket filing with category, description, and real-time status tracker (`NEW` $\to$ `IN_PROGRESS` $\to$ `RESOLVED`).
   - **Out-Pass Generator**: Leave submission with downloadable approved pass details.
   - **Mess Menu & Feedback**: Daily food timetable and rating slider.
2. **Warden Console**:
   - **Room Allocation Matrix**: Visual grid of rooms with dynamic progress bars (`occupied / capacity`), colored green for available and red for full.
   - **Bed Allocation Modal**: Single-click student assignment and discharge.
   - **Leave Approval Queue**: One-click Approve / Reject buttons with reason and destination review.
   - **Daily Attendance Sheet**: Interactive Present / Absent / Leave toggle list for all assigned residents.
   - **Visitor Gate Registry**: Real-time logging of visitor name, student host, relationship, and check-out timestamp.
3. **Accountant Ledger**:
   - **Receivables Dashboard**: Total assessed fees, collections to date, and outstanding dues.
   - **Defaulters Audit**: Instant exportable view of overdue students with balance due.
   - **Fee Structure Manager**: Create or update pricing tariffs per room type.
4. **Admin Executive Control**:
   - **Hostel Blocks & Warden Assignment**: Create buildings, assign wardens, track capacities.
   - **Room Inventory**: Add rooms, set floors, configure capacities.
   - **Central Asset Control**: Track chairs, tables, beds, fans, and log maintenance repairs.
   - **Notice Broadcaster**: Publish alerts visible to students and wardens with audience filters.

---

## 7. Testing, Verification & Concurrency Validation

The repository includes dedicated verification scripts to certify data integrity, concurrency, and security.

### 7.1. Database Verification Scripts
- **`check_db_status.py`**: Connects via psycopg2, verifies relational integrity, and prints row counts across all 21 tables:
  ```
  attendance: 250 rows | complaint: 51 rows | fee_structure: 50 rows
  hostel: 51 rows     | inventory: 50 rows | leave_request: 51 rows
  mess_menu: 56 rows  | payment: 50 rows   | room: 60 rows
  room_allocation: 63 rows | student: 60 rows | users: 112 rows
  ```
- **`test_all_logins.py`**: Verifies JWT authentication across all test roles:
  - `admin` $\to$ Role: `ADMIN`
  - `warden_boys` $\to$ Role: `WARDEN`
  - `accountant` $\to$ Role: `ACCOUNTANT`
  - `sahaana` $\to$ Role: `STUDENT`
- **`test_pg_direct.py`**: Tests low-level socket connections to PostgreSQL 18.
- **`scratch_fix_roommate.py`**: Validates relational self-joins for roommate identification.

---

## 8. End-to-End Deployment Lifecycle

SmartHostel is architected to transition smoothly from a developer workstation to enterprise cloud environments.

### 8.1. Local Development Setup

#### Prerequisites:
- Python 3.12 or newer
- Node.js 18+ & npm
- PostgreSQL 18 installed locally on port 5432

#### Step-by-Step Execution:
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Nethra-R368/dbms.git
   cd dbms
   ```
2. **Setup Virtual Environment & Install Dependencies**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r backend\requirements.txt
   ```
3. **Configure Environment Variables**:
   Copy `.env.example` to `.env`:
   ```env
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/smarthostel
   JWT_SECRET=supersecretkey_smarthostel_dbms_project_2026
   PORT=8000
   HOST=127.0.0.1
   ```
4. **Initialize Database Schema & Sample Data**:
   ```bash
   python seed.py
   ```
   *This automatically creates the `smarthostel` database, runs `schema.sql` (creating all 21 tables, views, triggers, and procedures), and seeds 100+ realistic users and records.*
5. **Launch Backend & Frontend Simultaneously**:
   Execute the provided batch script:
   ```cmd
   start_full_app.bat
   ```
   - **Frontend UI**: [http://localhost:5173](http://localhost:5173)
   - **Backend API & Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 8.2. Automated Single-Server Unified Production Build

In production, running separate Node and Python servers adds unnecessary overhead. SmartHostel includes an automated script, `build_unified.bat`, that compiles the React frontend into static HTML/CSS/JS and embeds it directly into FastAPI:

```cmd
build_unified.bat
```
**Mechanism:**
1. Navigates into `frontend/` and executes `npm run build`.
2. Packages the resulting production bundle into `backend/static`.
3. FastAPI's `app.mount("/assets", ...)` serves the production UI on port 8000 alongside the API.
4. The entire application runs from a single unified server instance.

---

### 8.3. Public HTTPS Tunnel Deployment

To showcase the project remotely or perform live project demonstrations without cloud hosting fees, use `launch_online_link.bat`:
```cmd
launch_online_link.bat
```
- Starts the PostgreSQL service.
- Spawns the unified FastAPI backend on port 8000.
- Connects a high-speed reverse proxy tunnel providing a public `https://*.bore.pub` or Cloudflare HTTPS link accessible from any phone or external browser.

---

### 8.4. Enterprise Cloud Deployment (Azure Database for PostgreSQL & AWS RDS)

The repository provides production-ready deployment guides for top cloud providers:

#### 1. Azure Database for PostgreSQL (Flexible Server) + Azure App Service
- Detailed instructions in `AZURE_POSTGRES_SETUP.md`.
- Uses Azure Flexible Server with automated daily backups, high availability, and SSL connection enforcement (`sslmode=require`).
- Connection string format:
  ```env
  DATABASE_URL=postgresql://dbadmin:<password>@dbhostel.postgres.database.azure.com:5432/smarthostel?sslmode=require
  ```
- Deploy backend via Azure App Service Linux Python 3.12 container using `startup.sh`.

#### 2. AWS RDS PostgreSQL + AWS Elastic Beanstalk / EC2
- Detailed instructions in `AWS_POSTGRES_SETUP.md`.
- Allocates an `db.t4g.micro` or `db.t3.micro` PostgreSQL 18 instance with encrypted EBS storage.
- Multi-AZ deployment for failover resilience.
- Security group configuration allowing inbound port 5432 from the application tier.

---

## 9. Repository Organization & File Manifest

| File / Directory | Purpose & Description |
|---|---|
| `PROJECT_REPORT.md` | Academic & Technical Project Report (this comprehensive document) |
| `README.md` | Repository landing page with badges, quickstart, and feature walkthrough |
| `schema.sql` | Pure PostgreSQL DDL script creating all 21 tables, constraints, indexes, views, triggers, and stored procedures |
| `seed.py` | Python automation script to create the database, execute `schema.sql`, and populate realistic demo data |
| `build_unified.bat` | Production script compiling React into FastAPI `static` for single-port serving |
| `start_full_app.bat` | Batch script launching PostgreSQL, FastAPI backend, and React dev server concurrently |
| `launch_online_link.bat` | Batch script exposing local instance to a live public HTTPS tunnel |
| `check_db_status.py` | Diagnostic script printing live row counts for all database tables |
| `test_all_logins.py` | Automated testing suite validating authentication tokens for all roles |
| `AZURE_POSTGRES_SETUP.md`| Cloud deployment manual for Microsoft Azure Flexible Server |
| `AWS_POSTGRES_SETUP.md` | Cloud deployment manual for Amazon Web Services (AWS RDS) |
| `.env.example` | Sanitized configuration template for environment variables |
| `.gitignore` | Configured to protect secrets (`.env`), exclude large binaries (`.exe`), and omit build artifacts |
| `backend/` | Complete FastAPI backend application |
| `backend/app/main.py` | FastAPI application entry point, CORS config, and static SPA serving |
| `backend/app/models.py` | SQLAlchemy 2.0 ORM class declarations mapping all relational tables |
| `backend/app/schemas.py` | Pydantic data models for request validation and response serialization |
| `backend/app/database.py`| Database engine instantiation and connection session factory |
| `backend/app/routers/` | API routing logic partitioned by role (`auth`, `student`, `warden`, `accountant`, `admin`, `common`) |
| `backend/app/auth/` | JWT token generation and Bcrypt password verification routines |
| `backend/requirements.txt`| Python dependency specification |
| `frontend/` | Complete React 19 + Vite frontend application |
| `frontend/src/App.jsx` | Main React application containing all role portals and dashboards |
| `frontend/src/services/api.js`| Axios/fetch wrapper for backend REST API communication |
| `frontend/package.json` | Node.js frontend dependencies and build scripts |

---

## 10. Conclusion & Future Enhancements

### 10.1. Summary of Achievements
SmartHostel demonstrates the fusion of database theoretical foundations with modern full-stack web engineering:
- **Database Soundness**: Implemented a 21-table schema normalized to 3NF/BCNF, eliminating update and deletion anomalies.
- **Transactional Safety**: Utilized PL/pgSQL stored procedures (`allocate_room`, `vacate_room`) ensuring ACID compliance and eliminating race conditions.
- **Automated Intelligence**: Integrated active database triggers for real-time occupancy and financial balance updates.
- **Enterprise-Ready**: Equipped with automated unified production build scripts, role-based dashboards, and multi-cloud deployment guides.

### 10.2. Planned Future Enhancements
1. **Biometric IoT Attendance Integration**: Connecting facial recognition and fingerprint hardware directly to the `attendance` table via an IoT webhook gateway.
2. **Automated SMS & WhatsApp Alerts**: Trigger-based messaging to guardians when students check out on an approved leave pass.
3. **AI Roommate Compatibility Matching**: Utilizing cosine similarity embeddings on student study habits, sleep schedules, and departments to recommend optimal room pairings.
4. **Payment Gateway Integration**: Direct webhooks with Razorpay / Stripe for automated UPI QR code generation and real-time bank reconciliation.

---
*SmartHostel — Empowering Campus Residential Living through Advanced Database Systems.*
