import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from models import Plant
from database import get_db_connection, create_tables
from utils import save_image

class HouseplantCatalogApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Houseplant Catalog")
        create_tables()
        self.setup_gui()

    def setup_gui(self):
        self.tree = ttk.Treeview(self.root, columns=("ID", "Common Name", "Scientific Name", "Purchase Date", "Care History", "Image Path"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Common Name", text="Commmon Name")
        self.tree.heading("Scientific Name", text="Scientific Name")
        self.tree.heading("Purchase Date", text="Purchase Date")
        self.tree.heading("Care History", text="Care History")
        self.tree.heading("Image Path", text="Image Path")
        self.tree.pack(expand=True, fill=tk.BOTH)

        self.add_button = tk.Button(self.root, text="Add Plant", command=self.add_plant)
        self.edit_button = tk.Button(self.root, text="Edit Plant", command=self.edit_plant)
        self.delete_button = tk.Button(self.root, text="Delete Plant", command=self.delete_plant)

        self.add_button.pack(side=tk.LEFT)
        self.edit_button.pack(side=tk.LEFT)
        self.delete_button.pack(side=tk.LEFT)

        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn  = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM plants')
        
        for row in cursor.fetchall():
            self.tree.insert('', tk.END, values=(row['id'], row['common_name'], row['scientific_name'], row['purchase_date'], row['care_history'], row['image_path']))

        conn.close()

    def add_plant(self):
        def save_plant():
            common_name = common_name_entry.get()
            scientific_name = scientific_name_entry.get()
            purchase_date = purchase_date_entry.get()
            care_history = care_history_entry.get()
            image_path = image_path_var.get()

            if not common_name:
                messagebox.showerror("Error", "Common Name is required.")
                return
            
            if image_path:
                image_path = save_image(image_path)

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                            INSERT INTO plants (common_name, scientific_name, purchase_date, care_history, image_path)
                            VALUES (?, ?, ?, ?, ?)
                           ''', (common_name, scientific_name, purchase_date, care_history, image_path))
            conn.commit()
            conn.close()

            self.load_data()
            add_window.destroy()

        def add_another():
            save_plant()
            add_window.destroy()
            self.add_plant()
        
        def cancel():
            add_window.destroy()
            

        add_window = tk.Toplevel(self.root)
        add_window.title("Add Plant")

        tk.Label(add_window, text="Common Name").grid(row=0, column=0)
        common_name_entry = tk.Entry(add_window)
        common_name_entry.grid(row=0, column=1)

        tk.Label(add_window, text="Scientific Name").grid(row=1, column=0)
        scientific_name_entry = tk.Entry(add_window)
        scientific_name_entry.grid(row=1, column=1)

        tk.Label(add_window, text="Purchase Date").grid(row=2, column=0)
        purchase_date_entry = tk.Entry(add_window)
        purchase_date_entry.grid(row=2, column=1)

        tk.Label(add_window, text="Care History").grid(row=3, column=0)
        care_history_entry = tk.Entry(add_window)
        care_history_entry.grid(row=3, column=1)

        tk.Label(add_window, text="Image").grid(row=4, column=0)
        image_path_var = tk.StringVar()
        image_entry = tk.Entry(add_window, textvariable=image_path_var)
        image_entry.grid(row=4, column=1)
        image_button = tk.Button(add_window, text="Browse", command=lambda: image_path_var.set(filedialog.askopenfilename()))
        image_button.grid(row=4, column=2)

        save_button = tk.Button(add_window, text="Save", command=save_plant)
        save_button.grid(row=5, column=0, columnspan=2)
        save_button = tk.Button(add_window, text="Add Another", command=add_another)
        save_button.grid(row=5, column=1, columnspan=3)
        save_button = tk.Button(add_window, text="Cancel", command=cancel)
        save_button.grid(row=5, column=3, columnspan=2)

    def edit_plant(self):
        selected_items = self.tree.selection()

        if not selected_items:
            messagebox.showwarning("Warning", "No plant was selected.")
            return
        elif len(selected_items) > 1:
            messagebox.showwarning("Warning", "More than one selection detected. Select only 1 plant.")

        plant_id = self.tree.item(selected_items, "values")[0]

        def save_plant():
            common_name = common_name_entry.get()
            scientific_name = scientific_name_entry.get()
            purchase_date = purchase_date_entry.get()
            care_history = care_history_entry.get()
            image_path = image_path_var.get()

            if not common_name:
                messagebox.showerror("Error", "Common Name is required.")
                return
            
            if image_path:
                image_path = save_image(image_path)

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                            UPDATE plants
                            SET common_name = ?, scientific_name = ?, purchase_date = ?, care_history = ?, image_path = ?
                            WHERE id = ?
                           ''', (common_name, scientific_name, purchase_date, care_history, image_path, plant_id))
            conn.commit()
            conn.close()

            self.load_data()
            edit_window.destroy()

        def cancel():
            edit_window.destroy()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM plants WHERE id = ?', (plant_id))
        plant = cursor.fetchone()
        conn.close()

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Plant")

        tk.Label(edit_window, text="Common Name").grid(row=0, column=0)
        common_name_entry = tk.Entry(edit_window)
        common_name_entry.insert(0, plant['common_name'])
        common_name_entry.grid(row=0, column=1)

        tk.Label(edit_window, text="Scientific Name").grid(row=1, column=0)
        scientific_name_entry = tk.Entry(edit_window)
        scientific_name_entry.insert(0, plant['scientific_name'])
        scientific_name_entry.grid(row=1, column=1)

        tk.Label(edit_window, text="Purchase Date").grid(row=2, column=0)
        purchase_date_entry = tk.Entry(edit_window)
        purchase_date_entry.insert(0, plant['purchase_date'])
        purchase_date_entry.grid(row=2, column=1)

        tk.Label(edit_window, text="Care History").grid(row=3, column=0)
        care_history_entry = tk.Entry(edit_window)
        care_history_entry.insert(0, plant['care_history'])
        care_history_entry.grid(row=3, column=1)

        tk.Label(edit_window, text="Image").grid(row=4, column=0)
        image_path_var = tk.StringVar()
        image_entry = tk.Entry(edit_window, textvariable=image_path_var)
        image_entry.insert(0, plant['image_path'])
        image_entry.grid(row=4, column=1)
        image_button = tk.Button(edit_window, text="Browse", command=lambda: image_path_var.set(filedialog.askopenfilename()))
        image_button.grid(row=4, column=2)

        save_button = tk.Button(edit_window, text="Save", command=save_plant)
        save_button.grid(row=5, column=0, columnspan=2)
        save_button = tk.Button(edit_window, text="Cancel", command=cancel)
        save_button.grid(row=5, column=1, columnspan=2)
            

        

    def delete_plant(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "No plants were selected.")
            return
        
        conn = get_db_connection()
        cursor = conn.cursor()

        for item in selected_items:
            plant_id = self.tree.item(item, "values")[0]
            cursor.execute('DELETE FROM plants WHERE id = ?', (plant_id))
            conn.commit()

        self.reorganize_ids(cursor)

        conn.close()
        self.load_data()

    def reorganize_ids(self, cursor):
        cursor.execute('SELECT * FROM plants')
        plants = cursor.fetchall()
        cursor.execute('DELETE FROM plants')
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="plants"')

        for i, plant in enumerate(plants):
            cursor.execute('''
                            INSERT INTO plants (id, common_name, scientific_name, purchase_date, care_history, image_path)
                           VALUES (?, ?, ?, ?, ?, ?)
                           ''', (i+ 1, plant['common_name'], plant['scientific_name'], plant['purchase_date'], plant['care_history'], plant['image_path']))
        cursor.connection.commit()

    def run(self):
        self.root.mainloop()