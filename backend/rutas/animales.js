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
})