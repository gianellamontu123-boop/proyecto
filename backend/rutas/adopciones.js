javascript
const express = require('express');
const pool = require('../bd/conexion');
const router = express.Router();


// =============================
// AGREGAR UNA ADOPCIÓN
// =============================
router.post('/', async (req, res) => {
    const { fecha, estado_seguimiento, id_animal, id_persona } = req.body;

    try {
        await pool.execute(
            `INSERT INTO adopciones 
            (fecha, estado_seguimiento, id_animal, id_persona) 
            VALUES (?, ?, ?, ?)`,
            [fecha, estado_seguimiento, id_animal, id_persona]
        );

        return res.status(201).json({
            mensaje: 'Adopción agregada correctamente'
        });

    } catch (error) {
        return res.status(500).json({
            error: 'No se pudo agregar la adopción',
            detalle: error.message
        });
    }
});


// =============================
// LEER TODAS LAS ADOPCIONES
// =============================
router.get('/', async (req, res) => {
    try {
        const [adopciones] = await pool.execute(
            'SELECT * FROM adopciones'
        );

        return res.status(200).json(adopciones);

    } catch (error) {
        return res.status(500).json({
            error: 'No se pudieron obtener las adopciones',
            detalle: error.message
        });
    }
});


// =============================
// LEER UNA ADOPCIÓN POR ID
// =============================
router.get('/:id', async (req, res) => {
    const { id } = req.params;

    try {
        const [adopciones] = await pool.execute(
            'SELECT * FROM adopciones WHERE id_adopcion = ?',
            [id]
        );

        if (adopciones.length === 0) {
            return res.status(404).json({
                error: 'Adopción no encontrada'
            });
        }

        return res.status(200).json(adopciones[0]);

    } catch (error) {
        return res.status(500).json({
            error: 'No se pudo obtener la adopción',
            detalle: error.message
        });
    }
});


// =============================
// EDITAR UNA ADOPCIÓN
// =============================
router.put('/:id', async (req, res) => {
    const { id } = req.params;
    const { fecha, estado_seguimiento, id_animal, id_persona } = req.body;

    try {
        const [resultado] = await pool.execute(
            `UPDATE adopciones
             SET fecha = ?,
                 estado_seguimiento = ?,
                 id_animal = ?,
                 id_persona = ?
             WHERE id_adopcion = ?`,
            [fecha, estado_seguimiento, id_animal, id_persona, id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: 'Adopción no encontrada'
            });
        }

        return res.status(200).json({
            mensaje: 'Adopción actualizada correctamente'
        });

    } catch (error) {
        return res.status(500).json({
            error: 'No se pudo actualizar la adopción',
            detalle: error.message
        });
    }
});


// =============================
// ELIMINAR UNA ADOPCIÓN
// =============================
router.delete('/:id', async (req, res) => {
    const { id } = req.params;

    try {
        const [resultado] = await pool.execute(
            'DELETE FROM adopciones WHERE id_adopcion = ?',
            [id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: 'Adopción no encontrada'
            });
        }

        return res.status(200).json({
            mensaje: 'Adopción eliminada correctamente'
        });

    } catch (error) {
        return res.status(500).json({
            error: 'No se pudo eliminar la adopción',
            detalle: error.message
        });
    }
});


module.exports = router;
