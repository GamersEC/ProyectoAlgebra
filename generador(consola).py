import numpy as np
import math

def generar_contrasena(longitud, usar_minusculas, usar_mayusculas, usar_numeros, usar_especiales):
    # Definición de conjuntos de caracteres como arrays de numpy para operaciones vectorizadas
    conjuntos = [
        np.array(list("abcdefghijklmnopqrstuvwxyz")),  # Minúsculas
        np.array(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")),  # Mayúsculas
        np.array(list("0123456789")),                  # Números
        np.array(list("!@#$%^&*()-_=+[]{};:,.<>/?"))   # Especiales
    ]

    # Vector booleano para activar/desactivar conjuntos
    activaciones = np.array([
        usar_minusculas,
        usar_mayusculas,
        usar_numeros,
        usar_especiales
    ], dtype=bool)

    # Filtrar conjuntos activos usando indexación booleana
    conjuntos_activos = [conjuntos[i] for i in np.where(activaciones)[0]]

    if not conjuntos_activos:
        raise ValueError("Debe seleccionar al menos un tipo de carácter")

    # Cálculo de probabilidades proporcionales al tamaño de cada conjunto
    probabilidades = np.array([len(c) for c in conjuntos_activos], dtype=np.float64)
    probabilidades /= np.sum(probabilidades)  # Normalización a distribución de probabilidad

    # Generación de índices para selección de conjuntos
    indices = np.random.choice(len(conjuntos_activos), size=longitud, p=probabilidades)

    # Creación de la contraseña seleccionando caracteres aleatorios
    password = [np.random.choice(conjuntos_activos[i]) for i in indices]

    # Garantizar al menos un carácter de cada conjunto seleccionado
    for i, conjunto in enumerate(conjuntos_activos):
        if not any(np.isin(password, conjunto)):
            # Reemplazar aleatoriamente un carácter si no hay representación del conjunto
            pos = np.random.randint(0, longitud)
            password[pos] = np.random.choice(conjunto)

    return ''.join(password)

def calcular_seguridad(password):
    # Detección de tipos de caracteres presentes
    presencia = np.array([
        any(c.islower() for c in password),  # Minúsculas presentes
        any(c.isupper() for c in password),  # Mayúsculas presentes
        any(c.isdigit() for c in password),  # Números presentes
        any(not c.isalnum() for c in password)  # Especiales presentes
    ], dtype=int)

    # Tamaño de cada espacio de caracteres
    espacios = np.array([26, 26, 10, 32])  # Corresponden a: min, may, num, esp

    # Cálculo del espacio total de posibilidades
    espacio_total = np.dot(presencia, espacios)
    if espacio_total == 0:  # Caso extremo sin caracteres válidos
        return 0.0

    # Fórmula de entropía: longitud * log2(espacio_posible)
    entropia = len(password) * math.log2(espacio_total)

    # Bonus por diversidad de caracteres (usando norma L1)
    entropia += np.linalg.norm(presencia, ord=1) * 0.75

    return entropia

def main():
    print("********************************")
    print("=== Generador de Contraseñas ===")
    print("********************************\n")

    try:
        # Captura de parámetros con validación básica
        longitud = int(input("Ingrese la longitud de la contraseña (8-128): "))
        if not 8 <= longitud <= 128:
            print("Longitud inválida, usando valor por defecto 16")
            longitud = 16  # Valor por defecto seguro

        # Conversión de respuestas a booleanos
        mayus = input("¿Incluir mayúsculas? (s/n): ").lower() == 's'
        numeros = input("¿Incluir números? (s/n): ").lower() == 's'
        especiales = input("¿Incluir caracteres especiales? (s/n): ").lower() == 's'

        # Generación y cálculo de seguridad
        password = generar_contrasena(
            longitud=longitud,
            usar_minusculas=True,  # Minúsculas siempre activas
            usar_mayusculas=mayus,
            usar_numeros=numeros,
            usar_especiales=especiales
        )

        seguridad = calcular_seguridad(password)

        # Presentación de resultados
        print("\nContraseña generada:", password)
        print(f"Seguridad estimada: {seguridad:.2f} bits")

    except ValueError as ve:
        print(f"\nError de validación: {str(ve)}")
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")

if __name__ == "__main__":
    main()