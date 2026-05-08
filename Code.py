from tkinter import messagebox, simpledialog, Tk

root = Tk()
root.withdraw()

passwords = {}

def read_from_file():  
    with open("passwords.txt") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            app, password = line.split("/")
            passwords[app] = password

def write_to_file(ask_name, add_name):
    with open("passwords.txt", "a")as file:
        file.write(ask_name + "/" + add_name + "\n")

add = ""

def ask_question():
    ask = simpledialog.askstring(
        "Password manager",
        "Type the name of a app"
    )

    if ask is None:
        root.quit()
        return

    ask = ask.strip()

    if ask in passwords:
        result = passwords[ask]
        messagebox.showinfo(
            "Password manager",
            f"The password of {ask} is {result}"
        )
        add = result
    else:
        add = simpledialog.askstring(
            "Password manager",
            f"What is the password of {ask}"
        )

        passwords[ask] = add
        write_to_file(ask, add)

    if add is None:
        root.quit()
        return

    add = add.strip()

    root.after(1000, ask_question)
    read_from_file()
    
ask_question()

root.mainloop()
