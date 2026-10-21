
import tkinter as tk
from tkinter import messagebox

from frames.animales import crear_animales
from frames.adopciones import crear_adopciones
from frames.donaciones import crear_donaciones
from frames.voluntarios import voluntarios


# ==========================================
# PALETA ARCA
# ==========================================
FONDO = "#F5F3ED"
BLANCO = "#FFFFFF"

VERDE = "#4F7F5F"
VERDE_OSCURO = "#396348"
VERDE_SELECCION = "#6D997A"
VERDE_CLARO = "#EAF4ED"

NARANJA = "#F27B21"
NARANJA_CLARO = "#FFF1E5"

BEIGE_CLARO = "#F7F1E5"
GRIS = "#777777"
GRIS_CLARO = "#E5E5E0"
NEGRO = "#222222"


def crear_inicio(parent):

    # ==========================================
    # FRAME PRINCIPAL
    # ==========================================
    frame = tk.Frame(parent, bg=FONDO)

    # ==========================================
    # BARRA LATERAL: SE CREA UNA SOLA VEZ
    # ==========================================
    sidebar = tk.Frame(
        frame,
        bg=VERDE,
        width=225
    )
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    tk.Label(
        sidebar,
        text="🐾  ARCA",
        font=("Arial", 18, "bold"),
        bg=VERDE,
        fg=BLANCO
    ).pack(pady=(25, 8))

    tk.Label(
        sidebar,
        text="Refugio de animales",
        font=("Arial", 9),
        bg=VERDE,
        fg="#DCEADE"
    ).pack(pady=(0, 20))

    tk.Frame(
        sidebar,
        bg="#638C70",
        height=1
    ).pack(fill="x", pady=(0, 12))

    # ==========================================
    # CONTENIDO DERECHO
    # ==========================================
    contenido = tk.Frame(frame, bg=FONDO)
    contenido.pack(side="left", fill="both", expand=True)

    # Barra superior permanente
    barra_superior = tk.Frame(
        contenido,
        bg=BLANCO,
        height=58
    )
    barra_superior.pack(fill="x")
    barra_superior.pack_propagate(False)

    titulo_pagina = tk.Label(
        barra_superior,
        text="Inicio",
        font=("Arial", 15, "bold"),
        bg=BLANCO,
        fg=NEGRO
    )
    titulo_pagina.pack(side="left", padx=25)

    tk.Label(
        barra_superior,
        text="ARCA  |  Administración",
        font=("Arial", 10),
        bg=BLANCO,
        fg=VERDE
    ).pack(side="right", padx=20)

    # ==========================================
    # ÁREA ÚNICA PARA CAMBIAR LAS VISTAS
    # ==========================================
    area_vistas = tk.Frame(contenido, bg=FONDO)
    area_vistas.pack(fill="both", expand=True)

    # Diccionario de vistas existentes
    vistas = {
        "Inicio": None,
        "Animales": crear_animales,
        "Adopciones": crear_adopciones,
        "Donaciones": crear_donaciones,
        "Voluntarios": voluntarios,
        "Reportes": None,
        "Ayuda": None
    }

    botones_menu = {}

    # ==========================================
    # CAMBIAR CONTENIDO SIN BORRAR EL MENÚ
    # ==========================================
    def mostrar_frame(nombre):

        # Borrar solamente la vista central.
        for widget in area_vistas.winfo_children():
            widget.destroy()

        titulo_pagina.config(text=nombre)

        # Actualizar el botón seleccionado.
        for texto, boton in botones_menu.items():
            if texto == nombre:
                boton.config(bg=VERDE_SELECCION)
            else:
                boton.config(bg=VERDE)

        funcion = vistas.get(nombre)

        # Mostrar el dashboard de inicio.
        if nombre == "Inicio":
            mostrar_dashboard(area_vistas)
            return

        # Mostrar una vista todavía no implementada.
        if funcion is None:
            tk.Label(
                area_vistas,
                text=f"{nombre}\nEsta sección todavía no está disponible.",
                font=("Arial", 15),
                bg=FONDO,
                fg=GRIS,
                justify="center"
            ).pack(expand=True)
            return

        # Crear la vista dentro del área central.
        try:
            nuevo_frame = funcion(area_vistas)

            if nuevo_frame is not None:
                nuevo_frame.pack(
                    fill="both",
                    expand=True
                )

        except Exception as error:
            messagebox.showerror(
                "Error al abrir la vista",
                f"No se pudo abrir {nombre}.\n\n{error}"
            )

    # ==========================================
    # BOTONES DEL MENÚ
    # ==========================================
    opciones = [
        ("⌂", "Inicio"),
        ("♧", "Animales"),
        ("♡", "Adopciones"),
        ("♔", "Donaciones"),
        ("♧", "Voluntarios"),
        ("▤", "Reportes"),
        ("?", "Ayuda")
    ]

    for icono, nombre in opciones:

        boton = tk.Button(
            sidebar,
            text=f"  {icono}     {nombre}",
            font=("Arial", 11),
            bg=VERDE_SELECCION if nombre == "Inicio" else VERDE,
            fg=BLANCO,
            activebackground=VERDE_SELECCION,
            activeforeground=BLANCO,
            anchor="w",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=15,
            pady=13,
            command=lambda n=nombre: mostrar_frame(n)
        )

        boton.pack(fill="x", padx=8, pady=2)
        botones_menu[nombre] = boton

    # ==========================================
    # USUARIO EN LA PARTE INFERIOR
    # ==========================================
    usuario_frame = tk.Frame(sidebar, bg=VERDE)
    usuario_frame.pack(side="bottom", fill="x", padx=15, pady=20)

    tk.Label(
        usuario_frame,
        text="●",
        font=("Arial", 23),
        bg=VERDE,
        fg="#DCEADE"
    ).pack(side="left", padx=(0, 9))

    usuario_texto = tk.Frame(usuario_frame, bg=VERDE)
    usuario_texto.pack(side="left")

    tk.Label(
        usuario_texto,
        text="Usuario",
        font=("Arial", 10, "bold"),
        bg=VERDE,
        fg=BLANCO
    ).pack(anchor="w")

    tk.Label(
        usuario_texto,
        text="Administrador",
        font=("Arial", 9),
        bg=VERDE,
        fg="#D5E5D8"
    ).pack(anchor="w")

    # ==========================================
    # DASHBOARD DE INICIO
    # ==========================================
    def mostrar_dashboard(parent_dashboard):

        dashboard = tk.Frame(
            parent_dashboard,
            bg=FONDO
        )
        dashboard.pack(
            fill="both",
            expand=True,
            padx=22,
            pady=22
        )

        tk.Label(
            dashboard,
            text="Panel principal",
            font=("Arial", 21, "bold"),
            bg=FONDO,
            fg=VERDE_OSCURO
        ).pack(anchor="w")

        tk.Label(
            dashboard,
            text="Resumen general del refugio",
            font=("Arial", 11),
            bg=FONDO,
            fg=GRIS
        ).pack(anchor="w", pady=(4, 20))

        tarjetas = tk.Frame(dashboard, bg=FONDO)
        tarjetas.pack(fill="x")

        datos = [
            ("♧", "42", "Animales en el refugio", VERDE, VERDE_CLARO),
            ("♡", "18", "Animales adoptados", NARANJA, NARANJA_CLARO),
            ("♧", "7", "Adopciones este mes", VERDE, VERDE_CLARO),
            ("♔", "12", "Donaciones recibidas", "#9B7944", BEIGE_CLARO)
        ]

        for columna, (icono, numero, descripcion, color, fondo_icono) in enumerate(datos):

            tarjeta_dashboard = tk.Frame(
                tarjetas,
                bg=BLANCO,
                highlightbackground=GRIS_CLARO,
                highlightthickness=1
            )

            tarjeta_dashboard.grid(
                row=0,
                column=columna,
                sticky="nsew",
                padx=5
            )

            tarjetas.columnconfigure(columna, weight=1)

            tk.Label(
                tarjeta_dashboard,
                text=icono,
                font=("Arial", 21),
                bg=fondo_icono,
                fg=color,
                width=3
            ).pack(anchor="w", padx=12, pady=(15, 8))

            tk.Label(
                tarjeta_dashboard,
                text=numero,
                font=("Arial", 24, "bold"),
                bg=BLANCO,
                fg=color
            ).pack(anchor="w", padx=12)

            tk.Label(
                tarjeta_dashboard,
                text=descripcion,
                font=("Arial", 9),
                bg=BLANCO,
                fg=GRIS,
                wraplength=145,
                justify="left"
            ).pack(anchor="w", padx=12, pady=(3, 15))

        # ======================================
        # ACCESOS RÁPIDOS
        # ======================================
        accesos = tk.Frame(
            dashboard,
            bg=BLANCO,
            highlightbackground=GRIS_CLARO,
            highlightthickness=1
        )
        accesos.pack(fill="x", pady=(25, 0))

        tk.Label(
            accesos,
            text="Accesos rápidos",
            font=("Arial", 14, "bold"),
            bg=BLANCO,
            fg=NEGRO
        ).pack(anchor="w", padx=18, pady=(18, 10))

        botones_rapidos = tk.Frame(accesos, bg=BLANCO)
        botones_rapidos.pack(fill="x", padx=13, pady=(0, 18))

        accesos_disponibles = [
            ("Registrar animal", "Animales"),
            ("Gestionar adopciones", "Adopciones"),
            ("Ver donaciones", "Donaciones"),
            ("Gestionar voluntarios", "Voluntarios")
        ]

        for texto, destino in accesos_disponibles:

            tk.Button(
                botones_rapidos,
                text=texto,
                font=("Arial", 10, "bold"),
                bg=VERDE_CLARO,
                fg=BLANCO,
                activebackground=VERDE,
                activeforeground=BLANCO,
                relief="flat",
                cursor="hand2",
                command=lambda n=destino: mostrar_frame(n)
            ).pack(
                side="left",
                fill="x",
                expand=True,
                padx=5,
                ipady=9
            )

        # Aviso
        tk.Label(
            dashboard,
            text="ARCA · Un hogar para cada huella",
            font=("Arial", 10, "italic"),
            bg=FONDO,
            fg=VERDE
        ).pack(anchor="w", side="bottom", pady=(15, 0))

    # Mostrar el dashboard inicial.
    mostrar_dashboard(area_vistas)

    return frame
