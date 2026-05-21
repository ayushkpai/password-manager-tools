from tkinter import messagebox, simpledialog, Tk

root = Tk()
root.withdraw()

passwords = {}

def read_from_file():
    decrypt_app_texts = ["<#currenguajis", "dvssfohvbkjt"]
    decrypt_password_texts = ["dsufgasudfba", "etvghbtvegcb#>"]

    try:
        with open("/Users/ayushpai/essentials/.passwords.txt", "r") as file:
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
        open("/Users/ayushpai/essentials/.passwords.txt", "w").close()

def write_to_file(app_name, password):
    with open("/Users/ayushpai/essentials/.passwords.txt", "a") as file:
        file.write(
            "<#currenguajis"
            + app_name
            + "dvssfohvbkjt"
            + "/"
            + "dsufgasudfba"
            + password
            + "etvghbtvegcb#>"
            + "\n"
        )

def ask_question():
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
            f"What is the password of {ask}"
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
    root.after(1000, ask_question)

read_from_file()
ask_question()

root.mainloop()
