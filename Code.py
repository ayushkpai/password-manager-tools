from tkinter import messagebox, simpledialog, Tk

root = Tk()
root.withdraw()

the_world = {}

def read_from_file():  
        with open("passwords.txt") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                country, city = line.split("/")
                country = country.lower()
                city = city.lower()
                the_world[country] = city
