students = {}


def clean_text(value):
    return value.strip().title()


def validate_email(email):
    return "@" in email and "." in email.split("@")[-1]


def make_roll_tuple(roll_input):
    parts = roll_input.strip().upper().split("-")
    if len(parts) != 3:
        return None
    return (parts[0], parts[1], parts[2])


def input_marks(subjects):
    marks = []
    for subject in subjects:
        while True:
            try:
                mark = float(input(f"  Enter marks for {subject}: "))
                if 0 <= mark <= 100:
                    marks.append(mark)
                    break
                print("  Error: Marks must be between 0 and 100.")
            except ValueError:
                print("  Error: Please enter a valid number.")
    return marks


def input_attendance(subjects):
    attendance = []
    for subject in subjects:
        while True:
            try:
                percent = float(input(f"  Enter attendance % for {subject}: "))
                if 0 <= percent <= 100:
                    attendance.append(percent)
                    break
                print("  Error: Attendance must be between 0 and 100.")
            except ValueError:
                print("  Error: Please enter a valid number.")
    return attendance


def add_student():
    print("\n--- Add New Student ---")

    roll_input = input("Enter Roll Number (format YEAR-DEPT-NUM, e.g. 2024-CS-001): ")
    roll_no = make_roll_tuple(roll_input)
    if roll_no is None:
        print("Error: Invalid roll number format.")
        return

    roll_key = "-".join(roll_no)
    if roll_key in students:
        print("Error: Student with this roll number already exists.")
        return

    reg_input = input("Enter Registration Number (format REG-YEAR-NUM): ")
    reg_no = make_roll_tuple(reg_input)
    if reg_no is None:
        print("Error: Invalid registration number format.")
        return

    dob_input = input("Enter Date of Birth (format YYYY-MM-DD): ")
    dob = make_roll_tuple(dob_input)
    if dob is None:
        print("Error: Invalid date format.")
        return

    name = input("Enter Student Name: ").strip()
    if not name:
        print("Error: Name cannot be empty.")
        return
    name = name.title()

    department = input("Enter Department: ").strip().title()
    if not department:
        print("Error: Department cannot be empty.")
        return

    email = input("Enter Email ID: ").strip()
    if not validate_email(email):
        print("Error: Invalid email address.")
        return

    address = input("Enter Address: ").strip()
    if not address:
        address = "Not Provided"

    subjects_input = input("Enter Subjects (comma-separated): ").strip()
    if not subjects_input:
        print("Error: At least one subject is required.")
        return
    subjects = [s.strip().title() for s in subjects_input.split(",") if s.strip()]

    if not subjects:
        print("Error: At least one valid subject is required.")
        return

    print("Enter marks for each subject:")
    marks = input_marks(subjects)

    print("Enter attendance for each subject:")
    attendance = input_attendance(subjects)

    clubs_input = input("Enter Clubs (comma-separated, or leave blank): ").strip()
    if clubs_input:
        clubs = {c.strip().title() for c in clubs_input.split(",") if c.strip()}
    else:
        clubs = set()

    student = {
        "roll_no": roll_no,
        "reg_no": reg_no,
        "dob": dob,
        "name": name,
        "department": department,
        "email": email,
        "address": address,
        "subjects": subjects,
        "marks": marks,
        "attendance": attendance,
        "clubs": clubs
    }

    students[roll_key] = student
    print("Student added successfully!")


def display_all_students():
    print("\n--- All Students ---")

    if not students:
        print("No students in the system.")
        return

    header = f"{'Roll No':<16}{'Name':<22}{'Department':<22}{'Avg Marks':<12}"
    print(header)
    print("-" * len(header))

    for roll_key, student in students.items():
        avg = sum(student["marks"]) / len(student["marks"]) if student["marks"] else 0
        name = student["name"]
        if len(name) > 19:
            name = name[:16] + "..."
        dept = student["department"]
        if len(dept) > 19:
            dept = dept[:16] + "..."
        print(f"{roll_key:<16}{name:<22}{dept:<22}{avg:<12.2f}")


