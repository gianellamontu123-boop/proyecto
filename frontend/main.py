import tkinter as tk
from tkinter import messagebox
import requests
from frames.inicio import crear_inicio

def mostrar_inicio():

    global contenedor

    # Eliminar la pantalla de login
    tarjeta.destroy()

    # Crear contenedor para la pantalla principal
    contenedor = tk.Frame(
        ventana,
        bg="#eef1f5"
    )

    contenedor.pack(
        fill="both",
        expand=True
    )

    # Crear la pantalla de inicio
    frame_inicio = crear_inicio(contenedor)

    frame_inicio.pack(
        fill="both",
        expand=True
    )

def iniciar_sesion():

    usuario = entrada_correo.get()
    contraseña = entrada_password.get()

    if usuario == "" or contraseña == "":
        messagebox.showwarning(
            "Campos vacíos",
            "Ingrese usuario y contraseña."
        )
        return

    datos = {
        "nombre_usuario": usuario,
        "contrasena": contraseña
    }

    try:
        respuesta = requests.post(
            "http://localhost:3000/api/login",
            json=datos
        )

        if respuesta.status_code == 200:
            messagebox.showinfo(
                "Inicio de sesión",
                "¡Bienvenido!"
            )
            mostrar_inicio()

        elif respuesta.status_code == 401:
            messagebox.showerror(
                "Error",
                "Usuario o contraseña incorrectos."
            )

        else:
            messagebox.showerror(
                "Error",
                "Ocurrió un error al iniciar sesión."
            )

    except requests.exceptions.RequestException:
        messagebox.showerror(
            "Error",
            "No se pudo conectar con el servidor."
        )




# =========================
# VENTANA PRINCIPAL
# =========================
ventana = tk.Tk()
ventana.title("ARCA - Refugio de animales")
ventana.geometry("800x650")
ventana.configure(bg="#F3F1E9")
ventana.resizable(False, False)


# =========================
# COLORES
# =========================
FONDO = "#F3F1E9"
BLANCO = "#FFFFFF"
VERDE = "#4F8561"
VERDE_CLARO = "#69AE7C"
VERDE_OSCURO = "#34704C"
NARANJA = "#F47B20"
GRIS = "#777777"
BORDE = "#D5DED5"





# =========================
# MOSTRAR / OCULTAR CONTRASEÑA
# =========================
def mostrar_password():
    if entrada_password.cget("show") == "":
        entrada_password.config(show="●")
        boton_ojo.config(text="◉")
    else:
        entrada_password.config(show="")
        boton_ojo.config(text="○")


# =========================
# REGISTRO
# =========================
def registrarse():
    messagebox.showinfo(
        "Registro",
        "Aquí se abrirá el formulario para registrarse."
    )


# =========================
# TARJETA PRINCIPAL
# =========================
tarjeta = tk.Frame(
    ventana,
    bg=BLANCO,
    width=450,
    height=600,
    highlightbackground="#E0E0D8",
    highlightthickness=1
)

tarjeta.place(relx=0.5, rely=0.5, anchor="center")


# =========================
# ENCABEZADO
# =========================
encabezado = tk.Frame(tarjeta, bg=BLANCO)
encabezado.pack(fill="x", padx=28, pady=(20, 0))

logo_pequeno = tk.Label(
    encabezado,
    text="🐾",
    font=("Arial", 23),
    bg=BLANCO,
    fg=VERDE
)
logo_pequeno.pack(side="left")

titulo_pequeno = tk.Label(
    encabezado,
    text="ARCA",
    font=("Arial", 14, "bold"),
    bg=BLANCO,
    fg=VERDE_OSCURO
)
titulo_pequeno.pack(side="left", padx=8)

subtitulo_pequeno = tk.Label(
    encabezado,
    text="Refugio de animales",
    font=("Arial", 9),
    bg=BLANCO,
    fg="#A36E45"
)
subtitulo_pequeno.pack(side="left")


# =========================
# LOGO CENTRAL
# =========================
logo = tk.Label(
    tarjeta,
    text="🐶",
    font=("Arial", 75),
    bg="#FFF5EA",
    width=3,
    height=1
)
logo.pack(pady=(55, 10))


# =========================
# ARCA
# =========================
titulo = tk.Label(
    tarjeta,
    text="🐾  ARCA",
    font=("Arial", 27, "bold"),
    bg=BLANCO,
    fg=VERDE
)
titulo.pack()

subtitulo = tk.Label(
    tarjeta,
    text="Refugio de animales",
    font=("Arial", 15),
    bg=BLANCO,
    fg="#A36E45"
)
subtitulo.pack(pady=(5, 0))

texto_inicio = tk.Label(
    tarjeta,
    text="Inicia sesión para continuar",
    font=("Arial", 11),
    bg=BLANCO,
    fg="#888888"
)
texto_inicio.pack(pady=(4, 25))


# =========================
# CORREO
# =========================
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
    bd=1,
    highlightthickness=0
)

entrada_correo.pack(
    fill="x",
    padx=38,
    ipady=10,
    pady=(7, 18)
)

entrada_correo.insert(0, "")


# =========================
# CONTRASEÑA
# =========================
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
    pady=(7, 15)
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
    relief="flat",
    bd=0,
    cursor="hand2",
    command=mostrar_password
)

boton_ojo.pack(side="right", padx=8)


# =========================
# RECORDARME / OLVIDASTE
# =========================
fila_opciones = tk.Frame(
    tarjeta,
    bg=BLANCO
)

fila_opciones.pack(
    fill="x",
    padx=38,
    pady=(0, 20)
)

recordarme = tk.BooleanVar()

check = tk.Checkbutton(
    fila_opciones,
    text="Recordarme",
    variable=recordarme,
    font=("Arial", 10),
    bg=BLANCO,
    fg="#777777",
    activebackground=BLANCO,
    selectcolor=BLANCO
)

check.pack(side="left")

olvidaste = tk.Label(
    fila_opciones,
    text="¿Olvidaste tu contraseña?",
    font=("Arial", 10, "bold"),
    bg=BLANCO,
    fg=VERDE_OSCURO,
    cursor="hand2"
)

olvidaste.pack(side="right")


# =========================
# BOTÓN INICIAR SESIÓN
# =========================
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

boton_login.pack(
    fill="x",
    padx=38,
    ipady=11
)


# =========================
# REGISTRO
# =========================
registro = tk.Frame(
    tarjeta,
    bg=BLANCO
)

registro.pack(pady=(27, 0))

tk.Label(
    registro,
    text="¿No tienes una cuenta?",
    font=("Arial", 10),
    bg=BLANCO,
    fg="#888888"
).pack(side="left")

boton_registro = tk.Button(
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
)

boton_registro.pack(side="left", padx=4)


# =========================
# ENTER PARA INICIAR SESIÓN
# =========================
ventana.bind("<Return>", lambda event: iniciar_sesion())


# =========================
# INICIAR PROGRAMA
# =========================
ventana.mainloop()