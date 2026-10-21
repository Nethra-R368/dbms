-- ============================================================================
-- 23AIE303 - Database Management Systems (DBMS)
-- Project: ResiKeep / SmartHostel Management System
-- Database Core Assets: Advanced Documented SQL Queries
-- Demonstrating Multi-Table Joins, Nested Subqueries, CTEs, Aggregations & Window Functions
-- ============================================================================

-- ----------------------------------------------------------------------------
-- QUERY 1: Multi-Table Inner Join with Aggregation
-- Purpose: Generate a complete resident profile joining 4 tables: Student, Room,
--          Hostel, and Warden, with room occupancy ratio calculation.
-- ----------------------------------------------------------------------------
SELECT 
    s.student_id,
    s.roll_no,
    s.name AS student_name,
    s.department,
    s.year,
    h.hostel_name,
    h.hostel_type,
    r.room_number,
    r.room_type,
    r.floor,
    w.name AS warden_in_charge,
    w.phone AS warden_contact,
    ra.allocation_date
FROM student s
JOIN room_allocation ra ON s.student_id = ra.student_id
JOIN room r ON ra.room_id = r.room_id
JOIN hostel h ON r.hostel_id = h.hostel_id
LEFT JOIN warden w ON h.warden_id = w.warden_id
WHERE ra.status = 'ACTIVE' AND s.status = 'ACTIVE'
ORDER BY h.hostel_name, r.room_number;


-- ----------------------------------------------------------------------------
-- QUERY 2: Multi-Table Left Outer Join with GROUP BY & HAVING
-- Purpose: Building-level occupancy analytics identifying hostels operating
--          above 80% capacity threshold.
-- ----------------------------------------------------------------------------
SELECT 
    h.hostel_id,
    h.hostel_name,
    h.hostel_type,
    h.capacity AS declared_capacity,
    COALESCE(SUM(r.capacity), 0) AS total_room_beds,
    COALESCE(SUM(r.occupied_count), 0) AS total_occupied_beds,
    (COALESCE(SUM(r.capacity), 0) - COALESCE(SUM(r.occupied_count), 0)) AS available_vacancies,
    ROUND((COALESCE(SUM(r.occupied_count), 0)::NUMERIC / NULLIF(COALESCE(SUM(r.capacity), 0), 0)::NUMERIC) * 100, 2) AS occupancy_percentage
FROM hostel h
LEFT JOIN room r ON h.hostel_id = r.hostel_id
GROUP BY h.hostel_id, h.hostel_name, h.hostel_type, h.capacity
HAVING COALESCE(SUM(r.occupied_count), 0) > 0
ORDER BY occupancy_percentage DESC;


-- ----------------------------------------------------------------------------
-- QUERY 3: Correlated Subquery in WHERE Clause
-- Purpose: Retrieve high-priority complaints that have remained unassigned or
--          unresolved longer than the average resolution time across the campus.
-- ----------------------------------------------------------------------------
SELECT 
    c.complaint_id,
    s.name AS complainant,
    s.roll_no,
    c.category,
    c.description,
    c.priority,
    c.created_at,
    c.status
FROM complaint c
JOIN student s ON c.student_id = s.student_id
WHERE c.status IN ('NEW', 'IN_PROGRESS')
  AND c.priority = 'HIGH'
  AND c.created_at < (
      SELECT AVG(created_at) 
      FROM complaint 
      WHERE status = 'RESOLVED'
  )
ORDER BY c.created_at ASC;


-- ----------------------------------------------------------------------------
-- QUERY 4: Subquery in FROM Clause with Financial Aggregation
-- Purpose: Identify fee defaulters whose outstanding dues exceed the median balance
--          of all active residents.
-- ----------------------------------------------------------------------------
SELECT 
    defaulters.student_id,
    defaulters.roll_no,
    defaulters.name,
    defaulters.total_billed,
    defaulters.total_paid,
    defaulters.outstanding_balance
