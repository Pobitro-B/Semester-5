import psycopg2
from psycopg2 import sql

# ---------- DATABASE CONNECTION ----------
def get_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="studentdb",
            user="postgres",
            password="pobitrob"
        )
        return conn
    except Exception as e:
        print("❌ Error connecting to database:", e)
        return None

# ---------- TASK 1: TABLE CREATION ----------
def create_table(table_name, columns):
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({});").format(
            sql.Identifier(table_name),
            sql.SQL(columns)
        )
        cur.execute(query)
        conn.commit()
        print(f"✅ Table '{table_name}' created successfully!")

        cur.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema='public';
        """)
        print("\n📋 Current Tables:")
        for t in cur.fetchall():
            print("-", t[0])

        cur.close()
    except Exception as e:
        print("❌ Error creating table:", e)
    finally:
        conn.close()

# ---------- TASK 2: DATA INSERTION & MANIPULATION ----------
def insert_students():
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        while True:
            name = input("Enter student name (or 'q' to quit): ")
            if name.lower() == 'q':
                break
            age = int(input("Enter age: "))
            dept = input("Enter department: ")
            cur.execute("INSERT INTO students (name, age, department) VALUES (%s, %s, %s);",
                        (name, age, dept))
            conn.commit()
            print("✅ Student added!\n")
        cur.close()
    except Exception as e:
        print("❌ Error inserting data:", e)
    finally:
        conn.close()

def update_student():
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        name = input("Enter student name to update department: ")
        new_dept = input("Enter new department: ")
        cur.execute("UPDATE students SET department = %s WHERE name = %s;", (new_dept, name))
        conn.commit()
        print("✅ Department updated!")
        cur.close()
    except Exception as e:
        print("❌ Error updating student:", e)
    finally:
        conn.close()

def delete_student():
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        sid = int(input("Enter student ID to delete: "))
        cur.execute("DELETE FROM students WHERE id = %s;", (sid,))
        conn.commit()
        print("🗑️ Student deleted!")
        cur.close()
    except Exception as e:
        print("❌ Error deleting student:", e)
    finally:
        conn.close()

# ---------- TASK 3: QUERY OPERATIONS ----------
def query_students():
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        print("\nQuery Options:")
        print("1. Show all students")
        print("2. Show students in a department")
        print("3. Show average age per department")
        print("4. Find students by starting letter")
        choice = input("Enter choice: ")

        if choice == '1':
            cur.execute("SELECT * FROM students;")
            print("\nAll Students:")
        elif choice == '2':
            dept = input("Enter department: ")
            cur.execute("SELECT * FROM students WHERE department = %s;", (dept,))
            print(f"\nStudents in {dept}:")
        elif choice == '3':
            cur.execute("SELECT department, AVG(age) FROM students GROUP BY department;")
            print("\nAverage Age by Department:")
        elif choice == '4':
            letter = input("Enter starting letter: ")
            cur.execute("SELECT * FROM students WHERE name ILIKE %s;", (letter + '%',))
            print(f"\nStudents whose names start with '{letter}':")
        else:
            print("❌ Invalid choice!")
            cur.close()
            conn.close()
            return

        rows = cur.fetchall()
        if rows:
            for r in rows:
                print(r)
        else:
            print("No results found.")
        cur.close()
    except Exception as e:
        print("❌ Query error:", e)
    finally:
        conn.close()

# ---------- TASK 4: MENU DESIGN ----------
def main_menu():
    print("\n🎓 Student Database Management System 🎓")
    while True:
        print("\nMenu:")
        print("1. Create Table")
        print("2. Insert Student(s)")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Query Data")
        print("6. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            create_table("students", "id SERIAL PRIMARY KEY, name VARCHAR(50), age INT, department VARCHAR(50)")
        elif choice == '2':
            insert_students()
        elif choice == '3':
            update_student()
        elif choice == '4':
            delete_student()
        elif choice == '5':
            query_students()
        elif choice == '6':
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again!")

# ---------- TASK 5: PROGRAM TERMINATION ----------
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        print("🧹 All connections closed. Program terminated.")
