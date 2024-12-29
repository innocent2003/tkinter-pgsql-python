import re
from tkinter import *
from tkinter import messagebox


def validate_phone():
    phone = entry_phone.get()

    # Regular expression for Vietnamese phone numbers
    vn_phone_pattern = r"^(03|05|07|08|09|02)\d{8,9}$"

    if re.match(vn_phone_pattern, phone):
        messagebox.showinfo("Validation Result", f"{phone} is a valid Vietnamese phone number.")
    else:
        messagebox.showerror("Validation Result", f"{phone} is not a valid Vietnamese phone number.")


# Tkinter GUI
root = Tk()
root.title("Vietnamese Phone Number Validator")
root.geometry("400x200")

# Label and Entry for phone number
Label(root, text="Enter Phone Number:").pack(pady=10)
entry_phone = Entry(root, width=30)
entry_phone.pack(pady=10)

# Button to validate phone number
Button(root, text="Validate", command=validate_phone).pack(pady=10)

# Run the application
root.mainloop()
