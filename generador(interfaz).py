import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
import numpy as np
import math

class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Generador de Contraseñas")
        self.geometry("450x400")
        self.configure(bg='#2A2A2A')

        # Intentar cargar icono principal
        try:
            self.icon_image = PhotoImage(file="icon.png")
            self.iconphoto(False, self.icon_image)
        except Exception as e:
            print("Icono principal no encontrado:", e)

        self.style = ttk.Style()
        self._configure_styles()
        self._create_widgets()

    def _configure_styles(self):
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#2A2A2A')
        self.style.configure('TLabel', background='#2A2A2A', foreground='white', font=('Helvetica', 10))
        self.style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'))
        self.style.configure('TButton', background='#4CAF50', foreground='white',
                             font=('Helvetica', 10, 'bold'), padding=10)
        self.style.map('TButton', background=[('active', '#45a049')])
        self.style.configure('TCheckbutton', background='#2A2A2A', foreground='white')
        self.style.configure('TScale', background='#2A2A2A', troughcolor='#3A3A3A')
        self.style.configure('TEntry', fieldbackground='#3A3A3A', foreground='white')

    def _create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)

        header = ttk.Label(main_frame, text="Generador AL de Contraseñas", style='Header.TLabel')
        header.pack(pady=(0, 20))

        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill='x', pady=10)

        ttk.Label(options_frame, text="Tipos de caracteres:").pack(anchor='w')
        self.mayusculas = tk.BooleanVar()
        self.numeros = tk.BooleanVar()
        self.especiales = tk.BooleanVar()

        ttk.Checkbutton(options_frame, text="Letras mayúsculas", variable=self.mayusculas).pack(anchor='w', pady=2)
        ttk.Checkbutton(options_frame, text="Números", variable=self.numeros).pack(anchor='w', pady=2)
        ttk.Checkbutton(options_frame, text="Caracteres especiales", variable=self.especiales).pack(anchor='w', pady=2)

        length_frame = ttk.Frame(main_frame)
        length_frame.pack(fill='x', pady=10)

        ttk.Label(length_frame, text="Longitud:").pack(side='left')
        self.length = tk.IntVar(value=16)
        ttk.Scale(length_frame, from_=8, to_=128, variable=self.length,
                  command=lambda v: self.length.set(round(float(v)))).pack(side='left', expand=True, fill='x', padx=10)
        ttk.Entry(length_frame, textvariable=self.length, width=4).pack(side='left')

        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=20)

        generate_btn = ttk.Button(buttons_frame, text="Generar Contraseña", command=self._generate_password)
        generate_btn.pack(side='left', padx=5)

        # Botón de copiar con manejo de icono
        try:
            original_icon = Image.open("copy_icon.png")
            self.copy_icon = ImageTk.PhotoImage(original_icon.resize((20, 20)))
            copy_button = ttk.Button(
                buttons_frame,
                image=self.copy_icon,
                command=self.copy_password,
                style='TButton'
            )
            copy_button.pack(side='left', padx=5)
        except Exception as e:
            print("Icono de copiar no encontrado:", e)
            copy_button = ttk.Button(
                buttons_frame,
                text="Copiar",
                command=self.copy_password,
                style='TButton'
            )
            copy_button.pack(side='left', padx=5)

        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill='x')

        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(result_frame, textvariable=self.password_var, font=('Courier', 12),
                                        state='readonly', width=50)
        self.password_entry.pack(pady=10)

        self.security_var = tk.StringVar()
        ttk.Label(result_frame, textvariable=self.security_var, foreground='#4CAF50').pack()

    def _generate_password(self):
        try:
            longitud = self.length.get()
            if not 8 <= longitud <= 128:
                raise ValueError("La longitud debe estar entre 8 y 128")

            password = self.generar_contrasena(
                longitud=longitud,
                usar_minusculas=True,
                usar_mayusculas=self.mayusculas.get(),
                usar_numeros=self.numeros.get(),
                usar_especiales=self.especiales.get()
            )

            self.password_var.set(password)
            self.password_entry.config(width=len(password) + 2)
            self.security_var.set(f"Seguridad: {self.calcular_seguridad(password):.2f} bits")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def copy_password(self):
        self.clipboard_clear()
        self.clipboard_append(self.password_var.get())

    def generar_contrasena(self, longitud, usar_minusculas, usar_mayusculas, usar_numeros, usar_especiales):
        # Matriz de caracteres usando numpy
        conjuntos = [
            np.array(list("abcdefghijklmnopqrstuvwxyz")),
            np.array(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")),
            np.array(list("0123456789")),
            np.array(list("!@#$%^&*()-_=+[]{};:,.<>/?"))
        ]

        # Vector de activación booleano
        activaciones = np.array([
            usar_minusculas,
            usar_mayusculas,
            usar_numeros,
            usar_especiales
        ], dtype=bool)

        # Filtrar conjuntos usando álgebra booleana
        conjuntos_activos = [conjuntos[i] for i in np.where(activaciones)[0]]

        if not conjuntos_activos:
            raise ValueError("Debe seleccionar al menos un tipo de carácter")

        # Vector de probabilidades (normalización L1)
        probabilidades = np.array([len(c) for c in conjuntos_activos], dtype=np.float64)
        probabilidades /= np.sum(probabilidades)

        # Generar contraseña usando selección vectorizada
        indices = np.random.choice(len(conjuntos_activos), size=longitud, p=probabilidades)
        password = [np.random.choice(conjuntos_activos[i]) for i in indices]

        # Asegurar al menos un carácter de cada conjunto
        for i, conjunto in enumerate(conjuntos_activos):
            if not any(np.isin(password, conjunto)):
                pos = np.random.randint(0, longitud)
                password[pos] = np.random.choice(conjunto)

        return ''.join(password)

    def calcular_seguridad(self, password):
        # Vector de presencia de caracteres
        presencia = np.array([
            any(c.islower() for c in password),
            any(c.isupper() for c in password),
            any(c.isdigit() for c in password),
            any(not c.isalnum() for c in password)
        ], dtype=int)

        # Vector de espacios posibles
        espacios = np.array([26, 26, 10, 32])

        # Cálculo de entropía usando álgebra lineal
        espacio_total = np.dot(presencia, espacios)
        if espacio_total == 0:
            return 0.0

        entropia = len(password) * math.log2(espacio_total)
        entropia += np.linalg.norm(presencia, ord=1) * 0.75  # Bonus por diversidad

        return entropia

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()