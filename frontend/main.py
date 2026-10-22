import tkinter as tk
from tkinter import messagebox
import requests

from frames.inicio import crear_inicio


# ==========================================
# COLORES ARCA
# ==========================================
FONDO = "#F5F3ED"
BLANCO = "#FFFFFF"
VERDE = "#4F7F5F"
VERDE_CLARO = "#69AE7C"
VERDE_OSCURO = "#396348"
NARANJA = "#F27B21"
GRIS = "#777777"
BORDE = "#D5DED5"


# ==========================================
# VENTANA PRINCIPAL
# ==========================================
ventana = tk.Tk()
ventana.title("ARCA - Refugio de animales")
ventana.geometry("800x650")
ventana.minsize(800, 600)
ventana.configure(bg=FONDO)

contenedor_app = None
sesion_iniciada = False


# ==========================================
# MOSTRAR LA APLICACIÓN
# ==========================================
def mostrar_inicio():
    global contenedor_app, sesion_iniciada

    if sesion_iniciada:
        return

    sesion_iniciada = True
    tarjeta.destroy()

    # Este contenedor se crea una sola vez.
    contenedor_app = tk.Frame(ventana, bg=FONDO)
    contenedor_app.pack(fill="both", expand=True)

    # Crear el menú principal una sola vez.
    frame_inicio = crear_inicio(contenedor_app)
    frame_inicio.pack(fill="both", expand=True)


# ==========================================
# INICIAR SESIÓN
# ==========================================
def iniciar_sesion():
    usuario = entrada_correo.get().strip()
    contrasena = entrada_password.get()

    if not usuario or not contrasena:
        messagebox.showwarning(
            "Campos vacíos",
            "Ingrese usuario y contraseña."
        )
        return

    datos = {
        "nombre_usuario": usuario,
        "contrasena": contrasena
    }

    boton_login.config(state="disabled", text="Ingresando...")

    try:
        respuesta = requests.post(
            "http://localhost:3000/api/login",
            json=datos,
            timeout=10
        )

        if respuesta.status_code == 200:
            mostrar_inicio()

        elif respuesta.status_code == 401:
            messagebox.showerror(
                "Error",
                "Usuario o contraseña incorrectos."
            )

        else:
            messagebox.showerror(
                "Error",
                "No se pudo iniciar sesión. "
                f"Código: {respuesta.status_code}"
            )

    except requests.exceptions.RequestException:
        messagebox.showerror(
            "Error de conexión",
            "No se pudo conectar con el servidor. "
            "Verifique que el backend esté funcionando."
        )

    finally:
        if not sesion_iniciada and boton_login.winfo_exists():
            boton_login.config(
                state="normal",
                text="♧  Iniciar sesión"
            )


# ==========================================
# MOSTRAR / OCULTAR CONTRASEÑA
# ==========================================
def mostrar_password():
    if entrada_password.cget("show"):
        entrada_password.config(show="")
        boton_ojo.config(text="◉")
    else:
        entrada_password.config(show="●")
        boton_ojo.config(text="○")


# ==========================================
# REGISTRO
# ==========================================
def registrarse():
    messagebox.showinfo(
        "Registro",
        "Aquí se abrirá el formulario para registrarse."
    )


# ==========================================
# TARJETA DEL LOGIN
# ==========================================
tarjeta = tk.Frame(
    ventana,
    bg=BLANCO,
    width=450,
    height=590,
    highlightbackground="#E0E0D8",
    highlightthickness=1
)
tarjeta.place(relx=0.5, rely=0.5, anchor="center")
tarjeta.pack_propagate(False)


# ==========================================
# ENCABEZADO
# ==========================================
encabezado = tk.Frame(tarjeta, bg=BLANCO)
encabezado.pack(fill="x", padx=28, pady=(20, 0))

tk.Label(
    encabezado,
    text="🐾",
    font=("Arial", 23),
    bg=BLANCO,
    fg=VERDE
).pack(side="left")

tk.Label(
    encabezado,
    text="ARCA",
    font=("Arial", 14, "bold"),
    bg=BLANCO,
    fg=VERDE_OSCURO
).pack(side="left", padx=8)

tk.Label(
    encabezado,
    text="Refugio de animales",
    font=("Arial", 9),
    bg=BLANCO,
    fg="#A36E45"
).pack(side="left")


