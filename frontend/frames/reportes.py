
import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime
import math


# ==========================================
# CONFIGURACIÓN DE LA API
# ==========================================

API_ANIMALES = "http://localhost:3000/api/reportes/animales-por-estado"
API_ADOPCIONES = "http://localhost:3000/api/reportes/adopciones-por-mes"


# ==========================================
# INTERFAZ DE REPORTES
# ==========================================

def crear_reportes(parent):

    # ==========================================
    # COLORES ARCA
    # ==========================================

    VERDE = "#4F7F5F"
    VERDE_OSCURO = "#396348"
    VERDE_CLARO = "#EAF4ED"
    FONDO = "#F5F3ED"
    BLANCO = "#FFFFFF"
    TEXTO = "#222222"
    GRIS = "#777777"
    GRIS_CLARO = "#E5E5E0"
    NARANJA = "#F27B21"

    COLORES_ESTADOS = {
        "Activo": "#4F7F5F",
        "Saludable": "#82A98B",
        "En tratamiento": "#F27B21",
        "Adoptado": "#D6A34D",
        "Inactivo": "#999999"
    }

    # ==========================================
    # LIMPIAR PANTALLA ANTERIOR
    # ==========================================

    for widget in parent.winfo_children():
        widget.destroy()

    parent.configure(bg=FONDO)

    datos_animales = []
    datos_adopciones = []

    anio_actual = datetime.now().year

    # ==========================================
    # ENCABEZADO
    # ==========================================

    encabezado = tk.Frame(
        parent,
        bg=BLANCO,
        height=60
    )
    encabezado.pack(fill="x")
    encabezado.pack_propagate(False)

    tk.Label(
        encabezado,
        text="☰   Reportes",
        font=("Segoe UI", 16, "bold"),
        bg=BLANCO,
        fg=TEXTO
    ).pack(side="left", padx=25, pady=15)

    tk.Label(
        encabezado,
        text="ARCA",
        font=("Segoe UI", 12, "bold"),
        bg=BLANCO,
        fg=VERDE
    ).pack(side="right", padx=25)

    # ==========================================
    # PANEL PRINCIPAL
    # ==========================================

    panel = tk.Frame(parent, bg=FONDO)
    panel.pack(fill="both", expand=True)

    # ==========================================
    # TÍTULO
    # ==========================================

    titulo = tk.Frame(panel, bg=FONDO)
    titulo.pack(fill="x", padx=25, pady=(22, 10))

    tk.Label(
        titulo,
        text="Panel de Reportes",
        font=("Segoe UI", 18, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).pack(anchor="w")

    tk.Label(
        titulo,
        text="Estadísticas generales del refugio ARCA",
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=GRIS
    ).pack(anchor="w", pady=(3, 0))

    # ==========================================
    # FILTRO DE AÑO Y ACTUALIZACIÓN
    # ==========================================

    barra = tk.Frame(panel, bg=FONDO)
    barra.pack(fill="x", padx=25, pady=(5, 15))

    tk.Label(
        barra,
        text="Año de consulta:",
        font=("Segoe UI", 10, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).pack(side="left", padx=(0, 8))

    seleccion_anio = tk.StringVar(value=str(anio_actual))

    combo_anio = ttk.Combobox(
        barra,
        textvariable=seleccion_anio,
        values=[str(anio_actual - i) for i in range(5)],
        state="readonly",
        width=9,
        font=("Segoe UI", 10)
    )
    combo_anio.pack(side="left", ipady=4)

    # ==========================================
    # TARJETAS DE TOTALES
    # ==========================================

    tarjetas = tk.Frame(panel, bg=FONDO)
    tarjetas.pack(fill="x", padx=25, pady=(0, 18))

    tarjetas.grid_columnconfigure(0, weight=1)
    tarjetas.grid_columnconfigure(1, weight=1)

    def crear_tarjeta(columna, icono, titulo_tarjeta, color):

        tarjeta = tk.Frame(
            tarjetas,
            bg=BLANCO,
            highlightbackground="#E2E7E2",
            highlightthickness=1
        )

        tarjeta.grid(
            row=0,
            column=columna,
            sticky="nsew",
            padx=(0, 7) if columna == 0 else (7, 0),
            ipady=5
        )

        tk.Label(
            tarjeta,
            text=icono,
            font=("Segoe UI", 19),
            bg=BLANCO,
            fg=color
        ).pack(pady=(8, 2))

        numero = tk.Label(
            tarjeta,
            text="0",
            font=("Segoe UI", 22, "bold"),
            bg=BLANCO,
            fg=color
        )
        numero.pack()

        tk.Label(
            tarjeta,
            text=titulo_tarjeta,
            font=("Segoe UI", 10),
            bg=BLANCO,
            fg=GRIS
        ).pack(pady=(2, 10))

        return numero

    total_animales = crear_tarjeta(
        0, "🐾", "Animales registrados", VERDE
    )

    total_adopciones = crear_tarjeta(
        1, "♡", "Adopciones del año", NARANJA
    )

    # ==========================================
    # CONTENEDOR DE GRÁFICOS
    # ==========================================

    graficos = tk.Frame(panel, bg=FONDO)
    graficos.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=(0, 20)
    )

    graficos.grid_columnconfigure(0, weight=1)
    graficos.grid_columnconfigure(1, weight=1)
    graficos.grid_rowconfigure(0, weight=1)

    # ==========================================
    # TARJETA DE CADA GRÁFICO
    # ==========================================

    def crear_marco_grafico(columna, titulo_grafico, descripcion):

        marco = tk.Frame(
            graficos,
            bg=BLANCO,
            highlightbackground="#E1E7E1",
            highlightthickness=1
        )

        marco.grid(
            row=0,
            column=columna,
            sticky="nsew",
            padx=(0, 7) if columna == 0 else (7, 0)
        )

        tk.Label(
            marco,
            text=titulo_grafico,
            font=("Segoe UI", 12, "bold"),
            bg=BLANCO,
            fg=TEXTO
        ).pack(anchor="w", padx=15, pady=(15, 3))

        tk.Label(
            marco,
            text=descripcion,
            font=("Segoe UI", 9),
            bg=BLANCO,
            fg=GRIS
        ).pack(anchor="w", padx=15)

        lienzo = tk.Canvas(
            marco,
            bg=BLANCO,
            highlightthickness=0
        )
        lienzo.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=10
        )

        return lienzo

    # GRÁFICO 1: ANIMALES POR ESTADO

    grafico_animales = crear_marco_grafico(
        0,
        "Animales por estado",
        "Distribución de los animales registrados"
    )

    # GRÁFICO 2: ADOPCIONES POR MES

    grafico_adopciones = crear_marco_grafico(
        1,
        "Adopciones por mes",
        "Cantidad de adopciones durante el año seleccionado"
    )

    # ==========================================
    # DIBUJAR GRÁFICO CIRCULAR
    # ==========================================

    def dibujar_animales(event=None):

        grafico_animales.delete("all")

        if not datos_animales:
            grafico_animales.create_text(
                150, 100,
                text="No hay datos disponibles",
                fill=GRIS,
                font=("Segoe UI", 10)
            )
            return

        ancho = grafico_animales.winfo_width()
        alto = grafico_animales.winfo_height()

        total = sum(
            item["cantidad"] for item in datos_animales
        )

        centro_x = ancho * 0.34
        centro_y = alto * 0.43

        radio = min(ancho * 0.27, alto * 0.32, 105)

        if total > 0:

            inicio = 0

            for item in datos_animales:

                cantidad = item["cantidad"]

                if cantidad <= 0:
                    continue

                angulo = cantidad / total * 360

                grafico_animales.create_arc(
                    centro_x - radio,
                    centro_y - radio,
                    centro_x + radio,
                    centro_y + radio,
                    start=inicio,
                    extent=angulo,
                    fill=COLORES_ESTADOS.get(
                        item["estado"], VERDE
                    ),
                    outline=BLANCO,
                    width=2
                )

                inicio += angulo

        else:
            grafico_animales.create_oval(
                centro_x - radio,
                centro_y - radio,
                centro_x + radio,
                centro_y + radio,
                fill=GRIS_CLARO,
                outline=BLANCO
            )

            grafico_animales.create_text(
                centro_x,
                centro_y,
                text="Sin datos",
                font=("Segoe UI", 9),
                fill=GRIS
            )

        # LEYENDA

        leyenda_x = ancho * 0.65
        leyenda_y = max(20, centro_y - 55)

        for indice, item in enumerate(datos_animales):

            y = leyenda_y + indice * 27

            color = COLORES_ESTADOS.get(
                item["estado"], VERDE
            )

            grafico_animales.create_rectangle(
                leyenda_x,
                y,
                leyenda_x + 12,
                y + 12,
                fill=color,
                outline=""
            )

            grafico_animales.create_text(
                leyenda_x + 19,
                y + 6,
                text=item["estado"],
                anchor="w",
                font=("Segoe UI", 8),
                fill=TEXTO
            )

            grafico_animales.create_text(
                ancho - 15,
                y + 6,
                text=str(item["cantidad"]),
                anchor="e",
                font=("Segoe UI", 9, "bold"),
                fill=TEXTO
            )

        grafico_animales.create_text(
            centro_x,
            centro_y,
            text=str(total),
            font=("Segoe UI", 16, "bold"),
            fill=TEXTO
        )

        grafico_animales.create_text(
            centro_x,
            centro_y + 19,
            text="Animales",
            font=("Segoe UI", 8),
            fill=GRIS
        )

    # ==========================================
    # DIBUJAR GRÁFICO DE BARRAS
    # ==========================================

    def dibujar_adopciones(event=None):

        grafico_adopciones.delete("all")

        if not datos_adopciones:
            grafico_adopciones.create_text(
                150, 100,
                text="No hay datos disponibles",
                fill=GRIS,
                font=("Segoe UI", 10)
            )
            return

        ancho = grafico_adopciones.winfo_width()
        alto = grafico_adopciones.winfo_height()

        margen_izq = 35
        margen_der = 12
        margen_sup = 25
        margen_inf = 35

        ancho_util = ancho - margen_izq - margen_der
        alto_util = alto - margen_sup - margen_inf

        maximo = max(
            (item["cantidad"] for item in datos_adopciones),
            default=0
        )

        escala = max(maximo, 1)

        # Líneas horizontales

        for i in range(5):

            y = margen_sup + alto_util * i / 4

            valor = round(escala * (4 - i) / 4)

            grafico_adopciones.create_line(
                margen_izq,
                y,
                ancho - margen_der,
                y,
                fill=GRIS_CLARO,
                dash=(2, 3)
            )

            grafico_adopciones.create_text(
                margen_izq - 7,
                y,
                text=str(valor),
                anchor="e",
                font=("Segoe UI", 8),
                fill=GRIS
            )

        # Barras

        cantidad_meses = len(datos_adopciones)
        espacio = ancho_util / cantidad_meses
        ancho_barra = min(22, espacio * 0.55)

        for indice, item in enumerate(datos_adopciones):

            x_centro = (
                margen_izq + espacio * indice + espacio / 2
            )

            altura = (
                item["cantidad"] / escala * alto_util
            )

            x1 = x_centro - ancho_barra / 2
            x2 = x_centro + ancho_barra / 2
            y1 = margen_sup + alto_util - altura
            y2 = margen_sup + alto_util

            if item["cantidad"] > 0:

                grafico_adopciones.create_rectangle(
                    x1, y1, x2, y2,
                    fill=VERDE,
                    outline=""
                )

                grafico_adopciones.create_text(
                    x_centro,
                    y1 - 10,
                    text=str(item["cantidad"]),
                    font=("Segoe UI", 8, "bold"),
                    fill=TEXTO
                )

            # Nombre del mes

            grafico_adopciones.create_text(
                x_centro,
                y2 + 15,
                text=item["mes"][:3],
                font=("Segoe UI", 8),
                fill=GRIS
            )

    # ==========================================
    # FUNCIONES DE CONEXIÓN CON LA API
    # ==========================================

    def cargar_reportes():

        nonlocal datos_animales, datos_adopciones

        try:

            # Obtener animales

            respuesta_animales = requests.get(
                API_ANIMALES,
                timeout=5
            )

            respuesta_animales.raise_for_status()

            resultado_animales = respuesta_animales.json()

            datos_animales = resultado_animales.get(
                "datos", []
            )

            # Obtener adopciones del año seleccionado

            anio = seleccion_anio.get()

            respuesta_adopciones = requests.get(
                API_ADOPCIONES,
                params={"anio": anio},
                timeout=5
            )

            respuesta_adopciones.raise_for_status()

            resultado_adopciones = respuesta_adopciones.json()

            datos_adopciones = resultado_adopciones.get(
                "datos", []
            )

            # Actualizar tarjetas

            total_animales.config(
                text=str(resultado_animales.get("total", 0))
            )

            total_adopciones.config(
                text=str(resultado_adopciones.get("total", 0))
            )

            # Actualizar gráficos

            dibujar_animales()
            dibujar_adopciones()

        except requests.RequestException as error:

            messagebox.showerror(
                "Error de conexión",
                "No se pudieron cargar los reportes.\n\n"
                "Verificá que el servidor esté funcionando.\n\n"
                f"{error}"
            )

    # ==========================================
    # BOTÓN ACTUALIZAR
    # ==========================================

    tk.Button(
        barra,
        text="↻  Actualizar reportes",
        font=("Segoe UI", 10, "bold"),
        bg=VERDE,
        fg=BLANCO,
        activebackground=VERDE_OSCURO,
        activeforeground=BLANCO,
        relief="flat",
        cursor="hand2",
        padx=15,
        pady=8,
        command=cargar_reportes
    ).pack(side="right")

    # ==========================================
    # REDIBUJAR AL CAMBIAR EL TAMAÑO
    # ==========================================

    grafico_animales.bind(
        "<Configure>",
        dibujar_animales
    )

    grafico_adopciones.bind(
        "<Configure>",
        dibujar_adopciones
    )

    # ==========================================
    # CAMBIAR EL AÑO
    # ==========================================

    combo_anio.bind(
        "<<ComboboxSelected>>",
        lambda event: cargar_reportes()
    )

    # ==========================================
    # CARGAR DATOS INICIALES
    # ==========================================

    cargar_reportes()
