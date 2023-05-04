import mysql.connector
import tkinter as tk

db_config = {
    'user': 'root',
    'password': 'SQL_shane1',
    'host': 'localhost',
    'database': 'contact_management'
}

def display_contacts():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    cursor.execute('SELECT name, phone, email, address FROM contacts')
    contacts = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    contact_list_window = tk.Toplevel(root)
    
    title_label = tk.Label(contact_list_window, text='Contact List', font=('Arial', 16))
    title_label.pack(pady=10)
    
    table_frame = tk.Frame(contact_list_window)
    table_frame.pack(padx=10, pady=10)
    
    headers = ['Name', 'Phone', 'Email', 'Address']
    for col, header in enumerate(headers):
        header_label = tk.Label(table_frame, text=header, font=('Arial', 12, 'bold'))
        header_label.grid(row=0, column=col, padx=5, pady=5)
    
    for row, contact in enumerate(contacts):
        for col, value in enumerate(contact):
            value_label = tk.Label(table_frame, text=value, font=('Arial', 12))
            value_label.grid(row=row+1, column=col, padx=5, pady=5)

    contact_list_window.resizable(True, True)

def open_contact_window(title, contact=None):
    contact_window = tk.Toplevel(root)
    contact_window.title(title)
    
    name_label = tk.Label(contact_window, text='Name', font=('Arial', 12))
    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(contact_window, font=('Arial', 12))
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    
    phone_label = tk.Label(contact_window, text='Phone', font=('Arial', 12))
    phone_label.grid(row=1, column=0, padx=5, pady=5)
    phone_entry = tk.Entry(contact_window, font=('Arial', 12))
    phone_entry.grid(row=1, column=1, padx=5, pady=5)
    
    email_label = tk.Label(contact_window, text='Email', font=('Arial', 12))
    email_label.grid(row=2, column=0, padx=5, pady=5)
    email_entry = tk.Entry(contact_window, font=('Arial', 12))
    email_entry.grid(row=2, column=1, padx=5, pady=5)

    address_label = tk.Label(contact_window, text='Address', font=('Arial', 12) )
    address_label.grid(row=3, column=0, padx=5, pady=5)
    address_entry = tk.Entry(contact_window, font=('Arial', 12))
    address_entry.grid(row=3, column=1, padx=5, pady=5)
    
    if contact:
        name_entry.insert(0, contact[0])
        phone_entry.insert(0, contact[1])
        email_entry.insert(0, contact[2])
        address_entry.insert(0, contact[3])
    
    submit_button = tk.Button(contact_window, text='Submit', font=('Arial', 12), command=lambda: save_contact(name_entry.get(), phone_entry.get(), email_entry.get(), address_entry.get(), contact))
    submit_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
    
    contact_window.resizable(False, False)

def add_contact():
    open_contact_window('Add Contact')

