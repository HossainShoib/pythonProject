import json
from prettytable import PrettyTable


class User:
    def __init__(self, user_id, name, email, password , balance=0.0):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.balance = balance

    def __str__(self):
        return f"User(user_id={self.user_id}, name='{self.name}', email='{self.email}', password='{self.password}')"


class UserCRUD:
    def __init__(self, filename="users.json"):
        self.filename = filename
        self.users = self.load_users_from_file()
        self.next_user_id = (
            max(user.user_id for user in self.users) + 1 if self.users else 1
        )

    def deposit(self, user_id, amount):
        for user in self.users:
            if user.user_id == user_id:
                user.balance += amount
                self.save_users_to_file()
                return user
        return None

    def withdraw(self, user_id, amount):
        for user in self.users:
            if user.user_id == user_id and user.balance >= amount:
                user.balance -= amount
                self.save_users_to_file()
                return user
        return None

    def load_users_from_file(self):
        try:
            with open(self.filename, "r") as file:
                users_data = json.load(file)
                return [
                    User(
                        user_data["user_id"],
                        user_data["name"],
                        user_data["email"],
                        user_data["password"],
                    )
                    for user_data in users_data
                ]
        except FileNotFoundError:
            return []

    def save_users_to_file(self):
        users_data = [
            {
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "password": user.password,
            }
            for user in self.users
        ]
        with open(self.filename, "w") as file:
            json.dump(users_data, file, indent=2)

    def create_user(self, name, email, password):
        new_user = User(self.next_user_id, name, email, password)
        self.next_user_id += 1
        self.users.append(new_user)
        self.save_users_to_file()
        return new_user

    def read_users(self):
        return self.users

    def update_user(self, user_id, name, email, password):
        for user in self.users:
            if user.user_id == user_id:
                user.name = name
                user.email = email
                user.password = password
                self.save_users_to_file()
                return user
        return None

    def delete_user(self, user_id):
        for i, user in enumerate(self.users):
            if user.user_id == user_id:
                del self.users[i]
                self.save_users_to_file()
                return True
        return False

    def login(self, email, password):
        for user in self.users:
            if user.email == email and user.password == password:
                return user
        return None


def display_users_table(users):
    table = PrettyTable()
    table.field_names = ["User ID", "Name", "Email", "Password"]

    for user in users:
        table.add_row([user.user_id, user.name, user.email, user.password])

    print(table)


def display_user_details(user):
    table = PrettyTable()
    table.field_names = ["User ID", "Name", "Email"]

    table.add_row([user.user_id, user.name, user.email])

    print(table)


# Main Program
print("Welcome to the User Management System!")

while True:
    print("\nOptions:")
    print("1. User Registration")
    print("2. User Login")
    print("3. Admin Login")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        name = input("Enter your full name: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        user_crud = UserCRUD()
        user_crud.create_user(name, email, password)
        print("User registered successfully!")

    elif choice == "2":
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        user_crud = UserCRUD()
        logged_in_user = user_crud.login(email, password)

        if logged_in_user:
            print(f"Login successful. Welcome, {logged_in_user.name}!")
            display_user_details(logged_in_user)

            while True:
                print("\nUser Options:")
                print("1. View Your Details")
                print("2. Update Your Details")
                print("3. Deposit Money")
                print("4. Withdraw Money")
                print("5. Delete Your Account")
                print("6. Logout")

                user_option = input("Enter your choice (1-6): ")

                if user_option == "1":
                    display_user_details(logged_in_user)

                elif user_option == "2":
                    name = input(
                        "Enter the updated name (press Enter to keep the existing name): "
                    )
                    email = input(
                        "Enter the updated email (press Enter to keep the existing email): "
                    )
                    password = input(
                        "Enter the updated password (press Enter to keep the existing password): "
                    )

                    if not name.strip():
                        name = logged_in_user.name

                    if not email.strip():
                        email = logged_in_user.email

                    if not password.strip():
                        password = logged_in_user.password

                    updated_user = user_crud.update_user(
                        logged_in_user.user_id, name, email, password
                    )

                    if updated_user:
                        print("Your details updated successfully!")
                        display_user_details(updated_user)
                    else:
                        print("Failed to update your details.")

                elif user_option == "3":
                    try:
                        amount = float(input("Enter the amount to deposit: "))
                        if amount > 0:
                            logged_in_user = user_crud.deposit(logged_in_user.user_id, amount)
                            print(f"Deposit of {amount} successful. New balance: {logged_in_user.balance}")
                        else:
                            print("Invalid amount. Please enter a positive value.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

                elif user_option == "4":
                    try:
                        amount = float(input("Enter the amount to withdraw: "))
                        if amount > 0:
                            if logged_in_user.balance >= amount:
                                logged_in_user = user_crud.withdraw(logged_in_user.user_id, amount)
                                print(f"Withdrawal of {amount} successful. New balance: {logged_in_user.balance}")
                            else:
                                print("Insufficient funds.")
                        else:
                            print("Invalid amount. Please enter a positive value.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

                elif user_option == "5":
                    confirm_delete = input(
                        "Are you sure you want to delete your account? (yes/no): "
                    ).lower()
                    if confirm_delete == "yes":
                        deleted = user_crud.delete_user(logged_in_user.user_id)
                        if deleted:
                            print("Your account has been deleted. Goodbye!")
                            break
                        else:
                            print("Failed to delete your account.")
                    else:
                        print("Account deletion canceled.")

                elif user_option == "6":
                    print("Logging out. Goodbye!")
                    break

                else:
                    print("Invalid choice. Please enter a number between 1 and 6.")

        else:
            print("Login failed. Invalid email or password.")

    elif choice == "3":
        admin_username = input("Enter admin username: ")
        admin_password = input("Enter admin password: ")

        if admin_username == "admin" and admin_password == "password":
            print("Admin login successful. Welcome, admin!")

            user_crud = UserCRUD()

            while True:
                print("\nAdmin Options:")
                print("1. View Users")
                print("2. Update User")
                print("3. Delete User")
                print("4. Exit")

                admin_choice = input("Enter your choice (1-4): ")

                if admin_choice == "1":
                    users = user_crud.read_users()
                    if users:
                        print("\nUsers:")
                        display_users_table(users)
                    else:
                        print("No users to display.")

                elif admin_choice == "2":
                    user_id = int(input("Enter the user ID to update: "))
                    name, email, password = user_registration()
                    updated_user = user_crud.update_user(user_id, name, email, password)
                    if updated_user:
                        print("User updated successfully!")
                        display_users_table([updated_user])
                    else:
                        print("User not found.")

                elif admin_choice == "3":
                    user_id = int(input("Enter the user ID to delete: "))
                    deleted = user_crud.delete_user(user_id)
                    if deleted:
                        print("User deleted successfully!")
                    else:
                        print("User not found.")

                elif admin_choice == "4":
                    print("Exiting admin panel. Goodbye, admin!")
                    break

                else:
                    print("Invalid choice. Please enter a number between 1 and 4.")

        else:
            print("Admin login failed. Access denied.")

    elif choice == "4":
        print("Exiting program. Goodbye!")
        break

    else:
        print("Invalid choice. Please enter a number between 1 and 4.")
