
const express = require('express');
const pool = require('../bd/conexion');

const router = express.Router();

// ==========================================
// GRÁFICO 1: ANIMALES POR ESTADO
// ==========================================

router.get('/animales-por-estado', async (req, res) => {
    try {
        const estados = [
            'Activo',
            'Saludable',
            'En tratamiento',
            'Adoptado',
            'Inactivo'
        ];

        // Consultar la cantidad de animales por estado
        const [filas] = await pool.execute(`
            SELECT estado_actual, COUNT(*) AS cantidad
            FROM animales
            GROUP BY estado_actual
        `);

        // Inicializar todos los estados en cero
        const resultados = estados.map(estado => {
            const registro = filas.find(fila =>
                (fila.estado_actual || '').trim().toLowerCase() ===
                estado.toLowerCase()
            );

            return {
                estado: estado,
                cantidad: registro ? Number(registro.cantidad) : 0
            };
        });

        res.status(200).json({
            mensaje: 'Reporte de animales generado correctamente',
            total: resultados.reduce(
                (suma, item) => suma + item.cantidad, 0
            ),
            datos: resultados
        });

    } catch (error) {
        console.error(error);

        res.status(500).json({
            error: 'No se pudo generar el reporte de animales',
            detalle: error.message
        });
    }
});


// ==========================================
// GRÁFICO 2: ADOPCIONES POR MES
// ==========================================

router.get('/adopciones-por-mes', async (req, res) => {
    try {
        // Si no se envía un año, utiliza el año actual
        const anio = Number(
            req.query.anio || new Date().getFullYear()
        );

        if (!Number.isInteger(anio) || anio < 2000 || anio > 2100) {
            return res.status(400).json({
                error: 'El año ingresado no es válido'
            });
        }

        const fechaInicio = `${anio}-01-01`;
        const fechaFin = `${anio + 1}-01-01`;

        // Consultar adopciones agrupadas por mes
        const [filas] = await pool.execute(`
            SELECT
                MONTH(fecha) AS mes,
                COUNT(*) AS cantidad
            FROM adopciones
            WHERE fecha >= ? AND fecha < ?
            GROUP BY MONTH(fecha)
            ORDER BY mes
        `, [fechaInicio, fechaFin]);

        const meses = [
            'Enero',
            'Febrero',
            'Marzo',
            'Abril',
            'Mayo',
            'Junio',
            'Julio',
            'Agosto',
            'Septiembre',
            'Octubre',
            'Noviembre',
            'Diciembre'
        ];

        // Inicializar los 12 meses en cero
        const resultados = meses.map((nombre, indice) => {
            const numeroMes = indice + 1;

            const registro = filas.find(
                fila => Number(fila.mes) === numeroMes
            );

            return {
                mes: nombre,
                cantidad: registro ? Number(registro.cantidad) : 0
            };
        });

        res.status(200).json({
            mensaje: 'Reporte de adopciones generado correctamente',
            anio: anio,
            total: resultados.reduce(
                (suma, item) => suma + item.cantidad, 0
            ),
            datos: resultados
        });

    } catch (error) {
        console.error(error);

        res.status(500).json({
            error: 'No se pudo generar el reporte de adopciones',
            detalle: error.message
        });
    }
});

module.exports = router;
