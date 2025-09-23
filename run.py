import tkinter as tk
from CRM_System.views.main_window import MainWindow
from CRM_System.views.login_view import LoginWindow
from CRM_System.utils.internationalization import I18n
from CRM_System.models.user import User

def main():
    i18n = I18n(language="es") # O el idioma que prefieras por defecto

    def on_login_success(user: User):
        # Esta función se llamará cuando el login sea exitoso
        root = tk.Tk()
        root.withdraw() # Ocultamos la raíz principal de tkinter
        app = MainWindow(user=user, i18n=i18n)
        app.mainloop()

    # Iniciar la ventana de login
    login_app = LoginWindow(i18n=i18n, on_success=on_login_success)
    login_app.mainloop()

if __name__ == "__main__":
    main()
