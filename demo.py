import tkinter as tk
from tkinter import messagebox

def validate_login():
    username = username_entry.get()
    password = password_entry.get()
    
    # Validate the username and password (Add your validation logic here)
    if username == "admin" and password == "password":
        messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Create main window
root = tk.Tk()
root.title("Login Form")

# Function to handle focus events and change border color to blue
def on_entry_focus(event):
    event.widget.config(highlightcolor="blue")

def on_entry_blur(event):
    event.widget.config(highlightcolor="gray")

# Username Label and Entry
username_label = tk.Label(root, text="Username:")
username_label.pack()
username_entry = tk.Entry(root, highlightthickness=2)
username_entry.pack()
username_entry.bind("<FocusIn>", on_entry_focus)
username_entry.bind("<FocusOut>", on_entry_blur)

# Password Label and Entry
password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*", highlightthickness=2)
password_entry.pack()
password_entry.bind("<FocusIn>", on_entry_focus)
password_entry.bind("<FocusOut>", on_entry_blur)

# Login Button
login_button = tk.Button(root, text="Login", command=validate_login)
login_button.pack()

# Run the main loop
root.mainloop()
