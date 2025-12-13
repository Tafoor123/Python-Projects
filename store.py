import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import hashlib

class BakeryLoginSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FreshBake Login System")
        self.root.geometry("400x500")
        self.root.configure(bg='#f8f9fa')
        self.root.resizable(False, False)
        
        # User data file
        self.users_file = "bakery_users.json"
        self.current_user = None
        
        # Load existing users
        self.load_users()
        
        # Create login window
        self.create_login_window()
        
    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            # Default users
            self.users = {
                "admin": {
                    "password": self.hash_password("admin123"),
                    "role": "admin",
                    "full_name": "Bakery Manager",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                "staff1": {
                    "password": self.hash_password("staff123"),
                    "role": "staff",
                    "full_name": "John Baker",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                "customer1": {
                    "password": self.hash_password("customer123"),
                    "role": "customer",
                    "full_name": "Sarah Smith",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            self.save_users()
    
    def save_users(self):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_login_window(self):
        """Create the main login window"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#f8f9fa')
        header_frame.pack(pady=(0, 30))
        
        # Bakery icon/logo
        self.create_bakery_icon(header_frame)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="FreshBake Bakery",
            font=('Arial', 24, 'bold'),
            fg='#d35400',
            bg='#f8f9fa'
        )
        title_label.pack(pady=(10, 5))
        
        subtitle_label = tk.Label(
            header_frame,
            text="Sweet Delights Await You!",
            font=('Arial', 12),
            fg='#7f8c8d',
            bg='#f8f9fa'
        )
        subtitle_label.pack()
        
        # Login form frame
        form_frame = tk.Frame(main_frame, bg='#ffffff', relief='raised', bd=2)
        form_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Form title
        form_title = tk.Label(
            form_frame,
            text="Login to Your Account",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='#ffffff'
        )
        form_title.pack(pady=20)
        
        # Username field
        username_frame = tk.Frame(form_frame, bg='#ffffff')
        username_frame.pack(fill='x', padx=30, pady=10)
        
        tk.Label(
            username_frame,
            text="Username:",
            font=('Arial', 11, 'bold'),
            fg='#34495e',
            bg='#ffffff'
        ).pack(anchor='w')
        
        self.username_entry = tk.Entry(
            username_frame,
            font=('Arial', 12),
            bg='#ecf0f1',
            relief='solid',
            bd=1
        )
        self.username_entry.pack(fill='x', pady=(5, 0))
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        
        # Password field
        password_frame = tk.Frame(form_frame, bg='#ffffff')
        password_frame.pack(fill='x', padx=30, pady=10)
        
        tk.Label(
            password_frame,
            text="Password:",
            font=('Arial', 11, 'bold'),
            fg='#34495e',
            bg='#ffffff'
        ).pack(anchor='w')
        
        self.password_entry = tk.Entry(
            password_frame,
            font=('Arial', 12),
            show='•',
            bg='#ecf0f1',
            relief='solid',
            bd=1
        )
        self.password_entry.pack(fill='x', pady=(5, 0))
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Login button
        login_btn = tk.Button(
            form_frame,
            text="Login to Bakery",
            font=('Arial', 12, 'bold'),
            bg='#e67e22',
            fg='white',
            command=self.login,
            cursor='hand2',
            relief='raised',
            bd=0,
            padx=20,
            pady=10
        )
        login_btn.pack(pady=20)
        
        # Register link
        register_frame = tk.Frame(form_frame, bg='#ffffff')
        register_frame.pack(pady=10)
        
        tk.Label(
            register_frame,
            text="Don't have an account?",
            font=('Arial', 10),
            fg='#7f8c8d',
            bg='#ffffff'
        ).pack(side='left')
        
        register_btn = tk.Button(
            register_frame,
            text="Register Here",
            font=('Arial', 10, 'bold'),
            fg='#3498db',
            bg='#ffffff',
            relief='flat',
            cursor='hand2',
            command=self.show_register_window
        )
        register_btn.pack(side='left')
        
        # Set focus to username field
        self.username_entry.focus()
    
    def create_bakery_icon(self, parent):
        """Create a simple bakery icon using canvas"""
        icon_canvas = tk.Canvas(
            parent,
            width=80,
            height=80,
            bg='#f8f9fa',
            highlightthickness=0
        )
        icon_canvas.pack()
        
        # Draw a simple bakery icon (bread and wheat)
        icon_canvas.create_oval(20, 30, 60, 70, fill='#f39c12', outline='#e67e22')  # Bread
        icon_canvas.create_arc(15, 25, 65, 75, start=0, extent=180, fill='#d35400', outline='')  # Bread top
        icon_canvas.create_line(40, 15, 40, 30, fill='#27ae60', width=3)  # Wheat stem
        icon_canvas.create_line(35, 20, 45, 25, fill='#27ae60', width=2)  # Wheat leaf
        icon_canvas.create_line(37, 15, 43, 15, fill='#f1c40f', width=2)  # Wheat head
    
    def show_register_window(self):
        """Show registration window"""
        register_window = tk.Toplevel(self.root)
        register_window.title("Register - FreshBake Bakery")
        register_window.geometry("400x550")
        register_window.configure(bg='#f8f9fa')
        register_window.resizable(False, False)
        
        # Center the window
        register_window.transient(self.root)
        register_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(register_window, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#f8f9fa')
        header_frame.pack(pady=(0, 20))
        
        title_label = tk.Label(
            header_frame,
            text="Create New Account",
            font=('Arial', 20, 'bold'),
            fg='#d35400',
            bg='#f8f9fa'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Join our bakery family!",
            font=('Arial', 11),
            fg='#7f8c8d',
            bg='#f8f9fa'
        )
        subtitle_label.pack()
        
        # Registration form
        form_frame = tk.Frame(main_frame, bg='#ffffff', relief='raised', bd=2)
        form_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Full Name
        name_frame = tk.Frame(form_frame, bg='#ffffff')
        name_frame.pack(fill='x', padx=25, pady=10)
        
        tk.Label(
            name_frame,
            text="Full Name:",
            font=('Arial', 11, 'bold'),
            fg='#34495e',
            bg='#ffffff'
        ).pack(anchor='w')
        
        name_entry = tk.Entry(
            name_frame,
            font=('Arial', 12),
            bg='#ecf0f1',
            relief='solid',
            bd=1
        )
        name_entry.pack(fill='x', pady=(5, 0))
        
        # Username
        username_frame = tk.Frame(form_frame, bg='#ffffff')
        username_frame.pack(fill='x', padx=25, pady=10)
        
        tk.Label(
            username_frame,
            text="Username:",
            font=('Arial', 11, 'bold'),
            fg='#34495e',
            bg='#ffffff'
        ).pack(anchor='w')
        
        reg_username_entry = tk.Entry(
            username_frame,
            font=('Arial', 12),
            bg='#ecf0f1',
            relief='solid',
            bd=1
        )
        reg_username_entry.pack(fill='x', pady=(5, 0))
        
        # Password
        password_frame = tk.Frame(form_frame, bg='#ffffff')
        password_frame.pack(fill='x', padx=25, pady=10)
        
        tk.Label(
            password_frame,
            text="Password:",
            font=('Arial', 11, 'bold'),
            fg='#34495e',
            bg='#ffffff'
        ).pack(anchor='w')
        
        reg_password_entry = tk.Entry(
            password_frame,
            font=('Arial', 12),
            show='•',
            bg='#ecf0f1',
            relief='solid',
            bd=1
        )
        reg_password_entry.pack(fill='x', pady=(5, 0))
        
        # Confirm Password
        confirm_frame = tk.Frame(form_frame, bg='#ffffff')
        confirm_frame.pack(fill='x', padx=25, pady=10)
        
        tk.Label(
            confirm_frame,
            text="Confirm Password:",
            font=('Arial', 11, 'bold'),
            fg='#34495e',
            bg='#ffffff'
        ).pack(anchor='w')
        
        confirm_password_entry = tk.Entry(
            confirm_frame,
            font=('Arial', 12),
            show='•',
            bg='#ecf0f1',
            relief='solid',
            bd=1
        )
        confirm_password_entry.pack(fill='x', pady=(5, 0))
        
        # Role selection
        role_frame = tk.Frame(form_frame, bg='#ffffff')
        role_frame.pack(fill='x', padx=25, pady=10)
        
        tk.Label(
            role_frame,
            text="Account Type:",
            font=('Arial', 11, 'bold'),
            fg='#34495e',
            bg='#ffffff'
        ).pack(anchor='w')
        
        role_var = tk.StringVar(value="customer")
        
        customer_radio = tk.Radiobutton(
            role_frame,
            text="Customer",
            variable=role_var,
            value="customer",
            bg='#ffffff',
            font=('Arial', 10)
        )
        customer_radio.pack(anchor='w')
        
        staff_radio = tk.Radiobutton(
            role_frame,
            text="Staff Member",
            variable=role_var,
            value="staff",
            bg='#ffffff',
            font=('Arial', 10)
        )
        staff_radio.pack(anchor='w')
        
        # Register button
        def register():
            full_name = name_entry.get().strip()
            username = reg_username_entry.get().strip()
            password = reg_password_entry.get()
            confirm_password = confirm_password_entry.get()
            role = role_var.get()
            
            if not all([full_name, username, password, confirm_password]):
                messagebox.showerror("Error", "Please fill in all fields!")
                return
                
            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match!")
                return
                
            if username in self.users:
                messagebox.showerror("Error", "Username already exists!")
                return
                
            # Register new user
            self.users[username] = {
                "password": self.hash_password(password),
                "role": role,
                "full_name": full_name,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.save_users()
            
            messagebox.showinfo("Success", "Account created successfully!\nYou can now login.")
            register_window.destroy()
        
        register_btn = tk.Button(
            form_frame,
            text="Create Account",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            command=register,
            cursor='hand2',
            relief='raised',
            bd=0,
            padx=20,
            pady=10
        )
        register_btn.pack(pady=20)
    
    def login(self):
        """Handle login process"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password!")
            return
        
        if username not in self.users:
            messagebox.showerror("Error", "Invalid username or password!")
            return
        
        hashed_password = self.hash_password(password)
        if self.users[username]["password"] != hashed_password:
            messagebox.showerror("Error", "Invalid username or password!")
            return
        
        # Successful login
        self.current_user = {
            "username": username,
            "role": self.users[username]["role"],
            "full_name": self.users[username]["full_name"]
        }
        
        messagebox.showinfo("Welcome!", f"Welcome back, {self.users[username]['full_name']}!")
        self.show_dashboard()
    
    def show_dashboard(self):
        """Show main dashboard after login"""
        # Clear login window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title(f"FreshBake Dashboard - Welcome {self.current_user['full_name']}")
        self.root.geometry("800x600")
        
        # Create dashboard
        self.create_dashboard()
    
    def create_dashboard(self):
        """Create the main dashboard"""
        # Header
        header_frame = tk.Frame(self.root, bg='#d35400')
        header_frame.pack(fill='x', padx=0, pady=0)
        
        # Welcome message
        welcome_label = tk.Label(
            header_frame,
            text=f"Welcome to FreshBake Bakery, {self.current_user['full_name']}!",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#d35400',
            pady=15
        )
        welcome_label.pack()
        
        # User info
        user_info_frame = tk.Frame(header_frame, bg='#e67e22')
        user_info_frame.pack(fill='x', padx=0, pady=5)
        
        user_info = tk.Label(
            user_info_frame,
            text=f"Role: {self.current_user['role'].title()} | Username: {self.current_user['username']}",
            font=('Arial', 10),
            fg='white',
            bg='#e67e22',
            pady=5
        )
        user_info.pack()
        
        # Main content
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Dashboard cards based on user role
        if self.current_user['role'] == 'admin':
            self.create_admin_dashboard(main_frame)
        elif self.current_user['role'] == 'staff':
            self.create_staff_dashboard(main_frame)
        else:
            self.create_customer_dashboard(main_frame)
        
        # Logout button
        logout_btn = tk.Button(
            self.root,
            text="Logout",
            font=('Arial', 10, 'bold'),
            bg='#e74c3c',
            fg='white',
            command=self.logout,
            cursor='hand2',
            padx=15,
            pady=5
        )
        logout_btn.place(x=700, y=10)
    
    def create_admin_dashboard(self, parent):
        """Create admin dashboard"""
        # Admin specific features
        cards = [
            ("Manage Users", "#3498db", "👥", self.manage_users),
            ("View Sales", "#2ecc71", "📊", self.view_sales),
            ("Inventory", "#e67e22", "📦", self.manage_inventory),
            ("Staff Management", "#9b59b6", "👨‍💼", self.manage_staff),
            ("Bakery Settings", "#34495e", "⚙️", self.bakery_settings),
            ("Reports", "#1abc9c", "📈", self.view_reports)
        ]
        
        self.create_dashboard_cards(parent, cards)
    
    def create_staff_dashboard(self, parent):
        """Create staff dashboard"""
        cards = [
            ("Take Orders", "#3498db", "🛒", self.take_orders),
            ("View Orders", "#2ecc71", "📋", self.view_orders),
            ("Baking Schedule", "#e67e22", "⏰", self.baking_schedule),
            ("Inventory Check", "#9b59b6", "🔍", self.check_inventory),
            ("Customer Service", "#1abc9c", "💬", self.customer_service)
        ]
        
        self.create_dashboard_cards(parent, cards)
    
    def create_customer_dashboard(self, parent):
        """Create customer dashboard"""
        cards = [
            ("Browse Menu", "#3498db", "🍰", self.browse_menu),
            ("Place Order", "#2ecc71", "🛍️", self.place_order),
            ("Order History", "#e67e22", "📖", self.order_history),
            ("Special Offers", "#9b59b6", "🎁", self.special_offers),
            ("Contact Us", "#1abc9c", "📞", self.contact_us)
        ]
        
        self.create_dashboard_cards(parent, cards)
    
    def create_dashboard_cards(self, parent, cards):
        """Create dashboard cards"""
        # Create a grid of cards
        row, col = 0, 0
        max_cols = 3
        
        for title, color, icon, command in cards:
            card_frame = tk.Frame(
                parent,
                bg=color,
                relief='raised',
                bd=2,
                width=200,
                height=150
            )
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            card_frame.pack_propagate(False)
            
            # Make the card clickable
            card_frame.bind('<Button-1>', lambda e, cmd=command: cmd())
            
            # Icon
            icon_label = tk.Label(
                card_frame,
                text=icon,
                font=('Arial', 24),
                bg=color,
                fg='white'
            )
            icon_label.pack(pady=(20, 5))
            
            # Title
            title_label = tk.Label(
                card_frame,
                text=title,
                font=('Arial', 12, 'bold'),
                bg=color,
                fg='white',
                wraplength=180
            )
            title_label.pack(pady=5)
            
            # Click hint
            hint_label = tk.Label(
                card_frame,
                text="Click to open",
                font=('Arial', 8),
                bg=color,
                fg='white'
            )
            hint_label.pack(pady=(0, 10))
            
            # Update grid position
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Configure grid weights
        for i in range(max_cols):
            parent.columnconfigure(i, weight=1)
        for i in range(row + 1):
            parent.rowconfigure(i, weight=1)
    
    def logout(self):
        """Logout and return to login screen"""
        self.current_user = None
        # Clear window and show login again
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("FreshBake Login System")
        self.root.geometry("400x500")
        self.create_login_window()
    
    # Placeholder methods for dashboard features
    def manage_users(self): messagebox.showinfo("Manage Users", "User management system would open here.")
    def view_sales(self): messagebox.showinfo("View Sales", "Sales dashboard would open here.")
    def manage_inventory(self): messagebox.showinfo("Inventory", "Inventory management system would open here.")
    def manage_staff(self): messagebox.showinfo("Staff Management", "Staff management system would open here.")
    def bakery_settings(self): messagebox.showinfo("Settings", "Bakery settings would open here.")
    def view_reports(self): messagebox.showinfo("Reports", "Reports and analytics would open here.")
    def take_orders(self): messagebox.showinfo("Take Orders", "Order taking interface would open here.")
    def view_orders(self): messagebox.showinfo("View Orders", "Order management system would open here.")
    def baking_schedule(self): messagebox.showinfo("Baking Schedule", "Baking schedule would open here.")
    def check_inventory(self): messagebox.showinfo("Inventory Check", "Inventory checking system would open here.")
    def customer_service(self): messagebox.showinfo("Customer Service", "Customer service interface would open here.")
    def browse_menu(self): messagebox.showinfo("Browse Menu", "Bakery menu would open here.")
    def place_order(self): messagebox.showinfo("Place Order", "Order placement system would open here.")
    def order_history(self): messagebox.showinfo("Order History", "Order history would open here.")
    def special_offers(self): messagebox.showinfo("Special Offers", "Current offers would open here.")
    def contact_us(self): messagebox.showinfo("Contact Us", "Contact information would open here.")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    print("Starting FreshBake Bakery Login System...")
    print("Default Login Credentials:")
    print("Admin: admin / admin123")
    print("Staff: staff1 / staff123") 
    print("Customer: customer1 / customer123")
    
    app = BakeryLoginSystem()
    app.run()