import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
from model import predict_disease
from disease_info import disease_info


class ModernPlantDiseaseDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌿 Plant Disease Detector - PG Project")
        self.root.geometry("1200x750")
        self.root.configure(bg="#f0f7f4")
        self.root.resizable(True, True)
        
        # Set application icon (if available)
        try:
            self.root.iconbitmap("plant_icon.ico")  # You can add an icon file
        except:
            pass
        
        self.image_path = None
        self.tk_image = None
        self.original_image = None
        
        # Custom colors
        self.colors = {
            "primary": "#2e7d32",
            "primary_light": "#4caf50",
            "primary_dark": "#1b5e20",
            "secondary": "#ff9800",
            "accent": "#ff5722",
            "background": "#f0f7f4",
            "card_bg": "#ffffff",
            "text_primary": "#212121",
            "text_secondary": "#757575",
            "success": "#4caf50",
            "warning": "#ff9800",
            "error": "#f44336"
        }
        
        # Configure styles
        self.setup_styles()
        
        # Create UI
        self.create_title_bar()
        self.create_main_content()
        self.create_status_bar()
        self.create_menu()
        
        # Center the window
        self.center_window()

    def setup_styles(self):
        # Configure custom styles for widgets
        self.root.option_add("*Font", "Arial 10")
        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_title_bar(self):
        # Header with gradient effect
        header_frame = tk.Frame(self.root, bg=self.colors["primary"], height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title and subtitle
        title_container = tk.Frame(header_frame, bg=self.colors["primary"])
        title_container.pack(expand=True, fill="both")
        
        title_label = tk.Label(
            title_container,
            text="🌱 Plant Disease Detection System",
            font=("Arial", 24, "bold"),
            fg="white",
            bg=self.colors["primary"]
        )
        title_label.pack(pady=(10, 0))
        
        subtitle_label = tk.Label(
            title_container,
            text="AI-Powered Plant Health Analysis",
            font=("Arial", 12),
            fg="#e8f5e9",
            bg=self.colors["primary"]
        )
        subtitle_label.pack(pady=(0, 10))
        
        # Decorative element
        decoration = tk.Frame(header_frame, height=4, bg=self.colors["secondary"])
        decoration.pack(fill="x", side="bottom")

    def create_main_content(self):
        # Main content container
        main_container = tk.Frame(self.root, bg=self.colors["background"])
        main_container.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Two-column layout
        left_frame = self.create_image_section(main_container)
        right_frame = self.create_results_section(main_container)
        
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

    def create_image_section(self, parent):
        # Image section with card design
        card = tk.Frame(parent, bg=self.colors["card_bg"], relief="flat", bd=0, width=500)
        card.pack_propagate(False)
        
        # Card header
        card_header = tk.Frame(card, bg=self.colors["primary_light"], height=40)
        card_header.pack(fill="x")
        card_header.pack_propagate(False)
        
        header_label = tk.Label(
            card_header,
            text="📷 Plant Image",
            font=("Arial", 12, "bold"),
            fg="white",
            bg=self.colors["primary_light"]
        )
        header_label.pack(side="left", padx=15, pady=10)
        
        # Image display area
        image_container = tk.Frame(card, bg="#f5f5f5", relief="sunken", bd=1)
        image_container.pack(expand=True, fill="both", padx=15, pady=15)
        
        self.image_label = tk.Label(
            image_container, 
            text="No Image Uploaded\n\nClick 'Upload Image' to begin analysis",
            font=("Arial", 12),
            bg="#fafafa", 
            fg=self.colors["text_secondary"],
            justify="center",
            wraplength=300
        )
        self.image_label.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Button container
        button_frame = tk.Frame(card, bg=self.colors["card_bg"])
        button_frame.pack(fill="x", padx=15, pady=15)
        
        # Upload button with modern style
        self.upload_button = tk.Button(
            button_frame,
            text="📁 Upload Image",
            command=self.upload_image,
            font=("Arial", 11, "bold"),
            bg=self.colors["primary"],
            fg="white",
            activebackground=self.colors["primary_dark"],
            activeforeground="white",
            relief="flat",
            padx=25,
            pady=10,
            cursor="hand2",
            bd=0
        )
        self.upload_button.pack(side="left", padx=(0, 10))
        
        # Clear button
        self.clear_button = tk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_image,
            font=("Arial", 10),
            bg=self.colors["text_secondary"],
            fg="white",
            activebackground="#616161",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            bd=0
        )
        self.clear_button.pack(side="left")
        
        return card

    def create_results_section(self, parent):
        # Results section with card design
        card = tk.Frame(parent, bg=self.colors["card_bg"], relief="flat", bd=0, width=500)
        card.pack_propagate(False)
        
        # Card header
        card_header = tk.Frame(card, bg=self.colors["primary_light"], height=40)
        card_header.pack(fill="x")
        card_header.pack_propagate(False)
        
        header_label = tk.Label(
            card_header,
            text="🔍 Analysis Results",
            font=("Arial", 12, "bold"),
            fg="white",
            bg=self.colors["primary_light"]
        )
        header_label.pack(side="left", padx=15, pady=10)
        
        # Results display area
        results_container = tk.Frame(card, bg=self.colors["card_bg"])
        results_container.pack(expand=True, fill="both", padx=15, pady=15)
        
        # Disease name with emphasis
        self.result_label = tk.Label(
            results_container,
            text="Waiting for image...",
            font=("Arial", 16, "bold"),
            bg=self.colors["card_bg"],
            fg=self.colors["text_primary"],
            wraplength=400
        )
        self.result_label.pack(pady=(0, 15))
        
        # Confidence indicator (placeholder)
        self.confidence_frame = tk.Frame(results_container, bg=self.colors["card_bg"])
        self.confidence_frame.pack(fill="x", pady=(0, 15))
        
        self.confidence_label = tk.Label(
            self.confidence_frame,
            text="Confidence: -",
            font=("Arial", 10),
            bg=self.colors["card_bg"],
            fg=self.colors["text_secondary"]
        )
        self.confidence_label.pack(side="left")
        
        # Progress bar for confidence (visual indicator)
        self.confidence_bar = tk.Frame(self.confidence_frame, bg="#e0e0e0", height=8)
        self.confidence_bar.pack(fill="x", pady=(5, 0))
        self.confidence_bar_inner = tk.Frame(self.confidence_bar, bg=self.colors["success"], height=8, width=0)
        self.confidence_bar_inner.pack(side="left")
        
        # Info text with tabs-like interface
        notebook_frame = tk.Frame(results_container, bg=self.colors["card_bg"])
        notebook_frame.pack(expand=True, fill="both")
        
        # Create tab buttons
        tab_buttons_frame = tk.Frame(notebook_frame, bg=self.colors["card_bg"])
        tab_buttons_frame.pack(fill="x")
        
        self.symptoms_tab = tk.Button(
            tab_buttons_frame,
            text="Symptoms",
            font=("Arial", 10, "bold"),
            bg=self.colors["primary"],
            fg="white",
            relief="flat",
            bd=0,
            command=lambda: self.switch_tab("symptoms")
        )
        self.symptoms_tab.pack(side="left", padx=(0, 2))
        
        self.remedies_tab = tk.Button(
            tab_buttons_frame,
            text="Remedies",
            font=("Arial", 10),
            bg=self.colors["text_secondary"],
            fg="white",
            relief="flat",
            bd=0,
            command=lambda: self.switch_tab("remedies")
        )
        self.remedies_tab.pack(side="left")
        
        # Info text area
        text_container = tk.Frame(notebook_frame, bg=self.colors["card_bg"], relief="sunken", bd=1)
        text_container.pack(expand=True, fill="both", pady=(5, 0))
        
        self.info_text = tk.Text(
            text_container,
            font=("Arial", 11),
            wrap="word",
            bg="#f9f9f9",
            fg=self.colors["text_primary"],
            relief="flat",
            padx=15,
            pady=15
        )
        self.info_text.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(text_container, command=self.info_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.info_text.config(yscrollcommand=scrollbar.set)
        
        self.info_text.insert(tk.END, "Please upload an image to analyze plant health.")
        self.info_text.config(state=tk.DISABLED)
        
        # Set initial tab
        self.current_tab = "symptoms"
        self.switch_tab("symptoms")
        
        return card

    def create_status_bar(self):
        # Modern status bar
        status_bar = tk.Frame(self.root, bg=self.colors["primary_dark"], height=30)
        status_bar.pack(side="bottom", fill="x")
        status_bar.pack_propagate(False)
        
        self.status_var = tk.StringVar()
        self.status_var.set("✅ Ready to analyze plant images")
        
        status_label = tk.Label(
            status_bar,
            textvariable=self.status_var,
            font=("Arial", 9),
            bg=self.colors["primary_dark"],
            fg="white",
            anchor="w"
        )
        status_label.pack(side="left", padx=15, pady=5)
        
        # Add a subtle progress indicator (invisible by default)
        self.progress_indicator = tk.Frame(status_bar, bg=self.colors["secondary"], width=0, height=3)
        self.progress_indicator.place(relx=0, rely=1, anchor="sw", relwidth=0)

    def create_menu(self):
        # Modern menu bar
        menubar = tk.Menu(self.root, bg=self.colors["card_bg"], fg=self.colors["text_primary"], relief="flat")
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg="white", fg=self.colors["text_primary"])
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Upload Image", command=self.upload_image, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg="white", fg=self.colors["text_primary"])
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="User Guide", command=self.show_guide)
        
        # Bind keyboard shortcuts
        self.root.bind("<Control-o>", lambda e: self.upload_image())
        self.root.bind("<Control-q>", lambda e: self.root.quit())

    def switch_tab(self, tab_name):
        # Update tab appearances
        if tab_name == "symptoms":
            self.symptoms_tab.config(bg=self.colors["primary"], font=("Arial", 10, "bold"))
            self.remedies_tab.config(bg=self.colors["text_secondary"], font=("Arial", 10))
            self.current_tab = "symptoms"
        else:
            self.symptoms_tab.config(bg=self.colors["text_secondary"], font=("Arial", 10))
            self.remedies_tab.config(bg=self.colors["primary"], font=("Arial", 10, "bold"))
            self.current_tab = "remedies"
        
        # Update content if we have disease info
        if hasattr(self, 'current_disease') and self.current_disease:
            self.update_info_text()

    def update_info_text(self):
        if not hasattr(self, 'current_disease') or not self.current_disease:
            return
            
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        
        if self.current_tab == "symptoms":
            if self.current_disease in disease_info:
                self.info_text.insert(tk.END, f"🌿 {self.current_disease}\n\n")
                self.info_text.insert(tk.END, "⚠️ Symptoms:\n\n")
                self.info_text.insert(tk.END, disease_info[self.current_disease]['symptoms'])
            else:
                self.info_text.insert(tk.END, "No symptom information available.")
        else:
            if self.current_disease in disease_info:
                self.info_text.insert(tk.END, f"🌿 {self.current_disease}\n\n")
                self.info_text.insert(tk.END, "💊 Treatment & Remedies:\n\n")
                self.info_text.insert(tk.END, disease_info[self.current_disease]['remedies'])
            else:
                self.info_text.insert(tk.END, "No remedy information available.")
                
        self.info_text.config(state=tk.DISABLED)

    def upload_image(self):
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff"),
            ("All files", "*.*")
        ]
        
        self.image_path = filedialog.askopenfilename(
            title="Select a Plant Image", 
            filetypes=filetypes
        )
        
        if self.image_path:
            # Show loading state
            self.status_var.set("⏳ Loading image...")
            self.update_progress(0.3)
            self.root.update()
            
            try:
                # Open and process image
                self.original_image = Image.open(self.image_path)
                
                # Create thumbnail for display
                display_image = self.original_image.copy()
                display_image.thumbnail((450, 350), Image.Resampling.LANCZOS)
                
                # Add a subtle border
                display_image = ImageOps.expand(display_image, border=2, fill='#e0e0e0')
                
                self.tk_image = ImageTk.PhotoImage(display_image)
                self.image_label.config(image=self.tk_image, text="")
                self.image_label.image = self.tk_image
                
                self.status_var.set("🔍 Analyzing image...")
                self.update_progress(0.6)
                self.root.update()
                
                # Detect disease
                self.detect_disease(self.original_image)
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {str(e)}")
                self.status_var.set("❌ Error loading image")
                self.update_progress(0)

    def clear_image(self):
        self.image_label.config(image="", text="No Image Uploaded\n\nClick 'Upload Image' to begin analysis")
        self.result_label.config(text="Waiting for image...")
        self.confidence_label.config(text="Confidence: -")
        self.confidence_bar_inner.config(width=0)
        
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, "Please upload an image to analyze plant health.")
        self.info_text.config(state=tk.DISABLED)
        
        self.status_var.set("✅ Ready to analyze plant images")
        self.update_progress(0)
        
        # Reset disease info
        if hasattr(self, 'current_disease'):
            self.current_disease = None

    def detect_disease(self, image):
        # Simulate processing delay for better UX
        self.root.after(500, self._perform_detection, image)
    
    def _perform_detection(self, image):
        try:
            disease_name = predict_disease(image)
            self.current_disease = disease_name
            
            # Update results
            self.result_label.config(text=f"🌿 {disease_name}")
            
            # Simulate confidence value (you would get this from your model)
            confidence = 0.85  # Replace with actual confidence from your model
            self.confidence_label.config(text=f"Confidence: {confidence:.1%}")
            
            # Update confidence bar
            bar_width = int(confidence * 400)  # Assuming bar frame is 400px wide
            self.confidence_bar_inner.config(width=bar_width)
            
            # Update info text
            self.update_info_text()
            
            self.status_var.set("✅ Analysis complete")
            self.update_progress(1.0)
            
        except Exception as e:
            messagebox.showerror("Analysis Error", f"Could not analyze image: {str(e)}")
            self.status_var.set("❌ Analysis failed")
            self.update_progress(0)

    def update_progress(self, value):
        # Animate progress indicator
        self.progress_indicator.place(relx=0, rely=1, anchor="sw", relwidth=value)
        
    def show_about(self):
        about_text = (
            "🌱 Plant Disease Detector\n\n"
            "Version 2.0 (Modern UI)\n\n"
            "Developed as a Postgraduate Project\n"
            "Using Python, Tkinter, and Machine Learning\n\n"
            "This application helps identify plant diseases\n"
            "from images and suggests appropriate treatments.\n\n"
            "👨‍💻 Author: Your Name\n"
            "📅 Year: 2025"
        )
        
        messagebox.showinfo("About Plant Disease Detector", about_text)

    def show_guide(self):
        guide_text = (
            "User Guide: Plant Disease Detector\n\n"
            "1. Click 'Upload Image' or use Ctrl+O to select a plant image\n"
            "2. The system will analyze the image for diseases\n"
            "3. View detected disease, confidence level, and details\n"
            "4. Switch between 'Symptoms' and 'Remedies' tabs\n"
            "5. Use 'Clear' to reset and analyze another image\n\n"
            "For best results:\n"
            "- Use clear, well-lit images of plant leaves\n"
            "- Ensure the plant occupies most of the image\n"
            "- Avoid blurry or distant shots"
        )
        
        messagebox.showinfo("User Guide", guide_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernPlantDiseaseDetectorApp(root)
    root.mainloop()
