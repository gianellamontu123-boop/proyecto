
const express = require('express');
const pool = require('../bd/conexion');
const router = express.Router();


// =============================
// AGREGAR UNA DONACIÓN
// =============================
router.post('/', async (req, res) => {
    const { fecha, tipo, detalle, id_persona } = req.body;

    try {
        await pool.execute(
            `INSERT INTO donaciones
            (fecha, tipo, detalle, id_persona)
            VALUES (?, ?, ?, ?)`,
            [fecha, tipo, detalle, id_persona]
        );

        return res.status(201).json({
            mensaje: 'Donación agregada correctamente'
        });

    } catch (error) {
        return res.status(500).json({
            error: 'No se pudo agregar la donación',
            detalle: error.message
        });
    }
});


// =============================
// LEER TODAS LAS DONACIONES
// =============================
router.get('/', async (req, res) => {
    try {
        const [donaciones] = await pool.execute(
            'SELECT * FROM donaciones'
        );

        return res.status(200).json(donaciones);

    } catch (error) {
        return res.status(500).json({
            error: 'No se pudieron obtener las donaciones',
            detalle: error.message
        });
    }
});


// =============================
// LEER UNA DONACIÓN POR ID
// =============================
router.get('/:id', async (req, res) => {
    const { id } = req.params;

    try {
        const [donaciones] = await pool.execute(
            'SELECT * FROM donaciones WHERE id_donacion = ?',
            [id]
        );

        if (donaciones.length === 0) {
            return res.status(404).json({
                error: 'Donación no encontrada'
            });
        }

        return res.status(200).json(donaciones[0]);

    } catch (error) {
        return res.status(500).json({
            error: 'No se pudo obtener la donación',
            detalle: error.message
        });
    }
});


// =============================
// EDITAR UNA DONACIÓN
// =============================
router.put('/:id', async (req, res) => {
    const { id } = req.params;
    const { fecha, tipo, detalle, id_persona } = req.body;

    try {
        const [resultado] = await pool.execute(
            `UPDATE donaciones
             SET fecha = ?,
                 tipo = ?,
                 detalle = ?,
                 id_persona = ?
             WHERE id_donacion = ?`,
            [fecha, tipo, detalle, id_persona, id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: 'Donación no encontrada'
            });
        }

        return res.status(200).json({
            mensaje: 'Donación actualizada correctamente'
        });

    } catch (error) {
        return res.status(500).json({
            error: 'No se pudo actualizar la donación',
            detalle: error.message
        });
    }
});


// =============================
// ELIMINAR UNA DONACIÓN
// =============================
router.delete('/:id', async (req, res) => {
    const { id } = req.params;

    try {
        const [resultado] = await pool.execute(
            'DELETE FROM donaciones WHERE id_donacion = ?',
            [id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: 'Donación no encontrada'
            });
        }

        return res.status(200).json({
            mensaje: 'Donación eliminada correctamente'
        });

    } catch (error) {
        return res.status(500).json({
            error: 'No se pudo eliminar la donación',
            detalle: error.message
        });
    }
});


module.exports = router;