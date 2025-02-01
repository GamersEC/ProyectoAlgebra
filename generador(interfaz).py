# Importación de bibliotecas necesarias
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk  # Para manejar imágenes
import numpy as np  # Para operaciones vectorizadas
import math  # Para cálculos matemáticos

class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        """Inicializa la aplicación principal"""
        super().__init__()
        # Configuración inicial de la ventana
        self.title("Generador de Contraseñas")
        self.geometry("450x400")
        self.configure(bg='#2A2A2A')  # Fondo oscuro

        # Intento de carga del icono principal
        try:
            self.icon_image = PhotoImage(file="icons/icon.png")
            self.iconphoto(False, self.icon_image)
        except Exception as e:
            print("Icono principal no encontrado:", e)

        # Configuración de estilos y creación de widgets
        self.style = ttk.Style()
        self._configure_styles()
        self._create_widgets()

    def _configure_styles(self):
        """Configura los estilos visuales de los componentes"""
        self.style.theme_use('clam')  # Tema base
        # Configuración de colores y fuentes para diferentes componentes
        self.style.configure('TFrame', background='#2A2A2A')
        self.style.configure('TLabel', background='#2A2A2A', foreground='white', font=('Helvetica', 10))
        self.style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'))  # Estilo especial para el encabezado
        self.style.configure('TButton', background='#4CAF50', foreground='white',
                             font=('Helvetica', 10, 'bold'), padding=10)
        self.style.map('TButton', background=[('active', '#45a049')])  # Efecto hover para botones
        self.style.configure('TCheckbutton', background='#2A2A2A', foreground='white')
        self.style.configure('TScale', background='#2A2A2A', troughcolor='#3A3A3A')
        self.style.configure('TEntry', fieldbackground='#3A3A3A', foreground='white')

    def _create_widgets(self):
        """Crea y organiza todos los componentes de la interfaz gráfica"""
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Encabezado de la aplicación
        header = ttk.Label(main_frame, text="Generador de Contraseñas", style='Header.TLabel')
        header.pack(pady=(0, 20))

        # Marco para opciones de caracteres
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill='x', pady=10)

        ttk.Label(options_frame, text="Tipos de caracteres:").pack(anchor='w')
        # Variables para almacenar selecciones de usuario
        self.mayusculas = tk.BooleanVar()
        self.numeros = tk.BooleanVar()
        self.especiales = tk.BooleanVar()

        # Checkboxes para tipos de caracteres
        ttk.Checkbutton(options_frame, text="Letras mayúsculas", variable=self.mayusculas).pack(anchor='w', pady=2)
        ttk.Checkbutton(options_frame, text="Números", variable=self.numeros).pack(anchor='w', pady=2)
        ttk.Checkbutton(options_frame, text="Caracteres especiales", variable=self.especiales).pack(anchor='w', pady=2)

        # Marco para control de longitud
        length_frame = ttk.Frame(main_frame)
        length_frame.pack(fill='x', pady=10)

        ttk.Label(length_frame, text="Longitud:").pack(side='left')
        self.length = tk.IntVar(value=16)  # Valor por defecto
        # Slider para seleccionar longitud
        ttk.Scale(length_frame, from_=8, to_=128, variable=self.length,
                  command=lambda v: self.length.set(round(float(v)))).pack(side='left', expand=True, fill='x', padx=10)
        ttk.Entry(length_frame, textvariable=self.length, width=4).pack(side='left')  # Entrada numérica

        # Marco para botones de acción
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=20)

        # Botón generador de contraseña
        generate_btn = ttk.Button(buttons_frame, text="Generar Contraseña", command=self._generate_password)
        generate_btn.pack(side='left', padx=5)

        # Botón de copiar con manejo de icono
        try:
            # Intento cargar icono de copiar
            original_icon = Image.open("icons/copy_icon.png")
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
            # Fallback a texto si no hay icono
            copy_button = ttk.Button(
                buttons_frame,
                text="Copiar",
                command=self.copy_password,
                style='TButton'
            )
            copy_button.pack(side='left', padx=5)

        # Marco para resultados
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill='x')

        # Entrada para mostrar la contraseña generada
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(result_frame, textvariable=self.password_var, font=('Courier', 12),
                                        state='readonly', width=50)
        self.password_entry.pack(pady=10)

        # Etiqueta para mostrar nivel de seguridad
        self.security_var = tk.StringVar()
        ttk.Label(result_frame, textvariable=self.security_var, foreground='#4CAF50').pack()

    def _generate_password(self):
        """Maneja el proceso de generación de contraseña"""
        try:
            longitud = self.length.get()
            # Validación de longitud
            if not 8 <= longitud <= 128:
                raise ValueError("La longitud debe estar entre 8 y 128")

            # Generación de contraseña
            password = self.generar_contrasena(
                longitud=longitud,
                usar_minusculas=True,  # Siempre activo
                usar_mayusculas=self.mayusculas.get(),
                usar_numeros=self.numeros.get(),
                usar_especiales=self.especiales.get()
            )

            # Actualización de la UI
            self.password_var.set(password)
            self.password_entry.config(width=len(password) + 2)  # Ajuste dinámico del ancho
            self.security_var.set(f"Seguridad: {self.calcular_seguridad(password):.2f} bits")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def copy_password(self):
        """Copia la contraseña al portapapeles"""
        self.clipboard_clear()
        self.clipboard_append(self.password_var.get())

    def generar_contrasena(self, longitud, usar_minusculas, usar_mayusculas, usar_numeros, usar_especiales):
        """
        Genera una contraseña segura usando operaciones vectorizadas con numpy
        """
        # Definición de conjuntos de caracteres
        conjuntos = [
            np.array(list("abcdefghijklmnopqrstuvwxyz")),  # Minúsculas
            np.array(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")),  # Mayúsculas
            np.array(list("0123456789")),                  # Números
            np.array(list("!@#$%^&*()-_=+[]{};:,.<>/?"))   # Especiales
        ]

        # Determinar qué conjuntos están activos
        activaciones = np.array([
            usar_minusculas,
            usar_mayusculas,
            usar_numeros,
            usar_especiales
        ], dtype=bool)

        conjuntos_activos = [conjuntos[i] for i in np.where(activaciones)[0]]

        if not conjuntos_activos:
            raise ValueError("Debe seleccionar al menos un tipo de carácter")

        # Cálculo de probabilidades según tamaño de conjuntos
        probabilidades = np.array([len(c) for c in conjuntos_activos], dtype=np.float64)
        probabilidades /= np.sum(probabilidades)  # Normalización

        # Selección de caracteres usando probabilidades
        indices = np.random.choice(len(conjuntos_activos), size=longitud, p=probabilidades)
        password = [np.random.choice(conjuntos_activos[i]) for i in indices]

        # Garantizar al menos un carácter de cada conjunto seleccionado
        for i, conjunto in enumerate(conjuntos_activos):
            if not any(np.isin(password, conjunto)):
                pos = np.random.randint(0, longitud)
                password[pos] = np.random.choice(conjunto)

        return ''.join(password)

    def calcular_seguridad(self, password):
        """
        Calcula la entropía de la contraseña en bits usando teoría de información
        """
        # Detección de tipos de caracteres presentes
        presencia = np.array([
            any(c.islower() for c in password),  # Minúsculas
            any(c.isupper() for c in password),  # Mayúsculas
            any(c.isdigit() for c in password),  # Números
            any(not c.isalnum() for c in password)  # Especiales
        ], dtype=int)

        # Espacio de posibilidades por tipo
        espacios = np.array([26, 26, 10, 32])  # Tamaño de cada conjunto

        # Cálculo de entropía base
        espacio_total = np.dot(presencia, espacios)
        if espacio_total == 0:
            return 0.0

        entropia = len(password) * math.log2(espacio_total)

        # Bonus por diversidad de caracteres (norma L1)
        entropia += np.linalg.norm(presencia, ord=1) * 0.75

        return entropia

if __name__ == "__main__":
    # Punto de entrada de la aplicación
    app = PasswordGeneratorApp()
    app.mainloop()