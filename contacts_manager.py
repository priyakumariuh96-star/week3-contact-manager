"""
Contact Management System
Week 3 Project - Functions & Dictionaries
"""

import json
import re
from datetime import datetime
import csv


# ==========================
# VALIDATION FUNCTIONS
# ==========================

def validate_phone(phone: str) -> tuple:
    """Validate phone number format (10–15 digits)."""
    digits = re.sub(r'\D', '', phone)
    if 10 <= len(digits) <= 15:
        return True, digits
    return False, None


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


# ==========================
# CRUD FUNCTIONS
# ==========================

def add_contact(contacts: dict) -> dict:
    print("\n--- ADD NEW CONTACT ---")

    while True:
        name = input("Enter contact name: ").strip()
        if not name:
            print("Name cannot be empty!")
            continue

        if name in contacts:
            print(f"Contact '{name}' already exists!")
            choice = input("Update instead? (y/n): ").lower()
            if choice == 'y':
                return update_contact(contacts, name)
            return contacts
        break

    while True:
        phone = input("Enter phone number: ").strip()
        valid, cleaned_phone = validate_phone(phone)
        if valid:
            break
        print("Invalid phone number! Must contain 10–15 digits.")

    while True:
        email = input("Enter email (optional): ").strip()
        if not email or validate_email(email):
            break
        print("Invalid email format!")

    address = input("Enter address (optional): ").strip()
    group = input("Enter group (Friends/Work/Family/Other): ").strip() or "Other"

    contacts[name] = {
        "phone": cleaned_phone,
        "email": email if email else None,
        "address": address if address else None,
        "group": group,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

    print(f"✅ Contact '{name}' added successfully!")
    return contacts


def update_contact(contacts: dict, name: str) -> dict:
    if name not in contacts:
        print("Contact not found!")
        return contacts

    print(f"\n--- UPDATE CONTACT: {name} ---")
    contact = contacts[name]

    new_phone = input(f"New phone (current: {contact['phone']}): ").strip()
    if new_phone:
        valid, cleaned_phone = validate_phone(new_phone)
        if valid:
            contact["phone"] = cleaned_phone
        else:
            print("Invalid phone. Keeping old one.")

    new_email = input(f"New email (current: {contact['email']}): ").strip()
    if new_email:
        if validate_email(new_email):
            contact["email"] = new_email
        else:
            print("Invalid email. Keeping old one.")

    new_address = input(f"New address (current: {contact['address']}): ").strip()
    if new_address:
        contact["address"] = new_address

    new_group = input(f"New group (current: {contact['group']}): ").strip()
    if new_group:
        contact["group"] = new_group

    contact["updated_at"] = datetime.now().isoformat()

    print("✅ Contact updated successfully!")
    return contacts


def delete_contact(contacts: dict, name: str) -> dict:
    if name not in contacts:
        print("Contact not found!")
        return contacts

    confirm = input(f"Are you sure you want to delete '{name}'? (y/n): ").lower()
    if confirm == 'y':
        del contacts[name]
        print("✅ Contact deleted.")
    else:
        print("Deletion cancelled.")

    return contacts


# ==========================
# SEARCH & DISPLAY
# ==========================

def search_contacts(contacts: dict, search_term: str) -> dict:
    search_term = search_term.lower()
    return {
        name: info
        for name, info in contacts.items()
        if search_term in name.lower()
    }


def display_contacts(contacts: dict) -> None:
    if not contacts:
        print("No contacts found.")
        return

    print(f"\nFound {len(contacts)} contact(s):")
    print("-" * 50)

    for i, (name, info) in enumerate(contacts.items(), 1):
        print(f"{i}. {name}")
        print(f"   Phone: {info['phone']}")
        if info["email"]:
            print(f"   Email: {info['email']}")
        if info["address"]:
            print(f"   Address: {info['address']}")
        print(f"   Group: {info['group']}")
        print()


# ==========================
# FILE OPERATIONS
# ==========================

def save_to_file(contacts: dict, filename="contacts_data.json") -> None:
    with open(filename, "w") as file:
        json.dump(contacts, file, indent=4)
    print("Contacts saved successfully!")


def load_from_file(filename="contacts_data.json") -> dict:
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def export_to_csv(contacts: dict, filename="contacts.csv") -> None:
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Phone", "Email", "Address", "Group"])

        for name, info in contacts.items():
            writer.writerow([
                name,
                info["phone"],
                info["email"],
                info["address"],
                info["group"]
            ])

    print("Contacts exported to CSV!")


# ==========================
# STATISTICS
# ==========================

def show_statistics(contacts: dict) -> None:
    print("\n--- CONTACT STATISTICS ---")
    print(f"Total Contacts: {len(contacts)}")

    groups = {}
    for contact in contacts.values():
        group = contact["group"]
        groups[group] = groups.get(group, 0) + 1

    print("\nContacts by Group:")
    for group, count in groups.items():
        print(f"{group}: {count}")


# ==========================
# MAIN MENU
# ==========================

def main():
    contacts = load_from_file()

    while True:
        print("\n====== CONTACT MANAGEMENT SYSTEM ======")
        print("1. Add Contact")
        print("2. Search Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Display All Contacts")
        print("6. Export to CSV")
        print("7. Show Statistics")
        print("8. Save & Exit")

        choice = input("Choose an option (1-8): ")

        if choice == '1':
            contacts = add_contact(contacts)
        elif choice == '2':
            term = input("Enter name to search: ")
            display_contacts(search_contacts(contacts, term))
        elif choice == '3':
            name = input("Enter exact name to update: ")
            contacts = update_contact(contacts, name)
        elif choice == '4':
            name = input("Enter exact name to delete: ")
            contacts = delete_contact(contacts, name)
        elif choice == '5':
            display_contacts(contacts)
        elif choice == '6':
            export_to_csv(contacts)
        elif choice == '7':
            show_statistics(contacts)
        elif choice == '8':
            save_to_file(contacts)
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()