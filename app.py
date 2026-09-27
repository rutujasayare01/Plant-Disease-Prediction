import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from model import predict_disease
from disease_info import disease_info



class PlantDiseaseDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Plant Disease Detector")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.image_path = None
        self.tk_image = None

        self.frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
        self.frame.pack(expand=True, fill="both")

        self.title_label = tk.Label(self.frame, text="Plant Disease Detector", font=("Helvetica", 24, "bold"), bg="#f0f0f0", fg="#333333")
        self.title_label.pack(pady=10)

        self.instruction_label = tk.Label(self.frame, text="Upload a plant leaf image to detect diseases.", font=("Helvetica", 12), bg="#f0f0f0", fg="#555555")
        self.instruction_label.pack(pady=5)

        self.image_frame = tk.Frame(self.frame, bg="#ffffff", bd=2, relief="solid")
        self.image_frame.pack(pady=20, expand=True, fill="both")
        self.image_label = tk.Label(self.image_frame, bg="#ffffff")
        self.image_label.pack(expand=True)

        self.upload_button = tk.Button(self.frame, text="Upload Image", command=self.upload_image, font=("Helvetica", 14), bg="#4CAF50", fg="white", cursor="hand2")
        self.upload_button.pack(pady=10)

        self.result_label = tk.Label(self.frame, text="", font=("Helvetica", 16, "bold"), bg="#f0f0f0", fg="#00796B")
        self.result_label.pack(pady=10)

        self.info_text = tk.Text(self.frame, height=8, width=70, font=("Helvetica", 12), relief="groove", bd=2)
        self.info_text.pack(pady=10)
        self.info_text.insert(tk.END, "Disease Information will appear here...\n\n")
        self.info_text.config(state=tk.DISABLED)

    def upload_image(self):
        filetypes = [("Image files", "*.jpg *.jpeg *.png")]
        self.image_path = filedialog.askopenfilename(title="Select an Image", filetypes=filetypes)
        if self.image_path:
            pil_image = Image.open(self.image_path)
            pil_image.thumbnail((self.image_frame.winfo_width()-4, self.image_frame.winfo_height()-4))
            self.tk_image = ImageTk.PhotoImage(pil_image)
            self.image_label.config(image=self.tk_image)
            self.image_label.image = self.tk_image
            self.detect_disease(pil_image)

    def detect_disease(self, image):
        disease_name = predict_disease(image)
        self.result_label.config(text=f"Detected Disease: {disease_name}")
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, f"Name: {disease_name}\n\n")
        if disease_name in disease_info:
            self.info_text.insert(tk.END, f"Symptoms:\n{disease_info[disease_name]['symptoms']}\n\n")
            self.info_text.insert(tk.END, f"Remedies:\n{disease_info[disease_name]['remedies']}")
        self.info_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = PlantDiseaseDetectorApp(root)
    root.mainloop()