def edit_contact_window():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM contacts')
    contacts = cursor.fetchall()

    cursor.close()
    conn.close()

    edit_contact_window = tk.Toplevel(root)

    title_label = tk.Label(edit_contact_window, text='Edit Contact', font=('Arial', 16))
    title_label.pack(pady=10)

    form_frame = tk.Frame(edit_contact_window)
    form_frame.pack(padx=10, pady=10)

    select_label = tk.Label(form_frame, text='Select Contact:', font=('Arial', 12))
    select_label.grid(row=0, column=0, padx=5, pady=5)

    select_var = tk.StringVar()
    select_dropdown = tk.OptionMenu(form_frame, select_var, *[contact[1] for contact in contacts])
    select_dropdown.grid(row=0, column=1, padx=5, pady=5)

    name_label = tk.Label(form_frame, text='Name:', font=('Arial', 12))
    name_label.grid(row=1, column=0, padx=5, pady=5)

    name_var = tk.StringVar()
    name_entry = tk.Entry(form_frame, textvariable=name_var, font=('Arial', 12))
    name_entry.grid(row=1, column=1, padx=5, pady=5)

    phone_label = tk.Label(form_frame, text='Phone:', font=('Arial', 12))
    phone_label.grid(row=2, column=0, padx=5, pady=5)

    phone_var = tk.StringVar()
    phone_entry = tk.Entry(form_frame, textvariable=phone_var, font=('Arial', 12))
    phone_entry.grid(row=2, column=1, padx=5, pady=5)

    email_label = tk.Label(form_frame, text='Email:', font=('Arial', 12))
    email_label.grid(row=3, column=0, padx=5, pady=5)

    email_var = tk.StringVar()
    email_entry = tk.Entry(form_frame, textvariable=email_var, font=('Arial', 12))
    email_entry.grid(row=3, column=1, padx=5, pady=5)

    address_label = tk.Label(form_frame, text='Address:', font=('Arial', 12))
    address_label.grid(row=4, column=0, padx=5, pady=5)

    address_var = tk.StringVar()
    address_entry = tk.Entry(form_frame, textvariable=address_var, font=('Arial', 12))
    address_entry.grid(row=4, column=1, padx=5, pady=5)

    def populate_fields():
        selected_contact = None
        for contact in contacts:
            if contact[1] == select_var.get():
                selected_contact = contact
                break

        if selected_contact:
            name_var.set(selected_contact[1])
            phone_var.set(selected_contact[2])
            email_var.set(selected_contact[3])
            address_var.set(selected_contact[4])

    def update_contact():
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        selected_contact_id = None
        for contact in contacts:
            if contact[1] == select_var.get():
                selected_contact_id = contact[0]
                break

        if selected_contact_id:
            update_query = "UPDATE contacts SET name=%s, phone=%s, email=%s, address=%s WHERE id=%s"
            update_data = (name_var.get(), phone_var.get(), email_var.get(), address_var.get(), selected_contact_id)
            cursor.execute(update_query, update_data)
            conn.commit()

        cursor.close()
        conn.close()

    update_button = tk.Button(form_frame, text='Update Contact', command=update_contact, font=('Arial', 12))
    update_button.grid(row=5, column=1, padx=5, pady=10)

    populate_fields()

    edit_contact_window.transient(root)
    edit_contact_window.grab_set()
    root.wait_window(edit_contact_window)

def delete_contact_by_name(name):
    conn = mysql.connector.connect(**db_config)

    cursor = conn.cursor()

    cursor.execute("DELETE FROM contacts WHERE name = %s", (name,))

    conn.commit()

    cursor.close()
    conn.close()

def fetch_contacts():
    conn = mysql.connector.connect(**db_config)

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()

    cursor.close()
    conn.close()

    return contacts


def open_delete_window():
    contacts = fetch_contacts()

    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Contact")

    prompt_label = tk.Label(delete_window, text="Select a contact to delete:")
    prompt_label.pack(pady=10)

    contacts_listbox = tk.Listbox(delete_window)
    contacts_listbox.pack()

    for contact in contacts:
        contacts_listbox.insert(tk.END, contact[1])

    def delete_contact():
        selected_contact = contacts_listbox.get(contacts_listbox.curselection())

        delete_contact_by_name(selected_contact)

        display_contacts()

        delete_window.destroy()

    delete_button = tk.Button(delete_window, text="Delete", command=delete_contact)
    delete_button.pack(pady=10)

def save_contact(name, phone, email, address, contact=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    if contact:
        cursor.execute('UPDATE contacts SET phone=%s, email=%s, address=%s, WHERE name=%s', (phone, email, address, contact[0]))
    else:
        cursor.execute('INSERT INTO contacts (name, phone, email, address) VALUES (%s, %s, %s, %s)', (name, phone, email, address))
    
    conn.commit()
    
    cursor.close()
    conn.close()
    
    root.focus_set()
    
    display_contacts()

root = tk.Tk()
root.title('Contacts')

display_button = tk.Button(root, text='Display Contacts', font=('Arial', 12), command=display_contacts)
display_button.pack(padx=10, pady=10)

add_button = tk.Button(root, text='Add Contact', font=('Arial', 12), command=add_contact)
add_button.pack(padx=10, pady=10)

display_button = tk.Button(root, text='Delete Contact', font=('Arial', 12), command=open_delete_window)
display_button.pack(padx=10, pady=10)

display_button = tk.Button(root, text='Edit Contact', font=('Arial', 12), command=edit_contact_window)
display_button.pack(padx=10, pady=10)

root.mainloop()