from tkinter import messagebox, simpledialog, Tk

root = Tk()
root.withdraw()

passwords = {}

PASSWORDS_FILE = "/Users/ayushpai/essentials/.password_manager/passwords.txt"
LOGIN_PASSWORD_FILE = "/Users/ayushpai/essentials/.password_manager/login/password.txt"
LOGIN_USERNAME_FILE = "/Users/ayushpai/essentials/.password_manager/login/username.txt"


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
    ask = simpledialog.askstring(
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
        add = simpledialog.askstring(
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
    username = simpledialog.askstring(
        "Password manager",
        "Enter username",
        show="•"
    )

    if username is None:
        root.destroy()
        return

    if username == get_username():

        password = simpledialog.askstring(
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
