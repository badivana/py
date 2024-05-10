import json
import os

class Student:
    def __init__(self, name):
        self.name = name
        self.attendance = {}
        self.marks = {}
        self.loaded = False

    def mark_attendance(self, date, status):
        self.attendance[date] = status

    def update_marks(self, subject, mark):
        self.marks[subject] = mark

    def save_data(self):
        data = {
            "name": self.name,
            "attendance": self.attendance,
            "marks": self.marks
        }
        file_name = f"{self.name.lower().replace(' ', '_')}.json"
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data saved for {self.name}.")
        print()

    def get_attendance_status(self, date):
        status = self.attendance.get(date)
        if status is not None:
            return status
        else:
            return "Not Marked"

    def get_mark(self, subject):
        return self.marks.get(subject, "Not Available")

    def load_data(self):
        file_name = f"{self.name.lower().replace(' ', '_')}.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                data = json.load(file)
                self.name = data["name"]
                self.attendance = data["attendance"]
                self.marks = data["marks"]
            print(f"Data loaded for {self.name}.")
            self.loaded = True
        else:
            print(f"No existing data found for {self.name}.")

def add_student():
    name = input("Enter student name: ").strip()
    if not name:
        print("Student name cannot be empty. Please try again.")
        return None
    student = Student(name)
    return student

def edit_student(students):
    name = input("Enter student name to edit: ").strip()
    if not name:
        print("Student name cannot be empty. Please try again.")
        return

    found = False
    for student in students:
        if student.name.lower() == name.lower():
            student.load_data()
            found = True
            print(f"Editing {student.name}'s data:")
            while True:
                print("1. Mark Attendance")
                print("2. Update Marks")
                print("3. Display Attendance for a Date")
                print("4. Display Marks for a Subject")
                print("5. Save and Exit")
                choice = input("Enter your choice: ")
                if choice == '1':
                    date = input("Enter date (YYYY-MM-DD): ")
                    status = input("Enter attendance status (Present/Absent): ").capitalize()
                    if status not in ["Present", "Absent"]:
                        print("Invalid attendance status. Please enter 'Present' or 'Absent'.")
                        continue
                    student.mark_attendance(date, status)
                elif choice == '2':
                    subject = input("Enter subject: ").strip()
                    mark = input("Enter mark: ").strip()
                    if not subject or not mark:
                        print("Subject and mark cannot be empty. Please try again.")
                        continue
                    student.update_marks(subject, mark)
                elif choice == '3':
                    date = input("Enter date to check attendance (YYYY-MM-DD): ")
                    status = student.get_attendance_status(date)
                    print(f"Attendance for {student.name} on {date}: {status}")
                elif choice == '4':
                    subject = input("Enter subject to check marks: ").strip()
                    mark = student.get_mark(subject)
                    print(f"Mark for {subject} for {student.name}: {mark}")
                elif choice == '5':
                    student.save_data()
                    break
                else:
                    print("Invalid choice. Please try again.")
            break
    if not found:
        print("Student not found.")

def load_student_list():
    if os.path.exists("student_list.json"):
        with open("student_list.json", 'r') as file:
            return json.load(file)
    return []

def save_student_list(students):
    student_names = [student.name for student in students]
    with open("student_list.json", 'w') as file:
        json.dump(student_names, file)

def main():
    students = [Student(name) for name in load_student_list()]
    while True:
        print("\n1. Add Student")
        print("2. Edit Student Data")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            student = add_student()
            if student is not None:
                students.append(student)
                save_student_list(students)
        elif choice == '2':
            if not students:
                print("No students added yet.")
                continue
            edit_student(students)
        elif choice == '3':
            print("Exiting...........")

            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
