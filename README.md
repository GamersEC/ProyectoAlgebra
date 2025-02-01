# Generador de Contraseñas Seguras

Herramienta para generación de contraseñas seguras con cálculo de entropía, disponible en versión GUI (interfaz gráfica) y CLI (línea de comandos).

## Características Principales

### Versión GUI (Graphical User Interface)
- ✔️ Selección de tipos de caracteres mediante checkboxes
- 🎚 Control deslizante para longitud (8-128 caracteres)
- 📋 Botón de copiado al portapapeles con icono
- 🔐 Cálculo de seguridad en tiempo real (en bits de entropía)
- 🎨 Interfaz moderna con tema oscuro

### Versión CLI (Command Line Interface)
- 🖥 Interfaz interactiva de texto
- ❓ Preguntas guiadas para configuración
- 📊 Visualización de métricas de seguridad
- ⚙️ Validación automática de parámetros
- 📤 Resultados formateados en consola

### Tecnologías Base
- **Algoritmo de generación**:
  - Distribución probabilística ponderada
  - Combinación de múltiples conjuntos de caracteres
  - Uso intensivo de NumPy para operaciones vectorizadas
- **Cálculo de seguridad**:
  - Entropía basada en teoría de información
  - Bonus por diversidad de caracteres
  - Cálculo matricial con NumPy

## Requisitos del Sistema

- Python 3.6 o superior
- Bibliotecas requeridas:
  ```bash
  pip install numpy tkinter pillow
