
import tkinter as tk
from tkinter import ttk, messagebox
import requests
from collections import Counter

# ==========================================
# CONFIGURACIÓN DE LA API
# ==========================================
API_URL = "http://localhost:3000/api/voluntarios"
PERSONAS_URL = "http://localhost:3000/api/personas"

# ==========================================
# INTERFAZ DE VOLUNTARIOS
# ==========================================
def voluntarios(parent):

    # Colores de la interfaz
    VERDE = "#4F7F5F"
    VERDE_CLARO = "#EAF4ED"
    FONDO = "#F5F3ED"
    BLANCO = "#FFFFFF"
    TEXTO = "#222222"
    GRIS = "#777777"
    NARANJA = "#F27B21"

    # Limpiar el contenido anterior del frame
    for widget in parent.winfo_children():
        widget.destroy()

    parent.configure(bg=FONDO)

    voluntarios_data = []
    personas_data = []
    busqueda = tk.StringVar()

    # ==========================================
    # FUNCIONES DE CONEXIÓN CON LA API
    # ==========================================
    def obtener_voluntarios():
        try:
            respuesta = requests.get(API_URL, timeout=5)
            respuesta.raise_for_status()
            return respuesta.json()
        except requests.RequestException as error:
            messagebox.showerror(
                "Error de conexión",
                f"No se pudieron cargar los voluntarios.\n\n{error}"
            )
            return None

    def cargar_datos():
        nonlocal voluntarios_data

        datos = obtener_voluntarios()

        if datos is None:
            return

        voluntarios_data = datos
        actualizar_tabla()

    def obtener_personas():
        nonlocal personas_data

        try:
            respuesta = requests.get(PERSONAS_URL, timeout=5)
            respuesta.raise_for_status()
            personas_data = respuesta.json()
        except requests.RequestException as error:
            messagebox.showerror(
                "Error de conexiÃ³n",
                f"No se pudieron cargar las personas.\n\n{error}"
            )
            personas_data = []

    def nombre_persona(id_persona):
        persona = next(
            (
                p for p in personas_data
                if str(p.get("id_persona")) == str(id_persona)
            ),
            None
        )

        if not persona:
            return f"ID {id_persona}" if id_persona else "Sin persona"

        return (
            f"{persona.get('nombre', '')} "
            f"{persona.get('apellido', '')}"
        ).strip()

    # ==========================================
    # ENCABEZADO
    # ==========================================
    encabezado = tk.Frame(parent, bg=BLANCO, height=60)
    encabezado.pack(fill="x")
    encabezado.pack_propagate(False)

    tk.Label(
        encabezado,
        text="☰   Voluntarios",
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
    # CONTENEDOR PRINCIPAL
    # ==========================================
    contenido = tk.Frame(parent, bg=FONDO)
    contenido.pack(fill="both", expand=True)

    # Menú lateral
    lateral = tk.Frame(contenido, bg=VERDE, width=205)
    lateral.pack(side="left", fill="y")
    lateral.pack_propagate(False)

    tk.Label(
        lateral,
        text="ARCA",
        font=("Segoe UI", 18, "bold"),
        bg=VERDE,
        fg=BLANCO
    ).pack(anchor="w", padx=25, pady=(25, 35))

    opciones = [
        ("⌂", "Inicio"),
        ("♧", "Animales"),
        ("♡", "Adopciones"),
        ("♙", "Donaciones"),
        ("♙", "Voluntarios"),
        ("▥", "Reportes"),
        ("?", "Ayuda")
    ]

    for icono, nombre in opciones:
        activo = nombre == "Voluntarios"

        boton = tk.Label(
            lateral,
            text=f"  {icono}   {nombre}",
            font=("Segoe UI", 11,
                  "bold" if activo else "normal"),
            bg="#70977B" if activo else VERDE,
            fg=BLANCO,
            anchor="w",
            padx=12,
            pady=13,
            cursor="hand2"
        )
        boton.pack(fill="x", padx=8, pady=2)

    # La navegación la gestiona el menú principal de inicio.py.
    lateral.destroy()

    # ==========================================
    # PANEL DE GESTIÓN
    # ==========================================
    panel = tk.Frame(contenido, bg=FONDO)
    panel.pack(side="left", fill="both", expand=True)

    # Encabezado de gestión
    titulo = tk.Frame(panel, bg=FONDO)
    titulo.pack(fill="x", padx=25, pady=(22, 12))

    bloque_titulo = tk.Frame(titulo, bg=FONDO)
    bloque_titulo.pack(side="left")

    tk.Label(
        bloque_titulo,
        text="Gestión de Voluntarios",
        font=("Segoe UI", 18, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).pack(anchor="w")

    subtitulo = tk.Label(
        bloque_titulo,
        text="Cargando voluntarios...",
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=GRIS
    )
    subtitulo.pack(anchor="w", pady=(3, 0))

    # ==========================================
    # BOTÓN AGREGAR
    # ==========================================
    boton_agregar = tk.Button(
        titulo,
        text="＋  Agregar Voluntario",
        font=("Segoe UI", 11, "bold"),
        bg=VERDE,
        fg=BLANCO,
        activebackground="#3F6B4D",
        activeforeground=BLANCO,
        relief="flat",
        cursor="hand2",
        padx=18,
        pady=12,
        command=lambda: abrir_formulario()
    )
    boton_agregar.pack(side="right", padx=5)

    # ==========================================
    # TARJETAS DE ROLES
    # ==========================================
    tarjetas = tk.Frame(panel, bg=FONDO)
    tarjetas.pack(fill="x", padx=25, pady=(5, 18))

    roles_config = [
        ("Cuidador/a", "#4F8060"),
        ("Veterinario", "#6550C9"),
        ("Administración", "#987444"),
        ("Educador/a", "#21838B"),
        ("Transportista", "#854FC4")
    ]

    for columna in range(5):
        tarjetas.grid_columnconfigure(columna, weight=1)

    tarjetas_widgets = {}

    for i, (rol, color) in enumerate(roles_config):
        tarjeta = tk.Frame(
            tarjetas,
            bg=BLANCO,
            highlightbackground="#E2E7E2",
            highlightthickness=1
        )
        tarjeta.grid(
            row=0, column=i, sticky="nsew",
            padx=(0 if i == 0 else 6, 6 if i < 4 else 0),
            ipady=7
        )

        tk.Label(
            tarjeta,
            text="♙",
            font=("Segoe UI", 17),
            bg="#E8EEE9",
            fg=color,
            padx=9,
            pady=3
        ).pack(pady=(10, 3))

        numero = tk.Label(
            tarjeta,
            text="0",
            font=("Segoe UI", 19, "bold"),
            bg=BLANCO,
            fg=color
        )
        numero.pack()

        tk.Label(
            tarjeta,
            text=rol,
            font=("Segoe UI", 9),
            bg=BLANCO,
            fg=GRIS
        ).pack(pady=(2, 10))

        tarjetas_widgets[rol] = numero

    # ==========================================
    # BUSCADOR
    # ==========================================
    barra_busqueda = tk.Frame(panel, bg=FONDO)
    barra_busqueda.pack(fill="x", padx=25, pady=(0, 15))

    entrada_busqueda = tk.Entry(
        barra_busqueda,
        textvariable=busqueda,
        font=("Segoe UI", 11),
        bg=BLANCO,
        fg=TEXTO,
        relief="solid",
        bd=1
    )
    entrada_busqueda.pack(
        side="left", fill="x", expand=True,
        ipady=9, padx=(0, 10)
    )

    entrada_busqueda.insert(0, "")

    tk.Button(
        barra_busqueda,
        text="Actualizar",
        font=("Segoe UI", 10),
        bg=BLANCO,
        fg=VERDE,
        relief="solid",
        bd=1,
        cursor="hand2",
        command=cargar_datos
    ).pack(side="right", ipady=6, padx=(0, 5))

    # ==========================================
    # TABLA DE VOLUNTARIOS
    # ==========================================
    marco_tabla = tk.Frame(
        panel,
        bg=BLANCO,
        highlightbackground="#E1E7E1",
        highlightthickness=1
    )
    marco_tabla.pack(
        fill="both", expand=True,
        padx=25, pady=(0, 20)
    )

    columnas = (
        "id", "persona", "rol", "turno",
        "dias", "fecha_ingreso", "estado"
    )

    tabla = ttk.Treeview(
        marco_tabla,
        columns=columnas,
        show="headings",
        selectmode="browse"
    )

    encabezados = {
        "id": "#",
        "persona": "PERSONA",
        "rol": "ROL",
        "turno": "TURNO",
        "dias": "DÍAS",
        "fecha_ingreso": "INGRESO",
        "estado": "ESTADO"
    }

    anchos = {
        "id": 40,
        "persona": 145,
        "rol": 130,
        "turno": 95,
        "dias": 140,
        "fecha_ingreso": 110,
        "estado": 90
    }

    for columna in columnas:
        tabla.heading(columna, text=encabezados[columna])
        tabla.column(
            columna,
            width=anchos[columna],
            minwidth=65,
            anchor="w",
            stretch=True
        )

    estilo = ttk.Style()
    estilo.configure(
        "Treeview",
        font=("Segoe UI", 10),
        rowheight=48,
        background=BLANCO,
        foreground=TEXTO,
        fieldbackground=BLANCO
    )
    estilo.configure(
        "Treeview.Heading",
        font=("Segoe UI", 9, "bold"),
        background=FONDO,
        foreground=GRIS,
        relief="flat",
        padding=10
    )
    estilo.map(
        "Treeview",
        background=[("selected", "#DCE9DF")],
        foreground=[("selected", TEXTO)]
    )

    scrollbar_y = ttk.Scrollbar(
        marco_tabla, orient="vertical",
        command=tabla.yview
    )
    scrollbar_x = ttk.Scrollbar(
        marco_tabla, orient="horizontal",
        command=tabla.xview
    )

    tabla.configure(
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set
    )

    tabla.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    marco_tabla.grid_rowconfigure(0, weight=1)
    marco_tabla.grid_columnconfigure(0, weight=1)

    tabla.tag_configure("par", background="#FFFFFF")
    tabla.tag_configure("impar", background="#F8FAF8")

    # ==========================================
    # ACTUALIZAR TABLA Y TARJETAS
    # ==========================================
    def actualizar_tabla(*args):
        filtro = busqueda.get().strip().lower()

        for fila in tabla.get_children():
            tabla.delete(fila)

        # Contadores de roles
        conteo_roles = Counter(
            v.get("rol", "")
            for v in voluntarios_data
            if str(v.get("estado", "Activo")).lower() == "activo"
        )

        for rol, etiqueta in tarjetas_widgets.items():
            etiqueta.config(text=str(conteo_roles.get(rol, 0)))

        activos = sum(
            1 for v in voluntarios_data
            if str(v.get("estado", "Activo")).lower() == "activo"
        )

        subtitulo.config(
            text=f"{activos} activos de {len(voluntarios_data)} registrados"
        )

        filtrados = [
            v for v in voluntarios_data
            if filtro in str(v.get("nombre", "")).lower()
            or filtro in str(v.get("rol", "")).lower()
            or filtro in nombre_persona(v.get("id_persona")).lower()
        ]

        for indice, v in enumerate(filtrados):
            tabla.insert(
                "",
                "end",
                values=(
                    v.get("id_voluntario", ""),
                    nombre_persona(v.get("id_persona")),
                    v.get("rol", ""),
                    v.get("turno", ""),
                    v.get("dias", ""),
                    str(v.get("fecha_ingreso", ""))[:10],
                    v.get("estado", "Activo")
                ),
                tags=("par" if indice % 2 == 0 else "impar",)
            )

    busqueda.trace_add("write", actualizar_tabla)

    # ==========================================
    # FORMULARIO PARA CREAR Y EDITAR
    # ==========================================
    def abrir_formulario(voluntario=None):
        editar = voluntario is not None

        ventana = tk.Toplevel(parent)
        ventana.title(
            "Editar voluntario" if editar else "Agregar voluntario"
        )
        ventana.geometry("440x640")
        ventana.configure(bg=FONDO)
        ventana.resizable(False, False)
        ventana.transient(parent.winfo_toplevel())
        ventana.grab_set()

        tk.Label(
            ventana,
            text="Editar voluntario" if editar else "Nuevo voluntario",
            font=("Segoe UI", 17, "bold"),
            bg=FONDO,
            fg=TEXTO
        ).pack(anchor="w", padx=25, pady=(20, 15))

        formulario = tk.Frame(ventana, bg=FONDO)
        formulario.pack(fill="both", expand=True, padx=25)

        campos = {}

        def crear_campo(etiqueta, clave, opciones=None):
            tk.Label(
                formulario,
                text=etiqueta,
                font=("Segoe UI", 10, "bold"),
                bg=FONDO,
                fg=TEXTO
            ).pack(anchor="w", pady=(7, 3))

            valor = (
                voluntario.get(clave, "")
                if editar else ""
            )

            if clave == "id_persona" and valor:
                valor = f"{valor} - {nombre_persona(valor)}"

            if opciones:
                campo = ttk.Combobox(
                    formulario,
                    values=opciones,
                    state="readonly",
                    font=("Segoe UI", 10)
                )
                campo.set(valor or opciones[0])
            else:
                campo = tk.Entry(
                    formulario,
                    font=("Segoe UI", 10),
                    relief="solid",
                    bd=1
                )
                campo.insert(0, str(valor))

            campo.pack(fill="x", ipady=5)
            campos[clave] = campo

        valores_personas = [
            f"{p.get('id_persona')} - "
            f"{p.get('nombre', '')} {p.get('apellido', '')}".strip()
            for p in personas_data
        ]

        crear_campo("Persona", "id_persona", valores_personas)
        crear_campo(
            "Rol", "rol",
            [
                "Cuidador/a",
                "Veterinario",
                "Administración",
                "Educador/a",
                "Transportista"
            ]
        )
        crear_campo(
            "Turno", "turno",
            ["Mañana", "Tarde", "Noche", "Flexible"]
        )
        crear_campo("Días disponibles", "dias")
        crear_campo(
            "Fecha de ingreso (AAAA-MM-DD)",
            "fecha_ingreso"
        )
        crear_campo(
            "Estado", "estado",
            ["Activo", "Inactivo"]
        )

        def guardar():
            datos = {
                clave: campo.get().strip()
                for clave, campo in campos.items()
            }

            persona_seleccionada = datos.get("id_persona", "")

            if not persona_seleccionada:
                messagebox.showwarning(
                    "Persona obligatoria",
                    "SeleccionÃ¡ la persona relacionada.",
                    parent=ventana
                )
                return

            try:
                datos["id_persona"] = int(
                    persona_seleccionada.split(" - ", 1)[0]
                )
            except (ValueError, IndexError):
                messagebox.showerror(
                    "Persona invÃ¡lida",
                    "SeleccionÃ¡ una persona vÃ¡lida.",
                    parent=ventana
                )
                return

            datos["nombre"] = nombre_persona(datos["id_persona"])

            if any(not valor for valor in datos.values()):
                messagebox.showwarning(
                    "Datos incompletos",
                    "Completá todos los campos.",
                    parent=ventana
                )
                return

            try:
                if editar:
                    respuesta = requests.put(
                        f"{API_URL}/{voluntario['id_voluntario']}",
                        json=datos,
                        timeout=5
                    )
                else:
                    respuesta = requests.post(
                        API_URL,
                        json=datos,
                        timeout=5
                    )

                respuesta.raise_for_status()

                messagebox.showinfo(
                    "Correcto",
                    "Voluntario actualizado correctamente."
                    if editar else
                    "Voluntario agregado correctamente.",
                    parent=ventana
                )

                ventana.destroy()
                cargar_datos()

            except requests.RequestException as error:
                detalle = error

                if getattr(error, "response", None) is not None:
                    detalle = error.response.text

                messagebox.showerror(
                    "Error",
                    f"No se pudo guardar el voluntario.\n{detalle}",
                    parent=ventana
                )

        tk.Button(
            ventana,
            text="Guardar cambios" if editar else "Guardar voluntario",
            font=("Segoe UI", 11, "bold"),
            bg=VERDE,
            fg=BLANCO,
            activebackground="#3F6B4D",
            activeforeground=BLANCO,
            relief="flat",
            cursor="hand2",
            command=guardar
        ).pack(fill="x", padx=25, pady=(12, 22), ipady=9)

    # ==========================================
    # EDITAR VOLUNTARIO SELECCIONADO
    # ==========================================
    def editar_voluntario():
        seleccionado = tabla.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Atención",
                "Seleccioná un voluntario de la tabla."
            )
            return

        valores = tabla.item(seleccionado[0], "values")
        id_voluntario = valores[0]

        voluntario = next(
            (
                v for v in voluntarios_data
                if str(v.get("id_voluntario")) == str(id_voluntario)
            ),
            None
        )

        if voluntario:
            abrir_formulario(voluntario)

    # ==========================================
    # ELIMINAR VOLUNTARIO SELECCIONADO
    # ==========================================
    def eliminar_voluntario():
        seleccionado = tabla.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Atención",
                "Seleccioná un voluntario de la tabla."
            )
            return

        valores = tabla.item(seleccionado[0], "values")
        id_voluntario = valores[0]
        nombre = valores[1]

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Querés eliminar a {nombre}?"
        )

        if not confirmar:
            return

        try:
            respuesta = requests.delete(
                f"{API_URL}/{id_voluntario}",
                timeout=5
            )
            respuesta.raise_for_status()

            messagebox.showinfo(
                "Correcto",
                "Voluntario eliminado correctamente."
            )
            cargar_datos()

        except requests.RequestException as error:
            detalle = error

            if getattr(error, "response", None) is not None:
                detalle = error.response.text

            messagebox.showerror(
                "Error",
                f"No se pudo eliminar el voluntario.\n{detalle}"
            )

    # ==========================================
    # BOTONES DE ACCIÓN
    # ==========================================
    acciones = tk.Frame(panel, bg=FONDO)
    acciones.pack(
        fill="x",
        padx=25,
        pady=(0, 15),
        before=marco_tabla
    )

    tk.Button(
        acciones,
        text="✎  Editar seleccionado",
        command=editar_voluntario,
        bg=VERDE,
        fg=BLANCO,
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        padx=12,
        pady=8
    ).pack(side="left", padx=(0, 8))

    tk.Button(
        acciones,
        text="♲  Eliminar seleccionado",
        command=eliminar_voluntario,
        bg=NARANJA,
        fg=BLANCO,
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        padx=12,
        pady=8
    ).pack(side="left")

    # Cargar personas antes de abrir formularios de voluntarios.
    obtener_personas()

    # Cargar los voluntarios al abrir la pantalla
    cargar_datos()
