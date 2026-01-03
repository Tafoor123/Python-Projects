import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import threading

class SimpleImageCompressor:
    def __init__(self, root):
        self.root = root
        self.root.title("📦 Smart Image Compressor")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2C3E50')
        
        # Initialize variables
        self.original_image = None
        self.compressed_image = None
        self.image_path = None
        self.original_size = 0
        self.compressed_size = 0
        self.quality = 85
        
        # Colors
        self.colors = {
            'primary': '#3498DB',
            'secondary': '#2ECC71', 
            'accent': '#E74C3C',
            'background': '#2C3E50',
            'card_bg': '#34495E',
            'text_light': '#ECF0F1'
        }
        
        self.setup_gui()
        
    def setup_gui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="📦 SMART IMAGE COMPRESSOR",
            font=('Arial', 20, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['primary'],
            pady=10
        )
        title_label.pack(fill='x')
        
        # Subtitle
        subtitle_label = tk.Label(
            main_frame,
            text="Reduce image size without compromising quality",
            font=('Arial', 12),
            bg=self.colors['background'],
            fg=self.colors['text_light'],
            pady=5
        )
        subtitle_label.pack(fill='x')
        
        # Create two columns
        container = tk.Frame(main_frame, bg=self.colors['background'])
        container.pack(fill='both', expand=True, pady=10)
        
        # Left column - Controls
        left_frame = tk.Frame(container, bg=self.colors['card_bg'], width=350)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # Right column - Preview
        right_frame = tk.Frame(container, bg=self.colors['background'])
        right_frame.pack(side='right', fill='both', expand=True)
        
        # === LEFT COLUMN CONTROLS ===
        
        # File selection
        file_frame = tk.LabelFrame(
            left_frame,
            text=" 📁 SELECT IMAGE ",
            font=('Arial', 11, 'bold'),
            bg=self.colors['card_bg'],
            fg=self.colors['text_light'],
            pady=10
        )
        file_frame.pack(fill='x', pady=5)
        
        self.select_btn = tk.Button(
            file_frame,
            text="📂 CHOOSE IMAGE FILE",
            font=('Arial', 12, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            command=self.open_image,
            pady=10,
            cursor='hand2'
        )
        self.select_btn.pack(fill='x', padx=10, pady=5)
        
        self.file_label = tk.Label(
            file_frame,
            text="No file selected",
            font=('Arial', 9),
            bg=self.colors['card_bg'],
            fg=self.colors['text_light'],
            wraplength=300
        )
        self.file_label.pack(fill='x', padx=10, pady=5)
        
        # Compression settings
        settings_frame = tk.LabelFrame(
            left_frame,
            text=" ⚙️ COMPRESSION SETTINGS ",
            font=('Arial', 11, 'bold'),
            bg=self.colors['card_bg'],
            fg=self.colors['text_light'],
            pady=10
        )
        settings_frame.pack(fill='x', pady=5)
        
        # Quality setting
        tk.Label(
            settings_frame,
            text="JPEG Quality:",
            font=('Arial', 10, 'bold'),
            bg=self.colors['card_bg'],
            fg=self.colors['text_light']
        ).pack(anchor='w', padx=10, pady=(5, 0))
        
        self.quality_scale = tk.Scale(
            settings_frame,
            from_=10,
            to=95,
            orient='horizontal',
            command=self.on_quality_change,
            bg=self.colors['card_bg'],
            fg=self.colors['text_light'],
            troughcolor='#2C3E50',
            length=300
        )
        self.quality_scale.set(self.quality)
        self.quality_scale.pack(fill='x', padx=10, pady=5)
        
        self.quality_label = tk.Label(
            settings_frame,
            text=f"Quality: {self.quality}%",
            font=('Arial', 9),
            bg=self.colors['card_bg'],
            fg=self.colors['secondary']
        )
        self.quality_label.pack(anchor='w', padx=10)
        
        # Format selection
        tk.Label(
            settings_frame,
            text="Output Format:",
            font=('Arial', 10, 'bold'),
            bg=self.colors['card_bg'],
            fg=self.colors['text_light']
        ).pack(anchor='w', padx=10, pady=(10, 5))
        
        self.format_var = tk.StringVar(value="JPEG")
        tk.Radiobutton(
            settings_frame,
            text="JPEG (Recommended for photos)",
            variable=self.format_var,
            value="JPEG",
            bg=self.colors['card_bg'],
            fg=self.colors['text_light'],
            selectcolor=self.colors['primary']
        ).pack(anchor='w', padx=20)
        
        tk.Radiobutton(
            settings_frame,
            text="PNG (Best for graphics)",
            variable=self.format_var,
            value="PNG", 
            bg=self.colors['card_bg'],
            fg=self.colors['text_light'],
            selectcolor=self.colors['primary']
        ).pack(anchor='w', padx=20)
        
        # === ACTION BUTTONS - THESE ARE THE IMPORTANT ONES ===
        action_frame = tk.LabelFrame(
            left_frame,
            text=" 🎯 ACTIONS ",
            font=('Arial', 11, 'bold'),
            bg=self.colors['card_bg'],
            fg=self.colors['text_light'],
            pady=15
        )
        action_frame.pack(fill='x', pady=10)
        
        # COMPRESS BUTTON
        self.compress_btn = tk.Button(
            action_frame,
            text="🔄 COMPRESS IMAGE",
            font=('Arial', 13, 'bold'),
            bg=self.colors['secondary'],
            fg='white',
            command=self.compress_image,
            pady=15,
            cursor='hand2',
            state='disabled'
        )
        self.compress_btn.pack(fill='x', padx=20, pady=10)
        
        # SAVE BUTTON  
        self.save_btn = tk.Button(
            action_frame,
            text="💾 SAVE COMPRESSED IMAGE",
            font=('Arial', 13, 'bold'),
            bg='#FF9800',
            fg='white',
            command=self.save_compressed,
            pady=15,
            cursor='hand2',
            state='disabled'
        )
        self.save_btn.pack(fill='x', padx=20, pady=10)
        
        # Results display
        results_frame = tk.LabelFrame(
            left_frame,
            text=" 📊 RESULTS ",
            font=('Arial', 11, 'bold'),
            bg=self.colors['card_bg'],
            fg=self.colors['text_light'],
            pady=10
        )
        results_frame.pack(fill='x', pady=5)
        
        self.results_text = tk.Text(
            results_frame,
            height=8,
            font=('Arial', 10),
            bg='#2C3E50',
            fg=self.colors['text_light'],
            wrap='word'
        )
        self.results_text.pack(fill='both', padx=10, pady=10, expand=True)
        self.results_text.config(state='disabled')
        
        # === RIGHT COLUMN PREVIEW ===
        
        # Original image
        original_frame = tk.LabelFrame(
            right_frame,
            text=" 📷 ORIGINAL IMAGE ",
            font=('Arial', 11, 'bold'),
            bg=self.colors['card_bg'],
            fg=self.colors['text_light']
        )
        original_frame.pack(fill='both', expand=True, pady=5)
        
        self.original_canvas = tk.Canvas(
            original_frame,
            bg='#2C3E50',
            highlightthickness=0
        )
        self.original_canvas.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.original_info = tk.Label(
            original_frame,
            text="No image loaded",
            font=('Arial', 10),
            bg=self.colors['card_bg'],
            fg=self.colors['text_light']
        )
        self.original_info.pack(fill='x', padx=10, pady=5)
        
        # Compressed image
        compressed_frame = tk.LabelFrame(
            right_frame,
            text=" 🎯 COMPRESSED IMAGE ",
            font=('Arial', 11, 'bold'),
            bg=self.colors['card_bg'],
            fg=self.colors['text_light']
        )
        compressed_frame.pack(fill='both', expand=True, pady=5)
        
        self.compressed_canvas = tk.Canvas(
            compressed_frame,
            bg='#2C3E50',
            highlightthickness=0
        )
        self.compressed_canvas.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.compressed_info = tk.Label(
            compressed_frame,
            text="No compression performed", 
            font=('Arial', 10),
            bg=self.colors['card_bg'],
            fg=self.colors['text_light']
        )
        self.compressed_info.pack(fill='x', padx=10, pady=5)
        
        # Status bar
        self.status_label = tk.Label(
            main_frame,
            text="🔄 Ready! Select an image file to begin compression.",
            font=('Arial', 10),
            bg=self.colors['primary'],
            fg='white',
            pady=8
        )
        self.status_label.pack(fill='x', side='bottom', pady=(10, 0))
        
    def open_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image to Compress",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.image_path = file_path
            self.file_label.config(text=os.path.basename(file_path))
            self.load_original_image()
            self.compress_btn.config(state='normal', bg=self.colors['secondary'])
            self.update_status("✅ Image loaded! Click 'COMPRESS IMAGE' to proceed.")
            
    def load_original_image(self):
        try:
            self.original_image = Image.open(self.image_path)
            self.original_size = os.path.getsize(self.image_path)
            
            # Display original image
            self.display_image(self.original_image, self.original_canvas)
            
            # Update info
            size_kb = self.original_size / 1024
            info_text = f"Size: {size_kb:.1f} KB | Dimensions: {self.original_image.width} x {self.original_image.height}"
            self.original_info.config(text=info_text)
            
            self.update_results()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {str(e)}")
            
    def display_image(self, image, canvas):
        canvas.update_idletasks()
        canvas_width = canvas.winfo_width() or 400
        canvas_height = canvas.winfo_height() or 300
        
        # Calculate display size
        img_ratio = image.width / image.height
        canvas_ratio = canvas_width / canvas_height
        
        if img_ratio > canvas_ratio:
            new_width = canvas_width - 40
            new_height = int((canvas_width - 40) / img_ratio)
        else:
            new_height = canvas_height - 40
            new_width = int((canvas_height - 40) * img_ratio)
            
        new_width = max(new_width, 50)
        new_height = max(new_height, 50)
        
        # Resize and display
        display_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.display_photo = ImageTk.PhotoImage(display_image)
        
        canvas.delete("all")
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        canvas.create_image(x, y, anchor='nw', image=self.display_photo)
        
    def on_quality_change(self, value):
        self.quality = int(value)
        self.quality_label.config(text=f"Quality: {self.quality}%")
        
    def compress_image(self):
        if not self.original_image:
            return
            
        try:
            self.update_status("🔄 Compressing image... Please wait.")
            self.compress_btn.config(state='disabled', text="COMPRESSING...", bg='gray')
            
            # Start in thread
            thread = threading.Thread(target=self.perform_compression)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Compression failed: {str(e)}")
            self.compress_btn.config(state='normal', text="🔄 COMPRESS IMAGE", bg=self.colors['secondary'])
            
    def perform_compression(self):
        try:
            compressed_img = self.original_image.copy()
            
            # Convert to RGB if JPEG
            if self.format_var.get() == "JPEG" and compressed_img.mode in ("RGBA", "P"):
                compressed_img = compressed_img.convert("RGB")
            
            # Save to temp file to get size
            temp_path = "temp_compressed.jpg"
            
            if self.format_var.get() == "JPEG":
                compressed_img.save(temp_path, "JPEG", quality=self.quality, optimize=True)
            else:
                compressed_img.save(temp_path, "PNG", optimize=True)
                
            self.compressed_size = os.path.getsize(temp_path)
            self.compressed_image = compressed_img
            
            self.root.after(0, self.update_after_compression)
            
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
        except Exception as e:
            self.root.after(0, lambda: self.compression_failed(str(e)))
            
    def update_after_compression(self):
        # Display compressed image
        self.display_image(self.compressed_image, self.compressed_canvas)
        
        # Update info
        size_kb = self.compressed_size / 1024
        info_text = f"Size: {size_kb:.1f} KB | Dimensions: {self.compressed_image.width} x {self.compressed_image.height}"
        self.compressed_info.config(text=info_text)
        
        # Enable save button
        self.save_btn.config(state='normal', bg='#FF9800')
        self.compress_btn.config(state='normal', text="🔄 COMPRESS IMAGE", bg=self.colors['secondary'])
        
        self.update_results()
        self.update_status("✅ Compression complete! Click 'SAVE COMPRESSED IMAGE' to save.")
        
    def compression_failed(self, error):
        self.compress_btn.config(state='normal', text="🔄 COMPRESS IMAGE", bg=self.colors['secondary'])
        messagebox.showerror("Error", f"Compression failed: {error}")
        
    def update_results(self):
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        
        if self.original_size > 0:
            original_kb = self.original_size / 1024
            compression_ratio = (1 - self.compressed_size / self.original_size) * 100 if self.compressed_size > 0 else 0
            
            results = "📊 COMPRESSION RESULTS:\n"
            results += "=" * 25 + "\n\n"
            results += f"Original Size: {original_kb:.1f} KB\n"
            
            if self.compressed_size > 0:
                compressed_kb = self.compressed_size / 1024
                results += f"Compressed Size: {compressed_kb:.1f} KB\n"
                results += f"Size Reduction: {compression_ratio:.1f}%\n"
                results += f"Space Saved: {original_kb - compressed_kb:.1f} KB\n\n"
                
                if compression_ratio > 50:
                    results += "🎉 Excellent compression!"
                elif compression_ratio > 25:
                    results += "👍 Good compression!"
                else:
                    results += "💡 Moderate compression"
                    
            self.results_text.insert(1.0, results)
            
        self.results_text.config(state='disabled')
        
    def save_compressed(self):
        if not self.compressed_image:
            return
            
        # Determine file extension
        ext = ".jpg" if self.format_var.get() == "JPEG" else ".png"
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=ext,
            filetypes=[
                ("JPEG files", "*.jpg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ],
            title="Save Compressed Image"
        )
        
        if file_path:
            try:
                if self.format_var.get() == "JPEG":
                    self.compressed_image.save(file_path, "JPEG", quality=self.quality, optimize=True)
                else:
                    self.compressed_image.save(file_path, "PNG", optimize=True)
                    
                saved_size = os.path.getsize(file_path)
                saved_kb = saved_size / 1024
                
                self.update_status(f"✅ Image saved! Size: {saved_kb:.1f} KB")
                messagebox.showinfo("Success", f"Image saved successfully!\n\nFile: {os.path.basename(file_path)}\nSize: {saved_kb:.1f} KB")
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not save image: {str(e)}")
                
    def update_status(self, message):
        self.status_label.config(text=message)
        
    def run(self):
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleImageCompressor(root)
    app.run()