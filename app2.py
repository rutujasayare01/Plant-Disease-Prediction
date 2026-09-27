import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from model import predict_disease
from disease_info import disease_info


class PlantDiseaseDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌿 Plant Disease Detector")
        self.root.geometry("900x650")
        self.root.configure(bg="#e8f5e9")  # Light green background

        self.image_path = None
        self.tk_image = None

        # Main Frame
        self.frame = tk.Frame(root, bg="#ffffff", bd=2, relief="ridge")
        self.frame.pack(padx=30, pady=30, expand=True, fill="both")

        # Title
        self.title_label = tk.Label(
            self.frame,
            text="🌱 Plant Disease Detector",
            font=("Helvetica", 28, "bold"),
            bg="#ffffff",
            fg="#2e7d32"
        )
        self.title_label.pack(pady=20)

        # Instructions
        self.instruction_label = tk.Label(
            self.frame,
            text="Upload a plant leaf image to detect diseases.",
            font=("Helvetica", 14),
            bg="#ffffff",
            fg="#555555"
        )
        self.instruction_label.pack(pady=5)

        # Image Frame
        self.image_frame = tk.Frame(self.frame, bg="#f9f9f9", bd=3, relief="groove")
        self.image_frame.pack(pady=20, expand=True, fill="both")
        self.image_label = tk.Label(self.image_frame, bg="#f9f9f9")
        self.image_label.pack(expand=True)

        # Default Placeholder
        placeholder = Image.open("placeholder.png") if False else None
        if placeholder:
            placeholder.thumbnail((400, 300))
            self.tk_image = ImageTk.PhotoImage(placeholder)
            self.image_label.config(image=self.tk_image)

        # Upload Button with hover effect
        self.upload_button = tk.Button(
            self.frame,
            text="📷 Upload Image",
            command=self.upload_image,
            font=("Helvetica", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            activebackground="#388e3c",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.upload_button.pack(pady=15)

        # Result Label
        self.result_label = tk.Label(
            self.frame,
            text="",
            font=("Helvetica", 18, "bold"),
            bg="#ffffff",
            fg="#00796B"
        )
        self.result_label.pack(pady=15)

        # Scrollable Info Box
        self.info_frame = tk.Frame(self.frame, bg="#ffffff")
        self.info_frame.pack(pady=10, fill="both", expand=True)

        self.info_text = tk.Text(
            self.info_frame,
            height=10,
            width=70,
            font=("Helvetica", 12),
            relief="flat",
            wrap="word",
            bg="#f1f8e9",
            fg="#333333"
        )
        self.info_text.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        self.scrollbar = tk.Scrollbar(self.info_frame, command=self.info_text.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.info_text.config(yscrollcommand=self.scrollbar.set)

        self.info_text.insert(tk.END, "📋 Disease information will appear here...\n\n")
        self.info_text.config(state=tk.DISABLED)

    def upload_image(self):
        filetypes = [("Image files", "*.jpg *.jpeg *.png")]
        self.image_path = filedialog.askopenfilename(title="Select an Image", filetypes=filetypes)
        if self.image_path:
            pil_image = Image.open(self.image_path)
            pil_image.thumbnail((500, 350))
            self.tk_image = ImageTk.PhotoImage(pil_image)
            self.image_label.config(image=self.tk_image)
            self.image_label.image = self.tk_image
            self.detect_disease(pil_image)

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


if __name__ == "__main__":
    root = tk.Tk()
    app = PlantDiseaseDetectorApp(root)
    root.mainloop()
