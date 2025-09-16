# estilos.py

from tkinter import ttk

class Estilos:
    def __init__(self, root):
        self.root = root
        self.style = ttk.Style(self.root)
        self.configurar_notebook()
        self.configurar_botones_ttk()

    def configurar_notebook(self):
        # Tema base que se puede modificar
        self.style.theme_use("default")

        # Estilo para las pestañas del Notebook
        self.style.configure("TNotebook.Tab",
                             font=("Arial", 10, "bold"),   # Fuente más grande
                             padding=[15, 10],             # Más anchas y altas
                             background="#ddd",            # Fondo claro
                             foreground="black")           # Texto negro

        # Fondo general del notebook
        self.style.configure("TNotebook", background="#222", borderwidth=0)

        # Pestaña seleccionada: colores distintos
        self.style.map("TNotebook.Tab",
                       background=[("selected", "#fff")],
                       foreground=[("selected", "#000")])

    def configurar_botones_ttk(self):
        # Estilo para botones grandes con ttk
        self.style.configure("BotonGrande.TButton",
                             font=("Arial", 14),
                             padding=10)
        

def estilo_botones_tk():
    """Retorna un diccionario de estilo para usar en botones tipo tk.Button"""
    return dict(
        bg="white",
        fg="black",
        font=("Roboto", 12),
        width=28,
        pady=3
    )
