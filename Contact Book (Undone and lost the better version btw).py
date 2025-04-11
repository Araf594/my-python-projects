# 📖 Contact Book (List-Based Approach)

contact_list = []  # Stores Contact


def add_new_contact():
    """Adds a new contact to the list"""
    name = input('\n 😁 Please enter the name of the contact you want to add: ').strip().upper()

    matching_contacts = [contact for contact in contact_list if contact['Name'] == name]

    if matching_contacts:
        print('\n 😲 A contact with this name already exists!')
        while True:
            update = input('\n 📖 Do you want to update the existing contact instead? (Yes/No): ').strip().lower()
            if update == 'yes':
                update_contact(name)
                return
            elif update == 'no':
                print('\n ✌ Use a different name if this is a different person.')
                return
            else:
                print('\n 😐 Please enter "Yes" or "No".')

    phone_num_list = []
    while True:
        phone_number = input('\n 📞 Please enter the phone number: ').strip()
        if not phone_number.isdigit():
            print('\n 🚩 Please enter a valid number (digits only)!')
            continue
        phone_num_list.append(phone_number)
        if input('\n 📞 Do you want to add another phone number? (Yes/No): ').strip().lower() == 'no':
            break

    info = input('\n📧 Enter the email/address (Leave blank if not needed): ').strip()

    new_contact = {'Name': name, 'Phone Number': phone_num_list}
    if info:
        new_contact['Contact Info'] = info

    print('\n Assign this contact to a group:')
    print('1. Family 👪')
    print('2. Friends 👫')
    print('3. Work 🕴')

    while True:
        group_choice = input('\n Choose (1,2,3) or leave blank: ').strip()
        if group_choice == '1':
            new_contact['Group'] = 'Family'
            break
        elif group_choice == '2':
            new_contact['Group'] = 'Friends'
            break
        elif group_choice == '3':
            new_contact['Group'] = 'Work'
            break
        elif not group_choice:
            break
        else:
            print('\n 🙃 Please enter a valid option (1,2,3) or leave blank.')

    contact_list.append(new_contact)
    print('\n ✅ Contact successfully added!')


def search_contact(contact_name):
    """Searches for a contact in the contact list"""
    results = [contact for contact in contact_list if contact_name.upper() in contact['Name']]

    if results:
        print('\n------------------📖 Search Results 📖------------------')
        for idx, contact in enumerate(results, start=1):
            print(f'\n {idx}. Contact Name: {contact["Name"]}')
            print(f' 📞 Phone Number: {", ".join(contact["Phone Number"])}')
            if 'Contact Info' in contact:
                print(f' 📧 Contact Info: {contact["Contact Info"]}')
            if 'Group' in contact:
                print(f' 👥 Group: {contact["Group"]}')
    else:
        print('\n ☹ No matching contact found.')


def update_contact(contact_name):
    """Updates a contact in the contact list"""
    matches = [contact for contact in contact_list if contact['Name'] == contact_name.upper()]

    if not matches:
        print('\n 🚩 Contact not found!')
        return

    if len(matches) > 1:
        print('\n ⚠ Multiple contacts found. Please confirm:')
        for idx, contact in enumerate(matches, start=1):
            print(f'\n {idx}. {contact["Name"]} | 📞 {", ".join(contact["Phone Number"])}')

        while True:
            try:
                choice = int(input('\n Choose the number of the contact to update: '))
                selected_contact = matches[choice - 1]
                break
            except (IndexError, ValueError):
                print('\n 😐 Please enter a valid number.')
    else:
        selected_contact = matches[0]

    print('\n 🛠 What would you like to update?')
    print('1. Name 📄')
    print('2. Phone Number 📞')
    print('3. Contact Info 📧')
    print('4. Group 👥')

    while True:
        choice = input('\n Choose an option (1,2,3,4): ').strip()
        if choice == '1':
            new_name = input('\n 📄 Enter new name: ').strip().upper()
            selected_contact['Name'] = new_name
            print('\n ✅ Name updated!')
            return
        elif choice == '2':
            print(f'\n 📞 Current Numbers: {", ".join(selected_contact["Phone Number"])}')
            selected_contact['Phone Number'] = input('\n 📞 Enter new numbers (comma-separated): ').split(',')
            print('\n ✅ Phone number updated!')
            return
        elif choice == '3':
            selected_contact['Contact Info'] = input('\n 📧 Enter new contact info: ').strip()
            print('\n ✅ Contact Info updated!')
            return
        elif choice == '4':
            selected_contact['Group'] = input('\n 👥 Enter new group (Family, Friends, Work): ').strip()
            print('\n ✅ Group updated!')
            return
        else:
            print('\n 😐 Please enter a valid option.')


def delete_contact(contact_name):
    """Deletes a contact from the contact list"""
    matches = [contact for contact in contact_list if contact['Name'] == contact_name.upper()]

    if not matches:
        print('\n ☹ No matching contact found!')
        return

    if len(matches) > 1:
        print('\n ⚠ Multiple contacts found. Please confirm:')
        for idx, contact in enumerate(matches, start=1):
            print(f'\n {idx}. {contact["Name"]} | 📞 {", ".join(contact["Phone Number"])}')

        while True:
            try:
                choice = int(input('\n Choose the number of the contact to delete: '))
                contact_list.remove(matches[choice - 1])
                print('\n ✅ Contact deleted successfully!')
                return
            except (IndexError, ValueError):
                print('\n 😐 Please enter a valid number.')
    else:
        contact_list.remove(matches[0])
        print('\n ✅ Contact deleted successfully!')


def display_contacts():
    """Displays all contacts in a sorted or default order"""
    if not contact_list:
        print('\n 🙃 No contacts available.')
        return

    print('\n Choose display order:')
    print('1. Default (As Added)')
    print('2. Sorted by Name (A-Z)')
    print('3. Sorted by Name (Z-A)')

    while True:
        choice = input('\n Choose an option (1,2,3): ').strip()
        if choice == '1':
            sorted_contacts = contact_list
        elif choice == '2':
            sorted_contacts = sorted(contact_list, key=lambda x: x['Name'])
        elif choice == '3':
            sorted_contacts = sorted(contact_list, key=lambda x: x['Name'], reverse=True)
        else:
            print('\n 😐 Please enter a valid option.')
            continue
        break

    print('\n------------------📄 Contact List 📄------------------')
    for idx, contact in enumerate(sorted_contacts, start=1):
        print(f'\n {idx}. Contact Name: {contact["Name"]}')
        print(f' 📞 Number: {", ".join(contact["Phone Number"])}')
        if 'Contact Info' in contact:
            print(f' 📧 Contact Info: {contact["Contact Info"]}')
        if 'Group' in contact:
            print(f' 👥 Group: {contact["Group"]}')


# Run Contact Book
def contact_book():
    while True:
        print('\n------------------⚙ Contact Book ⚙------------------')
        print('1. Add Contact  2. Search  3. Update  4. Delete  5. Display  6. Exit')
        option = input('\n Choose an option: ').strip()
        if option == '1':
            add_new_contact()
        elif option == '2':
            search_contact(input('\n Enter contact name to search: '))
        elif option == '3':
            update_contact(input('\n Enter contact name to update: '))
        elif option == '4':
            delete_contact(input('\n Enter contact name to delete: '))
        elif option == '5':
            display_contacts()
        elif option == '6':
            break


contact_book()
