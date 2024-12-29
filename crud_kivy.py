import psycopg2
from tkinter import *
from tkinter import messagebox


# Database connection
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="crud_db",
            user="postgres",
            password="123",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# CRUD Functions
def create_record():
    name = entry_name.get()
    email = entry_email.get()
    phone = entry_phone.get()

    if not name or not email or not phone:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO employees (name, email, phone) VALUES (%s, %s, %s)",
            (name, email, phone)
        )
        conn.commit()
        messagebox.showinfo("Success", "Record added successfully!")
        fetch_records()
        clear_inputs()
    except Exception as e:
        messagebox.showerror("Insert Error", str(e))
    finally:
        conn.close()


def fetch_records():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        listbox_records.delete(0, END)
        for row in rows:
            listbox_records.insert(END, row)
    except Exception as e:
        messagebox.showerror("Fetch Error", str(e))
    finally:
        conn.close()


def update_record():
    try:
        selected = listbox_records.get(listbox_records.curselection())
        record_id = selected[0]
    except IndexError:
        messagebox.showwarning("Selection Error", "Select a record to update")
        return

    name = entry_name.get()
    email = entry_email.get()
    phone = entry_phone.get()

    if not name or not email or not phone:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE employees SET name=%s, email=%s, phone=%s WHERE id=%s",
            (name, email, phone, record_id)
        )
        conn.commit()
        messagebox.showinfo("Success", "Record updated successfully!")
        fetch_records()
        clear_inputs()
    except Exception as e:
        messagebox.showerror("Update Error", str(e))
    finally:
        conn.close()


def delete_record():
    try:
        selected = listbox_records.get(listbox_records.curselection())
        record_id = selected[0]
    except IndexError:
        messagebox.showwarning("Selection Error", "Select a record to delete")
        return

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM employees WHERE id=%s", (record_id,))
        conn.commit()
        messagebox.showinfo("Success", "Record deleted successfully!")
        fetch_records()
    except Exception as e:
        messagebox.showerror("Delete Error", str(e))
    finally:
        conn.close()


def clear_inputs():
    entry_name.delete(0, END)
    entry_email.delete(0, END)
    entry_phone.delete(0, END)


def on_listbox_select(event):
    try:
        # Get selected item
        selected = listbox_records.get(listbox_records.curselection())
        # Populate the entry fields with selected item data
        entry_name.delete(0, END)
        entry_name.insert(END, selected[1])
        entry_email.delete(0, END)
        entry_email.insert(END, selected[2])
        entry_phone.delete(0, END)
        entry_phone.insert(END, selected[3])
    except IndexError:
        # If no item is selected, do nothing
        pass


# GUI Setup
root = Tk()
root.title("CRUD Application with PostgreSQL")
root.geometry("600x400")

# Labels and Entry Fields
Label(root, text="Name").grid(row=0, column=0, padx=10, pady=10)
entry_name = Entry(root, width=30)
entry_name.grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Email").grid(row=1, column=0, padx=10, pady=10)
entry_email = Entry(root, width=30)
entry_email.grid(row=1, column=1, padx=10, pady=10)

Label(root, text="Phone").grid(row=2, column=0, padx=10, pady=10)
entry_phone = Entry(root, width=30)
entry_phone.grid(row=2, column=1, padx=10, pady=10)

# Buttons
Button(root, text="Add", command=create_record, width=10).grid(row=3, column=0, pady=10)
Button(root, text="Update", command=update_record, width=10).grid(row=3, column=1, pady=10)
Button(root, text="Delete", command=delete_record, width=10).grid(row=3, column=2, pady=10)
Button(root, text="Clear", command=clear_inputs, width=10).grid(row=3, column=3, pady=10)

# Listbox for Records
listbox_records = Listbox(root, width=70, height=15)
listbox_records.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

# Bind the Listbox select event
listbox_records.bind("<<ListboxSelect>>", on_listbox_select)

# Fetch records on load
fetch_records()

# Run the application
root.mainloop()
