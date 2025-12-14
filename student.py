import mysql.connector
import shutil
import datetime
from tabulate import tabulate


def connect_db():
    return mysql.connector.connect(host="localhost",user="root",password="Manasi!123",database="university_planner")


def print_header_main(title):
    print()
    border_color = "\033[1;38;2;120;150;110m"
    title_color = "\033[1;38;2;156;175;136m"
    color_end = "\033[0m"
    terminal_width = shutil.get_terminal_size().columns
    width = max(len(title) + 4, terminal_width)
    print(border_color + "═" * width + color_end)
    print(border_color + "-" * width + color_end)
    print()
    print(title_color + title.center(width) + color_end)
    print()
    print(border_color + "-" * width + color_end)
    print(border_color + "═" * width + color_end)
    print()


def print_header(title):
    print()
    border_color = "\033[1;38;2;120;150;110m"
    title_color = "\033[1;38;2;156;175;136m"
    color_end = "\033[0m"
    terminal_width = shutil.get_terminal_size().columns
    width = max(len(title) + 4, terminal_width)
    print(border_color + "═" * width + color_end)
    print(title_color + title.center(width) + color_end)
    print(border_color + "═" * width + color_end)
    print()

def print_success(msg): 
    print()
    print(f"\033[92m {msg}\033[0m") 
    print()

def print_error(msg): 
    print()
    print(f"\033[91m {msg}\033[0m") 
    print()

def print_warning(msg): 
    print()
    print(f"\033[93m {msg}\033[0m")
    print()

current_user_id = None
current_username = None

def client_main():
    print_header_main(" University Planner - Student ")
    global current_user_id, current_username
    while True:
        print("1. Login")
        print("2. Signup")
        print("3. Exit")
        choice = input("\nEnter your choice: ")
        if choice == "1":
            if login():
                break
        elif choice == "2":
            signup()
        elif choice == "3":
            return
        else:
            print_warning("Invalid choice. Please try again.")
    while True:
        print()
        print("="*50)
        print(f"Welcome, {current_username}!")
        print("="*50)
        print("1. View Dashboard")
        print("2. My Subjects")
        print("3. My Attendance")
        print("4. My Assignments")
        print("5. My Timetable")
        print("6. Change Password")
        print("7. Logout")
        print("="*50)       
        choice = input("\nEnter your choice: ").strip()        
        if choice == "1":
            view_dashboard()
        elif choice == "2":
            my_subjects_menu()
        elif choice == "3":
            my_attendance_menu()
        elif choice == "4":
            my_assignments_menu()
        elif choice == "5":
            view_my_timetable()
        elif choice == "6":
            change_password()
        elif choice == "7":
            print_success("Logged out successfully!")
            current_user_id = None
            current_username = None
            break
        else:
            print_warning("Invalid choice. Please try again.")
def login():
    print_header("Login")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    db = connect_db()
    if not db:
        return False   
    cursor = db.cursor()
    try:
        cursor.execute("SELECT id, username FROM students WHERE username=%s AND password=%s",(username, password))
        result = cursor.fetchone()
        if result:
            global current_user_id, current_username
            current_user_id = result[0]
            current_username = result[1]
            print_success(f"Welcome back, {current_username}!")
            return True
        else:
            print_error("Invalid username or password!")
            return False
    except mysql.connector.Error as err:
        print_error(f"MySQL Error: {err}")
        return False
    finally:
        cursor.close()
        db.close()

def signup():
    print_header("Register New Student")   
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    email = input("Enter email: ").strip()
    phone = input("Enter phone: ").strip()   
    if not username or not password:
        print_error("Username and password are required!")
        return   
    db = connect_db()
    if not db:
        return   
    cursor = db.cursor()
    try:
        cursor.execute( "INSERT INTO students (username, password, email, phone) VALUES (%s, %s, %s, %s)",(username, password, email, phone))
        db.commit()
        print_success("Registration successful! You can now login.")
    except mysql.connector.Error as err:
        if err.errno == 1062:
            print_error("Username already exists!")
        else:
            print_error(f"MySQL Error: {err}")
    finally:
        cursor.close()
        db.close()

