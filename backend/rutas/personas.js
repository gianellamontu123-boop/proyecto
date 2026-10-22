
const express = require("express");
const pool = require("../bd/conexion");

const router = express.Router();

const CAMPOS = [
    "nombre",
    "apellido",
    "dni",
    "telefono",
    "correo_electronico",
    "direccion"
];

// Obtener y limpiar los datos de una persona
function datosPersona(body) {
    return CAMPOS.map((campo) => {
        const valor = body[campo];
        return typeof valor === "string" ? valor.trim() : valor ?? "";
    });
}

// Validar que todos los campos estén completos
function datosValidos(datos) {
    return datos.every((valor) => String(valor).trim() !== "");
}

// =============================
// CREAR UNA PERSONA
// =============================
router.post("/", async (req, res) => {
    const datos = datosPersona(req.body);

    if (!datosValidos(datos)) {
        return res.status(400).json({
            error: "Todos los campos de la persona son obligatorios"
        });
    }

    try {
        const [resultado] = await pool.execute(
            `INSERT INTO personas
            (nombre, apellido, dni, telefono, correo_electronico, direccion)
            VALUES (?, ?, ?, ?, ?, ?)`,
            datos
        );

        return res.status(201).json({
            id_persona: resultado.insertId,
            mensaje: "Persona creada correctamente"
        });
    } catch (error) {
        return res.status(500).json({
            error: "No se pudo crear la persona",
            detalle: error.message
        });
    }
});

// =============================
// LISTAR TODAS LAS PERSONAS
// =============================
router.get("/", async (req, res) => {
    try {
        const [personas] = await pool.execute(
            `SELECT id_persona, nombre, apellido, dni, telefono,
                    correo_electronico, direccion
             FROM personas
             ORDER BY id_persona DESC`
        );

        return res.status(200).json(personas);
    } catch (error) {
        console.error("ERROR AL CARGAR PERSONAS:", error);
        return res.status(500).json({
            error: "No se pudieron obtener las personas",
            detalle: error.message
        });
    }
});

// =============================
// BUSCAR UNA PERSONA POR ID
// =============================
router.get("/:id", async (req, res) => {
    try {
        const [personas] = await pool.execute(
            `SELECT id_persona, nombre, apellido, dni, telefono,
                    correo_electronico, direccion
             FROM personas
             WHERE id_persona = ?`,
            [req.params.id]
        );

        if (personas.length === 0) {
            return res.status(404).json({
                error: "Persona no encontrada"
            });
        }

        return res.status(200).json(personas[0]);
    } catch (error) {
        return res.status(500).json({
            error: "No se pudo obtener la persona",
            detalle: error.message
        });
    }
});

// =============================
// ACTUALIZAR UNA PERSONA
// =============================
router.put("/:id", async (req, res) => {
    const datos = datosPersona(req.body);

    if (!datosValidos(datos)) {
        return res.status(400).json({
            error: "Todos los campos de la persona son obligatorios"
        });
    }

    try {
        const [resultado] = await pool.execute(
            `UPDATE personas
             SET nombre = ?, apellido = ?, dni = ?, telefono = ?,
                 correo_electronico = ?, direccion = ?
             WHERE id_persona = ?`,
            [...datos, req.params.id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: "Persona no encontrada"
            });
        }

        return res.status(200).json({
            mensaje: "Persona actualizada correctamente"
        });
    } catch (error) {
        return res.status(500).json({
            error: "No se pudo actualizar la persona",
            detalle: error.message
        });
    }
});

// =============================
// ELIMINAR UNA PERSONA
// =============================
router.delete("/:id", async (req, res) => {
    try {
        const [resultado] = await pool.execute(
            "DELETE FROM personas WHERE id_persona = ?",
            [req.params.id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: "Persona no encontrada"
            });
        }

        return res.status(200).json({
            mensaje: "Persona eliminada correctamente"
        });
    } catch (error) {
        return res.status(409).json({
            error: "No se pudo eliminar la persona. Puede estar relacionada con adopciones o donaciones.",
            detalle: error.message
        });
    }
});

module.exports = router;
