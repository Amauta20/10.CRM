import tkinter as tk
from CRM_System.views.main_window import MainWindow


def main():
    root = tk.Tk()
    root.withdraw() # Hide the main window

    app = MainWindow()
    app.mainloop()

    root.destroy() # Destroy the hidden root window

if __name__ == "__main__":
    main()