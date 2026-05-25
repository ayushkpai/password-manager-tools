from tkinter import messagebox, simpledialog, Tk

root = Tk()
root.withdraw()

passwords = {}

PASSWORDS_FILE = "/Users/ayushpai/essentials/.password_manager/passwords.txt"
LOGIN_PASSWORD_FILE = "/Users/ayushpai/essentials/.password_manager/login_password.txt"

def get_login_password():
    try:
        with open(LOGIN_PASSWORD_FILE, "r") as file:
            return file.read().strip()

    except FileNotFoundError:
        with open(LOGIN_PASSWORD_FILE, "w") as file:
            file.write("password")

        return "password"

def read_from_file():
    decrypt_app_texts = ["<#[currenguajis", "dvssfohvbkjt"]
    decrypt_password_texts = ["dsufgasudfba", "etvghbtvegcb]#>"]

    try:
        with open(PASSWORDS_FILE, "r") as file:
            passwords.clear()

            for line in file:
                line = line.strip()

                if not line:
                    continue

                app, password = line.split("/")

                for substring in decrypt_app_texts:
                    app = app.replace(substring, "")

                for substring in decrypt_password_texts:
                    password = password.replace(substring, "")

                passwords[app] = password

    except FileNotFoundError:
        open(PASSWORDS_FILE, "w").close()

def write_to_file(app_name, password):
    with open(PASSWORDS_FILE, "a") as file:
        file.write(
            "<#[currenguajis"
            + app_name
            + "dvssfohvbkjt"
            + "/"
            + "dsufgasudfba"
            + password
            + "etvghbtvegcb]#>"
            + "\n"
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
        result = passwords[ask]

        messagebox.showinfo(
            "Password manager",
            f"The password of {ask} is {result}"
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

    read_from_file()
    root.after(1000, run)

def ask_question():
    login = simpledialog.askstring(
        "Password manager",
        "Enter password",
        show="•"
    )

    saved_password = get_login_password()

    if login == saved_password:
        run()

    elif login is None:
        root.destroy()

    else:
        messagebox.showinfo(
            "Password manager",
            "Unauthorized access"
        )
        root.destroy()

read_from_file()
ask_question()

root.mainloop()
