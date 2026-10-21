import tkinter as tk
from tkinter import ttk, messagebox
import requests


API_URL = "http://localhost:3000/api/personas"


def crear_personas(parent):

    FONDO = "#F5F3ED"
    BLANCO = "#FFFFFF"
    VERDE = "#4F7F5F"
    VERDE_OSCURO = "#396348"
    VERDE_CLARO = "#EAF4ED"
    GRIS = "#777777"
    BORDE = "#E0E0D8"
    NEGRO = "#222222"
    ROJO = "#C95C5C"

    frame = tk.Frame(parent, bg=FONDO)
    frame.pack(fill="both", expand=True)

    encabezado = tk.Frame(frame, bg=BLANCO, height=58)
    encabezado.pack(fill="x")
    encabezado.pack_propagate(False)

    tk.Label(
        encabezado,
        text="Personas",
        font=("Arial", 15, "bold"),
        bg=BLANCO,
        fg=NEGRO
    ).pack(side="left", padx=25)

    boton_nuevo = tk.Button(
        encabezado,
        text="+  Nueva persona",
        font=("Arial", 10, "bold"),
        bg=VERDE,
        fg=BLANCO,
        activebackground=VERDE_OSCURO,
        activeforeground=BLANCO,
        relief="flat",
        cursor="hand2",
        padx=15,
        pady=8
    )
    boton_nuevo.pack(side="right", padx=20, pady=9)

    contenido = tk.Frame(frame, bg=FONDO)
    contenido.pack(fill="both", expand=True, padx=22, pady=22)

    formulario = tk.Frame(
        contenido,
        bg=BLANCO,
        width=285,
        highlightbackground=BORDE,
        highlightthickness=1
    )
    formulario.pack(side="right", fill="y", padx=(16, 0))
    formulario.pack_propagate(False)

    tk.Label(
        formulario,
        text="Nueva / Editar persona",
        font=("Arial", 13, "bold"),
        bg=BLANCO,
        fg=NEGRO
    ).pack(anchor="w", padx=18, pady=(18, 14))

    id_actual = tk.StringVar()
    campos = {
        "nombre": tk.StringVar(),
        "apellido": tk.StringVar(),
        "dni": tk.StringVar(),
        "telefono": tk.StringVar(),
        "email": tk.StringVar(),
        "direccion": tk.StringVar()
    }

    def crear_campo(etiqueta, clave):
        tk.Label(
            formulario,
            text=etiqueta,
            font=("Arial", 9, "bold"),
            bg=BLANCO,
            fg=NEGRO,
            anchor="w"
        ).pack(fill="x", padx=18, pady=(4, 3))

        entry = tk.Entry(
            formulario,
            textvariable=campos[clave],
            font=("Arial", 10),
            relief="solid",
            bd=1
        )
        entry.pack(fill="x", padx=18, ipady=6)

    for etiqueta, clave in [
        ("Nombre", "nombre"),
        ("Apellido", "apellido"),
        ("DNI", "dni"),
        ("Teléfono", "telefono"),
        ("Email", "email"),
        ("Dirección", "direccion")
    ]:
        crear_campo(etiqueta, clave)

    tk.Label(
        formulario,
        textvariable=id_actual,
        font=("Arial", 9),
        bg=VERDE_CLARO,
        fg=GRIS,
        anchor="w",
        padx=8
    ).pack(fill="x", padx=18, pady=(12, 8), ipady=5)

    acciones = tk.Frame(formulario, bg=BLANCO)
    acciones.pack(side="bottom", fill="x", padx=18, pady=18)

    tabla_panel = tk.Frame(
        contenido,
        bg=BLANCO,
        highlightbackground=BORDE,
        highlightthickness=1
    )
    tabla_panel.pack(side="left", fill="both", expand=True)

    buscar = tk.StringVar()
    personas_data = []

    barra = tk.Frame(tabla_panel, bg=BLANCO)
    barra.pack(fill="x", padx=15, pady=15)

    tk.Label(
        barra,
        text="Personas registradas",
        font=("Arial", 12, "bold"),
        bg=BLANCO,
        fg=NEGRO
    ).pack(side="left")

    tk.Entry(
        barra,
        textvariable=buscar,
        font=("Arial", 10),
        relief="solid",
        bd=1
    ).pack(side="right", ipady=6, padx=(10, 0))

    tabla_frame = tk.Frame(tabla_panel, bg=BLANCO)
    tabla_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    columnas = (
        "id_persona", "nombre", "apellido", "dni",
        "telefono", "email", "direccion"
    )

    tabla = ttk.Treeview(
        tabla_frame,
        columns=columnas,
        show="headings",
        selectmode="browse"
    )

    encabezados = {
        "id_persona": "ID",
        "nombre": "NOMBRE",
        "apellido": "APELLIDO",
        "dni": "DNI",
        "telefono": "TELÉFONO",
        "email": "EMAIL",
        "direccion": "DIRECCIÓN"
    }

    anchos = {
        "id_persona": 45,
        "nombre": 110,
        "apellido": 110,
        "dni": 90,
        "telefono": 100,
        "email": 170,
        "direccion": 150
    }

    for columna in columnas:
        tabla.heading(columna, text=encabezados[columna])
        tabla.column(columna, width=anchos[columna], minwidth=45, anchor="w")

    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure(
        "Treeview",
        background=BLANCO,
        foreground=NEGRO,
        fieldbackground=BLANCO,
        rowheight=36,
        font=("Arial", 9)
    )
    estilo.configure(
        "Treeview.Heading",
        background=FONDO,
        foreground=GRIS,
        font=("Arial", 9, "bold"),
        padding=8
    )
    estilo.map(
        "Treeview",
        background=[("selected", VERDE_CLARO)],
        foreground=[("selected", NEGRO)]
    )

    scrollbar = ttk.Scrollbar(
        tabla_frame,
        orient="vertical",
        command=tabla.yview
    )
    tabla.configure(yscrollcommand=scrollbar.set)
    tabla.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
    tabla_frame.grid_rowconfigure(0, weight=1)
    tabla_frame.grid_columnconfigure(0, weight=1)

    def limpiar_formulario():
        id_actual.set("")
        for variable in campos.values():
            variable.set("")

    def persona_seleccionada():
        seleccion = tabla.selection()
        if not seleccion:
            return None

        id_persona = tabla.item(seleccion[0], "values")[0]
        return next(
            (
                persona for persona in personas_data
                if str(persona.get("id_persona")) == str(id_persona)
            ),
            None
        )

    def cargar_formulario(persona):
        id_actual.set(f"ID: {persona.get('id_persona', '')}")
        for clave, variable in campos.items():
            variable.set(persona.get(clave, ""))

    def actualizar_tabla(*_args):
        filtro = buscar.get().strip().lower()
        tabla.delete(*tabla.get_children())

        for persona in personas_data:
            valores = tuple(persona.get(clave, "") for clave in columnas)
            if filtro and filtro not in " ".join(map(str, valores)).lower():
                continue
            tabla.insert("", "end", values=valores)

    def cargar_personas():
        nonlocal personas_data
        try:
            respuesta = requests.get(API_URL, timeout=5)
            respuesta.raise_for_status()
            personas_data = respuesta.json()
            actualizar_tabla()
        except requests.RequestException as error:
            messagebox.showerror(
                "Error de conexión",
                f"No se pudieron cargar las personas.\n\n{error}"
            )

    def guardar_persona():
        datos = {clave: variable.get().strip() for clave, variable in campos.items()}

        if any(not valor for valor in datos.values()):
            messagebox.showwarning(
                "Datos incompletos",
                "Completá todos los campos de la persona."
            )
            return

        try:
            id_persona = id_actual.get().replace("ID: ", "").strip()
            if id_persona:
                respuesta = requests.put(
                    f"{API_URL}/{id_persona}",
                    json=datos,
                    timeout=5
                )
            else:
                respuesta = requests.post(API_URL, json=datos, timeout=5)

            respuesta.raise_for_status()
            messagebox.showinfo("Correcto", "Persona guardada correctamente.")
            limpiar_formulario()
            cargar_personas()
        except requests.RequestException as error:
            detalle = getattr(error.response, "text", str(error))
            messagebox.showerror("Error", f"No se pudo guardar la persona.\n{detalle}")

    def eliminar_persona():
        persona = persona_seleccionada()
        if not persona:
            messagebox.showwarning(
                "Seleccionar persona",
                "Seleccioná una persona de la tabla."
            )
            return

        if not messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Querés eliminar a {persona.get('nombre', '')} {persona.get('apellido', '')}?"
        ):
            return

        try:
            respuesta = requests.delete(
                f"{API_URL}/{persona['id_persona']}",
                timeout=5
            )
            respuesta.raise_for_status()
            messagebox.showinfo("Correcto", "Persona eliminada correctamente.")
            limpiar_formulario()
            cargar_personas()
        except requests.RequestException as error:
            detalle = getattr(error.response, "text", str(error))
            messagebox.showerror("Error", f"No se pudo eliminar la persona.\n{detalle}")

    tabla.bind("<<TreeviewSelect>>", lambda _event: (
        cargar_formulario(persona_seleccionada())
        if persona_seleccionada() else None
    ))
    buscar.trace_add("write", actualizar_tabla)

    tk.Button(
        acciones,
        text="Guardar",
        font=("Arial", 10, "bold"),
        bg=VERDE,
        fg=BLANCO,
        activebackground=VERDE_OSCURO,
        relief="flat",
        cursor="hand2",
        pady=8,
        command=guardar_persona
    ).pack(fill="x", pady=(0, 7))

    tk.Button(
        acciones,
        text="Eliminar seleccionada",
        font=("Arial", 10, "bold"),
        bg=ROJO,
        fg=BLANCO,
        activebackground="#A94444",
        relief="flat",
        cursor="hand2",
        pady=8,
        command=eliminar_persona
    ).pack(fill="x", pady=(0, 7))

    tk.Button(
        acciones,
        text="Limpiar formulario",
        font=("Arial", 10),
        bg=FONDO,
        fg=NEGRO,
        relief="flat",
        cursor="hand2",
        pady=7,
        command=limpiar_formulario
    ).pack(fill="x")

    boton_nuevo.config(command=limpiar_formulario)
    cargar_personas()

    return frame
