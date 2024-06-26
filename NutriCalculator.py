import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class NutriCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nutri Calculadora")

        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.height_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.gender_var = tk.StringVar(value="Mujer")  # Default to Female

        self.create_ui()

    def create_ui(self):
        """" Creates the user interface. The labesl and it's entries are distrubuted in 4 rows and 2 columns. 
        Then 2 radiobuttons are created for the sex category.
        At the end there's a button that takes all the inputs and calculates."""
        main_frame = ttk.Frame(self.root, padding=(30, 15))
        main_frame.grid(row=0, column=0, sticky="nsew")
        

        ttk.Label(main_frame, text= "Nombre del paciente:").grid(column=0, row=0, sticky="w", pady=5)
        ttk.Entry(main_frame, textvariable= self.name_var).grid(column=1, row=0, sticky="ew", pady=5)
        ttk.Label(main_frame, text= "Edad del paciente:").grid(column=0, row=1, sticky="w", pady=5)
        ttk.Entry(main_frame, textvariable= self.age_var).grid(column=1, row=1, sticky="ew", pady=5)
        ttk.Label(main_frame, text= "Altura (en metros):").grid(column=0, row=2, sticky="w", pady=5)
        ttk.Entry(main_frame, textvariable= self.height_var).grid(column=1, row=2, sticky="ew", pady=5)
        ttk.Label(main_frame, text= "Peso en kilogramos:").grid(column=0, row=3, sticky="w", pady=5)
        ttk.Entry(main_frame, textvariable= self.weight_var).grid(column=1, row=3, sticky="ew", pady=5)


        ttk.Label(main_frame, text="Sexo:").grid(column=0, row=4, sticky="w")
        ttk.Radiobutton(main_frame, text="Hombre", variable=self.gender_var, value="Hombre").grid(column=1, row=4, sticky="w")
        ttk.Radiobutton(main_frame, text="Mujer", variable=self.gender_var, value="Mujer").grid(column=1, row=5, sticky="w")


        ttk.Button(main_frame, text="Calcular", command=self.calculate).grid(column=0, row=6, columnspan=2, sticky="ew")

    def calculate(self):
        """" The entries are converted to the right datatype, else an error is returned.
        We calculate the IMC, the calories according the 2 different equations: Harris-Benedict and
        Mifflin St. Jeor.
        
        The result is returned in a messagebox, a pdf is generated and opened."""
        try:
            age = int(self.age_var.get())
            height = float(self.height_var.get())
            weight = float(self.weight_var.get())

            self.validate_inputs(age, height, weight)

            hb_result = round(self.harris_benedict(weight, height, age),2)
            mf_result = round(self.mifflin(weight, height, age),2)
            imc_result = round(self.imc(weight, height),2)
            classification_result = self.classification_imc(imc_result)

            result_message = f"Harris Benedict: {hb_result}\n" \
                             f"Mifflin St. Jeor: {mf_result}\n" \
                             f"IMC: {imc_result}\n" \
                             f"Clasificación: {classification_result}"

            messagebox.showinfo("Resultados", result_message)

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
        pdf_folder = "C:/Users/Faskomilo/Desktop/Nutricalculator/patient_results"
        pdf_file = f"{pdf_folder}{self.name_var.get()} resultados.pdf"

        if not os.path.exists(pdf_folder):
            os.makedirs(pdf_folder)

        c = canvas.Canvas(pdf_file, pagesize=letter)
        c.drawString(72, 800, "Nutri Calculadora Resultados")
        c.drawString(72, 780, patient_info)
        c.drawString(72, 720, f"Harris Benedict: {hb_result} calorías")
        c.drawString(72, 700, f"Mifflin St. Jeor: {mf_result} calorías")
        c.drawString(72, 680, f"IMC: {imc_result}")
        c.drawString(72, 660, f"Clasificación: {classification_result}")
        c.save()

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
