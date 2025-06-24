import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import cx_Oracle
from DBconnect import get_connection 
from PIL import Image, ImageTk
import os
import webbrowser
from ttkthemes import ThemedTk
from datetime import datetime

class BloodBankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Life Line - Blood Bank Management System")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Set theme and colors
        self.primary_color = "#E63946"  # Blood red
        self.secondary_color = "#ffffff"  # white
        self.accent_color = "#1D3557"  # Dark blue
        self.light_accent = "#A8DADC"  # Light blue
        
        # Connect to database
        self.conn = get_connection()
        if not self.conn:
            messagebox.showerror("Connection Error", "Failed to connect to the database!")
            root.destroy()
            return
        
        self.cursor = self.conn.cursor()
        
        # Create styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background=self.secondary_color)
        self.style.configure("TNotebook", background=self.secondary_color)
        self.style.configure("TNotebook.Tab", background=self.light_accent, foreground=self.accent_color, 
                             padding=[10, 5], font=('Arial', 11, 'bold'))
        self.style.map("TNotebook.Tab", background=[("selected", self.primary_color)], 
                       foreground=[("selected", self.accent_color)])
        
        self.style.configure("TLabel", background=self.secondary_color, foreground=self.accent_color, font=('Arial', 11))
        self.style.configure("Header.TLabel", background=self.secondary_color, foreground=self.primary_color, 
                             font=('Arial', 16, 'bold'))
        self.style.configure("Subheader.TLabel", background=self.secondary_color, foreground=self.accent_color, 
                             font=('Arial', 14, 'bold'))
        
        self.style.configure("TButton", background=self.accent_color, foreground=self.accent_color, 
                             font=('Arial', 11, 'bold'), borderwidth=0)
        self.style.map("TButton", background=[("active", self.primary_color)])
        
        self.style.configure("Action.TButton", background=self.primary_color, foreground="red", 
                             font=('Arial', 11, 'bold'), borderwidth=0)
        self.style.map("Action.TButton", background=[("active", "#c1303d")])
        
        self.style.configure("Dashboard.TButton", background=self.light_accent, foreground=self.accent_color, 
                             font=('Arial', 11, 'bold'), borderwidth=0, width=20, padding=10)
        self.style.map("Dashboard.TButton", background=[("active", "#7abec0")])
        
        # Create main container
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)
        
        # Create header frame with logo and title
        self.create_header()
        
        # Create content area with notebook for tabs
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Create tabs
        self.home_tab = ttk.Frame(self.notebook)
        self.admin_tab = ttk.Frame(self.notebook)
        self.staff_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.home_tab, text="  Home  ")
        self.notebook.add(self.admin_tab, text="  Admin  ")
        self.notebook.add(self.staff_tab, text="  Staff  ")
        
        # Initialize all tabs
        self.initialize_home_tab()
        self.initialize_admin_tab()
        self.initialize_staff_tab()
        
        # Create footer
        self.create_footer()

    def create_header(self):
        """Create a header with logo and title"""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill="x", padx=20, pady=10)
        
        # Logo 
        logo_label = ttk.Label(header_frame, text="🩸", font=('Arial', 30), background=self.secondary_color)
        logo_label.pack(side="left", padx=(0, 10))
        
        # Title and subtitle
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side="left")
        
        title_label = ttk.Label(title_frame, text="Life Line", style="Header.TLabel")
        title_label.pack(anchor="w")
        
        subtitle_label = ttk.Label(title_frame, text="Blood Bank Management System", font=('Arial', 12))
        subtitle_label.pack(anchor="w")
        
        # Date and time
        date_frame = ttk.Frame(header_frame)
        date_frame.pack(side="right")
        
        self.date_label = ttk.Label(date_frame, text=datetime.now().strftime("%d %b %Y"), font=('Arial', 10))
        self.date_label.pack(anchor="e")
        
        self.time_label = ttk.Label(date_frame, text=datetime.now().strftime("%H:%M:%S"), font=('Arial', 10))
        self.time_label.pack(anchor="e")
        
        # Update time every second
        self.update_time()

    def update_time(self):
        """Update the time label every second"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

    def create_footer(self):
        """Create a footer with contact information"""
        footer_frame = ttk.Frame(self.main_frame)
        footer_frame.pack(fill="x", padx=20, pady=10)
        
        separator = ttk.Separator(footer_frame, orient="horizontal")
        separator.pack(fill="x", pady=5)
        
        footer_text = ttk.Label(footer_frame, text="© Life Line 2025 | Donate blood, save lives", 
                              font=('Arial', 9))
        footer_text.pack(side="left")
        
        help_button = ttk.Button(footer_frame, text="Help", width=8, 
                               command=lambda: messagebox.showinfo("Help", "For assistance, please contact the administrator."))
        help_button.pack(side="right", padx=5)

    # Home Tab
    def initialize_home_tab(self):
        """Initialize the home tab with welcome message and dashboard"""
        # Banner
        banner_frame = ttk.Frame(self.home_tab, style="TFrame")
        banner_frame.pack(fill="x", pady=(0, 20))
        banner_frame.configure(height=100)
            
        banner_text = ttk.Label(banner_frame, text="\nNot all heroes wear capes, some donate blood.", 
                                  style="Header.TLabel", font=('Lato', 13, 'bold'))
        banner_text.pack(expand=True)
        
        # Main content
        content_frame = ttk.Frame(self.home_tab)
        content_frame.pack(fill="both", expand=True, padx=20)
        
        # Left panel - Quick access
        left_panel = ttk.Frame(content_frame)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        actions_label = ttk.Label(left_panel, text="Quick Actions", style="Subheader.TLabel")
        actions_label.pack(anchor="w", pady=(0, 10))
        
        # Quick action buttons 
        donor_button = ttk.Button(left_panel, text="View Donor's Data", style="Dashboard.TButton", 
                                command=self.view_donor_data)
        donor_button.pack(pady=5, fill="x")
        
        recipient_button = ttk.Button(left_panel, text="View Recipient's Data", style="Dashboard.TButton", 
                                    command=self.view_recipient_data)
        recipient_button.pack(pady=5, fill="x")
        
        # Right panel - Info boxes
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        info_label = ttk.Label(right_panel, text=" ", style="Subheader.TLabel")
        info_label.pack(anchor="w", pady=(0, 10))
        
        # We Offer info box 
        self.create_info_box(right_panel, "We Offer:", 
                           "Blood Types:\nA+, A-, B+, B-, AB+, AB-, O+, O-\n\n"
                           "Blood Components:\nWhole Blood\nPacked RBCs\nPlatelets\nPlasma\nCryoprecipitate")
        
        # Emergency contacts info box 
        self.create_info_box(right_panel, "Emergency Contacts", 
                           "Main Office: 555-1234\nEmail: lifeline@gmail.com" \
                           "\nHospital Address: HMC LinkRoad, Taxila.")

    def create_info_box(self, parent, title, content):
        """Create an information box with title and content"""
        frame = ttk.Frame(parent, style="TFrame", borderwidth=1, relief="solid")
        frame.pack(fill="x", pady=10, ipady=5)
        
        title_label = ttk.Label(frame, text=title, style="Subheader.TLabel", font=('Arial', 12, 'bold'))
        title_label.pack(anchor="w", padx=10, pady=(5, 0))
        
        separator = ttk.Separator(frame, orient="horizontal")
        separator.pack(fill="x", padx=10, pady=5)
        
        content_label = ttk.Label(frame, text=content, justify="left")
        content_label.pack(anchor="w", padx=10, pady=(0, 10))

    def view_blood_inventory(self):
        """View blood inventory data"""
        try:
            self.cursor.execute("SELECT * FROM bloodinventory")
            data = self.cursor.fetchall()
            column_names = [desc[0] for desc in self.cursor.description]
            
            if data:
                self.display_table(data, column_names, "Blood Inventory")
            else:
                messagebox.showinfo("No Data", "No inventory records found.")
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Database Error", str(e))

    def view_statistics(self):
        """Show system statistics"""
        try:
            # Get donor count
            self.cursor.execute("SELECT COUNT(*) FROM donor")
            donor_count = self.cursor.fetchone()[0]
            
            # Get recipient count
            self.cursor.execute("SELECT COUNT(*) FROM recipient")
            recipient_count = self.cursor.fetchone()[0]
            
            # Get blood units
            self.cursor.execute("SELECT COUNT(*) FROM bloodinventory")
            blood_units = self.cursor.fetchone()[0]
            
            # Get transfusion count
            self.cursor.execute("SELECT COUNT(*) FROM transfusion")
            transfusion_count = self.cursor.fetchone()[0]
            
            stats_window = tk.Toplevel(self.root)
            stats_window.title("System Statistics")
            stats_window.geometry("400x300")
            stats_window.resizable(False, False)
            stats_window.configure(bg=self.secondary_color)
            
            ttk.Label(stats_window, text="System Statistics", style="Header.TLabel").pack(pady=20)
            
            stats_frame = ttk.Frame(stats_window)
            stats_frame.pack(fill="both", expand=True, padx=20, pady=10)
            
            self.create_stat_item(stats_frame, "Total Donors ", donor_count, 0)
            self.create_stat_item(stats_frame, "Total Recipients ", recipient_count, 1)
            self.create_stat_item(stats_frame, "Blood Units Available ", blood_units, 2)
            self.create_stat_item(stats_frame, "Transfusions Performed ", transfusion_count, 3)
            
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Database Error", str(e))

    def create_stat_item(self, parent, label, value, row):
        """Create a statistics item with label and value"""
        ttk.Label(parent, text=label, font=('Arial', 11)).grid(row=row, column=0, sticky="w", pady=5)
        ttk.Label(parent, text=str(value), font=('Arial', 11, 'bold'), foreground=self.primary_color).grid(
            row=row, column=1, sticky="e", pady=5)

    def view_donor_data(self):
        """View donor data based on ID"""
        donor_id = self.custom_dialog("Donor Query", "Enter Donor ID:")
        if donor_id:
            try:
                self.cursor.execute("SELECT * FROM donorrecord WHERE donor_id = :id", {"id": donor_id})
                data = self.cursor.fetchall()
                if data:
                    column_names = [desc[0] for desc in self.cursor.description]
                    self.display_table(data, column_names, f"Donor Data - ID: {donor_id}")
                else:
                    messagebox.showinfo("No Record", "No Donor found with the given ID.")
            except cx_Oracle.DatabaseError as e:
                messagebox.showerror("Database Error", str(e))

    def view_recipient_data(self):
        """View recipient data based on ID"""
        recipient_id = self.custom_dialog("Recipient Query", "Enter Recipient ID:")
        if recipient_id:
            try:
                self.cursor.execute("SELECT * FROM recipientrecord WHERE recipient_id = :id", {"id": recipient_id})
                data = self.cursor.fetchall()
                if data:
                    column_names = [desc[0] for desc in self.cursor.description]
                    self.display_table(data, column_names, f"Recipient Data - ID: {recipient_id}")
                else:
                    messagebox.showinfo("No Record", "No Recipient found with the given ID.")
            except cx_Oracle.DatabaseError as e:
                messagebox.showerror("Database Error", str(e))

    def custom_dialog(self, title, prompt):
        """Custom dialog for input with styled appearance"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x150")
        dialog.resizable(True, True)
        dialog.configure(bg=self.secondary_color)
        dialog.transient(self.root)
        dialog.grab_set()
        
        result = tk.StringVar()
        
        ttk.Label(dialog, text=prompt, font=('Arial', 12)).pack(pady=(20, 10))
        
        entry = ttk.Entry(dialog, width=30, font=('Arial', 11))
        entry.pack(pady=10)
        entry.focus_set()
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Cancel", style="TButton", width=10,
                 command=dialog.destroy).pack(side="left", padx=5)
        
        def on_submit():
            result.set(entry.get())
            dialog.destroy()
        
        ttk.Button(button_frame, text="Submit", style="Action.TButton", width=10,
                 command=on_submit).pack(side="left", padx=5)
        
        dialog.bind("<Return>", lambda event: on_submit())
        
        self.root.wait_window(dialog)
        return result.get()

    def password_dialog(self, title, prompt):
        """Custom password dialog with hidden characters"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x150")
        dialog.resizable(False, False)
        dialog.configure(bg=self.secondary_color)
        dialog.transient(self.root)
        dialog.grab_set()
        
        result = tk.StringVar()
        
        ttk.Label(dialog, text=prompt, font=('Arial', 12)).pack(pady=(20, 10))
        
        entry = ttk.Entry(dialog, width=30, font=('Arial', 11), show="*")
        entry.pack(pady=10)
        entry.focus_set()
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Cancel", style="TButton", width=10,
                 command=dialog.destroy).pack(side="left", padx=5)
        
        def on_submit():
            result.set(entry.get())
            dialog.destroy()
        
        ttk.Button(button_frame, text="Submit", style="Action.TButton", width=10,
                 command=on_submit).pack(side="left", padx=5)
        
        dialog.bind("<Return>", lambda event: on_submit())
        
        self.root.wait_window(dialog)
        return result.get()

    # Admin Tab
    def initialize_admin_tab(self):
        """Initialize the admin tab with login and controls"""
        self.admin_frame = ttk.Frame(self.admin_tab)
        self.admin_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Login section
        self.admin_login_frame = ttk.Frame(self.admin_frame)
        self.admin_login_frame.pack(fill="x", pady=20)
        
        ttk.Label(self.admin_login_frame, text="Administrator Panel", style="Header.TLabel").pack(anchor="center")
        ttk.Label(self.admin_login_frame, text="Access restricted area - Authentication required").pack(anchor="center", pady=10)
        
        # Login button 
        self.admin_login_button = ttk.Button(self.admin_login_frame, text="Administrator Login", style="Action.TButton",
                                command=self.admin_login, width=25)
        self.admin_login_button.pack(pady=20)
        
        # Dashboard area (initially hidden)
        self.admin_dashboard = ttk.Frame(self.admin_frame)
        
        # This will be populated after successful login
        self.admin_logged_in = False

    def admin_login(self):
        """Handle admin login with password authentication"""
        password = self.password_dialog("Admin Authentication", "Enter Administrator Password:")
        if password == "admin123":
            self.show_admin_options()
            # Hide login button and frame after successful login
            self.admin_login_frame.pack_forget()
            self.admin_login_button.pack_forget()
        else:
            messagebox.showerror("Authentication Error", "Invalid administrator credentials!")

    def show_admin_options(self):
        """Display admin options after successful login"""
        if not self.admin_logged_in:
            self.admin_dashboard.pack(fill="both", expand=True)
            
            # Create a two-column layout
            left_panel = ttk.Frame(self.admin_dashboard)
            left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
            
            right_panel = ttk.Frame(self.admin_dashboard)
            right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
            
            ttk.Label(left_panel, text=" ", style="Subheader.TLabel").pack(anchor="w", pady=(0, 10))
            
            # Create buttons for each table
            tables = [
                ("Donor Records", "donor", left_panel),
                ("Donor Screening", "donorscreening", left_panel),
                ("Recipient Records", "recipient", left_panel),
                ("Staff Records", "staff", left_panel),
                ("Donation Records", "donation", right_panel),
                ("Transfusion Records", "transfusion", right_panel),
                ("Blood Inventory", "bloodinventory", right_panel),
                ("Expired Blood", "expiredblood", right_panel)
            ]
            
            ttk.Label(right_panel, text=" ", style="Subheader.TLabel").pack(anchor="w", pady=(0, 10))
            
            for table_label, table_name, parent in tables:
                table_button = ttk.Button(parent, text=table_label, style="Dashboard.TButton",
                                       command=lambda tn=table_name: self.admin_table_actions(tn))
                table_button.pack(pady=5, fill="x")
            
            self.admin_logged_in = True

    def admin_table_actions(self, table_name):
        """Display and provide actions for the selected table"""
        try:
            # Fetch the data from the selected table
            self.cursor.execute(f"SELECT * FROM {table_name}")
            data = self.cursor.fetchall()
            column_names = [desc[0] for desc in self.cursor.description]
            
            # Display the table data in a new window
            table_window = tk.Toplevel(self.root)
            table_window.title(f"{table_name.capitalize()} Management")
            table_window.geometry("800x600")
            table_window.configure(bg=self.secondary_color)
            
            main_frame = ttk.Frame(table_window)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Title
            ttk.Label(main_frame, text=f"{table_name.capitalize()} Records", 
                    style="Header.TLabel").pack(pady=(0, 20))
            
            # Table display
            tree_frame = ttk.Frame(main_frame)
            tree_frame.pack(fill="both", expand=True)
            
            # Create scrollbar
            scrollbar_y = ttk.Scrollbar(tree_frame)
            scrollbar_y.pack(side="right", fill="y")
            
            scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal")
            scrollbar_x.pack(side="bottom", fill="x")
            
            # Create treeview
            tree = ttk.Treeview(tree_frame, columns=column_names, show="headings",
                              yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
            
            # Configure scrollbars
            scrollbar_y.config(command=tree.yview)
            scrollbar_x.config(command=tree.xview)
            
            # Configure columns and headings
            for col in column_names:
                tree.heading(col, text=col.upper())
                tree.column(col, width=100, anchor="center")
            
            # Insert data
            for row in data:
                tree.insert("", "end", values=row)
            
            tree.pack(fill="both", expand=True)
            
            # Buttons frame
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill="x", pady=20)
            
            # Action buttons
            ttk.Button(button_frame, text="Insert Record", style="Action.TButton",
                     command=lambda: self.insert_data(table_name, column_names, table_window, tree)).pack(side="left", padx=5)
            
            ttk.Button(button_frame, text="Update Record", style="Action.TButton",
                     command=lambda: self.update_data(table_name, column_names, table_window, tree)).pack(side="left", padx=5)
            
            ttk.Button(button_frame, text="Delete Record", style="Action.TButton",
                     command=lambda: self.delete_data(table_name, column_names, table_window, tree)).pack(side="left", padx=5)
            
            ttk.Button(button_frame, text="Refresh", style="TButton",
                     command=lambda: self.refresh_table(table_name, tree)).pack(side="right", padx=5)
            
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Database Error", str(e))

    def refresh_table(self, table_name, tree):
        """Refresh the treeview with updated data"""
        try:
            # Clear existing data
            for item in tree.get_children():
                tree.delete(item)
            
            # Fetch and insert new data
            self.cursor.execute(f"SELECT * FROM {table_name}")
            data = self.cursor.fetchall()
            
            for row in data:
                tree.insert("", "end", values=row)
                
            messagebox.showinfo("Success", "Table data refreshed successfully!")
            
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Database Error", str(e))

    def insert_data(self, table_name, column_names, parent_window, tree=None):
        """Open a form to insert new data into the selected table"""
        try:
            # Create a form for data entry
            insert_window = tk.Toplevel(parent_window)
            insert_window.title(f"Insert Data - {table_name.capitalize()}")
            insert_window.geometry("500x600")
            insert_window.configure(bg=self.secondary_color)
            insert_window.transient(parent_window)
            insert_window.grab_set()
            
            main_frame = ttk.Frame(insert_window)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            ttk.Label(main_frame, text=f"Add New {table_name.capitalize()} Record", 
                    style="Header.TLabel").pack(pady=(0, 20))
            
            canvas = tk.Canvas(main_frame, bg=self.secondary_color, highlightthickness=0)
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            
            form_frame = ttk.Frame(canvas)
            
            canvas.configure(yscrollcommand=scrollbar.set)
            
            scrollbar.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)
            
            canvas_window = canvas.create_window((0, 0), window=form_frame, anchor="nw")
            
            def configure_canvas(event):
                canvas.configure(scrollregion=canvas.bbox("all"), width=event.width)
            
            canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            form_frame.bind("<Configure>", configure_canvas)
            
            # Entry fields
            entry_fields = {}
            for i, col in enumerate(column_names):
                frame = ttk.Frame(form_frame)
                frame.pack(fill="x", pady=5)
                
                label = ttk.Label(frame, text=f"{col.upper()}:", width=20, anchor="e")
                label.pack(side="left", padx=(0, 10))
                
                entry = ttk.Entry(frame, width=30)
                entry.pack(side="left", fill="x", expand=True)
                entry_fields[col] = entry
            
            button_frame = ttk.Frame(form_frame)
            button_frame.pack(side="bottom")
            
            def submit_insert():
                data = {col: entry.get() for col, entry in entry_fields.items()}
                
                # Use stored procedures for specific tables
                if table_name.lower() == "donation":
                    try:
                        # Call the InsertDonation procedure
                        self.cursor.callproc("InsertDonation", [
                            int(data.get("DONATION_ID")),
                            int(data.get("DONOR_ID")),
                            data.get("DONATED_BLOODTYPE"),
                            int(data.get("DONATED_QUANTITY")),
                            data.get("DONATION_DATE"),
                            int(data.get("RECIPIENT_ID")),
                            int(data.get("INVENTORY_ID"))
                        ])
                        self.conn.commit()
                        messagebox.showinfo("Success", "Donation record inserted successfully!")
                        insert_window.destroy()
                        if tree:
                            self.refresh_table(table_name, tree)
                    except cx_Oracle.DatabaseError as e:
                        messagebox.showerror("Database Error", str(e))
                elif table_name.lower() == "transfusion":
                    try:
                        # Call the InsertTransfusion procedure
                        self.cursor.callproc("InsertTransfusion", [
                            int(data.get("TRANSFUSION_ID")),
                            int(data.get("RECIPIENT_ID")),
                            data.get("REQUESTED_BLOODTYPE"),
                            data.get("REQUESTED_COMPONENT"),
                            int(data.get("REQUESTED_QUANTITY")),
                            data.get("REQUEST_DATE"),
                            data.get("EXCHANGE_TYPE"),
                            int(data.get("EXCHANGE_DONOR_ID")),
                            int(data.get("DONATION_ID")),
                            int(data.get("INVENTORY_ID"))
                        ])
                        self.conn.commit()
                        messagebox.showinfo("Success", "Transfusion record inserted successfully!")
                        insert_window.destroy()
                        if tree:
                            self.refresh_table(table_name, tree)
                    except cx_Oracle.DatabaseError as e:
                        messagebox.showerror("Database Error", str(e))
                else:
                    # Default insert for other tables
                    placeholders = ", ".join([f":{col}" for col in column_names])
                    sql = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})"
                    
                    try:
                        self.cursor.execute(sql, data)
                        self.conn.commit()
                        messagebox.showinfo("Success", "Record inserted successfully!")
                        insert_window.destroy()
                        
                        # Refresh the table if available
                        if tree:
                            self.refresh_table(table_name, tree)
                            
                    except cx_Oracle.DatabaseError as e:
                        messagebox.showerror("Database Error", str(e))
            
            ttk.Button(button_frame, text="Cancel", style="TButton", width=10,
                     command=insert_window.destroy).pack(side="left", padx=5)
            
            ttk.Button(button_frame, text="Submit", style="Action.TButton", width=10,
                     command=submit_insert).pack(side="right", padx=5)
            
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Database Error", str(e))

    def update_data(self, table_name, column_names, parent_window, tree=None):
        """Open a form to update existing data in the selected table"""
        try:
            update_window = tk.Toplevel(parent_window)
            update_window.title(f"Update Data - {table_name.capitalize()}")
            update_window.geometry("500x300")
            update_window.configure(bg=self.secondary_color)
            update_window.transient(parent_window)
            update_window.grab_set()
            
            main_frame = ttk.Frame(update_window)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            ttk.Label(main_frame, text=f"Update {table_name.capitalize()} Record", 
                    style="Header.TLabel").pack(pady=(0, 20))
            
            # ID field
            id_frame = ttk.Frame(main_frame)
            id_frame.pack(fill="x", pady=10)
            
            ttk.Label(id_frame, text=f"{column_names[0].upper()}:", width=20, anchor="e").pack(
                side="left", padx=(0, 10))
            
            id_entry = ttk.Entry(id_frame, width=30)
            id_entry.pack(side="left", fill="x", expand=True)
            
            # Column selection
            column_frame = ttk.Frame(main_frame)
            column_frame.pack(fill="x", pady=10)
            
            ttk.Label(column_frame, text="Field to Update:", width=20, anchor="e").pack(
                side="left", padx=(0, 10))
            
            column_combo = ttk.Combobox(column_frame, values=column_names, width=28)
            column_combo.pack(side="left", fill="x", expand=True)
            
            value_frame = ttk.Frame(main_frame)
            value_frame.pack(fill="x", pady=10)
            
            ttk.Label(value_frame, text="New Value:", width=20, anchor="e").pack(
                side="left", padx=(0, 10))
            
            value_entry = ttk.Entry(value_frame, width=30)
            value_entry.pack(side="left", fill="x", expand=True)
            
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill="x", pady=20)
            
            def submit_update():
                pk_value = id_entry.get()
                column = column_combo.get()
                new_value = value_entry.get()
                
                if not pk_value or not column or not new_value:
                    messagebox.showerror("Input Error", "All fields are required!")
                    return
                
                try:
                    # Use stored procedures for specific tables
                    if table_name.lower() == "donation":
                        if column.upper() == "DONATED_QUANTITY":
                            self.cursor.callproc("UpdateDonation", [int(pk_value), int(new_value)])
                            self.conn.commit()
                            messagebox.showinfo("Success", "Donation record updated successfully!")
                        else:
                            messagebox.showerror("Update Error", "Only Donated_Quantity can be updated for Donation records")
                    elif table_name.lower() == "transfusion":
                        if column.upper() == "REQUESTED_QUANTITY":
                            self.cursor.callproc("UpdateTransfusion", [int(pk_value), int(new_value)])
                            self.conn.commit()
                            messagebox.showinfo("Success", "Transfusion record updated successfully!")
                        else:
                            messagebox.showerror("Update Error", "Only Requested_Quantity can be updated for Transfusion records")
                    else:
                        # Default update for other tables
                        sql = f"UPDATE {table_name} SET {column} = :new_value WHERE {column_names[0]} = :pk_value"
                        self.cursor.execute(sql, {"new_value": new_value, "pk_value": pk_value})
                        self.conn.commit()
                        messagebox.showinfo("Success", "Record updated successfully!")
                    
                    update_window.destroy()
                    
                    # Refresh the table if available
                    if tree:
                        self.refresh_table(table_name, tree)
                        
                except cx_Oracle.DatabaseError as e:
                    messagebox.showerror("Database Error", str(e))
            
            ttk.Button(button_frame, text="Cancel", style="TButton", width=10,
                     command=update_window.destroy).pack(side="left", padx=5)
            
            ttk.Button(button_frame, text="Update", style="Action.TButton", width=10,
                     command=submit_update).pack(side="right", padx=5)
            
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Database Error", str(e))

    def delete_data(self, table_name, column_names, parent_window, tree=None):
        """Open a form to delete data from the selected table"""
        try:
            delete_window = tk.Toplevel(parent_window)
            delete_window.title(f"Delete Data - {table_name.capitalize()}")
            delete_window.geometry("500x200")
            delete_window.configure(bg=self.secondary_color)
            delete_window.transient(parent_window)
            delete_window.grab_set()
            
            main_frame = ttk.Frame(delete_window)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            ttk.Label(main_frame, text=f"Delete {table_name.capitalize()} Record", 
                    style="Header.TLabel").pack(pady=(0, 20))
            
            # Warning message
            warning_label = ttk.Label(main_frame, text="Warning: This action cannot be undone!", 
                                    foreground=self.primary_color)
            warning_label.pack(pady=10)
            
            # ID field
            id_frame = ttk.Frame(main_frame)
            id_frame.pack(fill="x", pady=10)
            
            ttk.Label(id_frame, text=f"{column_names[0].upper()}:", width=20, anchor="e").pack(
                side="left", padx=(0, 10))
            
            id_entry = ttk.Entry(id_frame, width=30)
            id_entry.pack(side="left", fill="x", expand=True)
            
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill="x", pady=20)
            
            def submit_delete():
                pk_value = id_entry.get()
                
                if not pk_value:
                    messagebox.showerror("Input Error", "ID is required!")
                    return
                
                confirm = messagebox.askyesno("Confirm Delete", 
                                             f"Are you sure you want to delete record with ID: {pk_value}?")
                if not confirm:
                    return
                
                try:
                    # Use stored procedures 
                    if table_name.lower() == "donation":
                        self.cursor.callproc("DeleteDonation", [int(pk_value)])
                        self.conn.commit()
                        messagebox.showinfo("Success", "Donation record deleted successfully!")
                    elif table_name.lower() == "transfusion":
                        self.cursor.callproc("DeleteTransfusion", [int(pk_value)])
                        self.conn.commit()
                        messagebox.showinfo("Success", "Transfusion record deleted successfully!")
                    else:
                        # Default delete for other tables
                        sql = f"DELETE FROM {table_name} WHERE {column_names[0]} = :pk_value"
                        self.cursor.execute(sql, {"pk_value": pk_value})
                        self.conn.commit()
                        messagebox.showinfo("Success", "Record deleted successfully!")
                    
                    delete_window.destroy()
                    
                    # Refresh the table if available
                    if tree:
                        self.refresh_table(table_name, tree)
                        
                except cx_Oracle.DatabaseError as e:
                    messagebox.showerror("Database Error", str(e))
            
            ttk.Button(button_frame, text="Cancel", style="TButton", width=10,
                     command=delete_window.destroy).pack(side="left", padx=5)
            
            ttk.Button(button_frame, text="Delete", style="Action.TButton", width=10,
                     command=submit_delete).pack(side="right", padx=5)
            
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Database Error", str(e))

    def display_table(self, data, column_names, title="Database Records"):
        """Display data in a styled table view"""
        top = tk.Toplevel(self.root)
        top.title(title)
        top.geometry("800x500")
        top.configure(bg=self.secondary_color)
        
        main_frame = ttk.Frame(top)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text=title, style="Header.TLabel").pack(pady=(0, 20))
        
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True)
        
        scrollbar_y = ttk.Scrollbar(tree_frame)
        scrollbar_y.pack(side="right", fill="y")
        
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")
        
        tree = ttk.Treeview(tree_frame, columns=column_names, show="headings",
                          yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.config(command=tree.yview)
        scrollbar_x.config(command=tree.xview)
        
        # Configure columns and headings
        for col in column_names:
            tree.heading(col, text=col.upper())
            tree.column(col, width=100, anchor="center")
        
        # Insert data
        for row in data:
            tree.insert("", "end", values=row)
        
        tree.pack(fill="both", expand=True)
        
        # Button to close the window
        ttk.Button(main_frame, text="Close", command=top.destroy, style="TButton",
                 width=15).pack(pady=10)

    # Staff Tab
    def initialize_staff_tab(self):
        """Initialize the staff tab with staff specific functions"""
        self.staff_frame = ttk.Frame(self.staff_tab)
        self.staff_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Login section
        self.staff_login_frame = ttk.Frame(self.staff_frame)
        self.staff_login_frame.pack(fill="x", pady=20)
        
        ttk.Label(self.staff_login_frame, text="Staff Panel", style="Header.TLabel").pack(anchor="center")
        ttk.Label(self.staff_login_frame, text="Access restricted area - Authentication required").pack(anchor="center", pady=10)
        
        # Login button 
        self.staff_login_button = ttk.Button(self.staff_login_frame, text="Staff Login", style="Action.TButton",
                                command=self.staff_login, width=25)
        self.staff_login_button.pack(pady=20)
        
        # Dashboard area (initially hidden)
        self.staff_dashboard = ttk.Frame(self.staff_frame)
        
        # This will be populated after successful login
        self.staff_logged_in = False

    def staff_login(self):
        """Handle staff login with password authentication"""
        password = self.password_dialog("Staff Authentication", "Enter Staff Password:")
        if password == "staff123":
            self.show_staff_options()
            # Hide login button and frame after successful login
            self.staff_login_frame.pack_forget()
            self.staff_login_button.pack_forget()
        else:
            messagebox.showerror("Authentication Error", "Invalid staff credentials!")

    def show_staff_options(self):
        """Display staff options after successful login"""
        if not self.staff_logged_in:
            self.staff_dashboard.pack(fill="both", expand=True)
            
            ttk.Label(self.staff_dashboard, text="Staff Dashboard", style="Header.TLabel").pack(pady=(0, 20))
            
            # Split into two panels
            top_frame = ttk.Frame(self.staff_dashboard)
            top_frame.pack(fill="x", pady=10)
            
            # Create two columns
            left_panel = ttk.Frame(top_frame)
            left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
            
            right_panel = ttk.Frame(top_frame)
            right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
            
            # Left panel 
            ttk.Label(left_panel, text=" ", style="Subheader.TLabel").pack(anchor="w", pady=(0, 10))
            
            screening_button = ttk.Button(left_panel, text="Donor Screening", style="Dashboard.TButton",
                                    command=self.donor_screening)
            screening_button.pack(pady=5, fill="x")

            stats_button = ttk.Button(left_panel, text="System Statistics", style="Dashboard.TButton",
                                command=self.view_statistics)
            stats_button.pack(pady=5, fill="x")

            
            # Right panel 
            ttk.Label(right_panel, text=" ", style="Subheader.TLabel").pack(anchor="w", pady=(0, 10))
            
            inventory_button = ttk.Button(right_panel, text="Blood Inventory Status", style="Dashboard.TButton",
                                    command=self.view_blood_inventory)
            inventory_button.pack(pady=5, fill="x")
            
            expired_button = ttk.Button(right_panel, text="Check Expired Blood", style="Dashboard.TButton",
                                  command=self.check_expired_blood)
            expired_button.pack(pady=5, fill="x")
                    
            self.staff_logged_in = True

    def donor_screening(self):
        """Open form for donor screening"""
        try:
            self.cursor.execute("SELECT * FROM donorscreening WHERE 1=0")  
            column_names = [desc[0] for desc in self.cursor.description]
            
            self.insert_data("donorscreening", column_names, None , None)
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Database Error", str(e))

    def check_expired_blood(self):
        """Check and display expired blood units"""
        try:
            self.cursor.execute("SELECT * FROM expiredblood")
            data = self.cursor.fetchall()
            column_names = [desc[0] for desc in self.cursor.description]
            
            if data:
                self.display_table(data, column_names, "Expired Blood Units")
            else:
                messagebox.showinfo("Expired Blood", "No expired blood units found.")
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Database Error", str(e))

    def create_staff_form(self, title, table_name, column_names):
        """Create a properly aligned staff form with buttons below input fields"""
        form_window = tk.Toplevel(self.root)
        form_window.title(title)
        form_window.geometry("600x700")
        form_window.configure(bg=self.secondary_color)
        
        main_frame = ttk.Frame(form_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text=title, style="Header.TLabel").pack(pady=(0, 20))
        
        canvas = tk.Canvas(main_frame, bg=self.secondary_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        
        form_frame = ttk.Frame(canvas)
        
        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        canvas_window = canvas.create_window((0, 0), window=form_frame, anchor="nw")
        
        def configure_canvas(event):
            canvas.configure(scrollregion=canvas.bbox("all"), width=event.width)
        
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        form_frame.bind("<Configure>", configure_canvas)
        
        # Entry fields with proper alignment
        entry_fields = {}
        for i, col in enumerate(column_names):
            frame = ttk.Frame(form_frame)
            frame.pack(fill="x", pady=5, padx=10)
            
            label = ttk.Label(frame, text=f"{col.upper()}:", width=25, anchor="e")
            label.pack(side="left", padx=(0, 10))
            
            # Different input types 
            if "date" in col.lower():
                # For date fields
                date_frame = ttk.Frame(frame)
                date_frame.pack(side="left", fill="x", expand=True)
                
                day = ttk.Combobox(date_frame, values=[str(i).zfill(2) for i in range(1, 32)], width=5)
                day.pack(side="left", padx=2)
                day.set("DD")
                
                month = ttk.Combobox(date_frame, values=[str(i).zfill(2) for i in range(1, 13)], width=5)
                month.pack(side="left", padx=2)
                month.set("MM")
                
                year = ttk.Combobox(date_frame, values=[str(i) for i in range(2020, 2026)], width=6)
                year.pack(side="left", padx=2)
                year.set("YYYY")
                
                entry = ttk.Entry(frame)
                entry.pack_forget()  
                
                def update_date(event, entry=entry, day=day, month=month, year=year):
                    entry.delete(0, tk.END)
                    if day.get() != "DD" and month.get() != "MM" and year.get() != "YYYY":
                        entry.insert(0, f"{day.get()}/{month.get()}/{year.get()}")
                
                day.bind("<<ComboboxSelected>>", update_date)
                month.bind("<<ComboboxSelected>>", update_date)
                year.bind("<<ComboboxSelected>>", update_date)
                
            elif "blood" in col.lower() and "group" in col.lower():
                # For blood group fields
                entry = ttk.Combobox(frame, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], width=28)
                entry.pack(side="left", fill="x", expand=True)
                
            elif "gender" in col.lower():
                # For gender fields
                entry = ttk.Combobox(frame, values=["Male", "Female", "Other"], width=28)
                entry.pack(side="left", fill="x", expand=True)
                
            elif "status" in col.lower():
                # For status fields
                entry = ttk.Combobox(frame, values=["Active", "Inactive", "Pending"], width=28)
                entry.pack(side="left", fill="x", expand=True)
                
            else:
                # Default text entry
                entry = ttk.Entry(frame, width=30)
                entry.pack(side="left", fill="x", expand=True)
                
            entry_fields[col] = entry
        
        # Button frame at the bottom (outside the scrollable area)
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=20)
        
        def submit_form():
            # Collect data from entry fields
            data = {col: entry.get() for col, entry in entry_fields.items()}
            
            # Check if all required fields are filled
            if not all(data.values()):
                messagebox.showerror("Input Error", "All fields are required!")
                return
            
            # Prepare the SQL query
            placeholders = ", ".join([f":{col}" for col in column_names])
            sql = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})"
            
            try:
                self.cursor.execute(sql, data)
                self.conn.commit()
                messagebox.showinfo("Success", "Record submitted successfully!")
                form_window.destroy()
            except cx_Oracle.DatabaseError as e:
                messagebox.showerror("Database Error", str(e))
            
        ttk.Button(button_frame, text="Cancel", style="TButton", width=10,
                 command=form_window.destroy).pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Submit", style="Action.TButton", width=10,
                 command=submit_form).pack(side="right", padx=5)


# Main program
if __name__ == "__main__":
    try:
        root = ThemedTk(theme="arc")  
    except:
        root = tk.Tk()
        
    app = BloodBankApp(root)
    root.mainloop()