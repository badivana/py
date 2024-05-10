import json
import os
import getpass  # For secure password input

# File paths
CREDENTIALS_FILE = "credentials.json"
EMPLOYEES_DIRECTORY = "employees"

def admin_crd():
    credentials = {"admin": "admin"}
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(credentials, file)

def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    else:
        admin_crd()
        return load_credentials()

def save_credentials(credentials):
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(credentials, file)

def load_employee_data():
    if os.path.exists(EMPLOYEES_DIRECTORY):
        employees = {}
        for filename in os.listdir(EMPLOYEES_DIRECTORY):
            with open(os.path.join(EMPLOYEES_DIRECTORY, filename), "r") as file:
                employee_data = json.load(file)
                employees[employee_data["ID"]] = employee_data
        return employees
    else:
        os.makedirs(EMPLOYEES_DIRECTORY)
        return {}

def save_employee_data(employee_data):
    for emp_id, data in employee_data.items():
        filename = os.path.join(EMPLOYEES_DIRECTORY, f"{emp_id}.json")
        with open(filename, "w") as file:
            json.dump(data, file)

def admin_login():
    credentials = load_credentials()
    username = input("Enter admin username: ")
    password = getpass.getpass("Enter admin password: ")
    if username in credentials and credentials[username] == password:
        print("Admin login successful.")
        admin_options()
    else:
        print("Invalid username or password.")

def admin_options():
    while True:
        print("\n1. Create a new employee")
        print("2. Access employee details")
        print("3. Update employee details")
        print("4. Create a new admin account")
        print("5. View all employees")
        print("6. Delete employee")
        print("7. View salary statistics")
        print("8. Change own password")
        print("9. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            create_employee()
        elif choice == "2":
            access_employee_details()
        elif choice == "3":
            update_employee_details()
        elif choice == "4":
            create_admin_account()
        elif choice == "5":
            view_all_employees()
        elif choice == "6":
            delete_employee()
        elif choice == "7":
            view_salary_statistics()
        elif choice == "8":
            change_admin_password()
        elif choice == "9":
            break
        else:
            print("Invalid choice.")

def create_employee():
    emp_id = input("Enter employee ID: ")
    name = input("Enter employee name: ")
    designation = input("Enter employee designation: ")
    password = getpass.getpass("Enter employee password: ")
    salary = int(input("Enter Salary: "))

    employee_data = {
        "ID": emp_id,
        "Name": name,
        "Designation": designation,
        "Password": password,
        "Salary": salary
    }

    save_employee_data({emp_id: employee_data})
    print("Employee created successfully.")

def access_employee_details():
    emp_id = input("Enter employee ID: ")
    employee_data = load_employee_data().get(emp_id)
    if employee_data:
        print("Employee details:")
        print(json.dumps(employee_data, indent=4))
    else:
        print("Employee not found.")

def update_employee_details():
    emp_id = input("Enter employee ID to update details: ")
    employee_data = load_employee_data().get(emp_id)
    if employee_data:
        print("Current Employee details:")
        print(json.dumps(employee_data, indent=4))
        # Update employee details
        name = input("Enter updated employee name (leave blank to keep current): ")
        if name:
            employee_data["Name"] = name
        designation = input("Enter updated employee designation (leave blank to keep current): ")
        if designation:
            employee_data["Designation"] = designation
        password = getpass.getpass("Enter updated employee password (leave blank to keep current): ")
        if password:
            employee_data["Password"] = password
        salary = input("Enter updated employee salary (leave blank to keep current): ")
        if salary:
            employee_data["Salary"] = int(salary)
        save_employee_data({emp_id: employee_data})
        print("Employee details updated successfully.")
    else:
        print("Employee not found.")

def create_admin_account():
    credentials = load_credentials()
    username = input("Enter new admin username: ")
    if username in credentials:
        print("Username already exists. Please choose another one.")
        return
    password = getpass.getpass("Enter new admin password: ")
    credentials[username] = password
    save_credentials(credentials)
    print("Admin account created successfully.")

def view_all_employees():
    employee_data = load_employee_data()
    for emp_id, data in employee_data.items():
        print("Employee ID:", data["ID"])
        print("Employee Name:", data["Name"])
        print("Employee Designation:", data["Designation"])
        print("Employee Salary:", data["Salary"])
        print()

def delete_employee():
    emp_id = input("Enter employee ID to delete: ")
    employee_data = load_employee_data()
    if emp_id in employee_data:
        filename = os.path.join(EMPLOYEES_DIRECTORY, f"{emp_id}.json")
        os.remove(filename)
        print("Employee deleted successfully.")
    else:
        print("Employee not found.")

def view_salary_statistics():
    employee_data = load_employee_data()
    salaries = [data["Salary"] for data in employee_data.values() if "Salary" in data]
    if salaries:
        print("Salary Statistics:")
        print("Average Salary:", sum(salaries) / len(salaries))
        print("Highest Salary:", max(salaries))
        print("Lowest Salary:", min(salaries))
    else:
        print("No employees found or salary information missing.")

def change_admin_password():
    credentials = load_credentials()
    username = input("Enter admin username: ")
    if username in credentials:
        new_password = getpass.getpass("Enter new password: ")
        credentials[username] = new_password
        save_credentials(credentials)
        print("Password changed successfully.")
    else:
        print("Admin username not found.")

def is_employee():
    return input("Are you an employee? (yes/no): ").lower() == "yes"

def employee_login():
    while True:
        print("\n1. View own details")
        print("2. Change own password")
        print("3. Access employee details")
        print("4. Request leave")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            view_own_details()
        elif choice == "2":
            change_employee_password()
        elif choice == "3":
            access_employee_details()
        elif choice == "4":
            request_leave()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def view_own_details():
    emp_id = input("Enter your employee ID: ")
    employee_data = load_employee_data()
    if emp_id in employee_data:
        print("Your details:")
        print("Employee ID:", employee_data[emp_id]["ID"])
        print("Employee Name:", employee_data[emp_id]["Name"])
        print("Employee Designation:", employee_data[emp_id]["Designation"])
        print("Employee Salary:", employee_data[emp_id]["Salary"])
    else:
        print("Employee not found.")

def change_employee_password():
    emp_id = input("Enter your employee ID: ")
    employee_data = load_employee_data()
    if emp_id in employee_data:
        new_password = getpass.getpass("Enter new password: ")
        employee_data[emp_id]["Password"] = new_password
        save_employee_data(employee_data)
        print("Password changed successfully.")
    else:
        print("Employee not found.")

def request_leave():
    emp_id = input("Enter your employee ID: ")
    # Add leave request functionality here
    print("Leave request submitted successfully.")

def main():
    while True:
        print("\n1. Admin Login")
        print("2. Employee Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            admin_login()
        elif choice == "2":
            employee_login()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