# ==========================================
# LOGO CENTRAL
# ==========================================
tk.Label(
    tarjeta,
    text="🐶",
    font=("Arial", 65),
    bg="#FFF5EA",
    width=3,
    height=1
).pack(pady=(32, 8))


tk.Label(
    tarjeta,
    text="🐾  ARCA",
    font=("Arial", 27, "bold"),
    bg=BLANCO,
    fg=VERDE
).pack()

tk.Label(
    tarjeta,
    text="Refugio de animales",
    font=("Arial", 15),
    bg=BLANCO,
    fg="#A36E45"
).pack(pady=(5, 0))

tk.Label(
    tarjeta,
    text="Inicia sesión para continuar",
    font=("Arial", 11),
    bg=BLANCO,
    fg="#888888"
).pack(pady=(4, 18))


# ==========================================
# CORREO
# ==========================================
tk.Label(
    tarjeta,
    text="Correo electrónico:",
    font=("Arial", 11),
    bg=BLANCO,
    fg=VERDE_OSCURO,
    anchor="w"
).pack(fill="x", padx=38)

entrada_correo = tk.Entry(
    tarjeta,
    font=("Arial", 12),
    bg="#FAFBF8",
    fg="#444444",
    relief="solid",
    bd=1
)
entrada_correo.pack(
    fill="x",
    padx=38,
    ipady=9,
    pady=(7, 14)
)


# ==========================================
# CONTRASEÑA
# ==========================================
tk.Label(
    tarjeta,
    text="Contraseña:",
    font=("Arial", 11),
    bg=BLANCO,
    fg=VERDE_OSCURO,
    anchor="w"
).pack(fill="x", padx=38)

contenedor_password = tk.Frame(
    tarjeta,
    bg="#FAFBF8",
    highlightbackground=BORDE,
    highlightthickness=1
)
contenedor_password.pack(
    fill="x",
    padx=38,
    pady=(7, 12)
)

entrada_password = tk.Entry(
    contenedor_password,
    font=("Arial", 12),
    bg="#FAFBF8",
    fg="#444444",
    relief="flat",
    show="●"
)
entrada_password.pack(
    side="left",
    fill="x",
    expand=True,
    padx=10,
    pady=9
)

boton_ojo = tk.Button(
    contenedor_password,
    text="○",
    font=("Arial", 12),
    bg="#FAFBF8",
    fg="#718070",
    activebackground="#FAFBF8",
    relief="flat",
    bd=0,
    cursor="hand2",
    command=mostrar_password
)
boton_ojo.pack(side="right", padx=8)


# ==========================================
# OPCIONES
# ==========================================
fila_opciones = tk.Frame(tarjeta, bg=BLANCO)
fila_opciones.pack(fill="x", padx=38, pady=(0, 16))

recordarme = tk.BooleanVar(value=False)

tk.Checkbutton(
    fila_opciones,
    text="Recordarme",
    variable=recordarme,
    font=("Arial", 10),
    bg=BLANCO,
    fg=GRIS,
    activebackground=BLANCO,
    selectcolor=BLANCO
).pack(side="left")

tk.Label(
    fila_opciones,
    text="¿Olvidaste tu contraseña?",
    font=("Arial", 9, "bold"),
    bg=BLANCO,
    fg=VERDE_OSCURO,
    cursor="hand2"
).pack(side="right")


# ==========================================
# BOTÓN DE INGRESO
# ==========================================
boton_login = tk.Button(
    tarjeta,
    text="♧  Iniciar sesión",
    font=("Arial", 13, "bold"),
    bg=VERDE,
    fg=BLANCO,
    activebackground=VERDE_CLARO,
    activeforeground=BLANCO,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=iniciar_sesion
)
boton_login.pack(fill="x", padx=38, ipady=10)


# ==========================================
# REGISTRO
# ==========================================
registro = tk.Frame(tarjeta, bg=BLANCO)
registro.pack(pady=(20, 0))

tk.Label(
    registro,
    text="¿No tienes una cuenta?",
    font=("Arial", 10),
    bg=BLANCO,
    fg="#888888"
).pack(side="left")

tk.Button(
    registro,
    text="Regístrate",
    font=("Arial", 11, "bold"),
    bg=BLANCO,
    fg=NARANJA,
    activebackground=BLANCO,
    activeforeground=NARANJA,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=registrarse
).pack(side="left", padx=4)


# ==========================================
# ENTER PARA INICIAR SESIÓN
# ==========================================
ventana.bind("<Return>", lambda event: iniciar_sesion())

ventana.mainloop()