def view_student_details():
    print("\n--- View Student Details ---")
    roll_key = input("Enter Roll Number: ").strip().upper()

    if roll_key not in students:
        print("Error: Student not found.")
        return

    student = students[roll_key]
    print("\n--- Student Profile ---")
    print("Roll Number   :", "-".join(student["roll_no"]))
    print("Reg Number    :", "-".join(student["reg_no"]))
    print("Date of Birth :", "-".join(student["dob"]))
    print("Name          :", student["name"])
    print("Department    :", student["department"])
    print("Email         :", student["email"])
    print("Address       :", student["address"])

    print("\nSubjects and Marks:")
    for subject, mark in zip(student["subjects"], student["marks"]):
        print(f"  {subject:<20} {mark}")

    print("\nAttendance:")
    for subject, percent in zip(student["subjects"], student["attendance"]):
        print(f"  {subject:<20} {percent}%")

    if student["clubs"]:
        print("\nClubs:", ", ".join(sorted(student["clubs"])))
    else:
        print("\nClubs: None")


def search_by_roll():
    print("\n--- Search Student by Roll Number ---")
    roll_key = input("Enter Roll Number: ").strip().upper()

    if roll_key in students:
        student = students[roll_key]
        print("\nStudent Found:")
        print("Roll Number :", "-".join(student["roll_no"]))
        print("Name        :", student["name"])
        print("Department  :", student["department"])
        print("Email       :", student["email"])
    else:
        print("Student not found.")


def update_student():
    print("\n--- Update Student Information ---")
    roll_key = input("Enter Roll Number to update: ").strip().upper()

    if roll_key not in students:
        print("Error: Student not found.")
        return

    student = students[roll_key]

    print("\nCurrent values:")
    for key, value in student.items():
        print(f"  {key}: {value}")

    field = input("\nWhich field to update? ").strip().lower()

    if field not in student:
        print("Error: Field does not exist.")
        return

    if field in ("roll_no", "reg_no", "dob"):
        print("Error: Cannot update tuple fields (they are fixed).")
        return

    if field == "marks":
        print("Enter new marks:")
        student["marks"] = input_marks(student["subjects"])
        print("Marks updated successfully!")
        return

    if field == "attendance":
        print("Enter new attendance:")
        student["attendance"] = input_attendance(student["subjects"])
        print("Attendance updated successfully!")
        return

    if field == "clubs":
        clubs_input = input("Enter Clubs (comma-separated): ").strip()
        student["clubs"] = {c.strip().title() for c in clubs_input.split(",") if c.strip()}
        print("Clubs updated successfully!")
        return

    if field == "subjects":
        subjects_input = input("Enter Subjects (comma-separated): ").strip()
        new_subjects = [s.strip().title() for s in subjects_input.split(",") if s.strip()]
        if not new_subjects:
            print("Error: At least one subject is required.")
            return
        student["subjects"] = new_subjects
        student["marks"] = [0] * len(new_subjects)
        student["attendance"] = [0] * len(new_subjects)
        print("Subjects updated. Marks and attendance reset to 0.")
        return

    new_value = input("Enter new value: ").strip()
    if not new_value:
        print("Error: New value cannot be empty.")
        return

    if field == "email":
        if not validate_email(new_value):
            print("Error: Invalid email address.")
            return
    else:
        new_value = new_value.title()

    student[field] = new_value
    print("Student information updated successfully!")


def delete_student():
    print("\n--- Delete Student Record ---")
    roll_key = input("Enter Roll Number to delete: ").strip().upper()

    if roll_key not in students:
        print("Error: Student not found.")
        return

    student = students[roll_key]
    confirm = input(f"Are you sure you want to delete {student['name']}? (yes/no): ").strip().lower()

    if confirm == "yes":
        del students[roll_key]
        print("Student record deleted successfully.")
    else:
        print("Deletion cancelled.")


def calculate_average_marks():
    print("\n--- Calculate Average Marks ---")

    if not students:
        print("No students in the system.")
        return

    roll_key = input("Enter Roll Number (or 'ALL' for every student): ").strip().upper()

    if roll_key == "ALL":
        for key, student in students.items():
            avg = sum(student["marks"]) / len(student["marks"]) if student["marks"] else 0
            print(f"  {key:<16} {student['name']:<22} Average: {avg:.2f}")
    elif roll_key in students:
        student = students[roll_key]
        avg = sum(student["marks"]) / len(student["marks"]) if student["marks"] else 0
        print(f"\n{student['name']} - Average Marks: {avg:.2f}")
    else:
        print("Error: Student not found.")


