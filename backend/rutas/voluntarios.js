
const express = require('express');
const pool = require('../bd/conexion');
const router = express.Router();

// =============================
// AGREGAR UN VOLUNTARIO
// =============================
router.post('/', async (req, res) => {
    const {
        nombre,
        rol,
        turno,
        dias,
        fecha_ingreso,
        estado
    } = req.body;

    try {
        await pool.execute(
            `INSERT INTO voluntarios
            (nombre, rol, turno, dias, fecha_ingreso, estado)
            VALUES (?, ?, ?, ?, ?, ?)`,
            [nombre, rol, turno, dias, fecha_ingreso, estado || 'Activo']
        );

        return res.status(201).json({
            mensaje: 'Voluntario agregado correctamente'
        });

    } catch (error) {
        return res.status(500).json({
            error: 'No se pudo agregar el voluntario',
            detalle: error.message
        });
    }
});


// =============================
// LEER TODOS LOS VOLUNTARIOS
// =============================
router.get('/', async (req, res) => {
    try {
        const [voluntarios] = await pool.execute(
            'SELECT * FROM voluntarios'
        );

        return res.status(200).json(voluntarios);

    } catch (error) {
        return res.status(500).json({
            error: 'No se pudieron obtener los voluntarios',
            detalle: error.message
        });
    }
});


// =============================
// LEER UN VOLUNTARIO POR ID
// =============================
router.get('/:id', async (req, res) => {
    const { id } = req.params;

    try {
        const [voluntarios] = await pool.execute(
            'SELECT * FROM voluntarios WHERE id_voluntario = ?',
            [id]
        );

        if (voluntarios.length === 0) {
            return res.status(404).json({
                error: 'Voluntario no encontrado'
            });
        }

        return res.status(200).json(voluntarios[0]);

    } catch (error) {
        return res.status(500).json({
            error: 'No se pudo obtener el voluntario',
            detalle: error.message
        });
    }
});


// =============================
// EDITAR UN VOLUNTARIO
// =============================
router.put('/:id', async (req, res) => {
    const { id } = req.params;

    const {
        nombre,
        rol,
        turno,
        dias,
        fecha_ingreso,
        estado
    } = req.body;

    try {
        const [resultado] = await pool.execute(
            `UPDATE voluntarios
             SET nombre = ?,
                 rol = ?,
                 turno = ?,
                 dias = ?,
                 fecha_ingreso = ?,
                 estado = ?
             WHERE id_voluntario = ?`,
            [
                nombre,
                rol,
                turno,
                dias,
                fecha_ingreso,
                estado,
                id
            ]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: 'Voluntario no encontrado'
            });
        }

        return res.status(200).json({
            mensaje: 'Voluntario actualizado correctamente'
        });

    } catch (error) {
        return res.status(500).json({
            error: 'No se pudo actualizar el voluntario',
            detalle: error.message
        });
    }
});


// =============================
// ELIMINAR UN VOLUNTARIO
// =============================
router.delete('/:id', async (req, res) => {
    const { id } = req.params;

    try {
        const [resultado] = await pool.execute(
            'DELETE FROM voluntarios WHERE id_voluntario = ?',
            [id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: 'Voluntario no encontrado'
            });
        }

        return res.status(200).json({
            mensaje: 'Voluntario eliminado correctamente'
        });

    } catch (error) {
        return res.status(500).json({
            error: 'No se pudo eliminar el voluntario',
            detalle: error.message
        });
    }
});

module.exports = router;
