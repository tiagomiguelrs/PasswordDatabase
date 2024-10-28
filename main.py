from tkinter import *
from tkinter import messagebox  # It is another module and not a tkinter class, so it needs to be imported separately
from password_generator import generate_password
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def set_password():
    password_e.delete(0, END)
    generated_password = generate_password()
    password_e.insert(index=0, string=generated_password)
    pyperclip.copy(generated_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website, username, password = get_entries()

    is_empty = empty_fields(website, username, password)
    if not is_empty:
        message = f"Details entered:\nUsername: {username}\nPassword: {password}"
        is_ok = messagebox.askokcancel(title=website, message=message)

        if is_ok:
            new_data = create_new_data(website, username, password)

            save_data_to_json(new_data)

            delete_entries()


def get_entries():
    website, username, password = website_e.get().title(), username_e.get(), password_e.get()
    return website, username, password


def empty_fields(website: str, username: str, password: str):
    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showwarning(title="Empty fields", message="Some input fields may be empty. "
                                                             "Please fill them correctly.")
        return True
    else:
        return False


def create_new_data(website: str, username: str, password: str):
    new_data = {
        website: {
            "Username": username,
            "Password": password,
        }
    }
    return new_data


def save_data_to_json(new_data):
    try:
        # Load data
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)
            data.update(new_data)

    except FileNotFoundError:
        messagebox.Message(message="New .json file was created.")
         # Save data
        with open("data.json", mode="w") as data_file:
            json.dump(new_data, fp=data_file, indent=4)

    else:
        # Save data
        with open("data.json", mode="w") as data_file:
            json.dump(data, fp=data_file, indent=4)


def delete_entries():
    website_e.delete(0, END)
    password_e.delete(0, END)


# ------------------------ FIND PASSWORD ------------------------------ #
def find_password():
    website = website_e.get().title()

    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.Message(title="No file found", message="No .json file found. Please create one.").show()

    else:
        if website in data:
            prompt = f"Username: {data[website]['Username']}\nPassword: {data[website]['Password']}"
            messagebox.Message(title=website, message=prompt).show()

        else:
            prompt = f"No user for website {website} was found."
            messagebox.Message(title=website, message=prompt).show()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Generator")
window.config(padx=50, pady=50, bg="white")

# Image
canvas = Canvas(master=window, height=200, width=200, highlightthickness=0, bg="white")
locker_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=locker_img)
canvas.grid(column=1, row=0)

# Website label
website_l = Label(master=window, text="Website:")
website_l.config(width=15, anchor="e", bg="white")
website_l.grid(column=0, row=1)

# Email/Username label
username_l = Label(master=window, text="Email/Username:")
username_l.config(width=15, anchor="e", bg="white")
username_l.grid(column=0, row=2)

# Password label
password_l = Label(master=window, text="Password:")
password_l.config(width=15, anchor="e", bg="white")
password_l.grid(column=0, row=3)

# Website entry
website_e = Entry(master=window, width=32)
website_e.focus()   # Sets the cursor to be active here
website_e.grid(column=1, row=1)

# Email/Username entry
username_e = Entry(master=window, width=50)
username_e.insert(0, "tiago@email.com")
username_e.grid(column=1, row=2, columnspan=2)

# Password entry
password_e = Entry(master=window, width=32)
password_e.grid(column=1, row=3)

# Search button
search_b = Button(master=window, text="Search", width=14, command=find_password)
search_b.grid(column=2, row=1)

# Generate button
generate_b = Button(master=window, text="Generate Password", command=set_password)
generate_b.grid(column=2, row=3)

# Add button
add_b = Button(master=window, text="Add", width=43, command=save)
add_b.grid(column=1, row=4, columnspan=2)


window.mainloop()
