import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from model import predict_disease
from disease_info import disease_info


class PlantDiseaseDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌿 Plant Disease Detector - PG Project")
        self.root.geometry("1000x650")
        self.root.configure(bg="#e8f5e9")

        self.image_path = None
        self.tk_image = None

        # Title Bar
        title_frame = tk.Frame(root, bg="#1b5e20", height=60)
        title_frame.pack(fill="x")
        title_label = tk.Label(
            title_frame,
            text="🌱 Plant Disease Detection System",
            font=("Helvetica", 22, "bold"),
            fg="white",
            bg="#1b5e20"
        )
        title_label.pack(pady=10)

        # Main Content (Two Columns)
        content_frame = tk.Frame(root, bg="#e8f5e9")
        content_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Left Frame (Image & Buttons)
        left_frame = tk.Frame(content_frame, bg="white", bd=2, relief="groove")
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.image_label = tk.Label(left_frame, text="No Image Uploaded",
                                    font=("Helvetica", 14), bg="#fafafa", fg="#777")
        self.image_label.pack(expand=True, padx=10, pady=10)

        self.upload_button = tk.Button(
            left_frame,
            text="📷 Upload Image",
            command=self.upload_image,
            font=("Helvetica", 14, "bold"),
            bg="#388e3c",
            fg="white",
            activebackground="#2e7d32",
            activeforeground="white",
            relief="flat",
            padx=20, pady=10,
            cursor="hand2"
        )
        self.upload_button.pack(pady=15)

        self.clear_button = tk.Button(
            left_frame,
            text="🧹 Clear",
            command=self.clear_image,
            font=("Helvetica", 12),
            bg="#f57c00",
            fg="white",
            activebackground="#ef6c00",
            relief="flat",
            padx=15, pady=7,
            cursor="hand2"
        )
        self.clear_button.pack(pady=5)

        # Right Frame (Results & Info)
        right_frame = tk.Frame(content_frame, bg="white", bd=2, relief="groove")
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.result_label = tk.Label(
            right_frame,
            text="🩺 Detected Disease: -",
            font=("Helvetica", 18, "bold"),
            bg="white",
            fg="#00695c"
        )
        self.result_label.pack(pady=15)

        # Scrollable Info Box
        info_frame = tk.Frame(right_frame, bg="white")
        info_frame.pack(expand=True, fill="both", padx=15, pady=10)

        self.info_text = tk.Text(
            info_frame,
            font=("Helvetica", 12),
            wrap="word",
            bg="#f1f8e9",
            fg="#333",
            relief="flat"
        )
        self.info_text.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(info_frame, command=self.info_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.info_text.config(yscrollcommand=scrollbar.set)

        self.info_text.insert(tk.END, "📋 Disease details will appear here...\n")
        self.info_text.config(state=tk.DISABLED)

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("✅ Ready")
        status_bar = tk.Label(root, textvariable=self.status_var,
                              font=("Helvetica", 10), bg="#1b5e20", fg="white", anchor="w")
        status_bar.pack(side="bottom", fill="x")

        # Menu Bar (About Section)
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def upload_image(self):
        filetypes = [("Image files", "*.jpg *.jpeg *.png")]
        self.image_path = filedialog.askopenfilename(title="Select an Image", filetypes=filetypes)
        if self.image_path:
            pil_image = Image.open(self.image_path)
            pil_image.thumbnail((400, 300))
            self.tk_image = ImageTk.PhotoImage(pil_image)
            self.image_label.config(image=self.tk_image, text="")
            self.image_label.image = self.tk_image
            self.status_var.set("📂 Image loaded successfully")
            self.detect_disease(pil_image)

    def clear_image(self):
        self.image_label.config(image="", text="No Image Uploaded")
        self.result_label.config(text="🩺 Detected Disease: -")
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, "📋 Disease details will appear here...\n")
        self.info_text.config(state=tk.DISABLED)
        self.status_var.set("🧹 Cleared")

    def detect_disease(self, image):
        disease_name = predict_disease(image)

        self.result_label.config(text=f"🩺 Detected Disease: {disease_name}")

        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, f"🌿 Name: {disease_name}\n\n")

        if disease_name in disease_info:
            self.info_text.insert(tk.END, f"⚠️ Symptoms:\n{disease_info[disease_name]['symptoms']}\n\n")
            self.info_text.insert(tk.END, f"💊 Remedies:\n{disease_info[disease_name]['remedies']}")
        else:
            self.info_text.insert(tk.END, "No additional information found.")
        self.info_text.config(state=tk.DISABLED)

        self.status_var.set("✅ Prediction complete")

    def show_about(self):
        messagebox.showinfo(
            "About",
            "🌱 Plant Disease Detector\n\n"
            "Developed as a Postgraduate Project\n"
            "Using Python (Tkinter + ML)\n\n"
            "👨‍💻 Author: Your Name\n📅 Year: 2025"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = PlantDiseaseDetectorApp(root)
    root.mainloop()
