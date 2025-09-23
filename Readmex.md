# Sistema CRM Desktop - Python & SQLite

Un sistema de Customer Relationship Management (CRM) desarrollado en Python para escritorio, utilizando SQLite como base de datos.

## ✨ Características Principales

- **Gestión completa de contactos** con campos personalizables
- **Pipeline visual de ventas** con etapas personalizables
- **Sistema de actividades y recordatorios**
- **Dashboard con métricas y reportes**
- **Búsqueda avanzada y filtrado**
- **Sistema de etiquetas y categorización**
- **Interfaz intuitiva y responsive**
- **Base de datos SQLite local y portable**

## 🛠️ Tecnologías Utilizadas

- Python 3.8+
- SQLite3
- Tkinter para la interfaz gráfica

## 🚀 Distribución y Ejecución

### Opción 1: Ejecutable Standalone (Recomendado para usuarios finales)

Para la forma más sencilla de usar la aplicación sin necesidad de instalar Python o dependencias:

1.  **Descarga el ejecutable:** Obtén la última versión del ejecutable desde [enlace de descarga aquí - por ejemplo, tu página de lanzamientos de GitHub].
2.  **Ejecuta la aplicación:** Simplemente haz doble clic en el archivo `.exe` descargado.

**Cómo crear el ejecutable (para desarrolladores):**

Utilizamos `PyInstaller` para empaquetar la aplicación.

1.  **Instala PyInstaller:**
    ```bash
    pip install pyinstaller
    ```
2.  **Navega al directorio raíz del proyecto:**
    ```bash
    cd C:\Python\10.CRM
    ```
3.  **Crea el ejecutable:**
    ```bash
    pyinstaller --onefile --windowed run.py
    ```
    El ejecutable se encontrará en la carpeta `dist/`.

### Opción 2: Ejecutar desde el Código Fuente (Para desarrolladores)

Si deseas ejecutar la aplicación desde el código fuente o contribuir al desarrollo:

1.  **Verifica la instalación de Python:**
    Abre una terminal (Símbolo del sistema o PowerShell en Windows) y escribe:
    ```bash
    python --version
    ```
    Si Python no está instalado o la versión es inferior a 3.8, necesitarás instalarlo.

2.  **Instala Python (si es necesario):**
    Descarga la última versión estable de Python para Windows desde el sitio web oficial: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
    Durante la instalación, asegúrate de marcar la opción "Add Python to PATH" (Añadir Python al PATH) para que Python sea accesible desde la terminal.

3.  **Clona o descarga el proyecto:**
    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio.git
    cd tu-repositorio
    ```
    (Ajusta el enlace del repositorio según corresponda)

4.  **Instala las dependencias:**
    Navega al directorio raíz del proyecto en tu terminal y ejecuta:
    ```bash
    pip install -r CRM_System/requirements.txt
    ```

5.  **Ejecuta la aplicación:**
    ```bash
    python run.py
    ```
    O si `run.py` no existe o es un lanzador:
    ```bash
    python CRM_System/main.py
    ```

## 📦 Estructura del Proyecto

(Mantener la estructura existente o añadir una sección si es necesario)

## 📝 Versionado

Utilizamos [Git](https://git-scm.com/) para el control de versiones. Cada lanzamiento importante se etiquetará con un número de versión (ej. `v1.0.0`).

Para ver la versión actual de la aplicación, consulta el archivo `CRM_System/main.py` o un archivo `version.py` dedicado (si se implementa).

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor, lee `CONTRIBUTING.md` (si existe) para más detalles.

## 📄 Licencia

Este proyecto está bajo la Licencia [Nombre de la Licencia] - mira el archivo `LICENSE` para más detalles.