def find_highest_scorer():
    print("\n--- Highest Scorer ---")

    if not students:
        print("No students in the system.")
        return

    highest_name = None
    highest_avg = -1
    highest_roll = None

    for roll_key, student in students.items():
        if student["marks"]:
            avg = sum(student["marks"]) / len(student["marks"])
            if avg > highest_avg:
                highest_avg = avg
                highest_name = student["name"]
                highest_roll = roll_key

    if highest_name is None:
        print("No marks recorded for any student.")
        return

    print(f"Highest Scorer: {highest_name} ({highest_roll})")
    print(f"Average Marks : {highest_avg:.2f}")


def list_by_department():
    print("\n--- List Students by Department ---")

    if not students:
        print("No students in the system.")
        return

    department = input("Enter Department: ").strip().title()
    if not department:
        print("Error: Department cannot be empty.")
        return

    matches = [s for s in students.values() if s["department"] == department]

    if not matches:
        print(f"No students found in {department}.")
        return

    print(f"\n{len(matches)} student(s) in {department}:")
    for student in matches:
        print(f"  {student['name']:<22} ({'-'.join(student['roll_no'])})")


def count_students():
    print("\n--- Count Students ---")
    print(f"Total students in the system: {len(students)}")

    if not students:
        return

    dept_counts = {}
    for student in students.values():
        dept = student["department"]
        dept_counts[dept] = dept_counts.get(dept, 0) + 1

    print("\nStudents per department:")
    for dept, count in sorted(dept_counts.items()):
        print(f"  {dept:<22} {count}")


def show_unique_departments():
    print("\n--- Unique Departments ---")

    if not students:
        print("No students in the system.")
        return

    departments = {s["department"] for s in students.values()}
    print(f"{len(departments)} unique department(s):")
    for d in sorted(departments):
        print("  -", d)


def show_unique_subjects():
    print("\n--- Unique Subjects ---")

    if not students:
        print("No students in the system.")
        return

    subjects = set()
    for student in students.values():
        subjects.update(student["subjects"])

    print(f"{len(subjects)} unique subject(s):")
    for s in sorted(subjects):
        print("  -", s)


def show_unique_clubs():
    print("\n--- Unique Clubs ---")

    if not students:
        print("No students in the system.")
        return

    clubs = set()
    for student in students.values():
        clubs.update(student["clubs"])

    if not clubs:
        print("No clubs registered.")
        return

    print(f"{len(clubs)} unique club(s):")
    for c in sorted(clubs):
        print("  -", c)


def show_statistics():
    print("\n--- System Statistics ---")

    if not students:
        print("No students in the system.")
        return

    total = len(students)
    all_marks = []
    for student in students.values():
        all_marks.extend(student["marks"])

    overall_avg = sum(all_marks) / len(all_marks) if all_marks else 0
    departments = {s["department"] for s in students.values()}
    subjects = set()
    clubs = set()
    for student in students.values():
        subjects.update(student["subjects"])
        clubs.update(student["clubs"])

    print(f"Total students      : {total}")
    print(f"Unique departments  : {len(departments)}")
    print(f"Unique subjects     : {len(subjects)}")
    print(f"Unique clubs        : {len(clubs)}")
    print(f"Overall average mark: {overall_avg:.2f}")


def main():
    while True:
        print("\n===== STUDENT RECORD MANAGEMENT SYSTEM =====")
        print("1.  Add New Student")
        print("2.  Display All Students")
        print("3.  View Student Details")
        print("4.  Search by Roll Number")
        print("5.  Update Student Information")
        print("6.  Delete Student Record")
        print("7.  Calculate Average Marks")
        print("8.  Find Highest Scorer")
        print("9.  List Students by Department")
        print("10. Count Students")
        print("11. Show Unique Departments")
        print("12. Show Unique Subjects")
        print("13. Show Unique Clubs")
        print("14. System Statistics")
        print("15. Exit")

        choice = input("Enter your choice (1-15): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            display_all_students()
        elif choice == "3":
            view_student_details()
        elif choice == "4":
            search_by_roll()
        elif choice == "5":
            update_student()
        elif choice == "6":
            delete_student()
        elif choice == "7":
            calculate_average_marks()
        elif choice == "8":
            find_highest_scorer()
        elif choice == "9":
            list_by_department()
        elif choice == "10":
            count_students()
        elif choice == "11":
            show_unique_departments()
        elif choice == "12":
            show_unique_subjects()
        elif choice == "13":
            show_unique_clubs()
        elif choice == "14":
            show_statistics()
        elif choice == "15":
            print("Thank you for using the Student Record Management System.")
            break
        else:
            print("Invalid choice. Please enter 1 to 15.")


if __name__ == "__main__":
    main()
