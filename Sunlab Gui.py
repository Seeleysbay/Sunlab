import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import bcrypt

class AdminLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Login - SUN Lab Access System")

        self.show_login_frame()

    def show_login_frame(self):
        style = ttk.Style()
        style.theme_use('clam')

        def on_hover(event):
            event.widget["background"] = "lightblue"

        def on_leave(event):
            event.widget["background"] = btn_color

        bg_color = "#f5f5f5"
        btn_color = "#e0e0e0"
        font_color = "#333333"
        header_color = "#4f83c4"

        self.root.configure(bg=bg_color)

        style.configure("TFrame", background=bg_color)

        style.configure("TButton",
                        background=btn_color,
                        foreground=font_color,
                        borderwidth=1)
        style.map("TButton",
                  background=[('active', 'lightblue'), ('pressed', 'blue')],
                  foreground=[('pressed', 'white')])

        style.configure("TLabel",
                        background=bg_color,
                        foreground=font_color,
                        font=('Arial', 16))

        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(pady=100)

        self.header_label = ttk.Label(self.login_frame, text="Welcome to SunLab Access", font=('Arial', 24, 'bold'),
                                      foreground=header_color)
        self.header_label.pack(pady=30)

        self.label_username = ttk.Label(self.login_frame, text="Username:")
        self.label_username.pack(pady=10)

        self.entry_username = ttk.Entry(self.login_frame, font=('Arial', 14))
        self.entry_username.pack(pady=10)

        self.label_password = ttk.Label(self.login_frame, text="Password:")
        self.label_password.pack(pady=10)

        self.entry_password = ttk.Entry(self.login_frame, show="*", font=('Arial', 14))
        self.entry_password.pack(pady=10)

        self.btn_login = ttk.Button(self.login_frame, text="Login", command=self.verify_login)
        self.btn_login.pack(pady=20)
        self.btn_login.bind("<Enter>", on_hover)
        self.btn_login.bind("<Leave>", on_leave)

    def verify_login(self):
        entered_username = self.entry_username.get()
        entered_password = self.entry_password.get().encode('utf-8')

        conn = sqlite3.connect('sun_lab.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM admins WHERE username=?", (entered_username,))
        result = cursor.fetchone()

        if result:
            db_hashed_password = result[0]
            if bcrypt.checkpw(entered_password, db_hashed_password):
                self.load_main_options()
            else:
                messagebox.showerror("Error", "Invalid password.")
        else:
            messagebox.showerror("Error", "Invalid username.")

        conn.close()

    def load_main_options(self):
        self.login_frame.pack_forget()

        style = ttk.Style()
        style.theme_use('clam')

        def on_hover(event):
            event.widget["background"] = "lightblue"

        def on_leave(event):
            event.widget["background"] = btn_color

        bg_color = "#f5f5f5"
        btn_color = "#e0e0e0"
        font_color = "#333333"

        self.root.configure(bg=bg_color)

        style.configure("TFrame", background=bg_color)

        style.configure("TButton",
                        background=btn_color,
                        foreground=font_color,
                        borderwidth=1)
        style.map("TButton",
                  background=[('active', 'lightblue'), ('pressed', 'blue')],
                  foreground=[('pressed', 'white')])

        style.configure("TLabel",
                        background=bg_color,
                        foreground=font_color,
                        font=('Arial', 16))

        self.main_frame = ttk.Frame(self.root, style="TFrame")
        self.main_frame.pack(pady=100)

        self.label_main = ttk.Label(self.main_frame, text="Main Menu", font=('Arial', 20))
        self.label_main.pack(pady=20)

        self.btn_add_student = ttk.Button(self.main_frame, text="Add Student", command=self.show_add_student_frame)
        self.btn_add_student.pack(pady=10)
        self.btn_add_student.bind("<Enter>", on_hover)
        self.btn_add_student.bind("<Leave>", on_leave)

        self.btn_access_control = ttk.Button(self.main_frame, text="Access Control",
                                             command=self.show_access_control_frame)
        self.btn_access_control.pack(pady=10)
        self.btn_access_control.bind("<Enter>", on_hover)
        self.btn_access_control.bind("<Leave>", on_leave)

        self.btn_swipe_card = ttk.Button(self.main_frame, text="Swipe Card", command=self.show_swipe_frame)
        self.btn_swipe_card.pack(pady=10)
        self.btn_swipe_card.bind("<Enter>", on_hover)
        self.btn_swipe_card.bind("<Leave>", on_leave)

        self.btn_view_swipe_history = ttk.Button(self.main_frame, text="View Swipe History",
                                                 command=self.show_swipe_history_frame)
        self.btn_view_swipe_history.pack(pady=10)
        self.btn_view_swipe_history.bind("<Enter>", on_hover)
        self.btn_view_swipe_history.bind("<Leave>", on_leave)

    def show_swipe_frame(self):
        self.main_frame.pack_forget()

        self.swipe_frame = ttk.Frame(self.root, padding="30")
        self.swipe_frame.pack(pady=50)

        self.label_swipe = ttk.Label(self.swipe_frame, text="Swipe Card", font=('Arial', 24, 'bold'))
        self.label_swipe.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(self.swipe_frame, text="Student ID:", font=('Arial', 12)).grid(row=1, column=0, padx=(0, 10),
                                                                                 sticky='w')
        self.entry_student_id = ttk.Entry(self.swipe_frame, font=('Arial', 12))
        self.entry_student_id.grid(row=1, column=1, pady=5)

        ttk.Label(self.swipe_frame, text="Swiping:", font=('Arial', 12)).grid(row=2, column=0, padx=(0, 10), sticky='w')
        self.swipe_direction_var = tk.StringVar()
        self.swipe_direction = ttk.Combobox(self.swipe_frame, textvariable=self.swipe_direction_var,
                                            values=["In", "Out"], font=('Arial', 12))
        self.swipe_direction.grid(row=2, column=1, pady=5)

        self.btn_swipe = ttk.Button(self.swipe_frame, text="Swipe", command=self.process_swipe, style='TButton')
        self.btn_swipe.grid(row=3, column=0, columnspan=2, pady=20)

        self.btn_back = ttk.Button(self.swipe_frame, text="Back", command=self.back_to_main, style='TButton')
        self.btn_back.grid(row=4, column=0, columnspan=2, pady=20)

        self.swipe_direction_var.set("In")

        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12), padding=5)

    def process_swipe(self):
        student_id = self.entry_student_id.get()
        direction = self.swipe_direction_var.get().upper()

        if not student_id or not direction:
            messagebox.showerror("Error", "Please fill out both fields.")
            return

        conn = sqlite3.connect('sun_lab.db')
        cursor = conn.cursor()

        cursor.execute("SELECT status FROM users WHERE student_id=?", (student_id,))
        result = cursor.fetchone()



        if result:
            if result[0] == 'allowed':
                cursor.execute("INSERT INTO swipes (student_id, timestamp, direction) VALUES (?, datetime('now'), ?)",
                               (student_id, direction))
                conn.commit()
                if direction == "In":

                    messagebox.showinfo("Success", "Checked In Successfully!")
                elif direction == "Out":

                    messagebox.showinfo("Success", "Checked Out Successfully!")
            else:
                messagebox.showerror("Error", "You do not have access.")
        else:
            messagebox.showerror("Error", "Invalid Student ID.")

        conn.close()

    def show_add_student_frame(self):
        self.main_frame.pack_forget()

        self.add_student_frame = ttk.Frame(self.root, padding="30")
        self.add_student_frame.pack(pady=50)

        self.label_add_student = ttk.Label(self.add_student_frame, text="Add Student", font=('Arial', 24, 'bold'))
        self.label_add_student.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(self.add_student_frame, text="Student ID:", font=('Arial', 12)).grid(row=1, column=0, padx=(0, 10),
                                                                                       sticky='w')
        self.entry_id = ttk.Entry(self.add_student_frame, font=('Arial', 12))
        self.entry_id.grid(row=1, column=1, pady=5)

        ttk.Label(self.add_student_frame, text="Student Name:", font=('Arial', 12)).grid(row=2, column=0, padx=(0, 10),
                                                                                         sticky='w')
        self.entry_name = ttk.Entry(self.add_student_frame, font=('Arial', 12))
        self.entry_name.grid(row=2, column=1, pady=5)

        self.btn_submit = ttk.Button(self.add_student_frame, text="Add", command=self.add_student_to_db,
                                     style='TButton')
        self.btn_submit.grid(row=3, column=0, columnspan=2, pady=20)

        self.btn_back = ttk.Button(self.add_student_frame, text="Back", command=self.back_to_main, style='TButton')
        self.btn_back.grid(row=4, column=0, columnspan=2, pady=20)

        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12), padding=5)

    def add_student_to_db(self):
        student_name = self.entry_name.get()
        student_id = self.entry_id.get()

        if student_name and student_id:
            conn = sqlite3.connect('sun_lab.db')
            cursor = conn.cursor()

            try:
                cursor.execute("INSERT INTO users (student_id, name) VALUES (?, ?)", (student_id, student_name))
                conn.commit()
                messagebox.showinfo("Success", "Student added successfully!")
                self.back_to_main()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Student ID already exists.")
            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "Please enter the student's ID and name.")

    def back_to_main(self):
        if hasattr(self, 'add_student_frame'):
            self.add_student_frame.pack_forget()
        if hasattr(self, 'access_control_frame'):
            self.access_control_frame.pack_forget()
        if hasattr(self, 'swipe_frame'):
            self.swipe_frame.pack_forget()
        if hasattr(self, 'swipe_history_frame'):
            self.swipe_history_frame.pack_forget()
        self.load_main_options()

    def show_access_control_frame(self):
        self.main_frame.pack_forget()

        self.access_control_frame = ttk.Frame(self.root)
        self.access_control_frame.pack(pady=100)

        self.label_access_control = ttk.Label(self.access_control_frame, text="Access Control", font=('Arial', 20))
        self.label_access_control.pack(pady=20)

        self.label_select_student = ttk.Label(self.access_control_frame, text="Select Student:")
        self.label_select_student.pack(pady=10)

        self.dropdown_var = tk.StringVar(self.access_control_frame)

        self.dropdown_students = ttk.Combobox(self.access_control_frame, textvariable=self.dropdown_var)
        self.dropdown_students.pack(pady=10)

        self.update_student_dropdown()

        self.btn_revoke = ttk.Button(self.access_control_frame, text="Revoke Access",
                                     command=lambda: self.update_student_status("revoked"))
        self.btn_revoke.pack(pady=10)

        self.btn_allow = ttk.Button(self.access_control_frame, text="Allow Access",
                                    command=lambda: self.update_student_status("allowed"))
        self.btn_allow.pack(pady=10)

        self.btn_back = ttk.Button(self.access_control_frame, text="Back", command=self.back_to_main)
        self.btn_back.pack(pady=20)

    def update_student_dropdown(self):
        conn = sqlite3.connect('sun_lab.db')
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM users")
        students = cursor.fetchall()

        self.student_names = [student[0] for student in students]

        self.dropdown_students['values'] = self.student_names

        conn.close()

    def update_student_status(self, status):
        selected_student = self.dropdown_var.get()

        if selected_student:
            conn = sqlite3.connect('sun_lab.db')
            cursor = conn.cursor()

            cursor.execute("UPDATE users SET status=? WHERE name=?", (status, selected_student))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"Student {selected_student}'s access has been {status}.")
        else:
            messagebox.showerror("Error", "Please select a student.")

    def show_swipe_history_frame(self):
        self.main_frame.pack_forget()

        self.swipe_history_frame = ttk.Frame(self.root, padding="10")
        self.swipe_history_frame.pack(pady=50)

        self.label_swipe_history = ttk.Label(self.swipe_history_frame, text="Swipe History", font=('Arial', 24, 'bold'))
        self.label_swipe_history.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky='w')

        ttk.Label(self.swipe_history_frame, text="Student Name:", font=('Arial', 12)).grid(row=1, column=0,
                                                                                           padx=(0, 10), sticky='w')
        self.entry_student_name = ttk.Entry(self.swipe_history_frame, font=('Arial', 12))
        self.entry_student_name.grid(row=1, column=1, pady=5, sticky='w')

        ttk.Label(self.swipe_history_frame, text="Date (YYYY-MM-DD):", font=('Arial', 12)).grid(row=2, column=0,
                                                                                                padx=(0, 10),
                                                                                                sticky='w')
        self.entry_date = ttk.Entry(self.swipe_history_frame, font=('Arial', 12))
        self.entry_date.grid(row=2, column=1, pady=5, sticky='w')

        ttk.Label(self.swipe_history_frame, text="Start Time (HH:MM):", font=('Arial', 12)).grid(row=3, column=0,
                                                                                                 padx=(0, 10),
                                                                                                 sticky='w')
        self.entry_start_time = ttk.Entry(self.swipe_history_frame, font=('Arial', 12))
        self.entry_start_time.grid(row=3, column=1, pady=5, sticky='w')

        ttk.Label(self.swipe_history_frame, text="End Time (HH:MM):", font=('Arial', 12)).grid(row=4, column=0,
                                                                                               padx=(0, 10), sticky='w')
        self.entry_end_time = ttk.Entry(self.swipe_history_frame, font=('Arial', 12))
        self.entry_end_time.grid(row=4, column=1, pady=5, sticky='w')

        self.filter_button = ttk.Button(self.swipe_history_frame, text="Filter", command=self.load_swipe_data,
                                        style='TButton')
        self.filter_button.grid(row=5, column=0, columnspan=2, pady=20, sticky='w')

        self.tree_swipe_history = ttk.Treeview(self.swipe_history_frame,
                                               columns=('Student ID', 'Name', 'Time', 'Direction'),
                                               show="headings")
        self.tree_swipe_history.heading('Student ID', text='Student ID')
        self.tree_swipe_history.heading('Name', text='Name')
        self.tree_swipe_history.heading('Time', text='Time')
        self.tree_swipe_history.heading('Direction', text='Direction')
        self.tree_swipe_history.column('Student ID', width=100)
        self.tree_swipe_history.column('Name', width=200)
        self.tree_swipe_history.column('Time', width=150)
        self.tree_swipe_history.column('Direction', width=100)
        self.tree_swipe_history.grid(row=6, column=0, columnspan=2, pady=20, sticky='w')
        # End of the changes

        self.btn_back = ttk.Button(self.swipe_history_frame, text="Back", command=self.back_to_main, style='TButton')
        self.btn_back.grid(row=7, column=0, columnspan=2, pady=20, sticky='w')

        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12), padding=5)

    def load_swipe_data(self):

        for i in self.tree_swipe_history.get_children():
            self.tree_swipe_history.delete(i)

        conn = sqlite3.connect('sun_lab.db')
        cursor = conn.cursor()

        conditions = []
        parameters = []

        student_name = self.entry_student_name.get().strip()
        date = self.entry_date.get().strip()
        start_time = self.entry_start_time.get().strip()
        end_time = self.entry_end_time.get().strip()

        if student_name:
            conditions.append("st.name LIKE ?")
            parameters.append(f"%{student_name}%")

        if date:
            conditions.append("DATE(s.timestamp) = ?")
            parameters.append(date)

        if start_time:
            conditions.append("TIME(s.timestamp) >= ?")
            parameters.append(start_time)

        if end_time:
            conditions.append("TIME(s.timestamp) <= ?")
            parameters.append(end_time)

        query = """
            SELECT s.student_id, st.name, s.timestamp, s.direction 
            FROM swipes AS s
            JOIN users AS st ON s.student_id = st.student_id
        """

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY s.timestamp DESC"

        cursor.execute(query, parameters)

        for row in cursor.fetchall():
            self.tree_swipe_history.insert('', 'end', values=row)

        conn.close()

    def filter_swipe_history(self):
        self.load_swipe_data()


root = tk.Tk()
app = AdminLoginApp(root)
root.mainloop()

