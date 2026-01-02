import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import psutil
import platform
import socket
import time
from datetime import datetime
import requests
import json
import os
import subprocess
import webbrowser
import math
import random

class AllInOneSystemTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ultimate System Tool Pro")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a2e')
        self.root.minsize(1200, 800)
        
        # Initialize variables
        self.dark_mode = True
        self.weather_api_key = "your_api_key_here"
        self.stopwatch_running = False
        self.stopwatch_elapsed = 0
        self.stopwatch_start = 0
        
        self.setup_gui()
        self.setup_animations()
        self.start_updates()
        
    def setup_gui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_system_info_tab()
        self.create_battery_tab()
        self.create_control_tab()
        self.create_weather_tab()
        self.create_clock_calendar_tab()
        self.create_ludo_tab()
        self.create_screenshot_tab()
        self.create_quick_access_tab()
        
        # Mode switch button
        self.mode_btn = tk.Button(
            self.root,
            text="Dark Mode",
            font=('Arial', 12, 'bold'),
            bg='#e94560',
            fg='white',
            command=self.toggle_mode,
            cursor='hand2'
        )
        self.mode_btn.pack(side='bottom', pady=10)
        
    def create_system_info_tab(self):
        # System Info Tab
        self.system_frame = tk.Frame(self.notebook, bg='#16213e')
        self.notebook.add(self.system_frame, text="System Info")
        
        # Title
        title_label = tk.Label(
            self.system_frame,
            text="System Configuration",
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#16213e'
        )
        title_label.pack(pady=10)
        
        # System info display
        self.system_info_text = scrolledtext.ScrolledText(
            self.system_frame,
            height=15,
            font=('Arial', 11),
            wrap='word',
            bg='#0f3460',
            fg='white',
            state='disabled'
        )
        self.system_info_text.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(
            self.system_frame,
            text="Refresh System Info",
            font=('Arial', 12, 'bold'),
            bg='#00b894',
            fg='white',
            command=self.update_system_info,
            cursor='hand2'
        )
        refresh_btn.pack(pady=10)
        
    def create_battery_tab(self):
        # Battery Tab
        self.battery_frame = tk.Frame(self.notebook, bg='#16213e')
        self.notebook.add(self.battery_frame, text="Battery")
        
        # Battery info
        self.battery_canvas = tk.Canvas(
            self.battery_frame,
            width=300,
            height=200,
            bg='#16213e',
            highlightthickness=0
        )
        self.battery_canvas.pack(pady=20)
        
        self.battery_percent_label = tk.Label(
            self.battery_frame,
            text="Loading...",
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='#16213e'
        )
        self.battery_percent_label.pack()
        
        self.battery_status_label = tk.Label(
            self.battery_frame,
            text="",
            font=('Arial', 14),
            fg='#f39c12',
            bg='#16213e'
        )
        self.battery_status_label.pack()
        
        self.time_remaining_label = tk.Label(
            self.battery_frame,
            text="",
            font=('Arial', 12),
            fg='#bdc3c7',
            bg='#16213e'
        )
        self.time_remaining_label.pack()
        
    def create_control_tab(self):
        # Control Tab
        self.control_frame = tk.Frame(self.notebook, bg='#16213e')
        self.notebook.add(self.control_frame, text="Controls")
        
        # Brightness Control
        brightness_frame = tk.LabelFrame(
            self.control_frame,
            text="Brightness Control",
            font=('Arial', 14, 'bold'),
            bg='#16213e',
            fg='white'
        )
        brightness_frame.pack(fill='x', padx=20, pady=10)
        
        self.brightness_label = tk.Label(
            brightness_frame,
            text="Brightness: 50%",
            font=('Arial', 12),
            fg='white',
            bg='#16213e'
        )
        self.brightness_label.pack(pady=5)
        
        self.brightness_scale = tk.Scale(
            brightness_frame,
            from_=0,
            to=100,
            orient='horizontal',
            length=400,
            command=self.change_brightness,
            bg='#0f3460',
            fg='white',
            highlightbackground='#16213e'
        )
        self.brightness_scale.set(50)
        self.brightness_scale.pack(pady=10)
        
        # Volume Control
        volume_frame = tk.LabelFrame(
            self.control_frame,
            text="Volume Control",
            font=('Arial', 14, 'bold'),
            bg='#16213e',
            fg='white'
        )
        volume_frame.pack(fill='x', padx=20, pady=10)
        
        self.volume_label = tk.Label(
            volume_frame,
            text="Volume: 50%",
            font=('Arial', 12),
            fg='white',
            bg='#16213e'
        )
        self.volume_label.pack(pady=5)
        
        self.volume_scale = tk.Scale(
            volume_frame,
            from_=0,
            to=100,
            orient='horizontal',
            length=400,
            command=self.change_volume,
            bg='#0f3460',
            fg='white',
            highlightbackground='#16213e'
        )
        self.volume_scale.set(50)
        self.volume_scale.pack(pady=10)
        
    def create_weather_tab(self):
        # Weather Tab
        self.weather_frame = tk.Frame(self.notebook, bg='#16213e')
        self.notebook.add(self.weather_frame, text="Weather")
        
        # Location input
        input_frame = tk.Frame(self.weather_frame, bg='#16213e')
        input_frame.pack(pady=20)
        
        tk.Label(
            input_frame,
            text="Enter City:",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#16213e'
        ).pack(side='left', padx=5)
        
        self.city_entry = tk.Entry(
            input_frame,
            font=('Arial', 12),
            width=20
        )
        self.city_entry.pack(side='left', padx=5)
        
        search_btn = tk.Button(
            input_frame,
            text="Search",
            font=('Arial', 12),
            bg='#e94560',
            fg='white',
            command=self.get_weather,
            cursor='hand2'
        )
        search_btn.pack(side='left', padx=5)
        
        # Weather display
        self.weather_display = tk.Text(
            self.weather_frame,
            height=10,
            font=('Arial', 12),
            wrap='word',
            bg='#0f3460',
            fg='white',
            state='disabled'
        )
        self.weather_display.pack(fill='both', expand=True, padx=20, pady=10)
        
    def create_clock_calendar_tab(self):
        # Clock & Calendar Tab
        self.clock_frame = tk.Frame(self.notebook, bg='#16213e')
        self.notebook.add(self.clock_frame, text="Clock & Calendar")
        
        # Digital Clock
        self.clock_label = tk.Label(
            self.clock_frame,
            text="",
            font=('Arial', 48, 'bold'),
            fg='#e94560',
            bg='#16213e'
        )
        self.clock_label.pack(pady=20)
        
        # Calendar
        self.calendar_label = tk.Label(
            self.clock_frame,
            text="",
            font=('Arial', 18),
            fg='white',
            bg='#16213e'
        )
        self.calendar_label.pack(pady=10)
        
        # Stopwatch
        stopwatch_frame = tk.LabelFrame(
            self.clock_frame,
            text="Stopwatch",
            font=('Arial', 14, 'bold'),
            bg='#16213e',
            fg='white'
        )
        stopwatch_frame.pack(pady=20)
        
        self.stopwatch_label = tk.Label(
            stopwatch_frame,
            text="00:00:00",
            font=('Arial', 24, 'bold'),
            fg='#00b894',
            bg='#16213e'
        )
        self.stopwatch_label.pack(pady=10)
        
        btn_frame = tk.Frame(stopwatch_frame, bg='#16213e')
        btn_frame.pack(pady=10)
        
        self.start_btn = tk.Button(
            btn_frame,
            text="Start",
            font=('Arial', 12),
            bg='#00b894',
            fg='white',
            command=self.start_stopwatch,
            cursor='hand2'
        )
        self.start_btn.pack(side='left', padx=5)
        
        self.stop_btn = tk.Button(
            btn_frame,
            text="Stop",
            font=('Arial', 12),
            bg='#e94560',
            fg='white',
            command=self.stop_stopwatch,
            cursor='hand2'
        )
        self.stop_btn.pack(side='left', padx=5)
        
        self.reset_btn = tk.Button(
            btn_frame,
            text="Reset",
            font=('Arial', 12),
            bg='#f39c12',
            fg='white',
            command=self.reset_stopwatch,
            cursor='hand2'
        )
        self.reset_btn.pack(side='left', padx=5)
        
    def create_ludo_tab(self):
        # Ludo Game Tab
        self.ludo_frame = tk.Frame(self.notebook, bg='#16213e')
        self.notebook.add(self.ludo_frame, text="Ludo Game")
        
        # Ludo board will be implemented here
        ludo_title = tk.Label(
            self.ludo_frame,
            text="Ludo Game - Coming Soon!",
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='#16213e'
        )
        ludo_title.pack(pady=50)
        
        # Simple dice roller for now
        dice_frame = tk.Frame(self.ludo_frame, bg='#16213e')
        dice_frame.pack(pady=20)
        
        self.dice_label = tk.Label(
            dice_frame,
            text="Dice: 0",
            font=('Arial', 24),
            bg='#16213e',
            fg='white'
        )
        self.dice_label.pack()
        
        roll_btn = tk.Button(
            dice_frame,
            text="Roll Dice",
            font=('Arial', 14, 'bold'),
            bg='#e94560',
            fg='white',
            command=self.roll_dice,
            cursor='hand2'
        )
        roll_btn.pack(pady=10)
        
    def create_screenshot_tab(self):
        # Screenshot Tab
        self.screenshot_frame = tk.Frame(self.notebook, bg='#16213e')
        self.notebook.add(self.screenshot_frame, text="Screenshot")
        
        screenshot_btn = tk.Button(
            self.screenshot_frame,
            text="Take Screenshot",
            font=('Arial', 16, 'bold'),
            bg='#e94560',
            fg='white',
            command=self.take_screenshot,
            cursor='hand2',
            height=3,
            width=20
        )
        screenshot_btn.pack(pady=50)
        
        self.screenshot_status = tk.Label(
            self.screenshot_frame,
            text="",
            font=('Arial', 12),
            fg='#00b894',
            bg='#16213e'
        )
        self.screenshot_status.pack()
        
    def create_quick_access_tab(self):
        # Quick Access Tab
        self.quick_frame = tk.Frame(self.notebook, bg='#16213e')
        self.notebook.add(self.quick_frame, text="Quick Access")
        
        # File Explorer
        explorer_btn = tk.Button(
            self.quick_frame,
            text="Open File Explorer",
            font=('Arial', 14),
            bg='#00b894',
            fg='white',
            command=self.open_explorer,
            cursor='hand2',
            width=20
        )
        explorer_btn.pack(pady=10)
        
        # Google
        google_btn = tk.Button(
            self.quick_frame,
            text="Open Google",
            font=('Arial', 14),
            bg='#4285f4',
            fg='white',
            command=self.open_google,
            cursor='hand2',
            width=20
        )
        google_btn.pack(pady=10)
        
        # Close All Apps
        close_btn = tk.Button(
            self.quick_frame,
            text="Close All Apps",
            font=('Arial', 14, 'bold'),
            bg='#e94560',
            fg='white',
            command=self.close_all_apps,
            cursor='hand2',
            width=20
        )
        close_btn.pack(pady=20)
        
        # Custom URL
        url_frame = tk.Frame(self.quick_frame, bg='#16213e')
        url_frame.pack(pady=20)
        
        tk.Label(
            url_frame,
            text="Open URL:",
            font=('Arial', 12),
            fg='white',
            bg='#16213e'
        ).pack(side='left', padx=5)
        
        self.url_entry = tk.Entry(
            url_frame,
            font=('Arial', 12),
            width=30
        )
        self.url_entry.pack(side='left', padx=5)
        
        url_open_btn = tk.Button(
            url_frame,
            text="Open",
            font=('Arial', 12),
            bg='#533483',
            fg='white',
            command=self.open_url,
            cursor='hand2'
        )
        url_open_btn.pack(side='left', padx=5)
        
    def setup_animations(self):
        # Animation variables
        self.animation_angle = 0
        self.pulse_alpha = 1.0
        self.pulse_dir = -0.03
        
        # Start animations
        self.animate_title()
        
    def animate_title(self):
        self.animation_angle += 0.05
        # Rainbow color effect for title
        r = int(127 + 128 * math.sin(self.animation_angle))
        g = int(127 + 128 * math.sin(self.animation_angle + 2))
        b = int(127 + 128 * math.sin(self.animation_angle + 4))
        color = f'#{r:02x}{g:02x}{b:02x}'
        
        # Update any animated elements here
        self.root.after(100, self.animate_title)
        
    def start_updates(self):
        self.update_system_info()
        self.update_battery_info()
        self.update_clock()
        self.update_stopwatch()
        
    def update_system_info(self):
        try:
            # Get system information
            system_info = f"""
{'='*50}
SYSTEM INFORMATION
{'='*50}

Computer Name: {socket.gethostname()}
Operating System: {platform.system()} {platform.release()}
Processor: {platform.processor()}
Architecture: {platform.architecture()[0]}

RAM: {round(psutil.virtual_memory().total / (1024**3), 2)} GB
Available RAM: {round(psutil.virtual_memory().available / (1024**3), 2)} GB
RAM Usage: {psutil.virtual_memory().percent}%

CPU Cores: {psutil.cpu_count()}
CPU Usage: {psutil.cpu_percent()}%

Disk Usage: {psutil.disk_usage('/').percent}%
Boot Time: {datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}

Network IP: {socket.gethostbyname(socket.gethostname())}
{'='*50}
            """
            
            self.system_info_text.config(state='normal')
            self.system_info_text.delete(1.0, 'end')
            self.system_info_text.insert(1.0, system_info)
            self.system_info_text.config(state='disabled')
            
        except Exception as e:
            self.system_info_text.config(state='normal')
            self.system_info_text.delete(1.0, 'end')
            self.system_info_text.insert(1.0, f"Error getting system info: {e}")
            self.system_info_text.config(state='disabled')
            
    def update_battery_info(self):
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                plugged = battery.power_plugged
                time_left = battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unknown"
                
                # Update battery display
                self.battery_percent_label.config(text=f"{percent}%")
                
                status = "Charging" if plugged else "Discharging"
                self.battery_status_label.config(text=status)
                
                if time_left != "Unknown":
                    hours = time_left // 3600
                    minutes = (time_left % 3600) // 60
                    self.time_remaining_label.config(text=f"Time remaining: {hours}h {minutes}m")
                else:
                    self.time_remaining_label.config(text="Time remaining: Calculating...")
                    
                # Update battery visual
                self.draw_battery(percent, plugged)
                
        except Exception as e:
            self.battery_percent_label.config(text="Error")
            self.battery_status_label.config(text=str(e))
            
        self.root.after(5000, self.update_battery_info)  # Update every 5 seconds
        
    def draw_battery(self, percent, plugged):
        self.battery_canvas.delete("all")
        
        # Battery outline
        self.battery_canvas.create_rectangle(50, 50, 250, 150, outline='white', width=3)
        self.battery_canvas.create_rectangle(240, 70, 250, 130, outline='white', width=3)
        
        # Battery level
        fill_width = 190 * (percent / 100)
        color = '#00b894' if percent > 50 else '#f39c12' if percent > 20 else '#e94560'
        self.battery_canvas.create_rectangle(55, 55, 55 + fill_width, 145, fill=color, outline='')
        
        # Plug indicator
        if plugged:
            self.battery_canvas.create_text(150, 170, text="Plugged", font=('Arial', 12), fill='white')
            
    def change_brightness(self, value):
        try:
            # For Windows, you can use this command
            # set_brightness(int(value))
            self.brightness_label.config(text=f"Brightness: {value}%")
        except Exception as e:
            messagebox.showerror("Error", f"Could not change brightness: {e}")
            
    def change_volume(self, value):
        try:
            # This is a simplified volume control
            # You might need platform-specific implementations
            self.volume_label.config(text=f"Volume: {value}%")
        except Exception as e:
            messagebox.showerror("Error", f"Could not change volume: {e}")
            
    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name!")
            return
            
        try:
            # This is a placeholder - you need a real weather API
            weather_info = f"""
Weather information for: {city}

Temperature: 25°C
Condition: Sunny
Humidity: 65%
Wind Speed: 15 km/h

Note: Replace with actual weather API implementation
Add your API key at line 23 in the code
            """
            
            self.weather_display.config(state='normal')
            self.weather_display.delete(1.0, 'end')
            self.weather_display.insert(1.0, weather_info)
            self.weather_display.config(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not get weather: {e}")
            
    def update_clock(self):
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%A, %B %d, %Y")
        
        self.clock_label.config(text=time_str)
        self.calendar_label.config(text=date_str)
        
        self.root.after(1000, self.update_clock)
        
    def start_stopwatch(self):
        self.stopwatch_running = True
        self.stopwatch_start = time.time() - self.stopwatch_elapsed
        
    def stop_stopwatch(self):
        self.stopwatch_running = False
        self.stopwatch_elapsed = time.time() - self.stopwatch_start
        
    def reset_stopwatch(self):
        self.stopwatch_running = False
        self.stopwatch_elapsed = 0
        self.stopwatch_label.config(text="00:00:00")
        
    def update_stopwatch(self):
        if self.stopwatch_running:
            elapsed = time.time() - self.stopwatch_start
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            self.stopwatch_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            
        self.root.after(100, self.update_stopwatch)
        
    def roll_dice(self):
        roll = random.randint(1, 6)
        self.dice_label.config(text=f"Dice: {roll}")
        
    def take_screenshot(self):
        try:
            # For screenshot functionality, you need to install:
            # pip install pillow
            from PIL import ImageGrab
            screenshot = ImageGrab.grab()
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            screenshot.save(filename)
            self.screenshot_status.config(text=f"Screenshot saved as {filename}")
        except ImportError:
            messagebox.showerror("Error", "Please install Pillow: pip install pillow")
        except Exception as e:
            messagebox.showerror("Error", f"Could not take screenshot: {e}")
            
    def open_explorer(self):
        try:
            if platform.system() == "Windows":
                os.startfile(".")
            else:
                subprocess.Popen(["xdg-open", "."])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file explorer: {e}")
            
    def open_google(self):
        try:
            webbrowser.open("https://www.google.com")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Google: {e}")
            
    def open_url(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL!")
            return
            
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        try:
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open URL: {e}")
            
    def close_all_apps(self):
        result = messagebox.askyesno(
            "Confirm", 
            "Are you sure you want to close all applications?\nThis will close all running programs."
        )
        if result:
            try:
                # This is a simplified implementation
                # Be very careful with this in production
                if platform.system() == "Windows":
                    os.system("taskkill /f /im *")
                else:
                    messagebox.showinfo("Info", "This feature works best on Windows")
            except Exception as e:
                messagebox.showerror("Error", f"Could not close applications: {e}")
                
    def toggle_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.set_dark_mode()
            self.mode_btn.config(text="Dark Mode")
        else:
            self.set_light_mode()
            self.mode_btn.config(text="Light Mode")
            
    def set_dark_mode(self):
        # Dark mode colors
        bg_color = '#1a1a2e'
        frame_bg = '#16213e'
        text_bg = '#0f3460'
        
        self.root.configure(bg=bg_color)
        # Update all frames to dark mode
        for frame in [self.system_frame, self.battery_frame, self.control_frame, 
                     self.weather_frame, self.clock_frame, self.ludo_frame,
                     self.screenshot_frame, self.quick_frame]:
            try:
                frame.configure(bg=frame_bg)
                # Update child widgets
                for widget in frame.winfo_children():
                    if isinstance(widget, (tk.Frame, tk.LabelFrame)):
                        widget.configure(bg=frame_bg)
                    elif isinstance(widget, tk.Label):
                        if widget['bg'] == frame_bg or widget['bg'] == text_bg:
                            widget.configure(bg=frame_bg)
            except:
                pass
        
    def set_light_mode(self):
        # Light mode colors
        bg_color = '#f0f0f0'
        frame_bg = '#ffffff'
        text_bg = '#e0e0e0'
        
        self.root.configure(bg=bg_color)
        # Update all frames to light mode
        for frame in [self.system_frame, self.battery_frame, self.control_frame, 
                     self.weather_frame, self.clock_frame, self.ludo_frame,
                     self.screenshot_frame, self.quick_frame]:
            try:
                frame.configure(bg=frame_bg)
                # Update child widgets
                for widget in frame.winfo_children():
                    if isinstance(widget, (tk.Frame, tk.LabelFrame)):
                        widget.configure(bg=frame_bg)
                    elif isinstance(widget, tk.Label):
                        if widget['bg'] in ['#16213e', '#0f3460']:
                            widget.configure(bg=frame_bg)
            except:
                pass
        
    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Application error: {e}")

# Required installations:
# pip install psutil

if __name__ == "__main__":
    print("Starting Ultimate System Tool Pro...")
    print("Features:")
    print("1. System Configuration")
    print("2. Battery Monitoring")
    print("3. Brightness & Volume Control")
    print("4. Weather Information")
    print("5. Clock & Calendar")
    print("6. Ludo Game")
    print("7. Screenshot Tool")
    print("8. Quick Access")
    print("9. Dark/Light Mode")
    print("10. Close All Apps")
    
    app = AllInOneSystemTool()
    app.run()