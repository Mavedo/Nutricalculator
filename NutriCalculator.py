import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class NutriCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nutri Calculadora")

        # Variables
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.height_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.gender_var = tk.StringVar(value="Hombre")  # Default to Male

        # Create UI elements
        self.create_ui()

    def create_ui(self):
        main_frame = ttk.Frame(self.root, padding=(30, 15))
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Labels and Entries
        labels_entries = [
            ("Nombre del paciente:", self.name_var, 0),
            ("Edad del paciente:", self.age_var, 1),
            ("Altura (en metros):", self.height_var, 2),
            ("Peso en kilogramos:", self.weight_var, 3)
        ]

        for label, var, row in labels_entries:
            ttk.Label(main_frame, text=label).grid(column=0, row=row, sticky="w", pady=5)
            ttk.Entry(main_frame, textvariable=var).grid(column=1, row=row, sticky="ew", pady=5)

        # Radio Buttons
        ttk.Label(main_frame, text="Sexo:").grid(column=0, row=4, sticky="w")
        ttk.Radiobutton(main_frame, text="Hombre", variable=self.gender_var, value="Hombre").grid(column=1, row=4, sticky="w")
        ttk.Radiobutton(main_frame, text="Mujer", variable=self.gender_var, value="Mujer").grid(column=1, row=5, sticky="w")

        # Calculate Button
        ttk.Button(main_frame, text="Calcular", command=self.calculate).grid(column=0, row=6, columnspan=2, sticky="ew")

    def calculate(self):
        try:
            age = int(self.age_var.get())
            height = float(self.height_var.get())
            weight = float(self.weight_var.get())

            # Validate inputs
            self.validate_inputs(age, height, weight)

            # Perform calculations
            hb_result = round(self.harris_benedict(weight, height, age),2)
            mf_result = round(self.mifflin(weight, height, age),2)
            imc_result = round(self.imc(weight, height),2)
            classification_result = self.classification_imc(imc_result)

            # Display results
            result_message = f"Harris Benedict: {hb_result}\n" \
                             f"Mifflin St. Jeor: {mf_result}\n" \
                             f"IMC: {imc_result}\n" \
                             f"Clasificación: {classification_result}"

            messagebox.showinfo("Resultados", result_message)

            # Generate and open PDF
            patient_info = f"Paciente: {self.name_var.get()}, Edad: {age} años, Peso: {weight} kg, Altura: {height} metros."
            self.generate_pdf(hb_result, mf_result, imc_result, classification_result, patient_info)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def validate_inputs(self, age, height, weight):
        if not (2 <= age <= 99):
            raise ValueError("La edad debe estar entre 2 y 99 años")

        if not (0.99 <= height <= 2.20):
            raise ValueError("La estatura debe estar entre 0.99 y 2.20 metros")

        if not (15 <= weight <= 250):
            raise ValueError("El peso debe estar entre 15 y 250 kilogramos")

    def harris_benedict(self, weight, height, age):
        if self.gender_var.get() == "Hombre":
            return 66.5 + (13.8 * weight) + (5 * height * 100) - (6.8 * age)
        else:
            return 665 + (9.6 * weight) + (1.85 * height * 100) - (4.7 * age)

    def mifflin(self, weight, height, age):
        if self.gender_var.get() == "Hombre":
            return (10 * weight) + (6.25* height * 100) - (5* age) + 5
        else:
            return (10 * weight) + (6.25 * height * 100) - (5 * age) - 161

    def imc(self, weight, height):
        return weight / (height ** 2)

    def classification_imc(self, imc_result):
        if imc_result < 18.5:
            return "Bajo Peso"
        elif imc_result < 25:
            return "Normopeso"
        elif imc_result < 30:
            return "Sobrepeso"
        elif imc_result < 35:
            return "Obesidad grado 1"
        elif imc_result < 40:
            return "Obesidad grado 2"
        else:
            return "Obesidad grado 3"

    def generate_pdf(self, hb_result, mf_result, imc_result, classification_result, patient_info):
        import os
        pdf_folder = "C:/Users/Faskomilo/Desktop/Nutricalculator/"
        pdf_file = f"{pdf_folder}{self.name_var.get()} resultados.pdf"

        if not os.path.exists(pdf_folder):
            os.makedirs(pdf_folder)

        c = canvas.Canvas(pdf_file, pagesize=letter)
        c.drawString(72, 800, "Calculadora NutriMonchi Resultados")
        c.drawString(72, 780, patient_info)
        c.drawString(72, 720, f"Harris Benedict: {hb_result} calorías")
        c.drawString(72, 700, f"Mifflin St. Jeor: {mf_result} calorías")
        c.drawString(72, 680, f"IMC: {imc_result}")
        c.drawString(72, 660, f"Clasificación: {classification_result}")
        c.save()

        # Open the PDF file
        os.startfile(pdf_file)

if __name__ == "__main__":
    root = tk.Tk()
    app = NutriCalculatorApp(root)
    root.columnconfigure(0, weight= 1)

    window_width = 380
    window_height = 250
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    root.mainloop()
