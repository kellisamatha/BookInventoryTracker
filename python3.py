import tkinter as tk
from tkinter import messagebox,ttk
from datetime import datetime
import csv
import os
import hashlib

header_font = ("helvetica", 14, "bold")
label_font = ("Geist", 12)
button_font = ("Montserrat", 10, "bold")

# User class to handle login and registration data
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

class BookInventory:
    def __init__(self, book_id, title, author, quantity, borrowed=0):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.quantity = quantity
        self.borrowed = borrowed

class LoginRegister:
    def __init__(self, root):
        self.root = root
        self.root.title("Login or Register")
        self.root.geometry("500x500")
        self.root.config(bg="#f5f5f5")

        # Create a Notebook for tabs
        notebook = ttk.Notebook(root)
        notebook.pack(pady=20, expand=True)

        # Style
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=header_font, padding=[20, 5])

        # Login tab
        login_tab = tk.Frame(notebook, bg="#B9E5E8")
        notebook.add(login_tab, text="Login")

        # Register tab
        register_tab = tk.Frame(notebook, bg="#DFF2EB")
        notebook.add(register_tab, text="Register")

        # Login tab widgets
        tk.Label(login_tab, text="Login", font=header_font, bg="#B9E5E8").pack(pady=15)
        tk.Label(login_tab, text="Username", font=label_font, bg="#7AB2D3").pack(pady=5)
        self.username_entry_login = tk.Entry(login_tab, font=label_font)
        self.username_entry_login.pack(pady=5)

        tk.Label(login_tab, text="Password", font=label_font, bg="#7AB2D3").pack(pady=5)
        self.password_entry_login = tk.Entry(login_tab, font=label_font, show="*")
        self.password_entry_login.pack(pady=5)

        tk.Button(login_tab, text="Login", command=self.login, font=button_font, bg="#007ACC", fg="white").pack(pady=20)

        # Register tab widgets
        tk.Label(register_tab, text="Register", font=header_font, bg="#DFF2EB").pack(pady=15)
        tk.Label(register_tab, text="Username", font=label_font, bg="#87CEFA").pack(pady=5)
        self.username_entry_register = tk.Entry(register_tab, font=label_font)
        self.username_entry_register.pack(pady=5)

        tk.Label(register_tab, text="Password", font=label_font, bg="#87CEFA").pack(pady=5)
        self.password_entry_register = tk.Entry(register_tab, font=label_font, show="*")
        self.password_entry_register.pack(pady=5)

        tk.Button(register_tab, text="Register", command=self.register, font=button_font, bg="#28A745", fg="white").pack(pady=20)


    def login(self):
        username = self.username_entry_login.get()
        password = User.hash_password(self.password_entry_login.get())
        users_path = "D:\\class\\3-1\\App\\python_3\\users.csv"

        if os.path.exists(users_path):
            with open(users_path, mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0] == username and row[1] == password:
                        self.root.destroy()
                        root = tk.Tk()
                        app = BookInventoryTracker(root)
                        root.mainloop()
                        return
        messagebox.showinfo("Error", "Invalid credentials. Please try again.")

    def register(self):
        username = self.username_entry_register.get()
        password = self.password_entry_register.get()
        users_path ="D:\\class\\3-1\\App\\python_3\\users.csv"

        # Check if the file exists, if not, create it with the header
        if not os.path.exists(users_path):
            with open(users_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Username", "Password"])

        if not username or not password:
            messagebox.showinfo("Error", "Please fill all fields.")
            return

        if os.path.exists(users_path):
            with open(users_path, mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0] == username:
                        messagebox.showinfo("Error", "Username already exists.")
                        return

        with open(users_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([username, User.hash_password(password)])
            messagebox.showinfo("Success", "Registration successful! Please log in.")

class BookInventoryTracker:
    def __init__(self, root):
        directory = "D:/dmw/App/python_3"
        os.makedirs(directory, exist_ok=True)
        self.books = {}
        self.logs = []
        self.load_data()

        self.root = root
        self.root.title("Book Inventory Tracker")
        self.root.geometry("900x600")
        self.root.config(bg="#B9E5E8")

    # Add Book Section
        tk.Label(root, text="Add Book to Inventory", font=header_font, bg="#f7f7f7").grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(root, text="Book ID", font=label_font, bg="#7AB2D3").grid(row=1, column=0, sticky="e")
        tk.Label(root, text="Title", font=label_font, bg="#7AB2D3").grid(row=2, column=0, sticky="e")
        tk.Label(root, text="Author", font=label_font, bg="#7AB2D3").grid(row=3, column=0, sticky="e")
        tk.Label(root, text="Quantity", font=label_font, bg="#7AB2D3").grid(row=4, column=0, sticky="e")

        self.book_id_entry = tk.Entry(root, font=label_font)
        self.title_entry = tk.Entry(root, font=label_font)
        self.author_entry = tk.Entry(root, font=label_font)
        self.quantity_entry = tk.Entry(root, font=label_font)

        self.book_id_entry.grid(row=1, column=1, padx=10, pady=5)
        self.title_entry.grid(row=2, column=1, padx=10, pady=5)
        self.author_entry.grid(row=3, column=1, padx=10, pady=5)
        self.quantity_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Button(root, text="Add Book", command=self.add_book, font=button_font, bg="#007ACC", fg="white").grid(row=5, column=1, pady=10)

        # Borrow/Return Section
        tk.Label(root, text="Borrow/Return Book", font=header_font, bg="#f7f7f7").grid(row=0, column=2, columnspan=2, pady=10)
        tk.Label(root, text="Book ID", font=label_font, bg="#7AB2D3").grid(row=1, column=2, sticky="e")
        tk.Label(root, text="User ID", font=label_font, bg="#7AB2D3").grid(row=2, column=2, sticky="e")

        self.borrow_book_id_entry = tk.Entry(root, font=label_font)
        self.user_id_entry = tk.Entry(root, font=label_font)

        self.borrow_book_id_entry.grid(row=1, column=3, padx=10, pady=5)
        self.user_id_entry.grid(row=2, column=3, padx=10, pady=5)

        tk.Button(root, text="Borrow Book", command=self.borrow_book, font=button_font, bg="#4A628A", fg="white").grid(row=3, column=3, pady=10)
        tk.Button(root, text="Return Book", command=self.return_book, font=button_font, bg="#4A628A", fg="white").grid(row=3, column=2, pady=10)

        # Inventory and Logs
        tk.Button(root, text="Show Inventory", command=self.show_inventory, font=button_font, bg="#28A745", fg="white").grid(row=5, column=2, pady=10)
        tk.Button(root, text="Show Logs", command=self.show_logs, font=button_font, bg="#17A2B8", fg="white").grid(row=5, column=3, pady=10)

        # Exit and Save Button
        tk.Button(root, text="Save and Exit", command=self.save_and_exit, font=button_font, bg="#DC3545", fg="white").grid(row=5, column=4, pady=10)

        # Text Area for Displaying Inventory and Logs
        self.inventory_text = tk.Text(root, height=15, width=90, font=label_font, bg="#DFF2EB")
        self.inventory_text.grid(row=6, column=0, columnspan=5, padx=10, pady=10)


    def add_book(self):
        book_id=self.book_id_entry.get()
        title=self.title_entry.get()
        author=self.author_entry.get()
        quantity=self.quantity_entry.get()
        if book_id and title and author and quantity.isdigit():
            quantity=int(quantity)
            if book_id in self.books:
                existing_book = self.books[book_id]
                existing_book.quantity += quantity
                messagebox.showinfo("Success", f"Updated quantity of '{existing_book.title}' by {quantity}.")
            else:
                self.books[book_id] = BookInventory(book_id,title, author, quantity)
                messagebox.showinfo("Success", "Book added to inventory.")
            self.clear_entries()
        else:
            messagebox.showinfo("Error", "Please fill all fields with valid data.")

    def borrow_book(self):
        book_id=self.borrow_book_id_entry.get()
        #title=self.borrow_title_entry.get()
        user_id = self.user_id_entry.get()

        if not user_id:
            messagebox.showinfo("Error", "Please enter a User ID.")
            return

        if book_id in self.books:
            book=self.books[book_id]
            if book.borrowed < book.quantity:
                book.borrowed+= 1
                self.logs.append(f"Borrowed : {book.title} by User ID {user_id} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                messagebox.showinfo("Success", f"{book.title} has been borrowed by User ID {user_id}.")
            else:
                messagebox.showinfo("Error", f"No copies of {book.title} are available.")
        else:
            messagebox.showinfo("Error", "Book not found in inventory.")
        self.borrow_book_id_entry.delete(0, tk.END)

    def return_book(self):
        book_id=self.borrow_book_id_entry.get()
        user_id = self.user_id_entry.get()

        #title = self.borrow_title_entry.get()
        if not user_id:
            messagebox.showinfo("Error", "Please enter a User ID.")
            return

        if book_id in self.books:
            book = self.books[book_id]
            if book.borrowed > 0:
                book.borrowed -= 1
                self.logs.append(f"Returned  : {book.title} by User ID {user_id} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                messagebox.showinfo("Success", f"{book.title} has been returned by User ID {user_id}.")
            else:
                messagebox.showinfo("Error", f"No copies of {book.title} are currently borrowed.")
        else:
            messagebox.showinfo("Error", "Book not found in inventory.")
        self.borrow_book_id_entry.delete(0, tk.END)
        self.user_id_entry.delete(0, tk.END)

    def show_inventory(self):
        self.inventory_text.delete(1.0, tk.END)
        inventory_info = "Book ID\tTitle\t\tAuthor\t\t\tAvailable\t\tBorrowed\n"
        #inventory_info += "-" * 50 + "\n"
        for book in self.books.values():
            inventory_info += f"{book.book_id}\t{book.title}\t\t{book.author}\t\t\t{book.quantity - book.borrowed}\t\t{book.borrowed}\n"
        self.inventory_text.insert(tk.END, inventory_info)

    def show_logs(self):
        self.inventory_text.delete(1.0,tk.END)
        log_info="Borrow/Returns Logs:\n"
        log_info+="\n".join(self.logs)
        self.inventory_text.insert(tk.END, log_info)        
    
    def save_and_exit(self):
        self.save_data()
        self.root.destroy()
    def save_data(self):
        directory = "D:/dmw/App/python_3"
        os.makedirs(directory, exist_ok=True)
        inventory_path = os.path.join(directory, "BookInventory.csv")
        logs_path = os.path.join(directory, "BorrowReturnLogs.csv")
        with open(inventory_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Book ID", "Title", "Author", "Quantity", "Borrowed"])
            for book in self.books.values():
                writer.writerow([book.book_id, book.title, book.author, book.quantity, book.borrowed])

        with open(logs_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Log"])
            for log in self.logs:
                writer.writerow([log])

    def load_data(self):
        directory = "D:/dmw/App/python_3"
        os.makedirs(directory, exist_ok=True)
        inventory_path = os.path.join(directory, "BookInventory.csv")
        logs_path = os.path.join(directory, "BorrowReturnLogs.csv")
        if os.path.exists(inventory_path):
            with open(inventory_path, mode="r") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    book_id, title, author, quantity, borrowed = row
                    self.books[book_id] = BookInventory(book_id, title, author, int(quantity), int(borrowed))

        if os.path.exists(logs_path):
            with open(logs_path, mode="r") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    self.logs.append(row[0])

    def clear_entries(self):
        self.book_id_entry.delete(0,tk.END)
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)


root = tk.Tk()
login_register = LoginRegister(root)
root.mainloop()