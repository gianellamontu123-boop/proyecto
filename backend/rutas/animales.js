const express = require('express');
const pool = require('../bd/conexion');
const router = express.Router();

// =============================
// AGREGAR UN ANIMAL
// =============================
router.post('/', async (req, res) => {
    const { nombre, especie, raza, sexo, fecha_nacimiento, estado_actual } = req.body;

    try {
        await pool.execute(
            'INSERT INTO animales (especie, raza, nombre, sexo, fecha_nacimiento, estado_actual) VALUES (?, ?, ?, ?, ?, ?)',
            [especie, raza, nombre, sexo, fecha_nacimiento, estado_actual]
        );

        return res.status(201).json({
            mensaje: 'Animal agregado correctamente'
        });
    } catch (error) {
        return res.status(500).json({
            error: 'No se pudo agregar el animal',
            detalle: error.message
        });
    }
});


// =============================
// LEER TODOS LOS ANIMALES
// =============================
router.get('/', async (req, res) => {
    try {
        const [animales] = await pool.execute(
            'SELECT * FROM animales'
        );

        return res.status(200).json(animales);
    } catch (error) {
        return res.status(500).json({
            error: 'No se pudieron obtener los animales',
            detalle: error.message
        });
    }
});


// =============================
// LEER UN ANIMAL POR ID
// =============================
router.get('/:id', async (req, res) => {
    const { id } = req.params;

    try {
        const [animales] = await pool.execute(
            'SELECT * FROM animales WHERE id_animal = ?',
            [id]
        );

        if (animales.length === 0) {
            return res.status(404).json({
                error: 'Animal no encontrado'
            });
        }

        return res.status(200).json(animales[0]);
    } catch (error) {
        return res.status(500).json({
            error: 'No se pudo obtener el animal',
            detalle: error.message
        });
    }
});


// =============================
// EDITAR UN ANIMAL
// =============================
router.put('/:id', async (req, res) => {
    const { id } = req.params;
    const { nombre, especie, raza, sexo, fecha_nacimiento, estado_actual } = req.body;

    try {
        const [resultado] = await pool.execute(
            `UPDATE animales 
             SET especie = ?, 
                 raza = ?, 
                 nombre = ?, 
                 sexo = ?, 
                 fecha_nacimiento = ?, 
                 estado_actual = ?
             WHERE id_animal = ?`,
            [especie, raza, nombre, sexo, fecha_nacimiento, estado_actual, id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: 'Animal no encontrado'
            });
        }

        return res.status(200).json({
            mensaje: 'Animal actualizado correctamente'
        });
    } catch (error) {
        return res.status(500).json({
            error: 'No se pudo actualizar el animal',
            detalle: error.message
        });
    }
});


// =============================
// ELIMINAR UN ANIMAL
// =============================
router.delete('/:id', async (req, res) => {
    const { id } = req.params;

    try {
        const [resultado] = await pool.execute(
            'DELETE FROM animales WHERE id_animal = ?',
            [id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: 'Animal no encontrado'
            });
        }

        return res.status(200).json({
            mensaje: 'Animal eliminado correctamente'
        });
    } catch (error) {
        return res.status(500).json({
            error: 'No se pudo eliminar el animal',
            detalle: error.message
        });
    }
});


module.exports = router;