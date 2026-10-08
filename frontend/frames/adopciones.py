import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

BASE_URL = "http://localhost:3000"

# Si en tu app montaste las rutas así:
# app.use('/adopciones', adopcionesRouter);
ADOPCIONES_URL = f"{BASE_URL}/adopciones"

# Para poder mostrar nombre del animal y del adoptante
ANIMALES_URL = f"{BASE_URL}/animales"
PERSONAS_URL = f"{BASE_URL}/personas"


# ==========================================================
# PANTALLA DE ADOPCIONES
# ==========================================================

def crear_adopciones(parent):

    # ------------------------------------------------------
    # VARIABLES
    # ------------------------------------------------------

    animales = []
    personas = []

    mapa_animales = {}
    mapa_personas = {}

    adopciones_data = []

    # ------------------------------------------------------
    # FRAME PRINCIPAL
    # ------------------------------------------------------

    frame = tk.Frame(parent, bg="#F7F7F3")
    frame.pack(fill="both", expand=True)

    # ------------------------------------------------------
    # COLORES
    # ------------------------------------------------------

    VERDE = "#4F8060"
    VERDE_CLARO = "#E7F3EB"
    VERDE_OSCURO = "#28583A"

    NARANJA = "#D97706"
    NARANJA_CLARO = "#FFF3E5"

    ROJO = "#C92A2A"
    ROJO_CLARO = "#FDEAEA"

    GRIS = "#6B7280"
    GRIS_CLARO = "#F1F3F0"

    BLANCO = "#FFFFFF"

    # ------------------------------------------------------
    # ESTILO
    # ------------------------------------------------------

    style = ttk.Style()

    try:
        style.theme_use("clam")
    except:
        pass

    style.configure(
        "Treeview",
        background="white",
        foreground="#374151",
        rowheight=48,
        fieldbackground="white",
        font=("Segoe UI", 10)
    )

    style.configure(
        "Treeview.Heading",
        background="#F7F7F3",
        foreground="#64748B",
        font=("Segoe UI", 9, "bold"),
        relief="flat"
    )

    style.map(
        "Treeview",
        background=[("selected", "#E7F3EB")],
        foreground=[("selected", "#28583A")]
    )

    # ------------------------------------------------------
    # FUNCIONES API
    # ------------------------------------------------------

    def obtener_animales():
        nonlocal animales, mapa_animales

        try:
            respuesta = requests.get(ANIMALES_URL, timeout=5)

            if respuesta.status_code == 200:
                animales = respuesta.json()

                mapa_animales = {}

                for animal in animales:
                    id_animal = animal.get("id_animal")
                    nombre = animal.get("nombre", "Sin nombre")

                    if id_animal is not None:
                        mapa_animales[id_animal] = nombre

                return True

        except requests.exceptions.RequestException:
            pass

        return False


    def obtener_personas():
        nonlocal personas, mapa_personas

        try:
            respuesta = requests.get(PERSONAS_URL, timeout=5)

            if respuesta.status_code == 200:
                personas = respuesta.json()

                mapa_personas = {}

                for persona in personas:

                    id_persona = persona.get("id_persona")

                    nombre = persona.get("nombre", "")
                    apellido = persona.get("apellido", "")

                    nombre_completo = f"{nombre} {apellido}".strip()

                    if not nombre_completo:
                        nombre_completo = persona.get(
                            "nombre_completo",
                            persona.get("email", "Sin nombre")
                        )

                    if id_persona is not None:
                        mapa_personas[id_persona] = nombre_completo

                return True

        except requests.exceptions.RequestException:
            pass

        return False


    def obtener_adopciones():

        try:

            respuesta = requests.get(
                ADOPCIONES_URL,
                timeout=5
            )

            if respuesta.status_code == 200:

                return respuesta.json()

            messagebox.showerror(
                "Error",
                "No se pudieron obtener las adopciones."
            )

        except requests.exceptions.RequestException as error:

            messagebox.showerror(
                "Error de conexión",
                f"No se pudo conectar con el servidor.\n\n{error}"
            )

        return []


    # ------------------------------------------------------
    # FUNCIONES AUXILIARES
    # ------------------------------------------------------

    def nombre_animal(id_animal):

        return mapa_animales.get(
            id_animal,
            f"ID {id_animal}"
        )


    def nombre_persona(id_persona):

        return mapa_personas.get(
            id_persona,
            f"ID {id_persona}"
        )


    def color_estado(estado):

        estado = str(estado).lower()

        if estado == "aprobada":
            return VERDE_CLARO

        if estado == "pendiente":
            return NARANJA_CLARO

        if estado == "rechazada":
            return ROJO_CLARO

        return GRIS_CLARO


    def contar_estados(datos):

        aprobadas = 0
        pendientes = 0
        rechazadas = 0

        for adopcion in datos:

            estado = str(
                adopcion.get("estado_seguimiento", "")
            ).lower()

            if estado == "aprobada":
                aprobadas += 1

            elif estado == "pendiente":
                pendientes += 1

            elif estado == "rechazada":
                rechazadas += 1

        return aprobadas, pendientes, rechazadas


    # ------------------------------------------------------
    # ENCABEZADO
    # ------------------------------------------------------

    encabezado = tk.Frame(
        frame,
        bg="#F7F7F3"
    )

    encabezado.pack(
        fill="x",
        padx=25,
        pady=(20, 10)
    )


    titulo = tk.Label(
        encabezado,
        text="Gestión de Adopciones",
        font=("Segoe UI", 20, "bold"),
        bg="#F7F7F3",
        fg="#26352B"
    )

    titulo.pack(anchor="w")


    total_label = tk.Label(
        encabezado,
        text="Total registradas: 0",
        font=("Segoe UI", 10),
        bg="#F7F7F3",
        fg="#6B7280"
    )

    total_label.pack(anchor="w", pady=(2, 0))


    # ------------------------------------------------------
    # BOTÓN NUEVA ADOPCIÓN
    # ------------------------------------------------------

    boton_nueva = tk.Button(
        encabezado,
        text="＋  Nueva Adopción",
        font=("Segoe UI", 10, "bold"),
        bg=VERDE,
        fg="white",
        activebackground=VERDE_OSCURO,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        padx=18,
        pady=10,
        command=lambda: ventana_adopcion()
    )

    boton_nueva.place(
        relx=1,
        y=0,
        anchor="ne"
    )


    # ------------------------------------------------------
    # TARJETAS DE ESTADOS
    # ------------------------------------------------------

    tarjetas = tk.Frame(
        frame,
        bg="#F7F7F3"
    )

    tarjetas.pack(
        fill="x",
        padx=25,
        pady=5
    )


    # -------- APROBADAS --------

    tarjeta_aprobadas = tk.Frame(
        tarjetas,
        bg="white",
        highlightbackground="#E5E7EB",
        highlightthickness=1
    )

    tarjeta_aprobadas.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 7)
    )


    icono_aprobadas = tk.Label(
        tarjeta_aprobadas,
        text="♡",
        font=("Segoe UI", 25),
        bg=VERDE_CLARO,
        fg=VERDE
    )

    icono_aprobadas.pack(
        side="left",
        padx=15,
        pady=15
    )


    cont_aprobadas = tk.Frame(
        tarjeta_aprobadas,
        bg="white"
    )

    cont_aprobadas.pack(
        side="left",
        pady=12
    )


    aprobadas_label = tk.Label(
        cont_aprobadas,
        text="0",
        font=("Segoe UI", 24, "bold"),
        bg="white",
        fg=VERDE
    )

    aprobadas_label.pack(anchor="w")


    tk.Label(
        cont_aprobadas,
        text="Aprobadas",
        font=("Segoe UI", 10),
        bg="white",
        fg="#6B7280"
    ).pack(anchor="w")


    # -------- PENDIENTES --------

    tarjeta_pendientes = tk.Frame(
        tarjetas,
        bg="white",
        highlightbackground="#E5E7EB",
        highlightthickness=1
    )

    tarjeta_pendientes.pack(
        side="left",
        fill="both",
        expand=True,
        padx=7
    )


    tk.Label(
        tarjeta_pendientes,
        text="♡",
        font=("Segoe UI", 25),
        bg=NARANJA_CLARO,
        fg=NARANJA
    ).pack(
        side="left",
        padx=15,
        pady=15
    )


    cont_pendientes = tk.Frame(
        tarjeta_pendientes,
        bg="white"
    )

    cont_pendientes.pack(
        side="left",
        pady=12
    )


    pendientes_label = tk.Label(
        cont_pendientes,
        text="0",
        font=("Segoe UI", 24, "bold"),
        bg="white",
        fg=NARANJA
    )

    pendientes_label.pack(anchor="w")


    tk.Label(
        cont_pendientes,
        text="Pendientes",
        font=("Segoe UI", 10),
        bg="white",
        fg="#6B7280"
    ).pack(anchor="w")


    # -------- RECHAZADAS --------

    tarjeta_rechazadas = tk.Frame(
        tarjetas,
        bg="white",
        highlightbackground="#E5E7EB",
        highlightthickness=1
    )

    tarjeta_rechazadas.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(7, 0)
    )


    tk.Label(
        tarjeta_rechazadas,
        text="♡",
        font=("Segoe UI", 25),
        bg=ROJO_CLARO,
        fg=ROJO
    ).pack(
        side="left",
        padx=15,
        pady=15
    )


    cont_rechazadas = tk.Frame(
        tarjeta_rechazadas,
        bg="white"
    )

    cont_rechazadas.pack(
        side="left",
        pady=12
    )


    rechazadas_label = tk.Label(
        cont_rechazadas,
        text="0",
        font=("Segoe UI", 24, "bold"),
        bg="white",
        fg=ROJO
    )

    rechazadas_label.pack(anchor="w")


    tk.Label(
        cont_rechazadas,
        text="Rechazadas",
        font=("Segoe UI", 10),
        bg="white",
        fg="#6B7280"
    ).pack(anchor="w")


    # ------------------------------------------------------
    # BUSCADOR Y FILTROS
    # ------------------------------------------------------

    filtros = tk.Frame(
        frame,
        bg="#F7F7F3"
    )

    filtros.pack(
        fill="x",
        padx=25,
        pady=15
    )


    buscar_var = tk.StringVar()


    buscar = tk.Entry(
        filtros,
        textvariable=buscar_var,
        font=("Segoe UI", 10),
        bg="white",
        fg="#374151",
        relief="solid",
        bd=1
    )

    buscar.pack(
        side="left",
        ipady=9,
        ipadx=8,
        fill="x",
        expand=True
    )


    filtro_actual = tk.StringVar(
        value="Todos"
    )


    def cambiar_filtro(valor):

        filtro_actual.set(valor)
        cargar_tabla()


    for texto in [
        "Todos",
        "Aprobada",
        "Pendiente",
        "Rechazada"
    ]:

        boton = tk.Button(
            filtros,
            text=texto,
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=13,
            pady=9,
            command=lambda x=texto: cambiar_filtro(x)
        )

        boton.pack(
            side="left",
            padx=(8, 0)
        )


    buscar_var.trace_add(
        "write",
        lambda *args: cargar_tabla()
    )


    # ------------------------------------------------------
    # TABLA
    # ------------------------------------------------------

    cont_tabla = tk.Frame(
        frame,
        bg="white",
        highlightbackground="#E5E7EB",
        highlightthickness=1
    )

    cont_tabla.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=(0, 20)
    )


    columnas = (
        "id",
        "animal",
        "adoptante",
        "contacto",
        "fecha",
        "estado",
        "acciones"
    )


    tabla = ttk.Treeview(
        cont_tabla,
        columns=columnas,
        show="headings",
        selectmode="browse"
    )

    tabla.heading(
        "id",
        text="ID"
    )

    tabla.heading(
        "animal",
        text="ANIMAL"
    )

    tabla.heading(
        "adoptante",
        text="ADOPTANTE"
    )

    tabla.heading(
        "contacto",
        text="CONTACTO"
    )

    tabla.heading(
        "fecha",
        text="FECHA"
    )

    tabla.heading(
        "estado",
        text="ESTADO"
    )

    tabla.heading(
        "acciones",
        text="ACCIONES"
    )


    tabla.column(
        "id",
        width=50,
        anchor="center"
    )

    tabla.column(
        "animal",
        width=170
    )

    tabla.column(
        "adoptante",
        width=170
    )

    tabla.column(
        "contacto",
        width=180
    )

    tabla.column(
        "fecha",
        width=120
    )

    tabla.column(
        "estado",
        width=120,
        anchor="center"
    )

    tabla.column(
        "acciones",
        width=120,
        anchor="center"
    )


    scrollbar = ttk.Scrollbar(
        cont_tabla,
        orient="vertical",
        command=tabla.yview
    )

    tabla.configure(
        yscrollcommand=scrollbar.set
    )


    tabla.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )


    # ------------------------------------------------------
    # CARGAR TABLA
    # ------------------------------------------------------

    def cargar_tabla():

        nonlocal adopciones_data

        for item in tabla.get_children():
            tabla.delete(item)

        texto_busqueda = buscar_var.get().lower().strip()

        filtro = filtro_actual.get()

        for adopcion in adopciones_data:

            id_adopcion = adopcion.get(
                "id_adopcion"
            )

            id_animal = adopcion.get(
                "id_animal"
            )

            id_persona = adopcion.get(
                "id_persona"
            )

            animal = nombre_animal(
                id_animal
            )

            persona = nombre_persona(
                id_persona
            )

            estado = adopcion.get(
                "estado_seguimiento",
                ""
            )

            fecha = adopcion.get(
                "fecha",
                ""
            )

            # Filtro estado
            if filtro != "Todos":

                if str(estado).lower() != filtro.lower():
                    continue

            # Filtro búsqueda
            contenido = (
                f"{animal} "
                f"{persona} "
                f"{estado} "
                f"{id_adopcion}"
            ).lower()

            if texto_busqueda not in contenido:
                continue

            # Contacto
            contacto = ""

            persona_data = next(
                (
                    p for p in personas
                    if p.get("id_persona") == id_persona
                ),
                None
            )

            if persona_data:

                contacto = persona_data.get(
                    "email",
                    persona_data.get(
                        "telefono",
                        ""
                    )
                )

            item = tabla.insert(
                "",
                "end",
                values=(
                    id_adopcion,
                    animal,
                    persona,
                    contacto,
                    str(fecha)[:10],
                    estado,
                    "✎   👁   🗑"
                )
            )

            # Colores
            estado_lower = str(
                estado
            ).lower()

            if estado_lower == "aprobada":

                tabla.item(
                    item,
                    tags=("aprobada",)
                )

            elif estado_lower == "pendiente":

                tabla.item(
                    item,
                    tags=("pendiente",)
                )

            elif estado_lower == "rechazada":

                tabla.item(
                    item,
                    tags=("rechazada",)
                )


        tabla.tag_configure(
            "aprobada",
            background="#F8FCF9"
        )

        tabla.tag_configure(
            "pendiente",
            background="#FFFCF7"
        )

        tabla.tag_configure(
            "rechazada",
            background="#FFF9F9"
        )


    # ------------------------------------------------------
    # ACTUALIZAR ESTADÍSTICAS
    # ------------------------------------------------------

    def actualizar_estadisticas():

        aprobadas, pendientes, rechazadas = contar_estados(
            adopciones_data
        )

        aprobadas_label.config(
            text=str(aprobadas)
        )

        pendientes_label.config(
            text=str(pendientes)
        )

        rechazadas_label.config(
            text=str(rechazadas)
        )

        total_label.config(
            text=f"Total registradas: {len(adopciones_data)}"
        )


    # ------------------------------------------------------
    # RECARGAR DATOS
    # ------------------------------------------------------

    def recargar():

        obtener_animales()
        obtener_personas()

        adopciones_data = obtener_adopciones()

        actualizar_estadisticas()
        cargar_tabla()


    # ------------------------------------------------------
    # VENTANA AGREGAR / EDITAR
    # ------------------------------------------------------

    def ventana_adopcion(adopcion=None):

        editar = adopcion is not None

        ventana = tk.Toplevel(frame)

        ventana.title(
            "Editar Adopción"
            if editar
            else
            "Nueva Adopción"
        )

        ventana.geometry("450x500")

        ventana.configure(
            bg="#F7F7F3"
        )

        ventana.transient(
            frame.winfo_toplevel()
        )

        ventana.grab_set()


        # --------------------------------------------------
        # TÍTULO
        # --------------------------------------------------

        tk.Label(
            ventana,
            text=(
                "Editar Adopción"
                if editar
                else
                "Nueva Adopción"
            ),
            font=("Segoe UI", 18, "bold"),
            bg="#F7F7F3",
            fg="#26352B"
        ).pack(
            anchor="w",
            padx=30,
            pady=(25, 20)
        )


        formulario = tk.Frame(
            ventana,
            bg="#F7F7F3"
        )

        formulario.pack(
            fill="both",
            expand=True,
            padx=30
        )


        # --------------------------------------------------
        # FECHA
        # --------------------------------------------------

        tk.Label(
            formulario,
            text="Fecha",
            font=("Segoe UI", 10, "bold"),
            bg="#F7F7F3"
        ).pack(
            anchor="w"
        )


        fecha_entry = tk.Entry(
            formulario,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1
        )

        fecha_entry.pack(
            fill="x",
            ipady=8,
            pady=(5, 15)
        )


        if editar:

            fecha_entry.insert(
                0,
                str(
                    adopcion.get(
                        "fecha",
                        ""
                    )
                )[:10]
            )

        else:

            fecha_entry.insert(
                0,
                datetime.now().strftime(
                    "%Y-%m-%d"
                )
            )


        # --------------------------------------------------
        # ESTADO
        # --------------------------------------------------

        tk.Label(
            formulario,
            text="Estado de seguimiento",
            font=("Segoe UI", 10, "bold"),
            bg="#F7F7F3"
        ).pack(
            anchor="w"
        )


        estado_combo = ttk.Combobox(
            formulario,
            values=[
                "Aprobada",
                "Pendiente",
                "Rechazada"
            ],
            state="readonly",
            font=("Segoe UI", 10)
        )

        estado_combo.pack(
            fill="x",
            ipady=6,
            pady=(5, 15)
        )


        if editar:

            estado_combo.set(
                adopcion.get(
                    "estado_seguimiento",
                    "Pendiente"
                )
            )

        else:

            estado_combo.set(
                "Pendiente"
            )


        # --------------------------------------------------
        # ANIMAL
        # --------------------------------------------------

        tk.Label(
            formulario,
            text="Animal",
            font=("Segoe UI", 10, "bold"),
            bg="#F7F7F3"
        ).pack(
            anchor="w"
        )


        valores_animales = []

        for id_animal, nombre in mapa_animales.items():

            valores_animales.append(
                f"{id_animal} - {nombre}"
            )


        animal_combo = ttk.Combobox(
            formulario,
            values=valores_animales,
            state="readonly",
            font=("Segoe UI", 10)
        )

        animal_combo.pack(
            fill="x",
            ipady=6,
            pady=(5, 15)
        )


        if editar:

            id_animal_actual = adopcion.get(
                "id_animal"
            )

            animal_combo.set(
                f"{id_animal_actual} - "
                f"{nombre_animal(id_animal_actual)}"
            )


        # --------------------------------------------------
        # ADOPTANTE
        # --------------------------------------------------

        tk.Label(
            formulario,
            text="Adoptante",
            font=("Segoe UI", 10, "bold"),
            bg="#F7F7F3"
        ).pack(
            anchor="w"
        )


        valores_personas = []

        for id_persona, nombre in mapa_personas.items():

            valores_personas.append(
                f"{id_persona} - {nombre}"
            )


        persona_combo = ttk.Combobox(
            formulario,
            values=valores_personas,
            state="readonly",
            font=("Segoe UI", 10)
        )

        persona_combo.pack(
            fill="x",
            ipady=6,
            pady=(5, 20)
        )


        if editar:

            id_persona_actual = adopcion.get(
                "id_persona"
            )

            persona_combo.set(
                f"{id_persona_actual} - "
                f"{nombre_persona(id_persona_actual)}"
            )


        # --------------------------------------------------
        # GUARDAR
        # --------------------------------------------------

        def guardar():

            fecha = fecha_entry.get().strip()

            estado = estado_combo.get().strip()

            animal_seleccionado = animal_combo.get()

            persona_seleccionada = persona_combo.get()


            if not fecha:

                messagebox.showwarning(
                    "Falta información",
                    "Ingresá una fecha."
                )

                return


            if not animal_seleccionado:

                messagebox.showwarning(
                    "Falta información",
                    "Seleccioná un animal."
                )

                return


            if not persona_seleccionada:

                messagebox.showwarning(
                    "Falta información",
                    "Seleccioná un adoptante."
                )

                return


            try:

                id_animal = int(
                    animal_seleccionado.split(
                        " - "
                    )[0]
                )

                id_persona = int(
                    persona_seleccionada.split(
                        " - "
                    )[0]
                )

            except:

                messagebox.showerror(
                    "Error",
                    "Animal o persona inválidos."
                )

                return


            datos = {

                "fecha": fecha,

                "estado_seguimiento": estado,

                "id_animal": id_animal,

                "id_persona": id_persona

            }


            try:

                if editar:

                    id_adopcion = adopcion.get(
                        "id_adopcion"
                    )

                    respuesta = requests.put(
                        f"{ADOPCIONES_URL}/{id_adopcion}",
                        json=datos,
                        timeout=5
                    )

                else:

                    respuesta = requests.post(
                        ADOPCIONES_URL,
                        json=datos,
                        timeout=5
                    )


                if respuesta.status_code in [200, 201]:

                    messagebox.showinfo(
                        "Éxito",
                        (
                            "Adopción actualizada correctamente."
                            if editar
                            else
                            "Adopción agregada correctamente."
                        )
                    )

                    ventana.destroy()

                    recargar()

                else:

                    try:
                        error = respuesta.json()

                    except:
                        error = respuesta.text

                    messagebox.showerror(
                        "Error",
                        str(error)
                    )


            except requests.exceptions.RequestException as error:

                messagebox.showerror(
                    "Error de conexión",
                    f"No se pudo conectar con el servidor.\n\n{error}"
                )


        boton_guardar = tk.Button(
            formulario,
            text=(
                "Guardar cambios"
                if editar
                else
                "Guardar adopción"
            ),
            font=("Segoe UI", 10, "bold"),
            bg=VERDE,
            fg="white",
            activebackground=VERDE_OSCURO,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=10,
            command=guardar
        )

        boton_guardar.pack(
            fill="x"
        )


    # ------------------------------------------------------
    # VER DETALLES
    # ------------------------------------------------------

    def ver_adopcion(adopcion):

        ventana = tk.Toplevel(frame)

        ventana.title(
            "Detalle de adopción"
        )

        ventana.geometry(
            "400x350"
        )

        ventana.configure(
            bg="#F7F7F3"
        )


        tk.Label(
            ventana,
            text="Detalle de Adopción",
            font=("Segoe UI", 18, "bold"),
            bg="#F7F7F3",
            fg="#26352B"
        ).pack(
            pady=(25, 20)
        )


        id_animal = adopcion.get(
            "id_animal"
        )

        id_persona = adopcion.get(
            "id_persona"
        )


        datos = [

            (
                "ID:",
                adopcion.get(
                    "id_adopcion"
                )
            ),

            (
                "Animal:",
                nombre_animal(
                    id_animal
                )
            ),

            (
                "Adoptante:",
                nombre_persona(
                    id_persona
                )
            ),

            (
                "Fecha:",
                str(
                    adopcion.get(
                        "fecha",
                        ""
                    )
                )[:10]
            ),

            (
                "Estado:",
                adopcion.get(
                    "estado_seguimiento",
                    ""
                )
            ),

            (
                "ID Animal:",
                id_animal
            ),

            (
                "ID Persona:",
                id_persona
            )

        ]


        for etiqueta, valor in datos:

            fila = tk.Frame(
                ventana,
                bg="#F7F7F3"
            )

            fila.pack(
                fill="x",
                padx=35,
                pady=5
            )


            tk.Label(
                fila,
                text=etiqueta,
                width=14,
                anchor="w",
                font=("Segoe UI", 10, "bold"),
                bg="#F7F7F3"
            ).pack(
                side="left"
            )


            tk.Label(
                fila,
                text=str(valor),
                anchor="w",
                font=("Segoe UI", 10),
                bg="#F7F7F3",
                fg="#64748B"
            ).pack(
                side="left"
            )


    # ------------------------------------------------------
    # ELIMINAR
    # ------------------------------------------------------

    def eliminar_adopcion(adopcion):

        id_adopcion = adopcion.get(
            "id_adopcion"
        )


        confirmar = messagebox.askyesno(
            "Eliminar adopción",
            f"¿Seguro que querés eliminar la adopción #{id_adopcion}?"
        )


        if not confirmar:
            return


        try:

            respuesta = requests.delete(
                f"{ADOPCIONES_URL}/{id_adopcion}",
                timeout=5
            )


            if respuesta.status_code == 200:

                messagebox.showinfo(
                    "Éxito",
                    "Adopción eliminada correctamente."
                )

                recargar()

            else:

                try:
                    error = respuesta.json()

                except:
                    error = respuesta.text

                messagebox.showerror(
                    "Error",
                    str(error)
                )


        except requests.exceptions.RequestException as error:

            messagebox.showerror(
                "Error de conexión",
                f"No se pudo conectar con el servidor.\n\n{error}"
            )


    # ------------------------------------------------------
    # BOTONES DE ACCIONES
    # ------------------------------------------------------

    def accion_tabla(event):

        item = tabla.identify_row(
            event.y
        )

        columna = tabla.identify_column(
            event.x
        )


        if not item:
            return


        valores = tabla.item(
            item,
            "values"
        )


        if not valores:
            return


        id_adopcion = valores[0]


        adopcion = next(
            (
                a for a in adopciones_data
                if str(
                    a.get(
                        "id_adopcion"
                    )
                ) == str(id_adopcion)
            ),
            None
        )


        if not adopcion:
            return


        # La columna acciones es la número 7
        if columna == "#7":

            # Como ttk no tiene botones individuales
            # usamos un pequeño menú
            menu = tk.Menu(
                frame,
                tearoff=0
            )

            menu.add_command(
                label="✎ Editar",
                command=lambda: ventana_adopcion(
                    adopcion
                )
            )

            menu.add_command(
                label="👁 Ver detalles",
                command=lambda: ver_adopcion(
                    adopcion
                )
            )

            menu.add_separator()

            menu.add_command(
                label="🗑 Eliminar",
                command=lambda: eliminar_adopcion(
                    adopcion
                )
            )

            menu.tk_popup(
                event.x_root,
                event.y_root
            )


    tabla.bind(
        "<Button-1>",
        accion_tabla
    )


    # ------------------------------------------------------
    # CARGAR TODO AL INICIAR
    # ------------------------------------------------------

    obtener_animales()
    obtener_personas()

    adopciones_data = obtener_adopciones()

    actualizar_estadisticas()
    cargar_tabla()


    return frame