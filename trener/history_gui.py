import customtkinter as ctk
from tkinter import ttk
from datetime import datetime
import db_manager

UNCHECKED = "☐"
CHECKED = "☑"

class HistoryWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("TRAINING HISTORY")
        self.geometry("700x500")
        self.configure(fg_color="#121212")
        
        self.edit_mode = False
        
        # --- Панель керування ---
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(fill="x", padx=20, pady=10)
        
        self.btn_edit = ctk.CTkButton(self.btn_frame, text="CHANGE MODE", command=self.toggle_edit_mode)
        self.btn_edit.pack(side="left", padx=5)
        
        self.btn_delete = ctk.CTkButton(self.btn_frame, text="CONFIRM DELETE", 
                                        fg_color="#B20000", hover_color="#FF0000", 
                                        state="disabled", command=self.delete_selected)
        self.btn_delete.pack(side="left", padx=5)

        # --- Дерево записів ---
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#1e1e1e", foreground="white", 
                        fieldbackground="#1e1e1e", borderwidth=0, font=("Arial", 12))
        style.map('Treeview', background=[('selected', '#333333')])

        self.tree = ttk.Treeview(self, columns=("db_id",), displaycolumns="")
        self.tree.pack(expand=True, fill="both", padx=20, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)
        
        self.load_data()

    def format_duration(self, total_seconds):
        minutes, seconds = divmod(total_seconds, 60)
        return f"{minutes:02d}:{seconds:02d} хв"

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        records = db_manager.get_all_sessions()
        
        for rec in records:
            db_id, date_time_str, duration, reps, target, errors = rec
            
            # Парсинг дати з БД (формат SQLite: 'YYYY-MM-DD HH:MM:SS')
            dt_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
            year = dt_obj.strftime("%Y")
            month = dt_obj.strftime("%B")  # Назва місяця англійською (January, February...)
            date_str = dt_obj.strftime("%d.%m %H:%M")
            
            time_str = self.format_duration(duration)
            
            # Створення вузлів дерева
            if not self.tree.exists(year):
                self.tree.insert("", "end", year, text=year)
            month_id = f"{year}_{month}"
            if not self.tree.exists(month_id):
                self.tree.insert(year, "end", month_id, text=month)
                
            prefix = f"{UNCHECKED} " if self.edit_mode else ""
            display_text = f"{prefix}{date_str} | {reps}/{target} reps | {time_str} | Błędy: {errors}"
            
            self.tree.insert(month_id, "end", text=display_text, values=(db_id,))

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        if self.edit_mode:
            self.btn_edit.configure(text="CANCEL", fg_color="#555555")
            self.btn_delete.configure(state="normal")
        else:
            self.btn_edit.configure(text="CHANGE MODE", fg_color=['#3a7ebf', '#1f538d'])
            self.btn_delete.configure(state="disabled")
        self.load_data() 

    def on_tree_click(self, event):
        if not self.edit_mode:
            return
        item = self.tree.focus()
        if not item or not self.tree.item(item, "values"): 
            return
            
        text = self.tree.item(item, "text")
        if text.startswith(UNCHECKED):
            self.tree.item(item, text=text.replace(UNCHECKED, CHECKED, 1))
        elif text.startswith(CHECKED):
            self.tree.item(item, text=text.replace(CHECKED, UNCHECKED, 1))

    def delete_selected(self):
        ids_to_delete = []
        for year in self.tree.get_children():
            for month in self.tree.get_children(year):
                for record in self.tree.get_children(month):
                    if self.tree.item(record, "text").startswith(CHECKED):
                        ids_to_delete.append(self.tree.item(record, "values")[0])
        
        if ids_to_delete:
            db_manager.delete_records(ids_to_delete)
        self.toggle_edit_mode()