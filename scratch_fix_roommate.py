import psycopg2

conn = psycopg2.connect('postgresql://postgres:Nark%401231@localhost:5432/smarthostel')
cur = conn.cursor()

cur.execute("""
    SELECT s.student_id, s.name, s.gender, r.room_id, r.room_number, r.room_type, r.capacity, r.occupied_count 
    FROM student s 
    LEFT JOIN room_allocation ra ON s.student_id = ra.student_id AND ra.status = 'ACTIVE' 
    LEFT JOIN room r ON ra.room_id = r.room_id 
    WHERE s.name ILIKE '%sahaana%' OR s.student_id = 1
""")
print('Sahaana:', cur.fetchall())

# Find who is in B-303
cur.execute("""
    SELECT ra.allocation_id, s.student_id, s.name, r.room_number, ra.status 
    FROM room_allocation ra 
    JOIN student s ON ra.student_id = s.student_id 
    JOIN room r ON ra.room_id = r.room_id 
    WHERE r.room_number = 'B-303'
""")
print('In B-303:', cur.fetchall())

# Find other female students
cur.execute("""
    SELECT s.student_id, s.name, s.gender, r.room_id, r.room_number, ra.allocation_id
    FROM student s 
    JOIN room_allocation ra ON s.student_id = ra.student_id AND ra.status = 'ACTIVE'
    JOIN room r ON ra.room_id = r.room_id
    WHERE s.gender = 'F' AND s.name NOT ILIKE '%sahaana%'
    LIMIT 5
""")
print('Other active female allocations:', cur.fetchall())

conn.close()
