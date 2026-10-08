import tkinter as tk
from frames.adopciones import crear_adopciones

# ==============================
# COLORES
# ==============================
VERDE = "#4F7F5F"
VERDE_OSCURO = "#396348"
VERDE_CLARO = "#EAF4ED"

NARANJA = "#F27B21"
NARANJA_CLARO = "#FFF1E5"

BEIGE = "#F5F3ED"
BEIGE_CLARO = "#F7F1E5"

BLANCO = "#FFFFFF"
GRIS = "#777777"
GRIS_CLARO = "#E5E5E0"
NEGRO = "#222222"


def crear_inicio(parent):

    # ==========================================
    # FRAME PRINCIPAL
    # ==========================================
    frame = tk.Frame(
        parent,
        bg=BEIGE
    )

    def abrir_adopciones():
        vent = tk.Toplevel(frame)
        vent.geometry("1000x650")
        frame_adopciones=crear_adopciones(vent)
        frame_adopciones.pack(
            fill="both",
            expand=True
        )
    abrir_adopciones()
    # ==========================================
    # BARRA LATERAL
    # ==========================================
    sidebar = tk.Frame(
        frame,
        bg=VERDE,
        width=225
    )

    sidebar.pack(
        side="left",
        fill="y"
    )

    sidebar.pack_propagate(False)

    # ---------- Logo ----------
    logo = tk.Label(
        sidebar,
        text="ARCA",
        font=("Arial", 17, "bold"),
        bg=VERDE,
        fg="white"
    )

    logo.pack(
        pady=(27, 25)
    )

    # Línea
    tk.Frame(
        sidebar,
        bg="#638C70",
        height=1
    ).pack(fill="x")

    # ==========================================
    # MENÚ LATERAL
    # ==========================================

    opciones = [
        ("⌂", "Inicio"),
        ("♧", "Animales"),
        ("♡", "Adopciones"),
        ("♔", "Donaciones"),
        ("♧", "Voluntarios"),
        ("│", "Reportes"),
        ("?", "Ayuda")
    ]

    for icono, texto in opciones:

        fila = tk.Frame(
            sidebar,
            bg=VERDE,
            height=48
        )

        fila.pack(
            fill="x"
        )

        # Inicio seleccionado visualmente
        if texto == "Inicio":
            fila.config(bg="#6D997A")

        icono_label = tk.Label(
            fila,
            text=icono,
            font=("Arial", 18),
            bg=fila.cget("bg"),
            fg="white"
        )

        icono_label.pack(
            side="left",
            padx=(20, 12)
        )

        texto_label = tk.Label(
            fila,
            text=texto,
            font=("Arial", 11),
            bg=fila.cget("bg"),
            fg="white",
            anchor="w"
        )

        texto_label.pack(
            side="left"
        )

    # ==========================================
    # USUARIO ABAJO
    # ==========================================

    usuario_frame = tk.Frame(
        sidebar,
        bg=VERDE
    )

    usuario_frame.pack(
        side="bottom",
        fill="x",
        pady=15,
        padx=18
    )

    tk.Label(
        usuario_frame,
        text="●",
        font=("Arial", 25),
        bg=VERDE,
        fg="#DCEADE"
    ).pack(side="left")

    usuario_texto = tk.Frame(
        usuario_frame,
        bg=VERDE
    )

    usuario_texto.pack(
        side="left",
        padx=8
    )

    tk.Label(
        usuario_texto,
        text="Usuario",
        font=("Arial", 10, "bold"),
        bg=VERDE,
        fg="white"
    ).pack(anchor="w")

    tk.Label(
        usuario_texto,
        text="Administrador",
        font=("Arial", 9),
        bg=VERDE,
        fg="#D5E5D8"
    ).pack(anchor="w")

    tk.Label(
        usuario_frame,
        text="⌄",
        font=("Arial", 14),
        bg=VERDE,
        fg="white"
    ).pack(side="right")

    # ==========================================
    # CONTENIDO DERECHO
    # ==========================================

    contenido = tk.Frame(
        frame,
        bg=BEIGE
    )

    contenido.pack(
        side="left",
        fill="both",
        expand=True
    )

    # ==========================================
    # BARRA SUPERIOR
    # ==========================================

    barra_superior = tk.Frame(
        contenido,
        bg=BLANCO,
        height=58
    )

    barra_superior.pack(
        fill="x"
    )

    barra_superior.pack_propagate(False)

    tk.Label(
        barra_superior,
        text="☰",
        font=("Arial", 20),
        bg=BLANCO,
        fg=VERDE
    ).pack(
        side="left",
        padx=(25, 18)
    )

    tk.Label(
        barra_superior,
        text="Inicio",
        font=("Arial", 15),
        bg=BLANCO,
        fg=NEGRO
    ).pack(
        side="left"
    )

    # Parte derecha
    tk.Label(
        barra_superior,
        text="●",
        font=("Arial", 16),
        bg=BLANCO,
        fg="#7C9C84"
    ).pack(
        side="right",
        padx=15
    )

    tk.Label(
        barra_superior,
        text="● ● ●",
        font=("Arial", 12),
        bg=BLANCO,
        fg="#D9B98D"
    ).pack(
        side="right",
        padx=15
    )

    # ==========================================
    # CONTENEDOR DEL DASHBOARD
    # ==========================================

    dashboard = tk.Frame(
        contenido,
        bg=BEIGE
    )

    dashboard.pack(
        fill="both",
        expand=True,
        padx=23,
        pady=23
    )

    # ==========================================
    # TARJETAS SUPERIORES
    # ==========================================

    tarjetas = tk.Frame(
        dashboard,
        bg=BEIGE
    )

    tarjetas.pack(
        fill="x"
    )

    datos_tarjetas = [
        (
            "♧",
            "42",
            "Animales en el refugio",
            VERDE,
            VERDE_CLARO
        ),
        (
            "♡",
            "18",
            "Animales adoptados",
            NARANJA,
            NARANJA_CLARO
        ),
        (
            "♧",
            "7",
            "Adopciones este mes",
            VERDE,
            VERDE_CLARO
        ),
        (
            "♔",
            "12",
            "Donaciones recibidas",
            "#9B7944",
            BEIGE_CLARO
        )
    ]

    for i, datos in enumerate(datos_tarjetas):

        icono, numero, descripcion, color, fondo_icono = datos

        tarjeta = tk.Frame(
            tarjetas,
            bg=BLANCO,
            highlightbackground=GRIS_CLARO,
            highlightthickness=1
        )

        tarjeta.grid(
            row=0,
            column=i,
            sticky="nsew",
            padx=5
        )

        tarjetas.columnconfigure(
            i,
            weight=1
        )

        # Icono
        tk.Label(
            tarjeta,
            text=icono,
            font=("Arial", 22),
            bg=fondo_icono,
            fg=color,
            width=3,
            height=1
        ).pack(
            anchor="w",
            padx=18,
            pady=(18, 8)
        )

        # Número
        tk.Label(
            tarjeta,
            text=numero,
            font=("Arial", 27, "bold"),
            bg=BLANCO,
            fg=color
        ).pack(
            anchor="w",
            padx=18
        )

        # Descripción
        tk.Label(
            tarjeta,
            text=descripcion,
            font=("Arial", 10),
            bg=BLANCO,
            fg="#888888"
        ).pack(
            anchor="w",
            padx=18
        )

        # Ver más
        tk.Label(
            tarjeta,
            text="Ver más →",
            font=("Arial", 10),
            bg=BLANCO,
            fg=color
        ).pack(
            anchor="w",
            padx=18,
            pady=(14, 18)
        )

    # ==========================================
    # PARTE INFERIOR
    # ==========================================

    parte_inferior = tk.Frame(
        dashboard,
        bg=BEIGE
    )

    parte_inferior.pack(
        fill="both",
        expand=True,
        pady=(23, 0)
    )

    # ==========================================
    # RESUMEN MENSUAL
    # ==========================================

    resumen = tk.Frame(
        parte_inferior,
        bg=BLANCO,
        highlightbackground=GRIS_CLARO,
        highlightthickness=1
    )

    resumen.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 10)
    )

    # Título
    titulo_resumen = tk.Frame(
        resumen,
        bg=BLANCO
    )

    titulo_resumen.pack(
        fill="x",
        padx=20,
        pady=(18, 10)
    )

    tk.Label(
        titulo_resumen,
        text="Resumen mensual",
        font=("Arial", 14, "bold"),
        bg=BLANCO,
        fg=NEGRO
    ).pack(side="left")

    tk.Label(
        titulo_resumen,
        text="↗",
        font=("Arial", 16),
        bg=BLANCO,
        fg=VERDE
    ).pack(side="right")

    # Encabezados
    encabezados = tk.Frame(
        resumen,
        bg=BLANCO
    )

    encabezados.pack(
        fill="x",
        padx=20
    )

    nombres = [
        ("MES", 0),
        ("ANIMALES", 1),
        ("ADOPTADOS", 2),
        ("INGRESOS", 3),
        ("VARIACIÓN", 4)
    ]

    for nombre, columna in nombres:

        tk.Label(
            encabezados,
            text=nombre,
            font=("Arial", 9),
            bg=BLANCO,
            fg="#888888",
            anchor="w"
        ).grid(
            row=0,
            column=columna,
            sticky="w",
            padx=5,
            pady=7
        )

        encabezados.columnconfigure(
            columna,
            weight=1
        )

    # Datos
    meses = [
        ("Ene", "38", "5", "43", "—"),
        ("Feb", "40", "8", "48", "▲ 5%"),
        ("Mar", "35", "12", "47", "▼ 12%"),
        ("Abr", "42", "9", "51", "▲ 20%"),
        ("May", "44", "11", "55", "▲ 5%"),
        ("Jun", "42", "7", "49", "▼ 5%")
    ]

    for fila, datos in enumerate(meses):

        linea = tk.Frame(
            resumen,
            bg="#F9FAF8"
        )

        linea.pack(
            fill="x",
            padx=20
        )

        mes, animales, adoptados, ingresos, variacion = datos

        tk.Label(
            linea,
            text=mes,
            font=("Arial", 9),
            bg="#F9FAF8",
            fg=NEGRO,
            width=8,
            anchor="w"
        ).pack(side="left")

        # Barra animales
        barra_animales = tk.Frame(
            linea,
            bg="#E7EFE9",
            width=80,
            height=7
        )

        barra_animales.pack(
            side="left",
            padx=5
        )

        tk.Frame(
            barra_animales,
            bg=VERDE,
            width=55,
            height=7
        ).place(
            x=0,
            y=0
        )

        tk.Label(
            linea,
            text=animales,
            font=("Arial", 9),
            bg="#F9FAF8",
            fg=VERDE
        ).pack(
            side="left",
            padx=(0, 25)
        )

        tk.Label(
            linea,
            text=adoptados,
            font=("Arial", 9),
            bg="#F9FAF8",
            fg=NARANJA,
            width=10,
            anchor="w"
        ).pack(side="left")

        tk.Label(
            linea,
            text=ingresos,
            font=("Arial", 9),
            bg="#F9FAF8",
            fg="#555555",
            width=12,
            anchor="w"
        ).pack(side="left")

        tk.Label(
            linea,
            text=variacion,
            font=("Arial", 9),
            bg="#F9FAF8",
            fg=VERDE if "▲" in variacion else NARANJA
        ).pack(side="left")

        tk.Frame(
            linea,
            bg="#E3E6E3",
            height=1
        ).pack(
            side="bottom",
            fill="x"
        )

    # Total
    total = tk.Frame(
        resumen,
        bg=BLANCO
    )

    total.pack(
        fill="x",
        padx=20,
        pady=10
    )

    tk.Label(
        total,
        text="TOTAL",
        font=("Arial", 9),
        bg=BLANCO,
        fg="#666666",
        width=12,
        anchor="w"
    ).pack(side="left")

    tk.Label(
        total,
        text="241",
        font=("Arial", 9),
        bg=BLANCO,
        fg=VERDE
    ).pack(side="left", padx=20)

    tk.Label(
        total,
        text="52",
        font=("Arial", 9),
        bg=BLANCO,
        fg=NARANJA
    ).pack(side="left", padx=35)

    tk.Label(
        total,
        text="293",
        font=("Arial", 9),
        bg=BLANCO,
        fg=NEGRO
    ).pack(side="left", padx=30)

    # ==========================================
    # ACTIVIDAD RECIENTE
    # ==========================================

    actividad = tk.Frame(
        parte_inferior,
        bg=BLANCO,
        width=300,
        highlightbackground=GRIS_CLARO,
        highlightthickness=1
    )

    actividad.pack(
        side="right",
        fill="y"
    )

    actividad.pack_propagate(False)

    encabezado_actividad = tk.Frame(
        actividad,
        bg=BLANCO
    )

    encabezado_actividad.pack(
        fill="x",
        padx=20,
        pady=(18, 12)
    )

    tk.Label(
        encabezado_actividad,
        text="Actividad reciente",
        font=("Arial", 14, "bold"),
        bg=BLANCO,
        fg=NEGRO
    ).pack(side="left")

    tk.Label(
        encabezado_actividad,
        text="Ver todo",
        font=("Arial", 9),
        bg=BLANCO,
        fg=VERDE
    ).pack(side="right")

    # Actividades
    actividades = [
        ("♧", "Nuevo animal ingresado", "Hoy, 10:30", VERDE_CLARO, VERDE),
        ("♡", "Adopción realizada", "Hoy, 09:15", NARANJA_CLARO, NARANJA),
        ("♔", "Donación recibida", "Ayer, 16:45", BEIGE_CLARO, "#9B7944")
    ]

    for icono, titulo, hora, fondo, color in actividades:

        fila = tk.Frame(
            actividad,
            bg=BLANCO
        )

        fila.pack(
            fill="x",
            padx=18,
            pady=7
        )

        tk.Label(
            fila,
            text=icono,
            font=("Arial", 17),
            bg=fondo,
            fg=color,
            width=3
        ).pack(side="left")

        textos = tk.Frame(
            fila,
            bg=BLANCO
        )

        textos.pack(
            side="left",
            padx=10
        )

        tk.Label(
            textos,
            text=titulo,
            font=("Arial", 10),
            bg=BLANCO,
            fg=NEGRO
        ).pack(anchor="w")

        tk.Label(
            textos,
            text=hora,
            font=("Arial", 9),
            bg=BLANCO,
            fg="#999999"
        ).pack(anchor="w")

    # ==========================================
    # CAJA REGISTRAR ANIMAL
    # ==========================================

    registrar = tk.Frame(
        actividad,
        bg="#FCFEFC",
        highlightbackground="#C8D8CC",
        highlightthickness=1
    )

    registrar.pack(
        fill="x",
        padx=18,
        pady=(15, 10)
    )

    tk.Label(
        registrar,
        text="♧",
        font=("Arial", 20),
        bg=VERDE_CLARO,
        fg=VERDE
    ).pack(
        side="left",
        padx=10,
        pady=10
    )

    textos_registrar = tk.Frame(
        registrar,
        bg="#FCFEFC"
    )

    textos_registrar.pack(
        side="left",
        pady=8
    )

    tk.Label(
        textos_registrar,
        text="Registrar animal",
        font=("Arial", 10, "bold"),
        bg="#FCFEFC",
        fg=VERDE_OSCURO
    ).pack(anchor="w")

    tk.Label(
        textos_registrar,
        text="Agregar nuevo ingreso",
        font=("Arial", 9),
        bg="#FCFEFC",
        fg="#999999"
    ).pack(anchor="w")

    tk.Label(
        registrar,
        text="→",
        font=("Arial", 20),
        bg="#FCFEFC",
        fg=VERDE
    ).pack(
        side="right",
        padx=10
    )

    return frame