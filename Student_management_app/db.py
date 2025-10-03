import mysql.connector
import bcrypt

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password = "Harish@07",
        database = "stud_db"
    )

def login(mail, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("Select * from admin where email = %s", (mail,))
    admin = cursor.fetchone()

    cursor.close()
    conn.close()

    if admin:
        stored_hash = admin['password'].encode('utf-8') if isinstance(admin['password'],str) else admin['password']

        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return True
    return None

def register(name, mail, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("Select * from admin where email = %s", (mail, ))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return None
    
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("Insert into admin (name, email, password) Values (%s, %s, %s)", (name, mail, hashed_pw))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def fetch_adname(mail):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select name from admin where email = %s", (mail,))
    name = cursor.fetchone()
    if name:
        cursor.close()
        conn.close()
        return name[0]
    return None

def add_student(student_name, gender, admitted_date, dob, dept_name, grade_10_mark, grade_12_mark, phone_number, native, counselling_or_not, hosteller_or_not):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("Select Student_Name from students where Phone_Number = %s", (phone_number,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return None
    
    cursor.execute("Insert into students (Student_Name, Gender, Student_Admitted_Date, dob, Department_Name, Grade_10_Mark, Grade_12_Mark, Phone_Number, Native_Place, counselling_or_management, Hosteller_or_Not) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (student_name, gender, admitted_date, dob, dept_name, grade_10_mark, grade_12_mark, phone_number, native, counselling_or_not, hosteller_or_not))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def view_student():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select Student_Id, Student_Name from students")
    r = cursor.fetchall()
    if r:
        cursor.close()
        conn.close()
        return r
    else:
        cursor.close()
        conn.close()
        return None
        
    
def fetch_student(student_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from students where Student_ID = %s", (student_id,))
    s = cursor.fetchone()
    if s:
        cursor.close()
        conn.close()
        return s
    else:
        cursor.close()
        conn.close()
        return None
    
def view_students():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from students")
    re = cursor.fetchall()
    if re:
        cursor.close()
        conn.close()
        return re
    else:
        cursor.close()
        conn.close()
        return None

def update_student(id, new_name, gender, admitted_date, dob, dept_name, grade_10, grade_12, phone_number, native, counselling_or_not, hostel):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    id = int(id)
    grade_10 = int(grade_10)
    grade_12 = int(grade_12)
    cursor.execute("""
        UPDATE students 
        SET Student_Name=%s, Gender=%s, Student_Admitted_Date=%s, dob=%s, Department_Name=%s, Grade_10_Mark=%s, Grade_12_Mark=%s, Phone_Number = %s, Native_Place=%s, counselling_or_management = %s, Hosteller_or_Not=%s
        WHERE Student_ID=%s
    """, (new_name, gender, admitted_date, dob, dept_name, grade_10, grade_12, phone_number, native, counselling_or_not, hostel, id))
    conn.commit()
    conn.close()
    return True

def delete_student(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    id = int(id)
    cursor.execute("delete from students where Student_ID = %s", (id,))
    conn.commit()
    conn.close()
    return True