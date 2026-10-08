import tkinter as tk
from tkinter import ttk, messagebox
import requests


# ==========================================
# CONFIGURACIÓN
# ==========================================

URL_API = "http://localhost:3000/donaciones"


# ==========================================
# INTERFAZ DONACIONES
# ==========================================

def crear_donaciones(parent):

    # --------------------------------------
    # COLORES
    # --------------------------------------

    VERDE = "#4F7F5D"
    VERDE_CLARO = "#E8F4EC"
    VERDE_TEXTO = "#28784A"
    FONDO = "#F8F7F2"
    BLANCO = "#FFFFFF"
    TEXTO = "#26332D"
    GRIS = "#6D7973"
    NARANJA = "#F28C28"
    MORADO = "#6851C9"

    # --------------------------------------
    # FRAME PRINCIPAL
    # --------------------------------------

    frame = tk.Frame(parent, bg=FONDO)
    frame.pack(fill="both", expand=True)

    # ======================================
    # BARRA LATERAL
    # ======================================

    menu = tk.Frame(frame, bg=VERDE, width=225)
    menu.pack(side="left", fill="y")
    menu.pack_propagate(False)

    # Logo
    logo = tk.Label(
        menu,
        text="ARCA",
        bg=VERDE,
        fg="white",
        font=("Arial", 18, "bold")
    )
    logo.pack(pady=(25, 30))

    # Separador
    tk.Frame(menu, bg="#638D6F", height=1).pack(fill="x")

    opciones = [
        "⌂   Inicio",
        "♧   Animales",
        "♡   Adopciones",
        "🎁   Donaciones",
        "♧   Voluntarios",
        "▥   Reportes",
        "?   Ayuda"
    ]

    for opcion in opciones:

        color = "#6C9678" if "Donaciones" in opcion else VERDE

        boton = tk.Label(
            menu,
            text=opcion,
            bg=color,
            fg="white",
            anchor="w",
            padx=20,
            font=("Arial", 12)
        )

        boton.pack(fill="x", ipady=12)

    # Usuario abajo
    usuario_frame = tk.Frame(menu, bg=VERDE)
    usuario_frame.pack(side="bottom", fill="x", pady=20)

    tk.Label(
        usuario_frame,
        text="●",
        bg=VERDE,
        fg="#DDE9DF",
        font=("Arial", 20)
    ).pack(side="left", padx=15)

    datos_usuario = tk.Frame(usuario_frame, bg=VERDE)
    datos_usuario.pack(side="left")

    tk.Label(
        datos_usuario,
        text="Usuario",
        bg=VERDE,
        fg="white",
        font=("Arial", 10, "bold")
    ).pack(anchor="w")

    tk.Label(
        datos_usuario,
        text="Administrador",
        bg=VERDE,
        fg="#D6E4D9",
        font=("Arial", 9)
    ).pack(anchor="w")

    # ======================================
    # CONTENIDO
    # ======================================

    contenido = tk.Frame(frame, bg=FONDO)
    contenido.pack(side="left", fill="both", expand=True)

    # --------------------------------------
    # BARRA SUPERIOR
    # --------------------------------------

    barra = tk.Frame(
        contenido,
        bg=BLANCO,
        height=55
    )
    barra.pack(fill="x")
    barra.pack_propagate(False)

    tk.Label(
        barra,
        text="☰",
        bg=BLANCO,
        fg=VERDE,
        font=("Arial", 20)
    ).pack(side="left", padx=(25, 15))

    tk.Label(
        barra,
        text="Donaciones",
        bg=BLANCO,
        fg=TEXTO,
        font=("Arial", 15)
    ).pack(side="left")

    # ======================================
    # CONTENIDO PRINCIPAL
    # ======================================

    principal = tk.Frame(contenido, bg=FONDO)
    principal.pack(fill="both", expand=True, padx=25, pady=25)

    # --------------------------------------
    # TÍTULO
    # --------------------------------------

    titulo_frame = tk.Frame(principal, bg=FONDO)
    titulo_frame.pack(fill="x")

    textos_titulo = tk.Frame(titulo_frame, bg=FONDO)
    textos_titulo.pack(side="left")

    tk.Label(
        textos_titulo,
        text="Gestión de Donaciones",
        bg=FONDO,
        fg=TEXTO,
        font=("Arial", 18, "bold")
    ).pack(anchor="w")

    total_label = tk.Label(
        textos_titulo,
        text="Total registradas: 0",
        bg=FONDO,
        fg=GRIS,
        font=("Arial", 10)
    )
    total_label.pack(anchor="w", pady=(5, 0))

    # Botón registrar
    boton_registrar = tk.Button(
        titulo_frame,
        text="+  Registrar Donación",
        bg=VERDE,
        fg="white",
        activebackground="#426C4E",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        font=("Arial", 11, "bold"),
        padx=15,
        pady=10
    )
    boton_registrar.pack(side="right")

    # ======================================
    # TARJETAS
    # ======================================

    tarjetas = tk.Frame(principal, bg=FONDO)
    tarjetas.pack(fill="x", pady=(20, 18))

    tarjeta_labels = {}

    tipos = [
        ("Dinero", VERDE_TEXTO),
        ("Insumos", VERDE_TEXTO),
        ("Alimento", "#C66B00"),
        ("Medicamentos", MORADO)
    ]

    for tipo, color in tipos:

        tarjeta = tk.Frame(
            tarjetas,
            bg=BLANCO,
            highlightbackground="#E2E5E2",
            highlightthickness=1
        )
        tarjeta.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        icono = tk.Label(
            tarjeta,
            text="🎁",
            bg=VERDE_CLARO,
            fg=color,
            font=("Arial", 16)
        )
        icono.pack(side="left", padx=15, pady=15)

        info = tk.Frame(tarjeta, bg=BLANCO)
        info.pack(side="left", pady=10)

        numero = tk.Label(
            info,
            text="0",
            bg=BLANCO,
            fg=color,
            font=("Arial", 17, "bold")
        )
        numero.pack(anchor="w")

        tk.Label(
            info,
            text=tipo,
            bg=BLANCO,
            fg=GRIS,
            font=("Arial", 9)
        ).pack(anchor="w")

        tarjeta_labels[tipo] = numero

    # ======================================
    # BUSCADOR
    # ======================================

    buscar_frame = tk.Frame(principal, bg=FONDO)
    buscar_frame.pack(fill="x", pady=(0, 18))

    buscar_entry = tk.Entry(
        buscar_frame,
        width=40,
        font=("Arial", 10),
        relief="solid",
        bd=1
    )
    buscar_entry.pack(side="left", ipady=9, padx=(0, 10))

    buscar_entry.insert(0, "")

    # ======================================
    # TABLA
    # ======================================

    tabla_frame = tk.Frame(
        principal,
        bg=BLANCO,
        highlightbackground="#E2E5E2",
        highlightthickness=1
    )
    tabla_frame.pack(fill="both", expand=True)

    columnas = (
        "id",
        "donante",
        "tipo",
        "detalle",
        "fecha",
        "acciones"
    )

    tabla = ttk.Treeview(
        tabla_frame,
        columns=columnas,
        show="headings"
    )

    tabla.heading("id", text="ID")
    tabla.heading("donante", text="DONANTE")
    tabla.heading("tipo", text="TIPO")
    tabla.heading("detalle", text="MONTO / CANTIDAD")
    tabla.heading("fecha", text="FECHA")
    tabla.heading("acciones", text="ACCIONES")

    tabla.column("id", width=50)
    tabla.column("donante", width=150)
    tabla.column("tipo", width=130)
    tabla.column("detalle", width=180)
    tabla.column("fecha", width=120)
    tabla.column("acciones", width=130)

    tabla.pack(
        side="left",
        fill="both",
        expand=True,
        padx=5,
        pady=5
    )

    scrollbar = ttk.Scrollbar(
        tabla_frame,
        orient="vertical",
        command=tabla.yview
    )

    scrollbar.pack(side="right", fill="y")

    tabla.configure(
        yscrollcommand=scrollbar.set
    )

    # ======================================
    # FUNCIONES CRUD
    # ======================================

    donaciones = []

    def cargar_donaciones():

        nonlocal donaciones

        try:

            respuesta = requests.get(URL_API)

            if respuesta.status_code == 200:

                donaciones = respuesta.json()

                actualizar_tabla()

            else:

                messagebox.showerror(
                    "Error",
                    "No se pudieron obtener las donaciones."
                )

        except requests.exceptions.RequestException as error:

            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con el servidor.\n\n"
                + str(error)
            )

    # --------------------------------------
    # ACTUALIZAR TABLA
    # --------------------------------------

    def actualizar_tabla():

        # Limpiar tabla
        for item in tabla.get_children():
            tabla.delete(item)

        texto_busqueda = buscar_entry.get().lower()

        contadores = {
            "Dinero": 0,
            "Insumos": 0,
            "Alimento": 0,
            "Medicamentos": 0
        }

        for donacion in donaciones:

            id_donacion = donacion.get("id_donacion")
            fecha = donacion.get("fecha", "")
            tipo = donacion.get("tipo", "")
            detalle = donacion.get("detalle", "")
            id_persona = donacion.get("id_persona", "")

            # Convertir fecha si viene con formato datetime
            fecha = str(fecha)[:10]

            # Buscar
            texto = (
                str(id_persona) +
                " " +
                str(tipo) +
                " " +
                str(detalle)
            ).lower()

            if texto_busqueda not in texto:
                continue

            # Contadores
            if tipo in contadores:
                contadores[tipo] += 1

            # Agregar fila
            tabla.insert(
                "",
                "end",
                values=(
                    id_donacion,
                    "Persona " + str(id_persona),
                    tipo,
                    detalle,
                    fecha,
                    "✎     🗑"
                ),
                tags=(str(id_donacion),)
            )

        # Actualizar tarjetas
        for tipo in contadores:
            tarjeta_labels[tipo].config(
                text=str(contadores[tipo])
            )

        total_label.config(
            text=f"Total registradas: {len(donaciones)}"
        )

    # --------------------------------------
    # CREAR DONACIÓN
    # --------------------------------------

    def registrar_donacion():

        ventana = tk.Toplevel(frame)
        ventana.title("Registrar Donación")
        ventana.geometry("420x400")
        ventana.resizable(False, False)
        ventana.configure(bg=FONDO)

        tk.Label(
            ventana,
            text="Registrar Donación",
            bg=FONDO,
            fg=TEXTO,
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        formulario = tk.Frame(
            ventana,
            bg=FONDO
        )
        formulario.pack(padx=30, fill="x")

        # Fecha
        tk.Label(
            formulario,
            text="Fecha:",
            bg=FONDO,
            fg=TEXTO
        ).pack(anchor="w")

        fecha_entry = tk.Entry(
            formulario,
            font=("Arial", 10)
        )
        fecha_entry.pack(fill="x", pady=(3, 12))

        # Tipo
        tk.Label(
            formulario,
            text="Tipo:",
            bg=FONDO,
            fg=TEXTO
        ).pack(anchor="w")

        tipo_combo = ttk.Combobox(
            formulario,
            values=[
                "Dinero",
                "Insumos",
                "Alimento",
                "Medicamentos"
            ],
            state="readonly"
        )
        tipo_combo.pack(fill="x", pady=(3, 12))

        # Detalle
        tk.Label(
            formulario,
            text="Monto / Cantidad:",
            bg=FONDO,
            fg=TEXTO
        ).pack(anchor="w")

        detalle_entry = tk.Entry(
            formulario,
            font=("Arial", 10)
        )
        detalle_entry.pack(fill="x", pady=(3, 12))

        # Persona
        tk.Label(
            formulario,
            text="ID de persona:",
            bg=FONDO,
            fg=TEXTO
        ).pack(anchor="w")

        persona_entry = tk.Entry(
            formulario,
            font=("Arial", 10)
        )
        persona_entry.pack(fill="x", pady=(3, 15))

        def guardar():

            fecha = fecha_entry.get()
            tipo = tipo_combo.get()
            detalle = detalle_entry.get()
            id_persona = persona_entry.get()

            if not fecha or not tipo or not detalle or not id_persona:

                messagebox.showwarning(
                    "Campos incompletos",
                    "Completá todos los campos."
                )
                return

            datos = {
                "fecha": fecha,
                "tipo": tipo,
                "detalle": detalle,
                "id_persona": id_persona
            }

            try:

                respuesta = requests.post(
                    URL_API,
                    json=datos
                )

                if respuesta.status_code == 201:

                    messagebox.showinfo(
                        "Éxito",
                        "Donación agregada correctamente."
                    )

                    ventana.destroy()
                    cargar_donaciones()

                else:

                    messagebox.showerror(
                        "Error",
                        "No se pudo agregar la donación."
                    )

            except requests.exceptions.RequestException as error:

                messagebox.showerror(
                    "Error de conexión",
                    str(error)
                )

        tk.Button(
            ventana,
            text="Guardar Donación",
            command=guardar,
            bg=VERDE,
            fg="white",
            relief="flat",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8
        ).pack(pady=5)

    # ======================================
    # EDITAR DONACIÓN
    # ======================================

    def editar_donacion(id_donacion):

        try:

            respuesta = requests.get(
                f"{URL_API}/{id_donacion}"
            )

            if respuesta.status_code != 200:

                messagebox.showerror(
                    "Error",
                    "No se encontró la donación."
                )
                return

            donacion = respuesta.json()

        except requests.exceptions.RequestException as error:

            messagebox.showerror(
                "Error de conexión",
                str(error)
            )
            return

        ventana = tk.Toplevel(frame)
        ventana.title("Editar Donación")
        ventana.geometry("420x400")
        ventana.resizable(False, False)
        ventana.configure(bg=FONDO)

        tk.Label(
            ventana,
            text="Editar Donación",
            bg=FONDO,
            fg=TEXTO,
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        formulario = tk.Frame(
            ventana,
            bg=FONDO
        )
        formulario.pack(padx=30, fill="x")

        # Fecha
        tk.Label(
            formulario,
            text="Fecha:",
            bg=FONDO,
            fg=TEXTO
        ).pack(anchor="w")

        fecha_entry = tk.Entry(formulario)
        fecha_entry.pack(fill="x", pady=(3, 12))
        fecha_entry.insert(0, str(donacion.get("fecha", ""))[:10])

        # Tipo
        tk.Label(
            formulario,
            text="Tipo:",
            bg=FONDO,
            fg=TEXTO
        ).pack(anchor="w")

        tipo_combo = ttk.Combobox(
            formulario,
            values=[
                "Dinero",
                "Insumos",
                "Alimento",
                "Medicamentos"
            ],
            state="readonly"
        )
        tipo_combo.pack(fill="x", pady=(3, 12))
        tipo_combo.set(donacion.get("tipo", ""))

        # Detalle
        tk.Label(
            formulario,
            text="Monto / Cantidad:",
            bg=FONDO,
            fg=TEXTO
        ).pack(anchor="w")

        detalle_entry = tk.Entry(formulario)
        detalle_entry.pack(fill="x", pady=(3, 12))
        detalle_entry.insert(
            0,
            donacion.get("detalle", "")
        )

        # Persona
        tk.Label(
            formulario,
            text="ID de persona:",
            bg=FONDO,
            fg=TEXTO
        ).pack(anchor="w")

        persona_entry = tk.Entry(formulario)
        persona_entry.pack(fill="x", pady=(3, 15))
        persona_entry.insert(
            0,
            donacion.get("id_persona", "")
        )

        def actualizar():

            datos = {
                "fecha": fecha_entry.get(),
                "tipo": tipo_combo.get(),
                "detalle": detalle_entry.get(),
                "id_persona": persona_entry.get()
            }

            if not all(datos.values()):

                messagebox.showwarning(
                    "Campos incompletos",
                    "Completá todos los campos."
                )
                return

            try:

                respuesta = requests.put(
                    f"{URL_API}/{id_donacion}",
                    json=datos
                )

                if respuesta.status_code == 200:

                    messagebox.showinfo(
                        "Éxito",
                        "Donación actualizada correctamente."
                    )

                    ventana.destroy()
                    cargar_donaciones()

                else:

                    messagebox.showerror(
                        "Error",
                        "No se pudo actualizar la donación."
                    )

            except requests.exceptions.RequestException as error:

                messagebox.showerror(
                    "Error de conexión",
                    str(error)
                )

        tk.Button(
            ventana,
            text="Guardar Cambios",
            command=actualizar,
            bg=VERDE,
            fg="white",
            relief="flat",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8
        ).pack(pady=5)

    # ======================================
    # ELIMINAR DONACIÓN
    # ======================================

    def eliminar_donacion(id_donacion):

        confirmar = messagebox.askyesno(
            "Eliminar donación",
            "¿Estás seguro de que querés eliminar esta donación?"
        )

        if not confirmar:
            return

        try:

            respuesta = requests.delete(
                f"{URL_API}/{id_donacion}"
            )

            if respuesta.status_code == 200:

                messagebox.showinfo(
                    "Éxito",
                    "Donación eliminada correctamente."
                )

                cargar_donaciones()

            else:

                messagebox.showerror(
                    "Error",
                    "No se pudo eliminar la donación."
                )

        except requests.exceptions.RequestException as error:

            messagebox.showerror(
                "Error de conexión",
                str(error)
            )

    # ======================================
    # DETECTAR CLICK EN ACCIONES
    # ======================================

    def click_tabla(event):

        item = tabla.identify_row(event.y)
        columna = tabla.identify_column(event.x)

        if not item:
            return

        valores = tabla.item(item, "values")

        if not valores:
            return

        id_donacion = valores[0]

        # Columna acciones
        if columna == "#6":

            # Por simplicidad mostramos opciones
            ventana = tk.Toplevel(frame)
            ventana.title("Acciones")
            ventana.geometry("250x150")
            ventana.resizable(False, False)

            tk.Label(
                ventana,
                text="¿Qué querés hacer?",
                font=("Arial", 11, "bold")
            ).pack(pady=15)

            botones = tk.Frame(ventana)
            botones.pack()

            tk.Button(
                botones,
                text="Editar",
                bg=VERDE,
                fg="white",
                relief="flat",
                command=lambda: [
                    ventana.destroy(),
                    editar_donacion(id_donacion)
                ]
            ).pack(side="left", padx=5)

            tk.Button(
                botones,
                text="Eliminar",
                bg=NARANJA,
                fg="white",
                relief="flat",
                command=lambda: [
                    ventana.destroy(),
                    eliminar_donacion(id_donacion)
                ]
            ).pack(side="left", padx=5)

    tabla.bind("<ButtonRelease-1>", click_tabla)

    # ======================================
    # BUSCADOR EN TIEMPO REAL
    # ======================================

    buscar_entry.bind(
        "<KeyRelease>",
        lambda event: actualizar_tabla()
    )

    # ======================================
    # BOTÓN REGISTRAR
    # ======================================

    boton_registrar.config(
        command=registrar_donacion
    )

    # ======================================
    # CARGAR DATOS AL ABRIR
    # ======================================

    cargar_donaciones()

    return frame