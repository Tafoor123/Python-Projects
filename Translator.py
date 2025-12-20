import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from googletrans import Translator, LANGUAGES
import threading
import time
import math
import random
from datetime import datetime

class AdvancedTranslator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Language Translator Pro")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')
        self.root.minsize(1000, 700)
        
        # Initialize translator
        self.translator = Translator()
        self.translation_history = []
        
        self.setup_gui()
        self.setup_animations()
        
    def setup_gui(self):
        # Create main frames
        self.create_header()
        self.create_input_section()
        self.create_control_section()
        self.create_output_section()
        self.create_history_section()
        
    def create_header(self):
        # Animated header
        self.header_frame = tk.Frame(self.root, bg='#1a1a2e', height=120)
        self.header_frame.pack(fill='x', padx=20, pady=15)
        
        self.title_label = tk.Label(
            self.header_frame,
            text="Universal Language Translator Pro",
            font=('Arial', 28, 'bold'),
            fg='white',
            bg='#1a1a2e'
        )
        self.title_label.pack(pady=10)
        
        self.subtitle_label = tk.Label(
            self.header_frame,
            text="Translate any language with unlimited characters!",
            font=('Arial', 12),
            fg='#e94560',
            bg='#1a1a2e'
        )
        self.subtitle_label.pack()
        
    def create_input_section(self):
        # Input section with animation
        self.input_frame = tk.LabelFrame(
            self.root,
            text="Input Text",
            font=('Arial', 14, 'bold'),
            bg='#16213e',
            fg='white',
            relief='ridge',
            bd=3
        )
        self.input_frame.pack(fill='x', padx=20, pady=10)
        
        self.input_text = scrolledtext.ScrolledText(
            self.input_frame,
            height=8,
            font=('Arial', 12),
            wrap='word',
            bg='#0f3460',
            fg='white',
            insertbackground='white',
            relief='solid',
            bd=2
        )
        self.input_text.pack(fill='x', padx=10, pady=10)
        self.input_text.bind('<KeyRelease>', self.update_character_count)
        
        # Character count
        self.count_frame = tk.Frame(self.input_frame, bg='#16213e')
        self.count_frame.pack(fill='x', padx=10, pady=5)
        
        self.count_label = tk.Label(
            self.count_frame,
            text="Characters: 0 | Words: 0",
            font=('Arial', 10, 'bold'),
            fg='#f39c12',
            bg='#16213e'
        )
        self.count_label.pack(side='left')
        
    def create_control_section(self):
        # Control section
        self.control_frame = tk.Frame(self.root, bg='#1a1a2e')
        self.control_frame.pack(fill='x', padx=20, pady=15)
        
        # Language selection
        self.create_language_controls()
        
        # Buttons
        self.create_buttons()
        
    def create_language_controls(self):
        lang_frame = tk.Frame(self.control_frame, bg='#1a1a2e')
        lang_frame.pack(fill='x', pady=10)
        
        # Source language
        tk.Label(
            lang_frame,
            text="From Language:",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#1a1a2e'
        ).grid(row=0, column=0, sticky='w', padx=(0, 20))
        
        self.src_lang = ttk.Combobox(
            lang_frame,
            values=['Auto Detect'] + list(LANGUAGES.values()),
            state='readonly',
            width=25,
            font=('Arial', 11)
        )
        self.src_lang.set('Auto Detect')
        self.src_lang.grid(row=0, column=1, padx=(0, 40))
        
        # Target language
        tk.Label(
            lang_frame,
            text="To Language:",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#1a1a2e'
        ).grid(row=0, column=2, sticky='w', padx=(0, 20))
        
        self.dest_lang = ttk.Combobox(
            lang_frame,
            values=list(LANGUAGES.values()),
            state='readonly',
            width=25,
            font=('Arial', 11)
        )
        self.dest_lang.set('english')
        self.dest_lang.grid(row=0, column=3)
        
        # Swap languages button
        self.swap_btn = tk.Button(
            lang_frame,
            text="Swap Languages",
            font=('Arial', 10),
            bg='#e94560',
            fg='white',
            command=self.swap_languages,
            cursor='hand2'
        )
        self.swap_btn.grid(row=0, column=4, padx=(20, 0))
        
    def create_buttons(self):
        btn_frame = tk.Frame(self.control_frame, bg='#1a1a2e')
        btn_frame.pack(fill='x', pady=10)
        
        # Translate button with animation
        self.translate_btn = tk.Button(
            btn_frame,
            text="Start Translation",
            font=('Arial', 14, 'bold'),
            bg='#e94560',
            fg='white',
            relief='raised',
            bd=4,
            command=self.start_translation,
            cursor='hand2',
            width=20,
            height=2
        )
        self.translate_btn.pack(side='left', padx=(0, 15))
        
        # Clear button
        self.clear_btn = tk.Button(
            btn_frame,
            text="Clear All",
            font=('Arial', 12),
            bg='#533483',
            fg='white',
            command=self.clear_all,
            cursor='hand2'
        )
        self.clear_btn.pack(side='left', padx=(0, 15))
        
        # Copy button
        self.copy_btn = tk.Button(
            btn_frame,
            text="Copy Translation",
            font=('Arial', 12),
            bg='#00b894',
            fg='white',
            command=self.copy_translation,
            cursor='hand2'
        )
        self.copy_btn.pack(side='left')
        
    def create_output_section(self):
        # Output section
        self.output_frame = tk.LabelFrame(
            self.root,
            text="Translated Text",
            font=('Arial', 14, 'bold'),
            bg='#16213e',
            fg='white',
            relief='ridge',
            bd=3
        )
        self.output_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.output_text = scrolledtext.ScrolledText(
            self.output_frame,
            height=8,
            font=('Arial', 12),
            wrap='word',
            bg='#0f3460',
            fg='white',
            state='disabled',
            relief='solid',
            bd=2
        )
        self.output_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Progress animation
        self.progress_frame = tk.Frame(self.output_frame, bg='#16213e')
        self.progress_frame.pack(fill='x', padx=10, pady=5)
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="Ready to translate...",
            font=('Arial', 11, 'bold'),
            fg='#00b894',
            bg='#16213e'
        )
        self.progress_label.pack(side='left')
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='indeterminate',
            length=200
        )
        self.progress_bar.pack(side='right')
        
    def create_history_section(self):
        # Translation history
        self.history_frame = tk.LabelFrame(
            self.root,
            text="Translation History",
            font=('Arial', 12, 'bold'),
            bg='#16213e',
            fg='white',
            relief='ridge',
            bd=2
        )
        self.history_frame.pack(fill='x', padx=20, pady=10)
        
        self.history_text = scrolledtext.ScrolledText(
            self.history_frame,
            height=4,
            font=('Arial', 10),
            wrap='word',
            bg='#0f3460',
            fg='white',
            state='disabled'
        )
        self.history_text.pack(fill='x', padx=10, pady=10)
        
    def setup_animations(self):
        # Animation variables
        self.title_angle = 0
        self.pulse_alpha = 1.0
        self.pulse_dir = -0.03
        self.floating_pos = 0
        self.particles = []
        
        # Start animations
        self.animate_title()
        self.animate_pulse()
        self.animate_floating()
        self.create_particles()
        
    def animate_title(self):
        self.title_angle += 0.08
        # Rainbow color effect
        r = int(127 + 128 * math.sin(self.title_angle))
        g = int(127 + 128 * math.sin(self.title_angle + 2))
        b = int(127 + 128 * math.sin(self.title_angle + 4))
        color = f'#{r:02x}{g:02x}{b:02x}'
        
        self.title_label.config(fg=color)
        self.root.after(50, self.animate_title)
        
    def animate_pulse(self):
        self.pulse_alpha += self.pulse_dir
        if self.pulse_alpha <= 0.4 or self.pulse_alpha >= 1.0:
            self.pulse_dir *= -1
            
        # Create pulse effect for translate button
        color = f"#e94560"
        self.translate_btn.config(bg=color)
        self.root.after(80, self.animate_pulse)
        
    def animate_floating(self):
        self.floating_pos += 0.1
        offset = math.sin(self.floating_pos) * 3
        # Use pack instead of place for subtitle
        self.root.after(100, self.animate_floating)
        
    def create_particles(self):
        # Create floating particles in background
        if len(self.particles) < 10:
            particle = tk.Label(
                self.root,
                text="*",
                font=('Arial', 8),
                fg=random.choice(['#e94560', '#533483', '#00b894', '#f39c12']),
                bg='#1a1a2e'
            )
            x = random.randint(0, 1200)
            y = random.randint(0, 800)
            particle.place(x=x, y=y)
            self.particles.append((particle, x, y))
            
        # Move particles
        for i, (particle, x, y) in enumerate(self.particles):
            y += random.randint(1, 3)
            if y > 800:
                y = 0
                x = random.randint(0, 1200)
            particle.place(x=x, y=y)
            self.particles[i] = (particle, x, y)
            
        self.root.after(100, self.create_particles)
        
    def update_character_count(self, event=None):
        text = self.input_text.get(1.0, 'end-1c')
        char_count = len(text)
        word_count = len(text.split())
        self.count_label.config(text=f"Characters: {char_count} | Words: {word_count}")
        
    def swap_languages(self):
        current_src = self.src_lang.get()
        current_dest = self.dest_lang.get()
        
        if current_src != 'Auto Detect':
            self.src_lang.set(current_dest)
            self.dest_lang.set(current_src)
        
    def start_translation(self):
        text = self.input_text.get(1.0, 'end-1c').strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to translate!")
            return
            
        if not self.dest_lang.get():
            messagebox.showwarning("Warning", "Please select target language!")
            return
            
        # Disable button and show progress
        self.translate_btn.config(state='disabled', text="Translating...")
        self.progress_bar.start()
        self.progress_label.config(text="Translating your text...", fg='#f39c12')
        
        # Start translation in separate thread
        thread = threading.Thread(target=self.translate_text, args=(text,))
        thread.daemon = True
        thread.start()
        
    def translate_text(self, text):
        try:
            src_lang_key = 'auto'
            if self.src_lang.get() != 'Auto Detect':
                src_lang_key = [k for k, v in LANGUAGES.items() if v == self.src_lang.get()][0]
                
            dest_lang_key = [k for k, v in LANGUAGES.items() if v == self.dest_lang.get()][0]
            
            # Handle large text by splitting
            if len(text) > 5000:
                chunks = self.split_text(text, 4000)
                translated_chunks = []
                
                for i, chunk in enumerate(chunks):
                    self.root.after(0, self.update_progress, f"Translating chunk {i+1}/{len(chunks)}")
                    translated = self.translator.translate(chunk, src=src_lang_key, dest=dest_lang_key)
                    translated_chunks.append(translated.text)
                    
                translated_text = ' '.join(translated_chunks)
            else:
                translated = self.translator.translate(text, src=src_lang_key, dest=dest_lang_key)
                translated_text = translated.text
                
            # Add to history
            history_entry = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'source': text[:50] + "..." if len(text) > 50 else text,
                'translation': translated_text[:50] + "..." if len(translated_text) > 50 else translated_text,
                'languages': f"{self.src_lang.get()} -> {self.dest_lang.get()}"
            }
            self.translation_history.append(history_entry)
            
            # Update UI in main thread
            self.root.after(0, self.show_translation, translated_text)
            
        except Exception as e:
            self.root.after(0, self.show_error, str(e))
            
    def split_text(self, text, chunk_size):
        """Split text into chunks for large translations"""
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < chunk_size:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence + ". "
                
        if current_chunk:
            chunks.append(current_chunk)
            
        return chunks
        
    def update_progress(self, message):
        self.progress_label.config(text=message)
        
    def show_translation(self, translated_text):
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, 'end')
        self.output_text.insert(1.0, translated_text)
        self.output_text.config(state='disabled')
        
        # Update history
        self.update_history_display()
        
        # Re-enable button and stop progress
        self.translate_btn.config(state='normal', text="Start Translation")
        self.progress_bar.stop()
        self.progress_label.config(text="Translation Complete!", fg='#00b894')
        
    def update_history_display(self):
        self.history_text.config(state='normal')
        self.history_text.delete(1.0, 'end')
        
        for entry in self.translation_history[-5:]:  # Show last 5 entries
            self.history_text.insert('end', 
                                   f"Time: {entry['timestamp']} | {entry['languages']}\n"
                                   f"From: {entry['source']}\n"
                                   f"To: {entry['translation']}\n"
                                   f"{'-'*50}\n")
        
        self.history_text.config(state='disabled')
        
    def show_error(self, error_msg):
        messagebox.showerror("Translation Error", 
                           f"An error occurred during translation:\n\n{error_msg}\n\n"
                           f"Please check your internet connection and try again.")
        self.translate_btn.config(state='normal', text="Start Translation")
        self.progress_bar.stop()
        self.progress_label.config(text="Translation Failed", fg='#e94560')
        
    def copy_translation(self):
        try:
            self.output_text.config(state='normal')
            text = self.output_text.get(1.0, 'end-1c')
            self.output_text.config(state='disabled')
            
            if text.strip():
                self.root.clipboard_clear()
                self.root.clipboard_append(text)
                messagebox.showinfo("Success", "Translation copied to clipboard!")
            else:
                messagebox.showwarning("Warning", "No translation to copy!")
        except:
            messagebox.showerror("Error", "Failed to copy translation!")
            
    def clear_all(self):
        self.input_text.delete(1.0, 'end')
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, 'end')
        self.output_text.config(state='disabled')
        self.count_label.config(text="Characters: 0 | Words: 0")
        self.progress_label.config(text="Ready to translate...", fg='#00b894')
        
    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Application error: {e}")

# Run the application
if __name__ == "__main__":
    print("Starting Advanced Language Translator Pro...")
    print("Features:")
    print("   - Unlimited character translation")
    print("   - Beautiful animations")
    print("   - Translation history")
    print("   - Language swapping")
    print("   - Copy to clipboard")
    print("   - Real-time character count")
    
    app = AdvancedTranslator()
    app.run()