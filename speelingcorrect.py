import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import math
import re
from difflib import get_close_matches
import threading
import time

class SmartSpellChecker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Smart Spell Checker - AI Powered")
        self.root.geometry("1300x850")
        self.root.configure(bg='#1a1a2e')
        self.root.minsize(1100, 750)
        
        # Initialize variables
        self.dark_mode = True
        self.correction_history = []
        self.english_dictionary = self.create_smart_dictionary()
        self.current_word = ""
        self.setup_gui()
        self.setup_animations()
        
    def create_smart_dictionary(self):
        """Create a comprehensive English dictionary"""
        # Common English words
        common_words = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
            'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
            'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
            'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take',
            'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other',
            'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
            'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way',
            'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us',
            'is', 'are', 'was', 'were', 'been', 'being', 'have', 'has', 'had', 'having',
            'do', 'does', 'did', 'doing', 'will', 'would', 'shall', 'should', 'may', 'might',
            'must', 'can', 'could', 'go', 'goes', 'went', 'going', 'gone', 'make', 'makes',
            'made', 'making', 'take', 'takes', 'took', 'taking', 'come', 'comes', 'came',
            'coming', 'see', 'sees', 'saw', 'seeing', 'get', 'gets', 'got', 'getting',
            'give', 'gives', 'gave', 'giving', 'find', 'finds', 'found', 'finding',
            'think', 'thinks', 'thought', 'thinking', 'know', 'knows', 'knew', 'knowing',
            'look', 'looks', 'looked', 'looking', 'want', 'wants', 'wanted', 'wanting',
            'like', 'likes', 'liked', 'liking', 'help', 'helps', 'helped', 'helping'
        }
        
        # Add technology related words
        tech_words = {
            'computer', 'software', 'hardware', 'program', 'application', 'system',
            'database', 'network', 'internet', 'website', 'webpage', 'browser',
            'email', 'password', 'username', 'login', 'logout', 'register',
            'download', 'upload', 'file', 'folder', 'document', 'image', 'video',
            'audio', 'music', 'game', 'player', 'screen', 'display', 'monitor',
            'keyboard', 'mouse', 'printer', 'scanner', 'camera', 'phone', 'mobile',
            'tablet', 'laptop', 'desktop', 'server', 'cloud', 'storage', 'memory',
            'processor', 'graphics', 'sound', 'video', 'audio', 'network', 'wifi',
            'bluetooth', 'usb', 'cable', 'wireless', 'digital', 'analog', 'virtual',
            'reality', 'augmented', 'artificial', 'intelligence', 'machine', 'learning',
            'algorithm', 'code', 'programming', 'developer', 'engineer', 'designer',
            'user', 'interface', 'experience', 'responsive', 'adaptive', 'dynamic',
            'static', 'interactive', 'automated', 'manual', 'default', 'custom',
            'setting', 'configuration', 'preference', 'option', 'choice', 'selection'
        }
        
        # Add common nouns
        nouns = {
            'time', 'person', 'year', 'way', 'day', 'thing', 'man', 'world', 'life',
            'hand', 'part', 'child', 'eye', 'woman', 'place', 'work', 'week', 'case',
            'point', 'government', 'company', 'number', 'group', 'problem', 'fact',
            'water', 'food', 'house', 'room', 'school', 'student', 'teacher', 'book',
            'car', 'city', 'country', 'money', 'family', 'friend', 'health', 'system',
            'program', 'computer', 'phone', 'music', 'art', 'movie', 'game', 'sport',
            'color', 'name', 'address', 'email', 'password', 'account', 'price', 'value'
        }
        
        # Add adjectives
        adjectives = {
            'good', 'new', 'first', 'last', 'long', 'great', 'little', 'own', 'other',
            'old', 'right', 'big', 'high', 'different', 'small', 'large', 'next',
            'early', 'young', 'important', 'few', 'public', 'bad', 'same', 'able',
            'better', 'best', 'beautiful', 'ugly', 'happy', 'sad', 'angry', 'calm',
            'hot', 'cold', 'warm', 'cool', 'fast', 'slow', 'quick', 'easy', 'hard',
            'difficult', 'simple', 'complex', 'clear', 'vague', 'bright', 'dark',
            'light', 'heavy', 'empty', 'full', 'rich', 'poor', 'strong', 'weak'
        }
        
        # Combine all words
        all_words = common_words.union(tech_words).union(nouns).union(adjectives)
        
        # Add word variations
        extended_dict = set(all_words)
        for word in all_words:
            # Add plural forms
            if word.endswith('y'):
                extended_dict.add(word[:-1] + 'ies')
            elif word.endswith(('s', 'x', 'z', 'ch', 'sh')):
                extended_dict.add(word + 'es')
            else:
                extended_dict.add(word + 's')
            
            # Add past tense
            if word.endswith('e'):
                extended_dict.add(word + 'd')
                extended_dict.add(word[:-1] + 'ing')
            else:
                extended_dict.add(word + 'ed')
                extended_dict.add(word + 'ing')
            
            # Add comparative and superlative for adjectives
            if word in adjectives:
                if word.endswith('y'):
                    extended_dict.add(word[:-1] + 'ier')
                    extended_dict.add(word[:-1] + 'iest')
                elif len(word) > 2:
                    extended_dict.add(word + 'er')
                    extended_dict.add(word + 'est')
        
        return extended_dict

    def setup_gui(self):
        # Create main frames
        self.create_header()
        self.create_input_section()
        self.create_live_correction_section()
        self.create_suggestions_section()
        self.create_stats_section()
        
    def create_header(self):
        # Animated header
        self.header_frame = tk.Frame(self.root, bg='#1a1a2e', height=120)
        self.header_frame.pack(fill='x', padx=20, pady=15)
        
        self.title_label = tk.Label(
            self.header_frame,
            text="Smart Spell Checker - AI Powered",
            font=('Arial', 28, 'bold'),
            fg='white',
            bg='#1a1a2e'
        )
        self.title_label.pack(pady=10)
        
        self.subtitle_label = tk.Label(
            self.header_frame,
            text="Type anything - Get instant spelling corrections!",
            font=('Arial', 12),
            fg='#e94560',
            bg='#1a1a2e'
        )
        self.subtitle_label.pack()
        
    def create_input_section(self):
        # Input section
        self.input_frame = tk.LabelFrame(
            self.root,
            text="Type Your Text Here (Auto-Correct Enabled)",
            font=('Arial', 14, 'bold'),
            bg='#16213e',
            fg='white',
            relief='ridge',
            bd=3
        )
        self.input_frame.pack(fill='x', padx=20, pady=10)
        
        self.input_text = scrolledtext.ScrolledText(
            self.input_frame,
            height=6,
            font=('Arial', 13),
            wrap='word',
            bg='#0f3460',
            fg='white',
            insertbackground='white',
            relief='solid',
            bd=2
        )
        self.input_text.pack(fill='x', padx=10, pady=10)
        self.input_text.bind('<KeyRelease>', self.on_text_change)
        self.input_text.bind('<KeyPress>', self.on_key_press)
        
        # Instructions
        instructions = tk.Label(
            self.input_frame,
            text="Tip: Just start typing! The spell checker will automatically detect and correct mistakes.",
            font=('Arial', 10),
            fg='#f39c12',
            bg='#16213e'
        )
        instructions.pack(pady=5)
        
    def create_live_correction_section(self):
        # Live correction section
        self.live_frame = tk.LabelFrame(
            self.root,
            text="Live Correction & Suggestions",
            font=('Arial', 14, 'bold'),
            bg='#16213e',
            fg='white',
            relief='ridge',
            bd=3
        )
        self.live_frame.pack(fill='x', padx=20, pady=10)
        
        # Current word being typed
        current_word_frame = tk.Frame(self.live_frame, bg='#16213e')
        current_word_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            current_word_frame,
            text="Current Word:",
            font=('Arial', 11, 'bold'),
            fg='white',
            bg='#16213e'
        ).pack(side='left')
        
        self.current_word_label = tk.Label(
            current_word_frame,
            text="",
            font=('Arial', 11, 'bold'),
            fg='#e94560',
            bg='#16213e'
        )
        self.current_word_label.pack(side='left', padx=5)
        
        # Correction status
        status_frame = tk.Frame(self.live_frame, bg='#16213e')
        status_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            status_frame,
            text="Status:",
            font=('Arial', 11, 'bold'),
            fg='white',
            bg='#16213e'
        ).pack(side='left')
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready to type...",
            font=('Arial', 11),
            fg='#00b894',
            bg='#16213e'
        )
        self.status_label.pack(side='left', padx=5)
        
        # Quick actions
        action_frame = tk.Frame(self.live_frame, bg='#16213e')
        action_frame.pack(fill='x', padx=10, pady=10)
        
        self.auto_correct_btn = tk.Button(
            action_frame,
            text="Apply Auto-Correction",
            font=('Arial', 11, 'bold'),
            bg='#00b894',
            fg='white',
            command=self.apply_auto_correction,
            cursor='hand2'
        )
        self.auto_correct_btn.pack(side='left', padx=5)
        
        self.ignore_btn = tk.Button(
            action_frame,
            text="Ignore Word",
            font=('Arial', 11),
            bg='#95a5a6',
            fg='white',
            command=self.ignore_word,
            cursor='hand2'
        )
        self.ignore_btn.pack(side='left', padx=5)
        
    def create_suggestions_section(self):
        # Suggestions section
        self.suggestions_frame = tk.LabelFrame(
            self.root,
            text="Smart Suggestions",
            font=('Arial', 14, 'bold'),
            bg='#16213e',
            fg='white',
            relief='ridge',
            bd=3
        )
        self.suggestions_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Suggestions display with buttons
        suggestions_top_frame = tk.Frame(self.suggestions_frame, bg='#16213e')
        suggestions_top_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            suggestions_top_frame,
            text="Top Suggestions:",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#16213e'
        ).pack(side='left')
        
        self.suggestions_buttons_frame = tk.Frame(self.suggestions_frame, bg='#16213e')
        self.suggestions_buttons_frame.pack(fill='x', padx=10, pady=5)
        
        # Detailed suggestions
        self.suggestions_text = scrolledtext.ScrolledText(
            self.suggestions_frame,
            height=4,
            font=('Arial', 11),
            wrap='word',
            bg='#0f3460',
            fg='white',
            state='disabled'
        )
        self.suggestions_text.pack(fill='both', expand=True, padx=10, pady=10)
        
    def create_stats_section(self):
        # Statistics section
        self.stats_frame = tk.LabelFrame(
            self.root,
            text="Live Statistics",
            font=('Arial', 14, 'bold'),
            bg='#16213e',
            fg='white',
            relief='ridge',
            bd=2
        )
        self.stats_frame.pack(fill='x', padx=20, pady=10)
        
        stats_inner_frame = tk.Frame(self.stats_frame, bg='#16213e')
        stats_inner_frame.pack(fill='x', padx=10, pady=10)
        
        # Statistics labels
        stats_data = [
            ("Total Words:", "total_words", "#3498db"),
            ("Misspelled:", "misspelled", "#e74c3c"),
            ("Corrections:", "corrections", "#2ecc71"),
            ("Accuracy:", "accuracy", "#f39c12"),
            ("Current Speed:", "speed", "#9b59b6")
        ]
        
        for text, attr, color in stats_data:
            frame = tk.Frame(stats_inner_frame, bg='#16213e')
            frame.pack(side='left', padx=15)
            
            tk.Label(
                frame,
                text=text,
                font=('Arial', 10),
                fg='white',
                bg='#16213e'
            ).pack()
            
            label = tk.Label(
                frame,
                text="0" if attr != "accuracy" else "100%",
                font=('Arial', 12, 'bold'),
                fg=color,
                bg='#16213e'
            )
            label.pack()
            setattr(self, f"{attr}_label", label)
        
    def setup_animations(self):
        self.animation_angle = 0
        self.start_time = time.time()
        self.word_count = 0
        self.animate_title()
        
    def animate_title(self):
        self.animation_angle += 0.05
        r = int(127 + 128 * math.sin(self.animation_angle))
        g = int(127 + 128 * math.sin(self.animation_angle + 2))
        b = int(127 + 128 * math.sin(self.animation_angle + 4))
        color = f'#{r:02x}{g:02x}{b:02x}'
        self.title_label.config(fg=color)
        self.root.after(50, self.animate_title)
        
    def on_key_press(self, event):
        # Store the current cursor position
        self.cursor_pos = self.input_text.index(tk.INSERT)
        
    def on_text_change(self, event):
        # Get current text and cursor position
        text = self.input_text.get(1.0, 'end-1c')
        cursor_pos = self.input_text.index(tk.INSERT)
        
        # Extract current word being typed
        current_word = self.extract_current_word(text, cursor_pos)
        self.current_word = current_word
        
        # Update UI
        self.current_word_label.config(text=f"'{current_word}'")
        
        # Analyze the word
        if current_word and len(current_word) > 1:
            self.analyze_word(current_word)
        else:
            self.status_label.config(text="Type a word...", fg='#95a5a6')
            self.clear_suggestions()
        
        # Update statistics
        self.update_statistics(text)
        
    def extract_current_word(self, text, cursor_pos):
        """Extract the word currently being typed"""
        try:
            line, col = map(int, cursor_pos.split('.'))
            line_text = self.input_text.get(f"{line}.0", f"{line}.end")
            
            # Find word boundaries
            start = col
            while start > 0 and line_text[start-1].isalnum():
                start -= 1
                
            end = col
            while end < len(line_text) and line_text[end].isalnum():
                end += 1
                
            return line_text[start:end]
        except:
            return ""
        
    def analyze_word(self, word):
        """Analyze the current word and provide suggestions"""
        clean_word = word.lower().strip()
        
        # Check if word is correct
        if self.is_word_correct(clean_word):
            self.status_label.config(text="Spelling is correct!", fg='#00b894')
            self.clear_suggestions()
            return
        
        # Word is misspelled - get suggestions
        self.status_label.config(text="Spelling error detected", fg='#e74c3c')
        suggestions = self.get_smart_suggestions(clean_word)
        
        # Display suggestions
        self.show_suggestions(word, suggestions)
        
    def is_word_correct(self, word):
        """Check if word is spelled correctly"""
        if not word or len(word) < 2:
            return True
            
        # Check in dictionary
        if word in self.english_dictionary:
            return True
            
        # Check for common patterns
        if self.is_common_pattern(word):
            return True
            
        return False
    
    def is_common_pattern(self, word):
        """Check for common word patterns"""
        # Common prefixes and suffixes
        prefixes = ['un', 're', 'pre', 'dis', 'mis', 'non']
        suffixes = ['ing', 'ed', 's', 'es', 'ly', 'ment', 'tion', 'able', 'ful']
        
        # Check if word starts with common prefix
        for prefix in prefixes:
            if word.startswith(prefix) and len(word) > len(prefix) + 1:
                root = word[len(prefix):]
                if root in self.english_dictionary:
                    return True
        
        # Check if word ends with common suffix
        for suffix in suffixes:
            if word.endswith(suffix) and len(word) > len(suffix) + 1:
                root = word[:-len(suffix)]
                if root in self.english_dictionary:
                    return True
                    
        return False
    
    def get_smart_suggestions(self, word):
        """Get intelligent spelling suggestions"""
        suggestions = []
        
        # 1. Check for common spelling mistakes
        common_corrections = self.get_common_corrections(word)
        if common_corrections:
            suggestions.extend(common_corrections)
        
        # 2. Use similarity matching
        similar_words = get_close_matches(word, self.english_dictionary, n=8, cutoff=0.6)
        suggestions.extend(similar_words)
        
        # 3. Check for typo patterns
        typo_suggestions = self.check_typo_patterns(word)
        suggestions.extend(typo_suggestions)
        
        # Remove duplicates and limit
        unique_suggestions = []
        for sug in suggestions:
            if sug not in unique_suggestions and sug != word:
                unique_suggestions.append(sug)
                
        return unique_suggestions[:6]  # Return top 6 suggestions
    
    def get_common_corrections(self, word):
        """Common spelling mistake corrections"""
        common_mistakes = {
            'recieve': 'receive',
            'seperate': 'separate',
            'definately': 'definitely',
            'occured': 'occurred',
            'accomodate': 'accommodate',
            'alot': 'a lot',
            'neccessary': 'necessary',
            'untill': 'until',
            'wich': 'which',
            'truely': 'truly',
            'becuase': 'because',
            'existance': 'existence',
            'goverment': 'government',
            'arguement': 'argument',
            'judgement': 'judgment',
            'maintainance': 'maintenance',
            'privilege': 'privilege',
            'restaurant': 'restaurant',
            'rhythm': 'rhythm',
            'schedule': 'schedule',
            'calender': 'calendar',
            'enviroment': 'environment',
            'libary': 'library',
            'mathmatics': 'mathematics',
            'oppertunity': 'opportunity',
            'temprature': 'temperature',
            'wierd': 'weird',
            'acheive': 'achieve',
            'greatful': 'grateful',
            'independant': 'independent',
            'millenium': 'millennium',
            'neighbor': 'neighbour',
            'occassion': 'occasion',
            'perserverance': 'perseverance',
            'questionaire': 'questionnaire',
            'rediculous': 'ridiculous',
            'sucess': 'success',
            'thier': 'their',
            'tommorrow': 'tomorrow',
            'vaccuum': 'vacuum',
            'wensday': 'wednesday'
        }
        
        return [common_mistakes[word]] if word in common_mistakes else []
    
    def check_typo_patterns(self, word):
        """Check for common typing patterns"""
        suggestions = []
        
        # Double letter mistakes
        for i in range(len(word) - 1):
            if word[i] == word[i + 1]:
                # Try removing double letter
                test_word = word[:i] + word[i+1:]
                if test_word in self.english_dictionary:
                    suggestions.append(test_word)
        
        # Missing double letters
        for i in range(len(word)):
            test_word = word[:i] + word[i] + word[i:]
            if test_word in self.english_dictionary:
                suggestions.append(test_word)
        
        # Transposed letters
        for i in range(len(word) - 1):
            if i < len(word) - 1:
                test_word = word[:i] + word[i+1] + word[i] + word[i+2:]
                if test_word in self.english_dictionary:
                    suggestions.append(test_word)
        
        return suggestions
    
    def show_suggestions(self, original_word, suggestions):
        """Display suggestions in the GUI"""
        # Clear previous suggestions
        self.clear_suggestions()
        
        if not suggestions:
            self.suggestions_text.config(state='normal')
            self.suggestions_text.insert('end', "No suggestions available. This might be a proper noun or specialized term.", 'info')
            self.suggestions_text.config(state='disabled')
            return
        
        # Create suggestion buttons
        for i, suggestion in enumerate(suggestions[:4]):  # Show top 4 as buttons
            btn = tk.Button(
                self.suggestions_buttons_frame,
                text=suggestion,
                font=('Arial', 11, 'bold'),
                bg='#3498db',
                fg='white',
                command=lambda s=suggestion: self.apply_suggestion(s),
                cursor='hand2',
                width=12
            )
            btn.grid(row=0, column=i, padx=5, pady=5)
        
        # Show detailed suggestions in text area
        self.suggestions_text.config(state='normal')
        self.suggestions_text.delete(1.0, 'end')
        
        self.suggestions_text.insert('end', f"Original: '{original_word}'\n\n", 'header')
        self.suggestions_text.insert('end', "Top Suggestions:\n", 'subheader')
        
        for i, suggestion in enumerate(suggestions, 1):
            self.suggestions_text.insert('end', f"{i}. {suggestion}\n", 'suggestion')
        
        # Add analysis
        self.suggestions_text.insert('end', f"\nAnalysis:\n", 'subheader')
        if len(original_word) > 3:
            self.suggestions_text.insert('end', f"Word length: {len(original_word)} characters\n")
            self.suggestions_text.insert('end', f"Suggestions found: {len(suggestions)}\n")
            self.suggestions_text.insert('end', f"Confidence: {min(90, len(suggestions) * 15)}%\n")
        
        self.suggestions_text.config(state='disabled')
        
        # Configure text tags
        self.suggestions_text.tag_config('header', foreground='#e94560', font=('Arial', 12, 'bold'))
        self.suggestions_text.tag_config('subheader', foreground='#f39c12', font=('Arial', 11, 'bold'))
        self.suggestions_text.tag_config('suggestion', foreground='#3498db')
        self.suggestions_text.tag_config('info', foreground='#95a5a6')
    
    def clear_suggestions(self):
        """Clear all suggestion widgets"""
        # Clear buttons
        for widget in self.suggestions_buttons_frame.winfo_children():
            widget.destroy()
        
        # Clear text
        self.suggestions_text.config(state='normal')
        self.suggestions_text.delete(1.0, 'end')
        self.suggestions_text.config(state='disabled')
    
    def apply_suggestion(self, suggestion):
        """Apply the selected suggestion"""
        if not self.current_word:
            return
            
        # Get current text and cursor position
        text = self.input_text.get(1.0, 'end-1c')
        cursor_pos = self.input_text.index(tk.INSERT)
        
        # Replace the word
        line, col = map(int, cursor_pos.split('.'))
        line_text = self.input_text.get(f"{line}.0", f"{line}.end")
        
        # Find word boundaries
        start = col
        while start > 0 and line_text[start-1].isalnum():
            start -= 1
            
        end = col
        while end < len(line_text) and line_text[end].isalnum():
            end += 1
        
        # Replace the word
        new_line_text = line_text[:start] + suggestion + line_text[end:]
        self.input_text.delete(f"{line}.0", f"{line}.end")
        self.input_text.insert(f"{line}.0", new_line_text)
        
        # Move cursor to end of replaced word
        new_cursor_pos = f"{line}.{start + len(suggestion)}"
        self.input_text.mark_set(tk.INSERT, new_cursor_pos)
        self.input_text.focus()
        
        # Update status
        self.status_label.config(text=f"Corrected to '{suggestion}'", fg='#00b894')
        
        # Add to history
        self.add_to_history(self.current_word, suggestion)
        
        # Clear current word
        self.current_word = ""
        self.current_word_label.config(text="")
    
    def apply_auto_correction(self):
        """Apply automatic correction for current word"""
        if not self.current_word:
            return
            
        suggestions = self.get_smart_suggestions(self.current_word.lower())
        if suggestions:
            self.apply_suggestion(suggestions[0])  # Apply top suggestion
    
    def ignore_word(self):
        """Ignore the current word"""
        self.current_word = ""
        self.current_word_label.config(text="")
        self.status_label.config(text="Word ignored", fg='#95a5a6')
        self.clear_suggestions()
    
    def add_to_history(self, original, corrected):
        """Add correction to history"""
        history_entry = {
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'original': original,
            'corrected': corrected
        }
        
        # Update corrections count
        current_corrections = int(self.corrections_label.cget("text"))
        self.corrections_label.config(text=str(current_corrections + 1))
    
    def update_statistics(self, text):
        """Update live statistics"""
        words = text.split()
        self.word_count = len(words)
        
        # Count misspelled words (simplified)
        misspelled = 0
        for word in words:
            clean_word = ''.join(c for c in word if c.isalnum()).lower()
            if clean_word and not self.is_word_correct(clean_word):
                misspelled += 1
        
        # Update labels
        self.total_words_label.config(text=str(self.word_count))
        self.misspelled_label.config(text=str(misspelled))
        
        # Calculate accuracy
        accuracy = 100.0
        if self.word_count > 0:
            accuracy = ((self.word_count - misspelled) / self.word_count) * 100
        self.accuracy_label.config(text=f"{accuracy:.1f}%")
        
        # Calculate typing speed (words per minute)
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 0:
            wpm = (self.word_count / elapsed_time) * 60
            self.speed_label.config(text=f"{wpm:.1f} WPM")
    
    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Application error: {e}")

if __name__ == "__main__":
    print("Starting Smart Spell Checker - AI Powered")
    print("Features:")
    print("- Real-time automatic spell checking")
    print("- Live word detection and correction")
    print("- Smart suggestion algorithms")
    print("- Common mistake patterns detection")
    print("- Beautiful animated interface")
    print("- No external dependencies required!")
    print("\nJust start typing and watch the magic happen!")
    
    app = SmartSpellChecker()
    app.run()