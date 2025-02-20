# Simple Complaint Management System with Staff Roles

# Database Initialisation
user_accounts = {"admin": {"password": "admin123", "role": "admin"}}  # Default admin account
staff_accounts = {}  # Stores staff members and their assigned departments
complaints_db = []  # List to store complaints

# Register a new customer
def register_user():
    username = input("Enter your new username: ").strip()
    if username in user_accounts:
        print("That username is already taken. Try another.\n")
        return

    password = input("Create a password: ").strip()
    user_accounts[username] = {"password": password, "role": "customer"}
    print(f"\nWelcome, {username}! Your customer account has been created.")
    print("You may now login from your account!")

# Add staff and assign a department
def add_staff():
    staff_name = input("Enter new staff username: ").strip()
    if staff_name in user_accounts:
        print("That username is already taken. Try another.\n")
        return

    password = input("Create a password: ").strip()
    department = input("Assign department (IT, HR, Finance, Support, etc.): ").strip()

    user_accounts[staff_name] = {"password": password, "role": "staff"}
    staff_accounts[staff_name] = department
    print(f"Staff '{staff_name}' added to '{department}' department.\n")

# Submit a complaint
def submit_complaint(username):
    category = input("Enter complaint category (IT, HR, Finance, Support, etc.): ").strip()
    description = input("Describe your complaint: ").strip()

    complaints_db.append({
        "user": username,
        "category": category,
        "description": description,
        "status": "Pending"
    })

    print("Your complaint has been submitted successfully.\n")

# Customers view complaints
def view_my_complaints(username):
    print("\nYour Complaints:")
    has_complaints = False

    for idx, complaint in enumerate(complaints_db):
        if complaint["user"] == username:
            print(f"{idx+1}. [{complaint['status']}] {complaint['category']}")
            print(f"   {complaint['description']}\n")
            has_complaints = True

    if not has_complaints:
        print("You haven't submitted any complaints yet.\n")

# Staff view complaints
def view_staff_complaints(username):
    department = staff_accounts.get(username)
    if not department:
        print("You are not assigned to any department.\n")
        return

    print(f"\nComplaints in {department} Department:")
    has_complaints = False

    for idx, complaint in enumerate(complaints_db):
        if complaint["category"].lower() == department.lower():
            print(f"{idx+1}. {complaint['user']} - [{complaint['status']}] {complaint['category']}")
            print(f"   {complaint['description']}\n")
            has_complaints = True

    if not has_complaints:
        print(f"No complaints found for the {department} department.\n")

# Staff update complaint status
def update_staff_status(username):
    department = staff_accounts.get(username)
    if not department:
        print("You are not assigned to any department.\n")
        return

    view_staff_complaints(username)
    if not complaints_db:
        return

    while True:
        try:
            complaint_num = int(input("Enter complaint number to update (or 0 to cancel): ")) - 1
            if complaint_num == -1:
                print("Update canceled.\n")
                return
            if 0 <= complaint_num < len(complaints_db) and complaints_db[complaint_num]["category"].lower() == department.lower():
                new_status = input("Enter new status (Pending/In Progress/Resolved): ").strip()
                if new_status.lower() not in ["pending", "in progress", "resolved"]:
                    print("Invalid status. Try again.\n")
                    continue
                complaints_db[complaint_num]["status"] = new_status
                print("Complaint status updated successfully.\n")
                break
            else:
                print("Invalid complaint number or you are not authorized to update this complaint.\n")
        except ValueError:
            print("Please enter a valid number.\n")

# Admin view complaints
def view_complaints():
    if not complaints_db:
        print("No complaints have been submitted yet.\n")
        return

    print("\nAll Complaints:")
    for idx, complaint in enumerate(complaints_db):
        print(f"{idx+1}. {complaint['user']} - [{complaint['status']}] {complaint['category']}")
        print(f"   {complaint['description']}\n")

# Admin update complaint status
def update_status():
    view_complaints()
    if not complaints_db:
        return

    while True:
        try:
            complaint_num = int(input("Enter complaint number to update (or 0 to cancel): ")) - 1
            if complaint_num == -1:
                print("Update canceled.\n")
                return
            if 0 <= complaint_num < len(complaints_db):
                new_status = input("Enter new status (Pending/In Progress/Resolved): ").strip()
                complaints_db[complaint_num]["status"] = new_status
                print("Complaint status updated successfully.\n")
                break
            else:
                print("Invalid complaint number. Try again.\n")
        except ValueError:
            print("Please enter a valid number.\n")

# Login
def login():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if username in user_accounts and user_accounts[username]["password"] == password:
        role = user_accounts[username]["role"]
        print(f"\nLogin successful! Welcome, {username} ({role.capitalize()})\n")

        if role == "admin":
            admin_menu()
        elif role == "staff":
            staff_menu(username)
        else:
            customer_menu(username)
    else:
        print("Invalid username or password.\n")

# Customer Menu
def customer_menu(username):
    while True:
        print("\nCustomer Menu:")
        print("1. Submit Complaint")
        print("2. View Complaint Status")
        print("3. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            submit_complaint(username)
        elif choice == "2":
            view_my_complaints(username)
        elif choice == "3":
            print("Logging out...\n")
            break
        else:
            print("Invalid choice. Try again.\n")

# Staff Menu
def staff_menu(username):
    while True:
        print("\nStaff Menu:")
        print("1. View Assigned Complaints")
        print("2. Update Complaint Status")
        print("3. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_staff_complaints(username)
        elif choice == "2":
            update_staff_status(username)
        elif choice == "3":
            print("Logging out...\n")
            break
        else:
            print("Invalid choice. Try again.\n")

# Admin Menu
def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. View All Complaints")
        print("2. Update Any Complaint Status")
        print("3. Add Staff Member")
        print("4. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_complaints()
        elif choice == "2":
            update_status()
        elif choice == "3":
            add_staff()
        elif choice == "4":
            print("Logging out...\n")
            break
        else:
            print("Invalid choice. Try again.\n")

# Main Menu
while True:
    print("\nWelcome to Fixzy!\n")
    print("1. Login")
    print("2. Register as Customer")
    print("3. Exit")
    option = input("Choose an option: ").strip()

    if option == "1":
        login()
    elif option == "2":
        register_user()
    elif option == "3":
        print("Exiting... Goodbye!")
        break
    else:
        print("Invalid option. Please try again.\n")
