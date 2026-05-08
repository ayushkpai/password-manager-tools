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
