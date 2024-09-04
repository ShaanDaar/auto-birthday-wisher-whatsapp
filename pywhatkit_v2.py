import pywhatkit
import datetime
import pandas as pd

def send_birthday_message(phone_number, message):
    try:
        # Remove the country code from the phone number
        country_code = "+91"
        phone_number = phone_number.replace(country_code, "")

        # Send the message
        pywhatkit.sendwhatmsg_instantly(f"+91{phone_number}", message)
        print(f"Birthday message sent successfully to {phone_number}!")
    except Exception as e:
        print(f"Failed to send birthday message to {phone_number}: {str(e)}")

def get_contacts():
    try:
        contacts_df = pd.read_csv("contacts.csv")
        return contacts_df
    except FileNotFoundError:
        return pd.DataFrame(columns=["name", "phone_number", "birthday"])

def main() -> None:
    """
    Sends birthday wishes to contacts whose birthday is today.
    """
    contacts = get_contacts()
    today = datetime.datetime.now().strftime("%d/%m")

    date_str = input("Enter date (dd/mm): ")
    try:
        date_obj = datetime.datetime.strptime(date_str, "%d/%m").date()
    except ValueError:
        print("Invalid date format. Please use dd/mm.")
        return

    if date_str == today:
        for index, row in contacts.iterrows():
            birthday = row['birthday']
            phone_number = str(row['phone_number'])  # Convert phone number to string
            name = row['name']

            # Add country code to phone number if it doesn't already exist
            if not phone_number.startswith('+'):
                phone_number = '+91' + phone_number  # Assuming country code is +91

            if birthday == today:
                message = f"Happy birthday, {name}!"
                send_birthday_message(phone_number, message)
    else:
        print("No birthday messages sent today.")

def add_contact():
    name = input("Enter contact name: ")
    phone_number = input("Enter contact phone number: ")
    birthday = input("Enter contact birthday (dd/mm): ")

    new_contact = {
        "name": [name],
        "phone_number": [phone_number],
        "birthday": [birthday]
    }

    new_contact_df = pd.DataFrame(new_contact)

    try:
        contacts_df = pd.read_csv("contacts.csv")
        contacts_df = pd.concat([contacts_df, new_contact_df])
        contacts_df.to_csv("contacts.csv", index=False)
        print("Contact added successfully!")
    except FileNotFoundError:
        new_contact_df.to_csv("contacts.csv", index=False)
        print("Contact added successfully!")

def view_contacts():
    try:
        contacts_df = pd.read_csv("contacts.csv")
        print(contacts_df)
    except FileNotFoundError:
        print("No contacts found.")

def delete_contact():
    try:
        contacts_df = pd.read_csv("contacts.csv")
        print(contacts_df)
        index = int(input("Enter the index of the contact you want to delete: "))
        contacts_df = contacts_df.drop(index)
        contacts_df.to_csv("contacts.csv", index=False)
        print("Contact deleted successfully!")
    except FileNotFoundError:
        print("No contacts found.")

def main_menu():
    while True:
        print("\nBirthday Wisher Menu:")
        print("1. Send Birthday Wishes")
        print("2. Add Contact")
        print("3. View Contacts")
        print("4. Delete Contact")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            main()
        elif choice == "2":
            add_contact()
        elif choice == "3":
            view_contacts()
        elif choice == "4":
            delete_contact()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()