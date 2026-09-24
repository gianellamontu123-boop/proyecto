const express = requiere("express");
const pool = require(".,/bd/conexion");

const router = express.Router();

//Agregar un animal 
router.post("/", async(req, res) => {
    const {
        nombre,
        especie,
        raza,
        sexo,
        fecha_nacimiento,
        estado_actual
    } = req.body;
    try {
        const[resultado] = await pool.execute(
           `INSERT INTO animales (especie,raza,nombre,sexo,fecha_nacimiento,estado_actual) VALUES (?,?,?,?,?,?)`,
           [
              especie,
              raza,
              nombre,
              sexo,
              fecha_nacimiento,
              estado_actual
           ]
        )
        return res.status(201).json({mensaje:"animales agregado correctamente"
       } )
    }catch (error) {
        return res.status(500).json({
            error:"No se pudo agregar el producto",
            detalle:error.message
    })
    }

})