def change_password():
    print_header("Change Password")   
    old_password = input("Enter old password: ").strip()
    new_password = input("Enter new password: ").strip()
    confirm_password = input("Confirm new password: ").strip()   
    if new_password != confirm_password:
        print_error("Passwords do not match!")
        return    
    db = connect_db()
    if not db:
        return   
    cursor = db.cursor()
    try:
        cursor.execute("SELECT id FROM students WHERE id=%s AND password=%s",(current_user_id, old_password))
        if cursor.fetchone():
            cursor.execute("UPDATE students SET password=%s WHERE id=%s",(new_password, current_user_id))
            db.commit()
            print_success("Password changed successfully!")
        else:
            print_error("Old password is incorrect!")
    except mysql.connector.Error as err:
        print_error(f"MySQL Error: {err}")
    finally:
        cursor.close()
        db.close()

def view_dashboard():
    print_header(f" Dashboard - {datetime.datetime.now().strftime('%A, %B %d, %Y')}")   
    db = connect_db()
    if not db:
        return   
    cursor = db.cursor()
    
    try:
        day_name = datetime.datetime.now().strftime('%A')
        print("\n TODAY'S CLASSES")
        print("-" * 100)       
        cursor.execute("""SELECT t.start_time, t.end_time, s.name, s.code, s.professor, t.room FROM timetable t JOIN subjects s ON t.subject_id = s.id WHERE t.day_of_week = %s AND s.student_id = %s ORDER BY t.start_time""", (day_name, current_user_id))  
        today_classes = cursor.fetchall()
        if today_classes:
            current_time = datetime.datetime.now().time()
            table_data = []
            for cls in today_classes:
                start_time = cls[0]
                end_time = cls[1]           
                if end_time < current_time:
                    status = "Done"
                elif start_time <= current_time <= end_time:
                    status = "In Progress"
                else:
                    status = "Upcoming"
                if isinstance(start_time, datetime.timedelta):
                    hours = int(start_time.total_seconds() // 3600)
                    minutes = int((start_time.total_seconds() % 3600) // 60)
                    start_str = f"{hours:02d}:{minutes:02d}"
                else:
                    start_str = start_time.strftime('%H:%M')               
                if isinstance(end_time, datetime.timedelta):
                    hours = int(end_time.total_seconds() // 3600)
                    minutes = int((end_time.total_seconds() % 3600) // 60)
                    end_str = f"{hours:02d}:{minutes:02d}"
                else:
                    end_str = end_time.strftime('%H:%M')
                
                table_data.append([
                    start_str,
                    end_str,
                    f"{cls[2]} ({cls[3]})",
                    cls[4],
                    cls[5] or '-',
                    status
                ])           
            print(tabulate(table_data, 
                          headers=['Start', 'End', 'Subject', 'Professor', 'Room', 'Status'],
                          tablefmt='grid'))
        else:
            print("No classes scheduled for today! 🎉")       
        print("\n UPCOMING ASSIGNMENTS (Next 7 Days)")
        print("-" * 100)        
        today = datetime.datetime.now().date()
        next_week = today + datetime.timedelta(days=7)       
        cursor.execute("""SELECT a.title, s.name, s.code, a.deadline FROM assignments a JOIN subjects s ON a.subject_id = s.id WHERE a.status = 'pending'  AND a.deadline BETWEEN %s AND %s  AND s.student_id = %s ORDER BY a.deadline ASC""", (today, next_week, current_user_id))        
        upcoming_assignments = cursor.fetchall()      
        if upcoming_assignments:
            table_data = []
            for assignment in upcoming_assignments:
                days_left = (assignment[3] - today).days
                if days_left == 0:
                    urgency = "DUE TODAY!"
                elif days_left == 1:
                    urgency = "Due Tomorrow"
                else:
                    urgency = f"{days_left} days left"                
                table_data.append([
                    assignment[0],
                    f"{assignment[1]} ({assignment[2]})",
                    assignment[3].strftime('%Y-%m-%d'),
                    urgency
                ])            
            print(tabulate(table_data,
                          headers=['Assignment', 'Subject', 'Deadline', 'Urgency'],
                          tablefmt='grid'))
        else:
            print("No pending assignments in the next 7 days! 🎉")
        print("\n  ATTENDANCE STATUS")
        print("-" * 100)        
        cursor.execute("""
            SELECT 
                s.name,
                s.code,
                COUNT(a.id) as total_classes,
                SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) as attended,
                ROUND((SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) / COUNT(a.id)) * 100, 2) as percentage
            FROM subjects s
            LEFT JOIN attendance a ON s.id = a.subject_id
            WHERE s.student_id = %s
            GROUP BY s.id, s.name, s.code
            HAVING COUNT(a.id) > 0
        """, (current_user_id,))
       
        attendance_records = cursor.fetchall()
        
        if attendance_records:
            table_data = []
            has_low_attendance = False
            
            for subject in attendance_records:
                percentage = subject[4]
                if percentage < 75:
                    has_low_attendance = True
                    needed = calculate_classes_needed(subject[3], subject[2])
                    status = f" {percentage}% (Need {needed} classes)"
                else:
                    status = f" {percentage}%"
                
                table_data.append([
                    f"{subject[0]} ({subject[1]})",
                    f"{subject[3]}/{subject[2]}",
                    status
                ])
            
            print(tabulate(table_data,
                          headers=['Subject', 'Attended', 'Status'],
                          tablefmt='grid'))
            
            if not has_low_attendance:
                print("\n✓ All subjects have good attendance (≥75%)!")
        else:
            print("No attendance records found.")
        
    except mysql.connector.Error as err:
        print_error(f"MySQL Error: {err}")
    finally:
        cursor.close()
        db.close()
    
    print("\n" + "="*100)

def my_subjects_menu():
    while True:
        print_header(" My Subjects")
        print("1. View All Subjects")
        print("2. Add New Subject")
        print("3. Delete Subject")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            view_my_subjects()
        elif choice == "2":
            add_subject()
        elif choice == "3":
            delete_subject()
        elif choice == "0":
            break
        else:
            print_warning("Invalid choice!")

def view_my_subjects():
    print_header("My Subjects")
    
    db = connect_db()
    if not db:
        return
    
    cursor = db.cursor()
    try:
        cursor.execute("""
            SELECT 
                s.id,
                s.name,
                s.code,
                s.professor,
                COUNT(a.id) as total_classes,
                SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) as attended,
                CASE 
                    WHEN COUNT(a.id) > 0 THEN 
                        ROUND((SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) / COUNT(a.id)) * 100, 2)
                    ELSE 0 
                END as attendance_percentage
            FROM subjects s
            LEFT JOIN attendance a ON s.id = a.subject_id
            WHERE s.student_id = %s
            GROUP BY s.id, s.name, s.code, s.professor
        """, (current_user_id,))
        
        subjects = cursor.fetchall()
        
        if not subjects:
            print_warning("No subjects found. Add your first subject!")
            return
        
        table_data = []
        for subject in subjects:
            attendance_pct = subject[6]
            if attendance_pct < 75:
                status = "Low"
            else :
                status="✓"
            
            table_data.append([
                subject[0],
                subject[1],
                subject[2],
                subject[3],
                f"{subject[5]}/{subject[4]}",
                f"{attendance_pct}% {status}"
            ])
        
        print(tabulate(table_data,
                      headers=['ID', 'Name', 'Code', 'Professor', 'Attended', 'Attendance %'],
                      tablefmt='grid'))
        
        low_attendance = [s for s in subjects if s[6] < 75 and s[4] > 0]
        if low_attendance:
            print("\n  ATTENDANCE ALERTS:")
            for subject in low_attendance:
                needed = calculate_classes_needed(subject[5], subject[4])
                print(f"   • {subject[1]} ({subject[2]}): {subject[6]}%")
                print(f"     Need to attend {needed} consecutive classes to reach 75%")
    
    except mysql.connector.Error as err:
        print_error(f"MySQL Error: {err}")
    finally:
        cursor.close()
        db.close()

def add_subject():
    print_header("Add New Subject")    
    name = input("Enter subject name: ").strip()
    code = input("Enter subject code: ").strip().upper()
    professor = input("Enter professor name: ").strip()   
    if not name or not code:
        print_error("Subject name and code are required!")
        return   
    db = connect_db()
    if not db:
        return   
    cursor = db.cursor()
    try:
        cursor.execute("""
            INSERT INTO subjects (name, code, professor, student_id)
            VALUES (%s, %s, %s, %s)
        """, (name, code, professor, current_user_id))
        db.commit()
        print_success(f"Subject '{name}' added successfully!")
    except mysql.connector.Error as err:
        if err.errno == 1062:
            print_error(f"Subject with code '{code}' already exists!")
        else:
            print_error(f"MySQL Error: {err}")
    finally:
        cursor.close()
        db.close()
def delete_subject():
    print_header("Delete Subject")
    view_my_subjects()    
    subject_id = input("\nEnter subject ID to delete: ").strip()    
    if not subject_id.isdigit():
        print_error("Invalid subject ID!")
        return    
    confirm = input(f"Are you sure you want to delete subject ID {subject_id}? (yes/no): ").strip().lower()    
    if confirm != 'yes':
        print_warning("Deletion cancelled.")
        return   
    db = connect_db()
    if not db:
        return    
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM subjects WHERE id=%s AND student_id=%s", 
                      (int(subject_id), current_user_id))
        db.commit()       
        if cursor.rowcount > 0:
            print_success("Subject deleted successfully!")
        else:
            print_error("Subject not found or doesn't belong to you!")
    except mysql.connector.Error as err:
        print_error(f"MySQL Error: {err}")
    finally:
        cursor.close()
        db.close()

def my_attendance_menu():
    while True:
        print_header("My Attendance")
        print("1. Mark Attendance")
        print("2. View Attendance Records")
        print("3. View Subject Attendance")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            mark_attendance()
        elif choice == "2":
            view_attendance_records()
        elif choice == "3":
            view_subject_attendance()
        elif choice == "0":
            break
        else:
            print_warning("Invalid choice!")

def mark_attendance():
    print_header("Mark Attendance")
    view_my_subjects()
    
    subject_id = input("\nEnter subject ID: ").strip()
    
    if not subject_id.isdigit():
        print_error("Invalid subject ID!")
        return
    db = connect_db()
    if not db:
        return
    
    cursor = db.cursor()
    try:
        cursor.execute("SELECT name FROM subjects WHERE id=%s AND student_id=%s", 
                      (int(subject_id), current_user_id))
        result = cursor.fetchone()
        
        if not result:
            print_error("Subject not found or doesn't belong to you!")
            return
        
        subject_name = result[0]
        
        date_str = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
        if not date_str:
            date = datetime.datetime.now().date()
        else:
            try:
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                print_error("Invalid date format!")
                return
        
        status = input("Mark as (p)resent or (a)bsent: ").strip().lower()
        if status in ['p', 'present']:
            status = 'present'
        elif status in ['a', 'absent']:
            status = 'absent'
        else:
            print_error("Invalid status!")
            return
        
        notes = input("Notes (optional): ").strip()

        cursor.execute("""
            SELECT id FROM attendance 
            WHERE subject_id = %s AND date = %s
        """, (int(subject_id), date))
        
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute("""
                UPDATE attendance 
                SET status = %s, notes = %s
                WHERE id = %s
            """, (status, notes, existing[0]))
            print_success(f"Attendance updated to '{status}' for {date}")
        else:
            cursor.execute("""
                INSERT INTO attendance (subject_id, date, status, notes)
                VALUES (%s, %s, %s, %s)
            """, (int(subject_id), date, status, notes))
            print_success(f"Attendance marked as '{status}' for {date}")
        
        db.commit()
        check_attendance_alert(cursor, int(subject_id), subject_name)
        
    except mysql.connector.Error as err:
        print_error(f"MySQL Error: {err}")
    finally:
        cursor.close()
        db.close()

def view_attendance_records():
    print_header("Attendance Records")
    
    db = connect_db()
    if not db:
        return
    
    cursor = db.cursor()
    try:
        cursor.execute("""
            SELECT a.date, s.name, s.code, a.status, a.notes
            FROM attendance a
            JOIN subjects s ON a.subject_id = s.id
            WHERE s.student_id = %s
            ORDER BY a.date DESC
            LIMIT 20
        """, (current_user_id,))
        
        records = cursor.fetchall()
        
        if not records:
            print_warning("No attendance records found.")
            return
        
        table_data = []
        for record in records:
            status_icon = "✓" if record[3] == 'present' else "✗"
            table_data.append([
                record[0].strftime('%Y-%m-%d'),
                f"{record[1]} ({record[2]})",
                f"{status_icon} {record[3].upper()}",
                record[4] or '-'
            ])
        
        print(tabulate(table_data,
                      headers=['Date', 'Subject', 'Status', 'Notes'],
                      tablefmt='grid'))
    
    except mysql.connector.Error as err:
        print_error(f"MySQL Error: {err}")
    finally:
        cursor.close()
        db.close()

def view_subject_attendance():
    print_header("Subject Attendance")
    view_my_subjects()
    
    subject_id = input("\nEnter subject ID: ").strip()
    
    if not subject_id.isdigit():
        print_error("Invalid subject ID!")
        return
    
    db = connect_db()
    if not db:
        return
    
    cursor = db.cursor()
    try:
        cursor.execute("""
            SELECT a.date, a.status, a.notes
            FROM attendance a
            JOIN subjects s ON a.subject_id = s.id
            WHERE a.subject_id = %s AND s.student_id = %s
            ORDER BY a.date DESC
        """, (int(subject_id), current_user_id))
        
        records = cursor.fetchall()
        
        if not records:
            print_warning("No attendance records found for this subject.")
            return
        
        table_data = []
        for record in records:
            status_icon = "✓" if record[1] == 'present' else "✗"
            table_data.append([
                record[0].strftime('%Y-%m-%d'),
                f"{status_icon} {record[1].upper()}",
                record[2] or '-'
            ])
        
        print(tabulate(table_data,
                      headers=['Date', 'Status', 'Notes'],
                      tablefmt='grid'))
    
    except mysql.connector.Error as err:
        print_error(f"MySQL Error: {err}")
    finally:
        cursor.close()
        db.close()

def check_attendance_alert(cursor, subject_id, subject_name):
    try:
        cursor.execute("""
            SELECT 
                COUNT(a.id) as total_classes,
                SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) as attended,
                ROUND((SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) / COUNT(a.id)) * 100, 2) as percentage
            FROM attendance a
            WHERE a.subject_id = %s AND COUNT(a.id) > 0
        """, (subject_id,))
        
        result = cursor.fetchone()
        
        if result and result[0] > 0:
            percentage = result[2]
            if percentage < 75:
                needed = calculate_classes_needed(result[1], result[0])
                print(f"\n  ATTENDANCE ALERT!")
                print(f"   {subject_name}: {percentage}%")
                print(f"   You need to attend {needed} consecutive classes to reach 75%")
    
    except mysql.connector.Error as err:
        print_error(f"MySQL Error: {err}")

def calculate_classes_needed(attended, total):
    target = 0.75
    classes_needed = 0
    
    while attended / (total + classes_needed) < target:
        classes_needed += 1
        attended += 1
        if classes_needed > 100:
            break
    
    return classes_needed

def my_assignments_menu():
    while True:
        print_header("My Assignments")
        print("1. View All Assignments")
        print("2. View Pending Assignments")
        print("3. Add New Assignment")
        print("4. Mark Assignment Complete")
        print("5. Delete Assignment")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            view_my_assignments(None)
        elif choice == "2":
            view_my_assignments('pending')
        elif choice == "3":
            add_assignment()
        elif choice == "4":
            mark_assignment_complete()
        elif choice == "5":
            delete_assignment()
        elif choice == "0":
            break
        else:
            print_warning("Invalid choice!")

def view_my_assignments(status=None):
    if status:
        print_header("Pending Assignments")
    else:
        print_header("All Assignments")
    
    db = connect_db()
    if not db:
        return
    
    cursor = db.cursor()
    try:
        if status:
            cursor.execute("""
                SELECT a.id, a.title, s.name, s.code, a.deadline, a.status
                FROM assignments a
                JOIN subjects s ON a.subject_id = s.id
                WHERE a.status = %s AND s.student_id = %s
                ORDER BY a.deadline ASC
            """, (status, current_user_id))
        else:
            cursor.execute("""
                SELECT a.id, a.title, s.name, s.code, a.deadline, a.status
                FROM assignments a
                JOIN subjects s ON a.subject_id = s.id
                WHERE s.student_id = %s
                ORDER BY a.deadline ASC
            """, (current_user_id,))
        
        assignments = cursor.fetchall()
        
        if not assignments:
            print_warning("No assignments found.")
            return
        
        table_data = []
        today = datetime.datetime.now().date()
        
        for assignment in assignments:
            deadline = assignment[4]
            days_left = (deadline - today).days
            
            if days_left < 0:
                urgency = f" OVERDUE ({abs(days_left)} days)"
            elif days_left <= 3:
                urgency = f" {days_left} days left"
            elif days_left <= 7:
                urgency = f" {days_left} days left"
            else:
                urgency = f" {days_left} days left"
            
            if assignment[5] == 'completed':
                status_icon = "✓"
            else :
                status_icon = "To be done"
            
            table_data.append([
                assignment[0],
                assignment[1],
                f"{assignment[2]} ({assignment[3]})",
                deadline.strftime('%Y-%m-%d'),
                urgency,
                f"{status_icon} {assignment[5].upper()}"
            ])
        
        print(tabulate(table_data,
                      headers=['ID', 'Title', 'Subject', 'Deadline', 'Urgency', 'Status'],
                      tablefmt='grid'))
    
    except mysql.connector.Error as err:
        print_error(f"MySQL Error: {err}")
    finally:
        cursor.close()
        db.close()

def add_assignment():
    print_header("Add New Assignment")
    view_my_subjects()
    
    subject_id = input("\nEnter subject ID: ").strip()
    
    if not subject_id.isdigit():
        print_error("Invalid subject ID!")
        return
    
    db = connect_db()
    if not db:
        return
    
    cursor = db.cursor()
    try:
        cursor.execute("SELECT id FROM subjects WHERE id=%s AND student_id=%s",
                      (int(subject_id), current_user_id))
        if not cursor.fetchone():
            print_error("Subject not found or doesn't belong to you!")
            return
        
        title = input("Enter assignment title: ").strip()
        description = input("Enter description: ").strip()
        deadline_str = input("Enter deadline (YYYY-MM-DD): ").strip()
        
        if not title or not deadline_str:
            print_error("Title and deadline are required!")
            return
        
        try:
            deadline = datetime.datetime.strptime(deadline_str, '%Y-%m-%d').date()
        except ValueError:
            print_error("Invalid date format!")
            return
        
        cursor.execute("""
            INSERT INTO assignments (subject_id, title, description, deadline)
            VALUES (%s, %s, %s, %s)
        """, (int(subject_id), title, description, deadline))
        db.commit()
        print_success(f"Assignment '{title}' added successfully!")
    
    except mysql.connector.Error as err:
        print_error(f"MySQL Error: {err}")
    finally:
        cursor.close()
        db.close()

def mark_assignment_complete():
    print_header("Mark Assignment Complete")
    view_my_assignments('pending')
    
    assignment_id = input("\nEnter assignment ID to mark complete: ").strip()
    
    if not assignment_id.isdigit():
        print_error("Invalid assignment ID!")
        return
    
    db = connect_db()
    if not db:
        return
    
    cursor = db.cursor()
    try:
        cursor.execute("""
            UPDATE assignments a
            JOIN subjects s ON a.subject_id = s.id
            SET a.status = 'completed'
            WHERE a.id = %s AND s.student_id = %s
        """, (int(assignment_id), current_user_id))
        db.commit()
        
        if cursor.rowcount > 0:
            print_success("Assignment marked as completed!")
        else:
            print_error("Assignment not found or doesn't belong to you!")
    
    except mysql.connector.Error as err:
        print_error(f"MySQL Error: {err}")
    finally:
        cursor.close()
        db.close()

def delete_assignment():
    print_header("Delete Assignment")
    view_my_assignments()
    
    assignment_id = input("\nEnter assignment ID to delete: ").strip()
    
    if not assignment_id.isdigit():
        print_error("Invalid assignment ID!")
        return
    
    confirm = input(f"Are you sure you want to delete assignment ID {assignment_id}? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print_warning("Deletion cancelled.")
        return
    
    db = connect_db()
    if not db:
        return
    
    cursor = db.cursor()
    try:
        cursor.execute("""
            DELETE a FROM assignments a
            JOIN subjects s ON a.subject_id = s.id
            WHERE a.id = %s AND s.student_id = %s
        """, (int(assignment_id), current_user_id))
        db.commit()
        
        if cursor.rowcount > 0:
            print_success("Assignment deleted successfully!")
        else:
            print_error("Assignment not found or doesn't belong to you!")
    
    except mysql.connector.Error as err:
        print_error(f"MySQL Error: {err}")
    finally:
        cursor.close()
        db.close()

def view_my_timetable():

    print_header("📅 My Weekly Timetable")
    
    db = connect_db()
    if not db:
        return
    
    cursor = db.cursor()
    try:
        cursor.execute("""
            SELECT t.day_of_week, t.start_time, t.end_time, s.name, s.code, s.professor, t.room
            FROM timetable t
            JOIN subjects s ON t.subject_id = s.id
            WHERE s.student_id = %s
            ORDER BY 
                FIELD(t.day_of_week, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
                t.start_time
        """, (current_user_id,))
        
        entries = cursor.fetchall()
        
        if not entries:
            print_warning("No timetable entries found.")
            print("Add classes from the Subjects menu → Add Timetable Entry")
            return
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']        
        for day in days:
            day_entries = [e for e in entries if e[0] == day]
            if day_entries:
                print(f"\n{day.upper()}")
                print("-" * 100)
                table_data = []
                for entry in day_entries:
                    start_time = entry[1]
                    end_time = entry[2]                   
                    if isinstance(start_time, datetime.timedelta):
                        hours = int(start_time.total_seconds() // 3600)
                        minutes = int((start_time.total_seconds() % 3600) // 60)
                        start_str = f"{hours:02d}:{minutes:02d}"
                    else:
                        start_str = start_time.strftime('%H:%M')                   
                    if isinstance(end_time, datetime.timedelta):
                        hours = int(end_time.total_seconds() // 3600)
                        minutes = int((end_time.total_seconds() % 3600) // 60)
                        end_str = f"{hours:02d}:{minutes:02d}"
                    else:
                        end_str = end_time.strftime('%H:%M')
                    
                    table_data.append([
                        start_str,
                        end_str,
                        f"{entry[3]} ({entry[4]})",
                        entry[5],
                        entry[6] or '-'
                    ])
                print(tabulate(table_data,
                              headers=['Start', 'End', 'Subject', 'Professor', 'Room'],
                              tablefmt='simple'))
    
    except mysql.connector.Error as err:
        print_error(f"MySQL Error: {err}")
    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    client_main()
