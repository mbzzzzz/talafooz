import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from transformers import MBart50TokenizerFast, MBartForConditionalGeneration
import torch
import threading
import pyperclip
from PIL import Image, ImageTk
import os

class TalafoozTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("Talafooz - English to Urdu Translator")
        self.root.geometry("800x600")
        self.root.configure(bg="#000000")
        
        # Initialize model variables
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
        
        # Configure style
        self.setup_styles()
        
        # Create UI
        self.create_widgets()
        
        # Load model in background
        self.load_model_async()
    
    def setup_styles(self):
        """Configure the tangerine and pitch black theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        self.bg_color = "#000000"  # Pitch black
        self.accent_color = "#FF6B35"  # Tangerine
        self.text_color = "#FFFFFF"  # White text
        self.input_bg = "#1a1a1a"  # Dark gray for input
        self.button_bg = "#FF6B35"  # Tangerine buttons
        
        # Configure styles
        style.configure('Title.TLabel', 
                       background=self.bg_color, 
                       foreground=self.accent_color,
                       font=('Arial', 24, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       background=self.bg_color,
                       foreground=self.text_color,
                       font=('Arial', 12))
        
        style.configure('Tangerine.TButton',
                       background=self.button_bg,
                       foreground='white',
                       font=('Arial', 10, 'bold'),
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Tangerine.TButton',
                 background=[('active', '#E55A2B')])
    
    def create_widgets(self):
        """Create the main UI widgets"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="Talafooz", style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, text="English to Urdu Translator", style='Subtitle.TLabel')
        subtitle_label.pack(pady=(0, 20))
        
        # Input section
        input_frame = tk.Frame(main_frame, bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        input_label = ttk.Label(input_frame, text="English Text:", style='Subtitle.TLabel')
        input_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.input_text = scrolledtext.ScrolledText(
            input_frame,
            height=8,
            bg=self.input_bg,
            fg=self.text_color,
            font=('Arial', 11),
            wrap=tk.WORD,
            insertbackground=self.text_color,
            selectbackground=self.accent_color
        )
        self.input_text.pack(fill=tk.X, pady=(0, 10))
        
        # Bind text change event
        self.input_text.bind('<KeyRelease>', self.on_text_change)
        
        # Button frame
        button_frame = tk.Frame(input_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X)
        
        self.translate_btn = ttk.Button(
            button_frame,
            text="Translate",
            style='Tangerine.TButton',
            command=self.translate_text,
            state='disabled'
        )
        self.translate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = ttk.Button(
            button_frame,
            text="Clear",
            style='Tangerine.TButton',
            command=self.clear_text
        )
        self.clear_btn.pack(side=tk.LEFT)
        
        # Output section
        output_frame = tk.Frame(main_frame, bg=self.bg_color)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        output_label = ttk.Label(output_frame, text="Urdu Translation:", style='Subtitle.TLabel')
        output_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=8,
            bg=self.input_bg,
            fg=self.text_color,
            font=('Arial', 11),
            wrap=tk.WORD,
            insertbackground=self.text_color,
            selectbackground=self.accent_color,
            state='disabled'
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Copy button
        self.copy_btn = ttk.Button(
            output_frame,
            text="Copy Translation",
            style='Tangerine.TButton',
            command=self.copy_translation,
            state='disabled'
        )
        self.copy_btn.pack(anchor=tk.E)
        
        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="Loading model...",
            style='Subtitle.TLabel'
        )
        self.status_label.pack(pady=(20, 0))
    
    def load_model_async(self):
        """Load the model in a separate thread to avoid blocking the UI"""
        def load_model():
            try:
                self.root.after(0, lambda: self.status_label.config(text="Loading translation model..."))
                model_name = "abdulwaheed1/english-to-urdu-translation-mbart"
                
                self.tokenizer = MBart50TokenizerFast.from_pretrained(
                    model_name, 
                    src_lang="en_XX", 
                    tgt_lang="ur_PK"
                )
                self.model = MBartForConditionalGeneration.from_pretrained(model_name)
                
                self.model_loaded = True
                self.root.after(0, self.on_model_loaded)
                
            except Exception as e:
                self.root.after(0, lambda: self.on_model_error(str(e)))
        
        thread = threading.Thread(target=load_model)
        thread.daemon = True
        thread.start()
    
    def on_model_loaded(self):
        """Called when model is successfully loaded"""
        self.status_label.config(text="Model loaded successfully! Ready to translate.")
        self.translate_btn.config(state='normal')
    
    def on_model_error(self, error_msg):
        """Called when model loading fails"""
        self.status_label.config(text=f"Error loading model: {error_msg}")
        messagebox.showerror("Error", f"Failed to load translation model:\n{error_msg}")
    
    def on_text_change(self, event):
        """Called when input text changes"""
        text = self.input_text.get("1.0", tk.END).strip()
        if text and self.model_loaded:
            self.translate_btn.config(state='normal')
        else:
            self.translate_btn.config(state='disabled')
    
    def translate_text(self):
        """Translate the input text to Urdu"""
        if not self.model_loaded:
            messagebox.showwarning("Warning", "Model is still loading. Please wait.")
            return
        
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            return
        
        def translate():
            try:
                self.root.after(0, lambda: self.status_label.config(text="Translating..."))
                
                # Tokenize input
                inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
                
                # Generate translation
                with torch.no_grad():
                    translated = self.model.generate(
                        **inputs,
                        max_length=512,
                        num_beams=4,
                        early_stopping=True
                    )
                
                # Decode translation
                translation = self.tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
                
                # Update UI
                self.root.after(0, lambda: self.update_translation(translation))
                
            except Exception as e:
                self.root.after(0, lambda: self.on_translation_error(str(e)))
        
        thread = threading.Thread(target=translate)
        thread.daemon = True
        thread.start()
    
    def update_translation(self, translation):
        """Update the output text with translation"""
        self.output_text.config(state='normal')
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", translation)
        self.output_text.config(state='disabled')
        self.copy_btn.config(state='normal')
        self.status_label.config(text="Translation completed!")
    
    def on_translation_error(self, error_msg):
        """Handle translation errors"""
        self.status_label.config(text="Translation failed!")
        messagebox.showerror("Translation Error", f"Failed to translate text:\n{error_msg}")
    
    def copy_translation(self):
        """Copy translation to clipboard"""
        translation = self.output_text.get("1.0", tk.END).strip()
        if translation:
            pyperclip.copy(translation)
            self.status_label.config(text="Translation copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No translation to copy!")
    
    def clear_text(self):
        """Clear both input and output text"""
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state='normal')
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state='disabled')
        self.copy_btn.config(state='disabled')
        self.translate_btn.config(state='disabled')
        self.status_label.config(text="Text cleared!")

def main():
    root = tk.Tk()
    app = TalafoozTranslator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
