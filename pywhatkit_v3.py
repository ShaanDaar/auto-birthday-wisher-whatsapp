import tkinter as tk
from tkinter import messagebox
import pywhatkit
import pandas as pd
import datetime

class BirthdayWisher:
    def __init__(self, root):
        self.root = root
        self.root.title("Birthday Wisher")
        
        # Initialize contacts_df as a class attribute
        self.contacts_df = self.get_contacts()

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.main_frame, text="Birthday Wisher Menu:").pack(fill="x")

        tk.Button(self.main_frame, text="Send Birthday Wishes", command=self.send_birthday_wishes).pack(fill="x")
        tk.Button(self.main_frame, text="Add Contact", command=self.add_contact).pack(fill="x")
        tk.Button(self.main_frame, text="View Contacts", command=self.view_contacts).pack(fill="x")
        tk.Button(self.main_frame, text="Delete Contact", command=self.delete_contact).pack(fill="x")
        tk.Button(self.main_frame, text="Exit", command=self.root.destroy).pack(fill="x")

    def send_birthday_wishes(self):
        today = datetime.datetime.now().strftime("%d/%m")
        count = False
        for index, row in self.contacts_df.iterrows():
            birthday = row['birthday']
            phone_number = str(row['phone_number'])  # Convert phone number to string
            name = row['name']

            # Add country code to phone number if it doesn't already exist
            if not phone_number.startswith('+'):
                phone_number = '+91' + phone_number  # Assuming country code is +91

            if birthday == today:
                message = f"Happy birthday, {name}!"
                self.send_birthday_message(phone_number, message)
                count = True
        if count == False:
            messagebox.showinfo("No birthday messages sent today.")

    def add_contact(self):
        add_contact_window = tk.Toplevel(self.root)
        add_contact_window.title("Add Contact")

        tk.Label(add_contact_window, text="Enter contact name:").pack(fill="x")
        name_entry = tk.Entry(add_contact_window)
        name_entry.pack(fill="x")

        tk.Label(add_contact_window, text="Enter contact phone number:").pack(fill="x")
        phone_number_entry = tk.Entry(add_contact_window)
        phone_number_entry.pack(fill="x")

        tk.Label(add_contact_window, text="Enter contact birthday (dd/mm):").pack(fill="x")
        birthday_entry = tk.Entry(add_contact_window)
        birthday_entry.pack(fill="x")

        def add_contact_to_csv():
            name = name_entry.get()
            phone_number = phone_number_entry.get()
            birthday = birthday_entry.get()

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
                messagebox.showinfo("Contact added successfully!")
            except FileNotFoundError:
                new_contact_df.to_csv("contacts.csv", index=False)
                messagebox.showinfo("Contact added successfully!")

        tk.Button(add_contact_window, text="Add Contact", command=add_contact_to_csv).pack(fill="x")

    def view_contacts(self):
        view_contacts_window = tk.Toplevel(self.root)
        view_contacts_window.title("View Contacts")

        try:
            contacts_df = pd.read_csv("contacts.csv")
            text_widget = tk.Text(view_contacts_window)
            text_widget.pack(fill="both", expand=True)
            text_widget.insert("1.0", str(contacts_df))
        except FileNotFoundError:
            messagebox.showinfo("No contacts found.")

    def delete_contact(self):
        delete_contact_window = tk.Toplevel(self.root)
        delete_contact_window.title("Delete Contact")

        # Access contacts_df from the class attribute
        try:
            contacts_df = self.contacts_df  # Use the class attribute
            text_widget = tk.Text(delete_contact_window)
            text_widget.pack(fill="both", expand=True)
            text_widget.insert("1.0", str(contacts_df))

            tk.Label(delete_contact_window, text="Enter the index of the contact you want to delete:").pack(fill="x")
            index_entry = tk.Entry(delete_contact_window)
            index_entry.pack(fill="x")

            def delete_contact_from_csv():
                index = int(index_entry.get())
                # Ensure contacts_df is updated after deletion
                self.contacts_df = self.contacts_df.drop(index)
                self.contacts_df.to_csv("contacts.csv", index=False)
                messagebox.showinfo("Contact deleted successfully!")

            tk.Button(delete_contact_window, text="Delete Contact", command=delete_contact_from_csv).pack(fill="x")
        except FileNotFoundError:
            messagebox.showinfo("No contacts found.")
        except Exception as e:
            messagebox.showinfo(f"Error: {str(e)}")

    def get_contacts(self):
        try:
            contacts_df = pd.read_csv("contacts.csv")
            return contacts_df
        except FileNotFoundError:
            return pd.DataFrame(columns=["name", "phone_number", "birthday"])

    def send_birthday_message(self, phone_number, message):
        try:
            # Remove the country code from the phone number
            country_code = "+91"
            phone_number = phone_number.replace(country_code, "")

            # Send the message
            pywhatkit.sendwhatmsg_instantly(f"+91{phone_number}", message)
            messagebox.showinfo(f"Birthday message sent successfully to {phone_number}!")
        except Exception as e:
            messagebox.showinfo(f"Failed to send birthday message to {phone_number}: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")
    birthday_wisher = BirthdayWisher(root)
    root.mainloop()