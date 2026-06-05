import os
import json
import base64
import tkinter as tk
from tkinter import messagebox, simpledialog

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

VAULT_FILE = "vault.json"
ITERATIONS = 600_000
KEY_LEN = 32

APP_TITLE = "Password Manager"

def derive_key(password, salt):
    return PBKDF2(password, salt, dkLen=KEY_LEN, count=ITERATIONS)

def encrypt(text, key):
    iv = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher.encrypt_and_digest(text.encode())

    return {
        "iv": base64.b64encode(iv).decode(),
        "tag": base64.b64encode(tag).decode(),
        "data": base64.b64encode(ciphertext).decode()
    }

def decrypt(enc, key):
    try:
        cipher = AES.new(
            key,
            AES.MODE_GCM,
            nonce=base64.b64decode(enc["iv"])
        )

        return cipher.decrypt_and_verify(
            base64.b64decode(enc["data"]),
            base64.b64decode(enc["tag"])
        ).decode()

    except:
        return None

def load_vault():
    if not os.path.exists(VAULT_FILE):
        return None

    try:
        with open(VAULT_FILE, "r") as f:
            return json.load(f)
    except:
        return None

def save_vault(vault):
    with open(VAULT_FILE, "w") as f:
        json.dump(vault, f, indent=2)
    os.chmod(VAULT_FILE, 0o600)

class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("420x500")

        self.vault = None
        self.key = None

        self.login_screen()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_screen(self):
        self.clear()

        tk.Label(self.root, text="Master Password").pack(pady=10)

        self.pass_entry = tk.Entry(self.root, show="•")
        self.pass_entry.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=5)

        if not load_vault():
            tk.Button(self.root, text="Create Account", command=self.create_vault).pack(pady=5)

    def create_vault(self):
        p1 = simpledialog.askstring(APP_TITLE, "Master password:", show="•")
        if not p1:
            return

        p2 = simpledialog.askstring(APP_TITLE, "Confirm password:", show="•")
        if not p2:
            return

        if p1 != p2:
            messagebox.showerror(APP_TITLE, "Passwords do not match")
            return

        salt = get_random_bytes(16)
        key = derive_key(p1, salt)

        vault = {
            "salt": base64.b64encode(salt).decode(),
            "verify": encrypt("ok", key),
            "passwords": {}
        }

        save_vault(vault)
        messagebox.showinfo(APP_TITLE, "Account created")

    def login(self):
        vault = load_vault()

        if not vault:
            messagebox.showerror(APP_TITLE, "No account found")
            return

        password = self.pass_entry.get()
        if not password:
            return

        salt = base64.b64decode(vault["salt"])
        key = derive_key(password, salt)

        if decrypt(vault["verify"], key) != "ok":
            messagebox.showerror(APP_TITLE, "Wrong password")
            return

        self.vault = vault
        self.key = key
        self.main_screen()

    def main_screen(self):
        self.clear()

        tk.Label(self.root, text="Password Vault").pack(pady=5)

        self.listbox = tk.Listbox(self.root, width=50, height=15)
        self.listbox.pack()

        self.refresh()

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Button(frame, text="Add", command=self.add).grid(row=0, column=0)
        tk.Button(frame, text="View", command=self.view).grid(row=0, column=1)
        tk.Button(frame, text="Delete", command=self.delete).grid(row=0, column=2)

        tk.Button(frame, text="Change Password", command=self.change_master).grid(row=1, column=0)
        tk.Button(frame, text="Delete Account", command=self.delete_vault).grid(row=1, column=1)
        tk.Button(frame, text="Logout", command=self.login_screen).grid(row=1, column=2)

    def refresh(self):
        self.listbox.delete(0, tk.END)
        for k in self.vault["passwords"]:
            self.listbox.insert(tk.END, k)

    def add(self):
        name = simpledialog.askstring(APP_TITLE, "Service name:")
        if not name:
            return

        pwd = simpledialog.askstring(APP_TITLE, "Password:", show="•")
        if not pwd:
            return

        self.vault["passwords"][name] = encrypt(pwd, self.key)
        save_vault(self.vault)
        self.refresh()

    def view(self):
        item = self.listbox.get(tk.ACTIVE)
        if not item:
            return

        enc = self.vault["passwords"].get(item)
        pwd = decrypt(enc, self.key)

        messagebox.showinfo(APP_TITLE, pwd or "Cannot decrypt")

    def delete(self):
        item = self.listbox.get(tk.ACTIVE)
        if not item:
            return

        self.vault["passwords"].pop(item, None)
        save_vault(self.vault)
        self.refresh()

    def change_master(self):
        n1 = simpledialog.askstring(APP_TITLE, "New master password:", show="•")
        if not n1:
            return

        n2 = simpledialog.askstring(APP_TITLE, "Confirm password:", show="•")
        if not n2:
            return

        if n1 != n2:
            messagebox.showerror(APP_TITLE, "Mismatch")
            return

        new_salt = get_random_bytes(16)
        new_key = derive_key(n1, new_salt)

        new_data = {}

        for k, v in self.vault["passwords"].items():
            plain = decrypt(v, self.key)
            new_data[k] = encrypt(plain, new_key)

        self.vault["salt"] = base64.b64encode(new_salt).decode()
        self.vault["verify"] = encrypt("ok", new_key)
        self.vault["passwords"] = new_data

        save_vault(self.vault)
        messagebox.showinfo(APP_TITLE, "Master password changed")

    def delete_vault(self):
        confirm = simpledialog.askstring(APP_TITLE, "Type DELETE to confirm")

        if confirm == "DELETE":
            if os.path.exists(VAULT_FILE):
                os.remove(VAULT_FILE)

            messagebox.showinfo(APP_TITLE, "Account removed")
            self.login_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()
