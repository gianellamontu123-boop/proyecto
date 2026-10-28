
const express = require('express');
const pool = require('./bd/conexion');

const router = express.Router();

// ============================================
// 1. DASHBOARD: RESUMEN GENERAL
// GET /api/dashboard
// ============================================
router.get('/', async (req, res) => {
    try {
        const [
            [animales],
            [adopciones],
            [voluntarios],
            [donaciones]
        ] = await Promise.all([
            pool.execute(
                'SELECT COUNT(*) AS total FROM animales'
            ),
            pool.execute(
                'SELECT COUNT(*) AS total FROM adopciones'
            ),
            pool.execute(
                `SELECT COUNT(*) AS total
                 FROM voluntarios
                 WHERE estado = 'Activo'`
            ),
            pool.execute(
                'SELECT COUNT(*) AS total FROM donaciones'
            )
        ]);

        res.json({
            animales_registrados: animales[0].total,
            adopciones_registradas: adopciones[0].total,
            voluntarios_activos: voluntarios[0].total,
            donaciones_registradas: donaciones[0].total
        });

    } catch (error) {
        res.status(500).json({
            error: 'Error al obtener el dashboard',
            detalle: error.message
        });
    }
});

// ============================================
// 2. RESUMEN DE ADOPCIONES POR ESTADO
// GET /api/dashboard/estados
// ============================================
router.get('/estados', async (req, res) => {
    try {
        const [datos] = await pool.execute(`
            SELECT estado_seguimiento, COUNT(*) AS total
            FROM adopciones
            GROUP BY estado_seguimiento
        `);

        res.json(datos);

    } catch (error) {
        res.status(500).json({
            error: 'Error al consultar los estados',
            detalle: error.message
        });
    }
});

// ============================================
// 3. BUSCAR Y FILTRAR ANIMALES
// GET /api/dashboard/animales
// Parámetros: busqueda, nombre, especie, raza, estado
// ============================================
router.get('/animales', async (req, res) => {
    try {
        const {
            busqueda,
            nombre,
            especie,
            raza,
            estado
        } = req.query;

        let sql = `
            SELECT id_animal, nombre, especie, raza,
                   sexo, fecha_nacimiento, estado_actual
            FROM animales
            WHERE 1 = 1
        `;

        const params = [];

        if (busqueda && busqueda.trim()) {
            sql += `
                AND (
                    nombre LIKE ?
                    OR especie LIKE ?
                    OR raza LIKE ?
                    OR estado_actual LIKE ?
                )
            `;

            const termino = `%${busqueda.trim()}%`;
            params.push(termino, termino, termino, termino);
        }

        if (nombre) {
            sql += ' AND nombre LIKE ?';
            params.push(`%${nombre}%`);
        }

        if (especie) {
            sql += ' AND especie = ?';
            params.push(especie);
        }

        if (raza) {
            sql += ' AND raza LIKE ?';
            params.push(`%${raza}%`);
        }

        if (estado) {
            sql += ' AND estado_actual = ?';
            params.push(estado);
        }

        sql += ' ORDER BY id_animal DESC';

        const [resultados] = await pool.execute(sql, params);

        res.json(resultados);

    } catch (error) {
        res.status(500).json({
            error: 'Error al buscar animales',
            detalle: error.message
        });
    }
});

// ============================================
// 4. FILTRAR ADOPCIONES
// GET /api/dashboard/adopciones
// Parámetros: desde, hasta, estado_seguimiento
// ============================================
router.get('/adopciones', async (req, res) => {
    try {
        const { desde, hasta, estado_seguimiento } = req.query;

        let sql = `
            SELECT
                a.id_adopcion,
                a.fecha,
                a.estado_seguimiento,
                a.id_animal,
                an.nombre AS nombre_animal,
                an.especie,
                a.id_persona
            FROM adopciones a
            LEFT JOIN animales an
                ON a.id_animal = an.id_animal
            WHERE 1 = 1
        `;

        const params = [];

        if (desde) {
            sql += ' AND a.fecha >= ?';
            params.push(desde);
        }

        if (hasta) {
            sql += ' AND a.fecha <= ?';
            params.push(hasta);
        }

        if (
            estado_seguimiento &&
            estado_seguimiento !== 'Todos'
        ) {
            sql += ' AND a.estado_seguimiento = ?';
            params.push(estado_seguimiento);
        }

        sql += ' ORDER BY a.fecha DESC, a.id_adopcion DESC';

        const [resultados] = await pool.execute(sql, params);

        res.json(resultados);

    } catch (error) {
        res.status(500).json({
            error: 'Error al buscar adopciones',
            detalle: error.message
        });
    }
});

// ============================================
// 5. SEGUIMIENTO QUE REQUIERE ATENCIÓN
// GET /api/dashboard/seguimiento
// ============================================
router.get('/seguimiento', async (req, res) => {
    try {
        const [resultados] = await pool.execute(`
            SELECT
                a.id_adopcion,
                a.fecha,
                a.estado_seguimiento,
                a.id_animal,
                an.nombre AS nombre_animal,
                a.id_persona
            FROM adopciones a
            LEFT JOIN animales an
                ON a.id_animal = an.id_animal
            WHERE LOWER(TRIM(a.estado_seguimiento))
                IN ('pendiente', 'en proceso')
            ORDER BY a.fecha ASC, a.id_adopcion ASC
        `);

        res.json({
            total: resultados.length,
            adopciones: resultados
        });

    } catch (error) {
        res.status(500).json({
            error: 'Error al consultar seguimientos',
            detalle: error.message
        });
    }
});

