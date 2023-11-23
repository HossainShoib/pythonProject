import json
from prettytable import PrettyTable


class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

    def __str__(self):
        return f"User(user_id={self.user_id}, name='{self.name}', email='{self.email}')"


class UserCRUD:
    def __init__(self, filename='users.json'):
        self.filename = filename
        self.users = self.load_users_from_file()
        self.next_user_id = max(user.user_id for user in self.users) + 1 if self.users else 1

    def load_users_from_file(self):
        try:
            with open(self.filename, 'r') as file:
                users_data = json.load(file)
                return [User(**user_data) for user_data in users_data]
        except FileNotFoundError:
            return []

    def save_users_to_file(self):
        users_data = [{'user_id': user.user_id, 'name': user.name, 'email': user.email} for user in self.users]
        with open(self.filename, 'w') as file:
            json.dump(users_data, file, indent=2)

    def create_user(self, name, email):
        new_user = User(self.next_user_id, name, email)
        self.next_user_id += 1
        self.users.append(new_user)
        self.save_users_to_file()
        return new_user

    def read_users(self):
        return self.users

    def update_user(self, user_id, name, email):
        for user in self.users:
            if user.user_id == user_id:
                user.name = name
                user.email = email
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


def display_users_table(users):
    table = PrettyTable()
    table.field_names = ["User ID", "Name", "Email"]

    for user in users:
        table.add_row([user.user_id, user.name, user.email])

    print(table)


def login():
    expected_username = "admin"
    expected_password = "password"

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    return username == expected_username and password == expected_password


# Main Program


if login():
    print("Login successful. Welcome, admin!")

# Interactive Console Input
user_crud = UserCRUD()

while True:
    print("\nOptions:")
    print("1. Add User")
    print("2. View Users")
    print("3. Update User")
    print("4. Delete User")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        name = input("Enter the name: ")
        email = input("Enter the email: ")
        user_crud.create_user(name, email)
        print("User added successfully!")

    elif choice == "2":
        users = user_crud.read_users()
        if users:
            print("\nUsers:")
            display_users_table(users)
        else:
            print("No users to display.")

    elif choice == "3":

        user_id = int(input("Enter the user ID to update: "))

        # Modified name input handling

        name = input("Enter the updated name (press Enter to keep the existing name): ")

        if not name.strip():  # If the entered name is empty, keep the existing name

            existing_user = next((user for user in user_crud.read_users() if user.user_id == user_id), None)

            if existing_user:
                name = existing_user.name

        # Modified email input handling

        email = input("Enter the updated email (press Enter to keep the existing email): ")

        if not email.strip():  # If the entered email is empty, keep the existing email

            existing_user = next((user for user in user_crud.read_users() if user.user_id == user_id), None)

            if existing_user:
                email = existing_user.email

        updated_user = user_crud.update_user(user_id, name, email)

        if updated_user:

            print("User updated successfully!")

        else:

            print("User not found.")

    elif choice == "4":
        user_id = int(input("Enter the user ID to delete: "))
        deleted = user_crud.delete_user(user_id)
        if deleted:
            print("User deleted successfully!")
        else:
            print("User not found.")


    elif choice == "5":

        print("Exiting program. Goodbye!")

        break


    else:

        print("Invalid choice. Please enter a number between 1 and 5.")

else:

    print("Login failed. Access denied.")
