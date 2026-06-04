from dotenv import load_dotenv
import os
from tkinter import(
    messagebox, 
    Tk, 
    Toplevel, 
    Label, 
    Entry, 
    Button, 
    StringVar
)

load_dotenv()

root = Tk()
root.withdraw()

def ask_input(title, prompt, show=None):
    value = StringVar()
    result = {"value": None}

    win = Toplevel(root)
    win.title(title)
    win.geometry("360x150")
    win.configure(bg="white")

    Label(
        win,
        text=prompt,
        bg="white",
        fg="black"
    ).pack(pady=10)

    entry = Entry(
        win,
        textvariable=value,
        show=show,
        width=35,
        bg="white",
        fg="black",
        insertbackground="black"
    )
    entry.pack(pady=5)
    entry.focus_set()

    def ok():
        result["value"] = value.get()
        win.destroy()

    Button(win, text="OK", command=ok).pack(side="left", padx=60, pady=15)
    Button(win, text="Cancel", command=win.destroy).pack(side="right", padx=60, pady=15)

    win.grab_set()
    win.wait_window()

    return result["value"]

passwords = {}

PASSWORDS_FILE = os.getenv("PASSWORDS_FILE")
LOGIN_USERNAME_FILE = os.getenv("USERNAME_FILE")
LOGIN_PASSWORD_FILE = os.getenv("PASSWORD_FILE")

def encrypt(text):
    return f"<#[currenguajis{text}dvssfohvbkjt]#>"

def decrypt(text):
    text = text.strip()

    text = text.replace("<#[currenguajis", "")
    text = text.replace("dvssfohvbkjt]#>", "")

    return text

def get_username():
    try:
        with open(LOGIN_USERNAME_FILE, "r") as file:
            return decrypt(file.read())

    except FileNotFoundError:
        with open(LOGIN_USERNAME_FILE, "w") as file:
            file.write(encrypt("password"))

        return "password"

def get_password():
    try:
        with open(LOGIN_PASSWORD_FILE, "r") as file:
            return decrypt(file.read())

    except FileNotFoundError:
        with open(LOGIN_PASSWORD_FILE, "w") as file:
            file.write(encrypt("password"))

        return "password"

def read_from_file():
    passwords.clear()

    try:
        with open(PASSWORDS_FILE, "r") as file:
            for line in file:
                line = line.strip()

                if line == "":
                    continue

                line = decrypt(line)

                if "/" not in line:
                    continue

                app, password = line.split("/", 1)

                passwords[app] = password

    except FileNotFoundError:
        open(PASSWORDS_FILE, "w").close()

def write_to_file(app_name, password):
    with open(PASSWORDS_FILE, "a") as file:
        file.write(
            encrypt(f"{app_name}/{password}") + "\n"
        )

def run():
    ask = ask_input(
        "Password manager",
        "Type the name of an app"
    )

    if ask is None:
        root.destroy()
        return

    ask = ask.strip()

    if ask in passwords:
        messagebox.showinfo(
            "Password manager",
            f"The password of {ask} is {passwords[ask]}"
        )

    else:
        add = ask_input(
            "Password manager",
            f"What is the password of {ask}",
            show="•"
        )

        if add is None:
            root.destroy()
            return

        add = add.strip()

        passwords[ask] = add

        write_to_file(ask, add)

        messagebox.showinfo(
            "Password manager",
            "Password saved successfully"
        )

    root.after(100, run)

def ask_question():
    username = ask_input(
        "Password manager",
        "Enter username",
        show="•"
    )

    if username is None:
        root.destroy()
        return

    if username == get_username():

        password = ask_input(
            "Password manager",
            "Enter password",
            show="•"
        )

        if password is None:
            root.destroy()
            return

        if password == get_password():
            run()

        else:
            messagebox.showerror(
                "Password manager",
                "Unauthorized access"
            )
            root.destroy()

    else:
        messagebox.showerror(
            "Password manager",
            "Unauthorized access"
        )
        root.destroy()

read_from_file()
ask_question()

root.mainloop()
