from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    password_str = password_numbers + password_letters + password_symbols
    random.shuffle(password_str)
    password_generated = "".join(password_str)
    pyperclip.copy(password_generated)
    entry3.delete(0, END)
    entry3.insert(0, password_generated)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = entry1.get().lower()
    email_username = entry2.get()
    password = entry3.get()
    data_saved = {
        website: {
            "email": email_username,
            "password": password
        }
    }

    if website == "" or email_username == "" or password == "":
        messagebox.showwarning(message="Don't Leave Any Fields Blank!")
    else:
        is_ok = messagebox.askokcancel(message=f"These are the details to be saved: \n Email: {email_username} \n" 
                                                  f"Password: {password} \n Is it OK to save?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(data_saved, data_file, indent=4)
            else:
                data.update(data_saved)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                entry1.delete(0, END)
                entry3.delete(0, END)

# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search():
    search_website = entry1.get().lower()
    if search_website == "":
        messagebox.showwarning(message="Website Needed!")
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(message="No Data File Found")
    else:
        if search_website in data:
            search_email = data[search_website]["email"]
            search_password = data[search_website]["password"]
            entry2.delete(0, END)
            entry2.insert(0, search_email)
            entry3.delete(0, END)
            entry3.insert(0, search_password)
            pyperclip.copy(search_password)
        else:
            messagebox.showerror(message="No Related Data Found")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=50)
canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(120, 100, image=logo_image)
canvas.grid(column=1, row=0)

label1 = Label(text="Website:")
label1.grid(column=0, row=1, sticky=E)
label2 = Label(text="Email/Username:")
label2.grid(column=0, row=2, sticky=E)
label3 = Label(text="Password:")
label3.grid(column=0, row=3, sticky=E)

entry1 = Entry(width=19)
entry1.focus()
entry1.grid(column=1, row=1)
entry2 = Entry(width=34)
entry2.grid(column=1, row=2, columnspan=2)
entry2.insert(0, "glz2284585073@gmail.com")
entry3 = Entry(width=19)
entry3.grid(column=1, row=3)

button1 = Button(text="Generate Password", width=11, command=generate_password)
button1.grid(column=2, row=3, sticky=W)
button2 = Button(text="Add", width=33, command=save_password)
button2.grid(column=1, row=4, columnspan=2, sticky=E)
button3 = Button(text="Search", width=10, command=search)
button3.grid(column=2, row=1, sticky=W)

window.mainloop()
