from tkinter import *
from tkinter import messagebox
from random import choice,shuffle,randint
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters=[choice(letters) for _ in  range(randint(8, 10))]

    password_symbols=[choice(symbols) for _ in range(randint(2, 4))]

    password_numbers=[choice(numbers) for _ in range(randint(2, 4))]

    password_list=password_numbers+password_symbols+password_letters

    shuffle(password_list)

    password = "".join(password_list)

    password_input_text.insert(1.0,f"{password}")
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = web_input_text.get("1.0", "end").strip()
    email = email_username_input_text.get("1.0", "end").strip()
    password = password_input_text.get("1.0", "end").strip()
    new_data={website:{
          "email":email,
          "password":password,
       }
    }

    # Ensure no field is empty


    if website and email and password:
        new_data = {
            website: {
                "email": email,
                "password": password
            }
        }

        try:
            with open("data.json", "r") as data_file:
                # Reading the old data
                data = json.load(data_file)
        except FileNotFoundError:
            # If the file doesn't exist, create it and write new_data
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        except json.JSONDecodeError:
            # Handle corrupted or empty file
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating the old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving the updated data
                json.dump(data, data_file, indent=4)
        finally:
            # Clear the text boxes after saving
            web_input_text.delete("1.0", "end")
            password_input_text.delete("1.0", "end")
    else:
        messagebox.showinfo(title="Oops", message="Please make sure no field is empty.")

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = web_input_text.get("1.0", END).strip()
    if not website:  # Check if the input is empty
        messagebox.showinfo(title="Error", message="Please enter a website name.")
        return

    try:
        with open("data.json", "r") as data_file:  # Open in read mode explicitly
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    except json.JSONDecodeError:
        messagebox.showinfo(title="Error", message="Data file is empty or corrupted.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(
                title=website, message=f"Email: {email}\nPassword: {password}"
            )
        else:
            messagebox.showinfo(
                title="Error", message=f"No details for {website} exist."
            )


# ---------------------------- UI SETUP ------------------------------- #
window=Tk()
window.title("Password Manager")
window.config(padx=50,pady=50)

canvas = Canvas(height=200,width=200)
logo_img=PhotoImage(file="logo.png")
canvas.create_image(100,100,image=logo_img)
canvas.grid(column=1,row=0)


#webiste label
website_label=Label(text="Website:")
website_label.grid(column=0,row=1)

#input text for website
web_input_text=Text(width=30,height=1)
web_input_text.grid(column=1,row=1)
web_input_text.focus()

#email and username label
email_username_label=Label(text="Email/Username:")
email_username_label.grid(column=0,row=2)

#input text for email and username
email_username_input_text=Text(width=30,height=1)
email_username_input_text.grid(column=1,row=2)
email_username_input_text.insert(1.0,"nk7649847@gmail.com")

#password label
password_label=Label(text="Password:")
password_label.grid(column=0,row=3)

#input text for password
password_input_text=Text(width=30,height=1)
password_input_text.grid(column=1,row=3)


#button for generate password
generate_password_input=Button(text="Generate Password",command=generate_password)
generate_password_input.grid(column=2,row=3)


#add button
add_button=Button(text="Add",width=30,command=save)
add_button.grid(row=4,column=1)

#Search button
search_button=Button(text="Search",width=14,command=find_password)
search_button.grid(row=1,column=2)


window.mainloop()