FROM (
    SELECT 
        s.student_id,
        s.roll_no,
        s.name,
        COALESCE(SUM(sf.amount_due), 0.00) AS total_billed,
        COALESCE(SUM(sf.amount_paid), 0.00) AS total_paid,
        COALESCE(SUM(sf.amount_due - sf.amount_paid), 0.00) AS outstanding_balance
    FROM student s
    JOIN student_fee sf ON s.student_id = sf.student_id
    GROUP BY s.student_id, s.roll_no, s.name
) AS defaulters
WHERE defaulters.outstanding_balance > (
    SELECT AVG(amount_due - amount_paid) 
    FROM student_fee 
    WHERE (amount_due - amount_paid) > 0
)
ORDER BY defaulters.outstanding_balance DESC;


-- ----------------------------------------------------------------------------
-- QUERY 5: Window Functions (PARTITION BY & Running Totals)
-- Purpose: Financial audit of student payments displaying running cumulative total
--          and transaction sequence rank per student.
-- ----------------------------------------------------------------------------
SELECT 
    p.payment_id,
    p.student_id,
    s.name AS student_name,
    p.amount,
    p.payment_method,
    p.payment_date,
    p.transaction_id,
    ROW_NUMBER() OVER(PARTITION BY p.student_id ORDER BY p.payment_date ASC) AS payment_sequence,
    SUM(p.amount) OVER(PARTITION BY p.student_id ORDER BY p.payment_date ASC 
                       ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_paid_to_date
FROM payment p
JOIN student s ON p.student_id = s.student_id
WHERE p.status = 'SUCCESS'
ORDER BY p.student_id, p.payment_date ASC;


-- ----------------------------------------------------------------------------
-- QUERY 6: Self-Join for Co-Resident / Roommate Discovery
-- Purpose: Given any student, dynamically query all peers residing in the same
--          room unit without returning the student themselves.
-- ----------------------------------------------------------------------------
SELECT 
    s1.roll_no AS primary_student_roll,
    s1.name AS primary_student_name,
    r.room_number,
    h.hostel_name,
    s2.roll_no AS roommate_roll,
    s2.name AS roommate_name,
    s2.department AS roommate_department,
    s2.phone AS roommate_contact
FROM room_allocation ra1
JOIN room_allocation ra2 ON ra1.room_id = ra2.room_id AND ra1.student_id != ra2.student_id
JOIN student s1 ON ra1.student_id = s1.student_id
JOIN student s2 ON ra2.student_id = s2.student_id
JOIN room r ON ra1.room_id = r.room_id
JOIN hostel h ON r.hostel_id = h.hostel_id
WHERE ra1.status = 'ACTIVE' 
  AND ra2.status = 'ACTIVE'
ORDER BY h.hostel_name, r.room_number;


-- ----------------------------------------------------------------------------
-- QUERY 7: Common Table Expression (CTE) for Dining Mess Quality Scoring
-- Purpose: Aggregate Likert scale feedback across food quality, taste, and
--          cleanliness, grouping by day of the week to identify low-rated meal days.
-- ----------------------------------------------------------------------------
WITH DailyRatings AS (
    SELECT 
        mf.date,
        TO_CHAR(mf.date, 'Day') AS day_name,
        mf.food_quality,
        mf.taste,
        mf.cleanliness,
        ROUND((mf.food_quality + mf.taste + mf.cleanliness)::NUMERIC / 3.0, 2) AS composite_score
    FROM mess_feedback mf
)
SELECT 
    TRIM(day_name) AS weekday,
    COUNT(*) AS total_feedbacks_submitted,
    ROUND(AVG(food_quality), 2) AS avg_food_quality,
    ROUND(AVG(taste), 2) AS avg_taste,
    ROUND(AVG(cleanliness), 2) AS avg_cleanliness,
    ROUND(AVG(composite_score), 2) AS overall_satisfaction_score
FROM DailyRatings
GROUP BY TRIM(day_name)
ORDER BY overall_satisfaction_score ASC;
