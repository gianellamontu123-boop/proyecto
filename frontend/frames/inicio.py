
import tkinter as tk
from tkinter import messagebox
import requests

from frames.animales import crear_animales
from frames.adopciones import crear_adopciones
from frames.donaciones import crear_donaciones
from frames.voluntarios import voluntarios
from frames.personas import crear_personas
from frames.reportes import crear_reportes


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

API_REPORTES = "http://localhost:3000/api/reportes"


def obtener_datos(ruta):
    try:
        respuesta = requests.get(
            f"{API_REPORTES}/{ruta}",
            timeout=5
        )
        respuesta.raise_for_status()
        return respuesta.json()

    except requests.exceptions.RequestException as error:
        messagebox.showerror(
            "Error de conexión",
            f"No se pudieron obtener los datos.\n\n{error}"
        )
        return None


def crear_inicio(parent):

    frame = tk.Frame(parent, bg=FONDO)

    # ==========================================
    # BARRA LATERAL
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

    area_vistas = tk.Frame(contenido, bg=FONDO)
    area_vistas.pack(fill="both", expand=True)

    vistas = {
        "Inicio": None,
        "Animales": crear_animales,
        "Adopciones": crear_adopciones,
        "Donaciones": crear_donaciones,
        "Voluntarios": voluntarios,
        "Personas": crear_personas,
        "Reportes": crear_reportes,
        "Ayuda": None
    }

    botones_menu = {}

    # ==========================================
    # CAMBIAR VISTAS
    # ==========================================
    def mostrar_frame(nombre):

        for widget in area_vistas.winfo_children():
            widget.destroy()

        titulo_pagina.config(text=nombre)

        for texto, boton in botones_menu.items():
            boton.config(
                bg=VERDE_SELECCION if texto == nombre else VERDE
            )

        funcion = vistas.get(nombre)

        if nombre == "Inicio":
            mostrar_dashboard(area_vistas)
            return

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

        contenedor_vista = tk.Frame(area_vistas, bg=FONDO)
        contenedor_vista.pack(fill="both", expand=True)

        try:
            nuevo_frame = funcion(contenedor_vista)

            if nuevo_frame is not None and not nuevo_frame.winfo_manager():
                nuevo_frame.pack(fill="both", expand=True)

        except Exception as error:
            messagebox.showerror(
                "Error al abrir la vista",
                f"No se pudo abrir {nombre}.\n\n{error}"
            )

    # ==========================================
    # MENÚ
    # ==========================================
    opciones = [
        ("⌂", "Inicio"),
        ("P", "Personas"),
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
    # USUARIO
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
    # DASHBOARD
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

        # ======================================
        # CONSULTAR LAS DOS RUTAS
        # ======================================
        datos_animales = obtener_datos("animales-por-estado")
        datos_adopciones = obtener_datos("adopciones-por-mes")

        tarjetas = tk.Frame(dashboard, bg=FONDO)
        tarjetas.pack(fill="x")

        # Cantidades de animales
        total_animales = (
            datos_animales.get("total", 0)
            if datos_animales else 0
        )

        # Cantidades de adopciones
        total_adopciones = (
            datos_adopciones.get("total", 0)
            if datos_adopciones else 0
        )

        # Datos para las tarjetas
        datos = [
            ("♧", total_animales, "Animales registrados",
             VERDE, VERDE_CLARO),

            ("♡", total_adopciones, "Adopciones del año",
             NARANJA, NARANJA_CLARO)
        ]

        for columna, (icono, numero, descripcion, color, fondo_icono) in enumerate(datos):

            tarjeta = tk.Frame(
                tarjetas,
                bg=BLANCO,
                highlightbackground=GRIS_CLARO,
                highlightthickness=1
            )

            tarjeta.grid(
                row=0,
                column=columna,
                sticky="nsew",
                padx=5
            )

            tarjetas.columnconfigure(columna, weight=1)

            tk.Label(
                tarjeta,
                text=icono,
                font=("Arial", 21),
                bg=fondo_icono,
                fg=color,
                width=3
            ).pack(anchor="w", padx=12, pady=(15, 8))

            tk.Label(
                tarjeta,
                text=str(numero),
                font=("Arial", 24, "bold"),
                bg=BLANCO,
                fg=color
            ).pack(anchor="w", padx=12)

            tk.Label(
                tarjeta,
                text=descripcion,
                font=("Arial", 9),
                bg=BLANCO,
                fg=GRIS
            ).pack(anchor="w", padx=12, pady=(3, 15))

        # ======================================
        # ANIMALES POR ESTADO
        # ======================================
        seccion_animales = tk.Frame(
            dashboard,
            bg=BLANCO,
            highlightbackground=GRIS_CLARO,
            highlightthickness=1
        )
        seccion_animales.pack(fill="x", pady=(20, 0))

        tk.Label(
            seccion_animales,
            text="Animales por estado",
            font=("Arial", 14, "bold"),
            bg=BLANCO,
            fg=NEGRO
        ).pack(anchor="w", padx=18, pady=(15, 10))

        if datos_animales:

            for item in datos_animales.get("datos", []):

                fila = tk.Frame(seccion_animales, bg=BLANCO)
                fila.pack(fill="x", padx=20, pady=4)

                tk.Label(
                    fila,
                    text=item["estado"],
                    font=("Arial", 10),
                    bg=BLANCO,
                    fg=GRIS,
                    width=20,
                    anchor="w"
                ).pack(side="left")

                tk.Label(
                    fila,
                    text=str(item["cantidad"]),
                    font=("Arial", 10, "bold"),
                    bg=BLANCO,
                    fg=VERDE_OSCURO
                ).pack(side="right")

        else:
            tk.Label(
                seccion_animales,
                text="No se pudieron cargar los datos.",
                bg=BLANCO,
                fg=GRIS
            ).pack(pady=10)

        # ======================================
        # ADOPCIONES POR MES CON SCROLL
        # ======================================
        seccion_adopciones = tk.Frame(
            dashboard,
            bg=BLANCO,
            highlightbackground=GRIS_CLARO,
            highlightthickness=1
        )
        seccion_adopciones.pack(fill="both", expand=True, pady=(15, 0))

        tk.Label(
            seccion_adopciones,
            text="Adopciones por mes",
            font=("Arial", 14, "bold"),
            bg=BLANCO,
            fg=NEGRO
        ).pack(anchor="w", padx=18, pady=(15, 10))

        # Contenedor del scroll
        contenedor_scroll = tk.Frame(seccion_adopciones, bg=BLANCO)
        contenedor_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        canvas = tk.Canvas(
            contenedor_scroll,
            bg=BLANCO,
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            contenedor_scroll,
            orient="vertical",
            command=canvas.yview
        )

        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        contenido_scroll = tk.Frame(canvas, bg=BLANCO)

        ventana_scroll = canvas.create_window(
            (0, 0),
            window=contenido_scroll,
            anchor="nw"
        )

        def actualizar_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def ajustar_ancho(event):
            canvas.itemconfig(ventana_scroll, width=event.width)

        contenido_scroll.bind("<Configure>", actualizar_scroll)
        canvas.bind("<Configure>", ajustar_ancho)

        # Mostrar los 12 meses
        if datos_adopciones:

            for item in datos_adopciones.get("datos", []):

                fila = tk.Frame(contenido_scroll, bg=BLANCO)
                fila.pack(fill="x", padx=20, pady=4)

                tk.Label(
                    fila,
                    text=item["mes"],
                    font=("Arial", 9),
                    bg=BLANCO,
                    fg=GRIS,
                    width=20,
                    anchor="w"
                ).pack(side="left")

                tk.Label(
                    fila,
                    text=str(item["cantidad"]),
                    font=("Arial", 9, "bold"),
                    bg=BLANCO,
                    fg=NARANJA
                ).pack(side="right")

        else:
            tk.Label(
                contenido_scroll,
                text="No se pudieron cargar los datos.",
                bg=BLANCO,
                fg=GRIS
            ).pack(pady=10)
        # ======================================
        # ACCESOS RÁPIDOS
        # ======================================
        accesos = tk.Frame(
            dashboard,
            bg=BLANCO,
            highlightbackground=GRIS_CLARO,
            highlightthickness=1
        )
        accesos.pack(fill="x", pady=(20, 0))

        tk.Label(
            accesos,
            text="Accesos rápidos",
            font=("Arial", 14, "bold"),
            bg=BLANCO,
            fg=NEGRO
        ).pack(anchor="w", padx=18, pady=(15, 10))

        botones_rapidos = tk.Frame(accesos, bg=BLANCO)
        botones_rapidos.pack(fill="x", padx=13, pady=(0, 15))

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
                bg=VERDE,
                fg=BLANCO,
                activebackground=VERDE_OSCURO,
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

        tk.Label(
            dashboard,
            text="ARCA · Un hogar para cada huella",
            font=("Arial", 10, "italic"),
            bg=FONDO,
            fg=VERDE
        ).pack(anchor="w", side="bottom", pady=(15, 0))

    # Mostrar inicio
    mostrar_dashboard(area_vistas)

    return frame
