import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime


# ============================================================
# CONFIGURACIÓN
# ============================================================

API_URL = "http://localhost:3000/api/animales"


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def crear_animales(parent):

    # --------------------------------------------------------
    # COLORES
    # --------------------------------------------------------

    FONDO = "#F5F3ED"
    VERDE_OSCURO = "#396348"
    VERDE = "#4F7F5F"
    VERDE_CLARO = "#EAF4ED"
    BLANCO = "#FFFFFF"
    GRIS = "#777777"
    GRIS_CLARO = "#E5E5E0"
    BORDE = "#E0E0D8"
    ROJO = "#EF4444"
    NEGRO = "#222222"

    # --------------------------------------------------------
    # FRAME PRINCIPAL
    # --------------------------------------------------------

    frame = tk.Frame(parent, bg=FONDO)
    frame.pack(fill="both", expand=True)

    # ========================================================
    # BARRA LATERAL
    # ========================================================

    sidebar = tk.Frame(
        frame,
        bg=VERDE_OSCURO,
        width=190
    )

    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # Logo
    logo_frame = tk.Frame(sidebar, bg=VERDE_OSCURO)
    logo_frame.pack(fill="x", pady=(25, 35))

    tk.Label(
        logo_frame,
        text="🐾",
        font=("Arial", 25),
        bg=VERDE_OSCURO,
        fg="#1683E8"
    ).pack(side="left", padx=(20, 5))

    tk.Label(
        logo_frame,
        text="PetManager",
        font=("Arial", 16, "bold"),
        bg=VERDE_OSCURO,
        fg=BLANCO
    ).pack(side="left")

    # Botones del menú
    def boton_menu(texto, activo=False):

        color = VERDE_OSCURO

        boton = tk.Button(
            sidebar,
            text=texto,
            font=("Arial", 11),
            anchor="w",
            padx=25,
            pady=12,
            bg=color,
            fg=BLANCO,
            activebackground="#24496F",
            activeforeground=BLANCO,
            relief="flat",
            bd=0
        )

        boton.pack(fill="x", padx=10, pady=3)

        return boton

    boton_menu("⌂   Inicio")
    boton_menu("🐾   Animales", True)
    boton_menu("👥   Personal")
    boton_menu("▣   Turnos")
    boton_menu("⚙   Configuración")

    # Usuario
    usuario = tk.Frame(sidebar, bg=VERDE_OSCURO)
    usuario.pack(side="bottom", fill="x", pady=20)

    tk.Label(
        usuario,
        text="●",
        font=("Arial", 18),
        bg=VERDE_OSCURO,
        fg="#A9C7E8"
    ).pack(side="left", padx=(20, 8))

    tk.Label(
        usuario,
        text="Sarah Jenkins",
        font=("Arial", 10, "bold"),
        bg=VERDE_OSCURO,
        fg=BLANCO
    ).pack(side="left")

    # La navegación pertenece al menú principal de inicio.py. Esta vista no
    # debe crear un segundo menú lateral.
    sidebar.destroy()

    # ========================================================
    # CONTENIDO PRINCIPAL
    # ========================================================

    contenido = tk.Frame(frame, bg=FONDO)
    contenido.pack(fill="both", expand=True)

    # --------------------------------------------------------
    # CABECERA
    # --------------------------------------------------------

    header = tk.Frame(
        contenido,
        bg=BLANCO,
        height=58
    )

    header.pack(fill="x")
    header.pack_propagate(False)

    titulo = tk.Label(
        header,
        text="Registros de Animales",
        font=("Arial", 15, "bold"),
        bg=BLANCO,
        fg=NEGRO
    )

    titulo.pack(side="left", padx=25)

    # Botón agregar
    boton_agregar = tk.Button(
        header,
        text="+  Agregar animal",
        font=("Arial", 11, "bold"),
        bg=VERDE,
        fg=BLANCO,
        activebackground=VERDE_OSCURO,
        activeforeground=BLANCO,
        relief="flat",
        padx=15,
        pady=8,
        cursor="hand2"
    )

    boton_agregar.pack(side="right", padx=20, pady=9)

    # ========================================================
    # ZONA CENTRAL
    # ========================================================

    centro = tk.Frame(contenido, bg=FONDO)
    centro.pack(fill="both", expand=True, padx=22, pady=22)

    # ========================================================
    # PANEL TABLA
    # ========================================================

    tabla_panel = tk.Frame(
        centro,
        bg=BLANCO,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    tabla_panel.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 12)
    )

    # --------------------------------------------------------
    # INFORMACIÓN DE TABLA
    # --------------------------------------------------------

    info = tk.Frame(tabla_panel, bg=BLANCO)
    info.pack(fill="x", padx=15, pady=15)

    total_label = tk.Label(
        info,
        text="Total de Animales: 0",
        font=("Arial", 12, "bold"),
        bg=BLANCO,
        fg=NEGRO
    )

    total_label.pack(side="left")

    # --------------------------------------------------------
    # BUSCADOR
    # --------------------------------------------------------

    buscar_frame = tk.Frame(info, bg=BLANCO)
    buscar_frame.pack(side="right")

    tk.Label(
        buscar_frame,
        text="🔍",
        bg=BLANCO,
        font=("Arial", 12)
    ).pack(side="left")

    buscar_entry = tk.Entry(
        buscar_frame,
        width=25,
        font=("Arial", 10),
        relief="solid",
        bd=1
    )

    buscar_entry.pack(side="left", ipady=7, padx=5)

    # --------------------------------------------------------
    # FILTRO
    # --------------------------------------------------------

    tk.Label(
        tabla_panel,
        text="Filtrar por: Todos (Tabla)",
        font=("Arial", 9, "underline"),
        bg=BLANCO,
        fg=VERDE,
        anchor="w"
    ).pack(fill="x", padx=15)

    # ========================================================
    # TABLA
    # ========================================================

    tabla_frame = tk.Frame(tabla_panel, bg=BLANCO)
    tabla_frame.pack(fill="both", expand=True, padx=15, pady=10)

    columnas = (
        "id",
        "nombre",
        "especie",
        "raza",
        "sexo",
        "fecha",
        "estado"
    )

    tabla = ttk.Treeview(
        tabla_frame,
        columns=columnas,
        show="headings",
        selectmode="browse"
    )

    tabla.heading("id", text="ID")
    tabla.heading("nombre", text="Nombre")
    tabla.heading("especie", text="Especie")
    tabla.heading("raza", text="Raza")
    tabla.heading("sexo", text="Sexo")
    tabla.heading("fecha", text="Fecha de Nacimiento")
    tabla.heading("estado", text="Estado")

    tabla.column("id", width=55, anchor="center")
    tabla.column("nombre", width=110)
    tabla.column("especie", width=90)
    tabla.column("raza", width=140)
    tabla.column("sexo", width=80)
    tabla.column("fecha", width=130)
    tabla.column("estado", width=100)

    # Scroll vertical
    scroll_y = ttk.Scrollbar(
        tabla_frame,
        orient="vertical",
        command=tabla.yview
    )

    tabla.configure(yscrollcommand=scroll_y.set)

    tabla.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    # --------------------------------------------------------
    # ESTILO TABLA
    # --------------------------------------------------------

    estilo = ttk.Style()

    estilo.theme_use("clam")

    estilo.configure(
        "Treeview",
        background=BLANCO,
        foreground=NEGRO,
        rowheight=42,
        fieldbackground=BLANCO,
        font=("Arial", 9)
    )

    estilo.configure(
        "Treeview.Heading",
        background=FONDO,
        foreground=NEGRO,
        font=("Arial", 9, "bold"),
        padding=8
    )

    estilo.map(
        "Treeview",
        background=[
            ("selected", VERDE_CLARO)
        ],
        foreground=[
            ("selected", NEGRO)
        ]
    )

    # ========================================================
    # PANEL DERECHO - FORMULARIO
    # ========================================================

    formulario = tk.Frame(
        centro,
        bg=BLANCO,
        width=330,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    formulario.pack(side="right", fill="y")
    formulario.pack_propagate(False)

    # --------------------------------------------------------
    # TÍTULO
    # --------------------------------------------------------

    titulo_form = tk.Label(
        formulario,
        text="Nuevo / Editar Registro de Animal",
        font=("Arial", 13, "bold"),
        bg=BLANCO,
        fg=NEGRO
    )

    titulo_form.pack(
        fill="x",
        padx=18,
        pady=(20, 15)
    )

    # ========================================================
    # VARIABLES
    # ========================================================

    id_actual = tk.StringVar()

    nombre_var = tk.StringVar()
    especie_var = tk.StringVar()
    raza_var = tk.StringVar()
    sexo_var = tk.StringVar(value="Macho")
    fecha_var = tk.StringVar()
    estado_var = tk.StringVar(value="Activo")

    # ========================================================
    # CAMPOS
    # ========================================================

    def crear_campo(texto, variable):

        tk.Label(
            formulario,
            text=texto,
            font=("Arial", 9, "bold"),
            bg=BLANCO,
            fg=NEGRO,
            anchor="w"
        ).pack(fill="x", padx=18, pady=(5, 3))

        entry = tk.Entry(
            formulario,
            textvariable=variable,
            font=("Arial", 10),
            relief="solid",
            bd=1
        )

        entry.pack(
            fill="x",
            padx=18,
            ipady=7
        )

        return entry

    crear_campo("Nombre", nombre_var)

    # Especie
    tk.Label(
        formulario,
        text="Especie",
        font=("Arial", 9, "bold"),
        bg=BLANCO,
        fg=NEGRO,
        anchor="w"
    ).pack(fill="x", padx=18, pady=(10, 3))

    especie_combo = ttk.Combobox(
        formulario,
        textvariable=especie_var,
        values=("Perro", "Gato", "Ave", "Conejo", "Otro"),
        state="readonly"
    )

    especie_combo.pack(
        fill="x",
        padx=18,
        ipady=5
    )

    crear_campo("Raza", raza_var)

    # ========================================================
    # SEXO
    # ========================================================

    tk.Label(
        formulario,
        text="Sexo",
        font=("Arial", 9, "bold"),
        bg=BLANCO,
        fg=NEGRO,
        anchor="w"
    ).pack(fill="x", padx=18, pady=(10, 3))

    sexo_frame = tk.Frame(formulario, bg=BLANCO)
    sexo_frame.pack(fill="x", padx=18)

    tk.Radiobutton(
        sexo_frame,
        text="Macho",
        variable=sexo_var,
        value="Macho",
        bg=BLANCO
    ).pack(side="left")

    tk.Radiobutton(
        sexo_frame,
        text="Hembra",
        variable=sexo_var,
        value="Hembra",
        bg=BLANCO
    ).pack(side="left")

    tk.Radiobutton(
        sexo_frame,
        text="Desconocido",
        variable=sexo_var,
        value="Desconocido",
        bg=BLANCO
    ).pack(side="left")

    crear_campo(
        "Fecha de Nacimiento (dd/mm/aaaa)",
        fecha_var
    )

    # ========================================================
    # ESTADO
    # ========================================================

    tk.Label(
        formulario,
        text="Estado",
        font=("Arial", 9, "bold"),
        bg=BLANCO,
        fg=NEGRO,
        anchor="w"
    ).pack(fill="x", padx=18, pady=(10, 3))

    estado_combo = ttk.Combobox(
        formulario,
        textvariable=estado_var,
        values=(
            "Activo",
            "Saludable",
            "En tratamiento",
            "Adoptado",
            "Inactivo"
        ),
        state="readonly"
    )

    estado_combo.pack(
        fill="x",
        padx=18,
        ipady=5
    )

    # ========================================================
    # ID
    # ========================================================

    tk.Label(
        formulario,
        text="ID del Animal",
        font=("Arial", 9, "bold"),
        bg=BLANCO,
        fg=NEGRO,
        anchor="w"
    ).pack(fill="x", padx=18, pady=(10, 3))

    id_label = tk.Label(
        formulario,
        textvariable=id_actual,
        font=("Arial", 10),
        bg=VERDE_CLARO,
        fg=GRIS,
        anchor="w",
        padx=10
    )

    id_label.pack(
        fill="x",
        padx=18,
        ipady=7
    )

    # ========================================================
    # BOTONES
    # ========================================================

    botones = tk.Frame(formulario, bg=BLANCO)
    botones.pack(
        side="bottom",
        fill="x",
        padx=18,
        pady=20
    )

    botones.columnconfigure(0, weight=1)
    botones.columnconfigure(1, weight=1)

    boton_cancelar = tk.Button(
        botones,
        text="Cancelar",
        font=("Arial", 10, "bold"),
        bg=GRIS,
        fg=BLANCO,
        relief="flat",
        padx=18,
        pady=9
    )

    boton_cancelar.grid(
        row=0,
        column=0,
        sticky="ew",
        padx=(0, 4)
    )

    boton_eliminar = tk.Button(
        botones,
        text="Eliminar",
        font=("Arial", 10, "bold"),
        bg="#C95C5C",
        fg=BLANCO,
        activebackground="#A94444",
        activeforeground=BLANCO,
        relief="flat",
        padx=14,
        pady=9,
        cursor="hand2"
    )

    boton_eliminar.grid(
        row=0,
        column=1,
        sticky="ew",
        padx=(4, 0)
    )

    boton_guardar = tk.Button(
        botones,
        text="Guardar Registro",
        font=("Arial", 10, "bold"),
        bg=VERDE,
        fg=BLANCO,
        relief="flat",
        padx=15,
        pady=9
    )

    boton_guardar.grid(
        row=1,
        column=0,
        columnspan=2,
        sticky="ew",
        pady=(8, 0)
    )

    # ========================================================
    # FUNCIONES CRUD
    # ========================================================

    def convertir_fecha_para_api(valor):

        try:
            return datetime.strptime(
                valor.strip(),
                "%d/%m/%Y"
            ).strftime("%Y-%m-%d")
        except ValueError:
            return None


    def convertir_fecha_desde_api(valor):

        try:
            return datetime.strptime(
                str(valor)[:10],
                "%Y-%m-%d"
            ).strftime("%d/%m/%Y")
        except ValueError:
            return str(valor)

    def limpiar_formulario():

        id_actual.set("")
        nombre_var.set("")
        especie_var.set("")
        raza_var.set("")
        sexo_var.set("Macho")
        fecha_var.set("")
        estado_var.set("Activo")

        titulo_form.config(
            text="Nuevo / Editar Registro de Animal"
        )

    # --------------------------------------------------------
    # CARGAR ANIMALES
    # --------------------------------------------------------

    def cargar_animales():

        try:

            respuesta = requests.get(API_URL, timeout=5)

            if respuesta.status_code != 200:
                raise Exception("Error en el servidor")

            animales = respuesta.json()

            tabla.delete(*tabla.get_children())

            for animal in animales:

                tabla.insert(
                    "",
                    "end",
                    values=(
                        animal.get("id_animal", ""),
                        animal.get("nombre", ""),
                        animal.get("especie", ""),
                        animal.get("raza", ""),
                        animal.get("sexo", ""),
                        convertir_fecha_desde_api(
                            animal.get("fecha_nacimiento", "")
                        ),
                        animal.get("estado_actual", "")
                    )
                )

            total_label.config(
                text=f"Total de Animales: {len(animales)}"
            )

        except requests.exceptions.RequestException:

            messagebox.showerror(
                "Error",
                "No se pudo conectar con el backend.\n\n"
                "Verificá que Node.js esté ejecutándose."
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    # --------------------------------------------------------
    # AGREGAR
    # --------------------------------------------------------

    def agregar_animal():

        fecha_nacimiento = convertir_fecha_para_api(
            fecha_var.get()
        )

        if not fecha_nacimiento:
            messagebox.showwarning(
                "Fecha invÃ¡lida",
                "IngresÃ¡ la fecha con el formato dd/mm/aaaa."
            )
            return

        datos = {
            "nombre": nombre_var.get(),
            "especie": especie_var.get(),
            "raza": raza_var.get(),
            "sexo": sexo_var.get(),
            "fecha_nacimiento": fecha_nacimiento,
            "estado_actual": estado_var.get()
        }

        if not datos["nombre"] or not datos["especie"]:

            messagebox.showwarning(
                "Datos incompletos",
                "Completá como mínimo el nombre y la especie."
            )

            return

        try:

            respuesta = requests.post(
                API_URL,
                json=datos,
                timeout=5
            )

            if respuesta.status_code == 201:

                messagebox.showinfo(
                    "Correcto",
                    "Animal agregado correctamente."
                )

                limpiar_formulario()
                cargar_animales()

            else:

                messagebox.showerror(
                    "Error",
                    respuesta.json().get(
                        "error",
                        "No se pudo agregar el animal"
                    )
                )

        except requests.exceptions.RequestException:

            messagebox.showerror(
                "Error",
                "No se pudo conectar con el backend."
            )

    # --------------------------------------------------------
    # OBTENER ANIMAL
    # --------------------------------------------------------

    def obtener_animal(id_animal):

        try:

            respuesta = requests.get(
                f"{API_URL}/{id_animal}",
                timeout=5
            )

            if respuesta.status_code != 200:

                messagebox.showerror(
                    "Error",
                    "No se pudo obtener el animal."
                )

                return

            animal = respuesta.json()

            id_actual.set(animal.get("id_animal", ""))
            nombre_var.set(animal.get("nombre", ""))
            especie_var.set(animal.get("especie", ""))
            raza_var.set(animal.get("raza", ""))
            sexo_var.set(animal.get("sexo", "Macho"))

            fecha = animal.get(
                "fecha_nacimiento",
                ""
            )

            # MySQL puede devolver la fecha como string
            if fecha:
                fecha = convertir_fecha_desde_api(fecha)

            fecha_var.set(fecha)

            estado_var.set(
                animal.get(
                    "estado_actual",
                    "Activo"
                )
            )

            titulo_form.config(
                text="Editar Registro de Animal"
            )

        except requests.exceptions.RequestException:

            messagebox.showerror(
                "Error",
                "No se pudo conectar con el backend."
            )

    # --------------------------------------------------------
    # EDITAR
    # --------------------------------------------------------

    def editar_animal():

        id_animal = id_actual.get()

        if not id_animal:

            messagebox.showwarning(
                "Seleccionar animal",
                "Seleccioná primero un animal de la tabla."
            )

            return

        fecha_nacimiento = convertir_fecha_para_api(
            fecha_var.get()
        )

        if not fecha_nacimiento:
            messagebox.showwarning(
                "Fecha invÃ¡lida",
                "IngresÃ¡ la fecha con el formato dd/mm/aaaa."
            )
            return

        datos = {
            "nombre": nombre_var.get(),
            "especie": especie_var.get(),
            "raza": raza_var.get(),
            "sexo": sexo_var.get(),
            "fecha_nacimiento": fecha_nacimiento,
            "estado_actual": estado_var.get()
        }

        try:

            respuesta = requests.put(
                f"{API_URL}/{id_animal}",
                json=datos,
                timeout=5
            )

            if respuesta.status_code == 200:

                messagebox.showinfo(
                    "Correcto",
                    "Animal actualizado correctamente."
                )

                limpiar_formulario()
                cargar_animales()

            else:

                messagebox.showerror(
                    "Error",
                    respuesta.json().get(
                        "error",
                        "No se pudo actualizar el animal"
                    )
                )

        except requests.exceptions.RequestException:

            messagebox.showerror(
                "Error",
                "No se pudo conectar con el backend."
            )

    # --------------------------------------------------------
    # ELIMINAR
    # --------------------------------------------------------

    def eliminar_animal():

        seleccion = tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Seleccionar animal",
                "Seleccioná un animal de la tabla."
            )

            return

        datos = tabla.item(seleccion[0])
        id_animal = datos["values"][0]

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Querés eliminar al animal con ID {id_animal}?"
        )

        if not confirmar:
            return

        try:

            respuesta = requests.delete(
                f"{API_URL}/{id_animal}",
                timeout=5
            )

            if respuesta.status_code == 200:

                messagebox.showinfo(
                    "Correcto",
                    "Animal eliminado correctamente."
                )

                limpiar_formulario()
                cargar_animales()

            else:

                messagebox.showerror(
                    "Error",
                    respuesta.json().get(
                        "error",
                        "No se pudo eliminar el animal"
                    )
                )

        except requests.exceptions.RequestException:

            messagebox.showerror(
                "Error",
                "No se pudo conectar con el backend."
            )

    # ========================================================
    # EVENTOS DE TABLA
    # ========================================================

    def seleccionar_animal(event):

        seleccion = tabla.selection()

        if not seleccion:
            return

        datos = tabla.item(seleccion[0])

        id_animal = datos["values"][0]

        obtener_animal(id_animal)

    tabla.bind(
        "<<TreeviewSelect>>",
        seleccionar_animal
    )

    # ========================================================
    # BOTÓN GUARDAR
    # ========================================================

    def guardar():

        if id_actual.get():

            editar_animal()

        else:

            agregar_animal()

    boton_guardar.config(
        command=guardar
    )

    boton_eliminar.config(
        command=eliminar_animal
    )

    boton_agregar.config(
        command=limpiar_formulario
    )

    boton_cancelar.config(
        command=limpiar_formulario
    )

    # ========================================================
    # BUSCADOR
    # ========================================================

    def buscar(event=None):

        texto = buscar_entry.get().lower()

        for item in tabla.get_children():

            valores = tabla.item(item)["values"]

            encontrado = any(
                texto in str(valor).lower()
                for valor in valores
            )

            if encontrado:

                tabla.reattach(
                    item,
                    "",
                    "end"
                )

            else:

                tabla.detach(item)

    buscar_entry.bind(
        "<KeyRelease>",
        buscar
    )

    # ========================================================
    # CARGAR DATOS AL INICIAR
    # ========================================================

    cargar_animales()

    return frame
