import json
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# generate password


def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# save password
def save():
    website = website_entry.get()
    email = email_username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    new_data_txt = f"site: {website}, email: {email}, password: {password}\n"

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Missing information...", message="Please don't leave any fields empty!")
    else:
        with open("data.txt", "a") as data_file:
            data_file.write(new_data_txt)
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)

        except FileNotFoundError:

            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)


        else:  # This is the code which needs to run if there are no issues with "try:"
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# password finder


def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:  # else statements when used with try and except contain the code which will be executed if try is successful
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\n"
                                                       f"Password: {password})\n\n"
                                                       f"Password has been copied to clipboard")
            pyperclip.copy(password)
        else:
            messagebox.showinfo(title="Website not found", message=f"No details for {website} exists.")


# Tkinter

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
padlock_logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=padlock_logo)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_username_label = Label(text="Email/Username:")
email_username_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=32)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_username_entry = Entry(width=51)
email_username_entry.grid(row=2, column=1, columnspan=2)
email_username_entry.insert(0, "example.mail.com")

password_entry = Entry(width=32)
password_entry.grid(row=3, column=1)

# Buttons
generate_pass_button = Button(text="Generate Password", width=14, command=generate_password)
generate_pass_button.grid(row=3, column=2)

add_button = Button(text="Add", width=43, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2)


window.mainloop()