// ============================================
// 6. ACTUALIZAR SEGUIMIENTO
// PATCH /api/dashboard/adopciones/:id/seguimiento
// ============================================
router.patch('/adopciones/:id/seguimiento', async (req, res) => {
    try {
        const id = Number(req.params.id);
        const { estado_seguimiento } = req.body;

        const estados = [
            'Pendiente',
            'En proceso',
            'Completado'
        ];

        if (!Number.isInteger(id) || id <= 0) {
            return res.status(400).json({
                error: 'ID de adopción inválido'
            });
        }

        if (!estados.includes(estado_seguimiento)) {
            return res.status(400).json({
                error: 'Estado no permitido',
                estados_permitidos: estados
            });
        }

        const [resultado] = await pool.execute(
            `UPDATE adopciones
             SET estado_seguimiento = ?
             WHERE id_adopcion = ?`,
            [estado_seguimiento, id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: 'Adopción no encontrada'
            });
        }

        res.json({
            mensaje: 'Seguimiento actualizado correctamente'
        });

    } catch (error) {
        res.status(500).json({
            error: 'Error al actualizar seguimiento',
            detalle: error.message
        });
    }
});

// ============================================
// 7. DONACIONES RECIENTES
// GET /api/dashboard/donaciones
// Parámetro opcional: limite
// ============================================
router.get('/donaciones', async (req, res) => {
    try {
        const limite = Number(req.query.limite ?? 5);

        if (
            !Number.isInteger(limite) ||
            limite < 1 ||
            limite > 100
        ) {
            return res.status(400).json({
                error: 'El límite debe estar entre 1 y 100'
            });
        }

        const [resultados] = await pool.execute(
            `SELECT id_donacion, fecha, tipo, detalle, id_persona
             FROM donaciones
             ORDER BY fecha DESC, id_donacion DESC
             LIMIT ?`,
            [limite]
        );

        res.json(resultados);

    } catch (error) {
        res.status(500).json({
            error: 'Error al consultar donaciones',
            detalle: error.message
        });
    }
});

// ============================================
// 8. RESUMEN DE DONACIONES POR TIPO
// GET /api/dashboard/donaciones/resumen
// ============================================
router.get('/donaciones/resumen', async (req, res) => {
    try {
        const [resultados] = await pool.execute(`
            SELECT tipo, COUNT(*) AS total
            FROM donaciones
            GROUP BY tipo
            ORDER BY total DESC
        `);

        res.json(resultados);

    } catch (error) {
        res.status(500).json({
            error: 'Error al obtener resumen de donaciones',
            detalle: error.message
        });
    }
});

// ============================================
// 9. RESUMEN MENSUAL DEL AÑO ACTUAL
// GET /api/dashboard/mensual
// ============================================
router.get('/mensual', async (req, res) => {
    try {
        const anio = Number(req.query.anio ?? new Date().getFullYear());

        if (!Number.isInteger(anio) || anio < 1000 || anio > 9999) {
            return res.status(400).json({
                error: 'Año inválido'
            });
        }

        const [animales] = await pool.execute(`
            SELECT MONTH(fecha_nacimiento) AS mes, COUNT(*) AS total
            FROM animales
            WHERE fecha_nacimiento >= ?
              AND fecha_nacimiento < ?
            GROUP BY MONTH(fecha_nacimiento)
        `, [`${anio}-01-01`, `${anio + 1}-01-01`]);

        const [adopciones] = await pool.execute(`
            SELECT MONTH(fecha) AS mes, COUNT(*) AS total
            FROM adopciones
            WHERE fecha >= ? AND fecha < ?
            GROUP BY MONTH(fecha)
        `, [`${anio}-01-01`, `${anio + 1}-01-01`]);

        const [donaciones] = await pool.execute(`
            SELECT MONTH(fecha) AS mes, COUNT(*) AS total
            FROM donaciones
            WHERE fecha >= ? AND fecha < ?
            GROUP BY MONTH(fecha)
        `, [`${anio}-01-01`, `${anio + 1}-01-01`]);

        res.json({
            anio,
            animales_registrados_por_mes: animales,
            adopciones_por_mes: adopciones,
            donaciones_por_mes: donaciones
        });

    } catch (error) {
        res.status(500).json({
            error: 'Error al obtener resumen mensual',
            detalle: error.message
        });
    }
});

// ============================================
// 10. LISTAR VOLUNTARIOS
// GET /api/dashboard/voluntarios
// ============================================
router.get('/voluntarios', async (req, res) => {
    try {
        const { estado } = req.query;

        let sql = `
            SELECT id_voluntario, nombre, rol, turno,
                   dias, fecha_ingreso, estado
            FROM voluntarios
            WHERE 1 = 1
        `;

        const params = [];

        if (estado) {
            sql += ' AND estado = ?';
            params.push(estado);
        }

        sql += ' ORDER BY nombre ASC';

        const [resultados] = await pool.execute(sql, params);

        res.json(resultados);

    } catch (error) {
        res.status(500).json({
            error: 'Error al consultar voluntarios',
            detalle: error.message
        });
    }
});

module.exports = router;
