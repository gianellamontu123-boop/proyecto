const express = require ("express");

const pool = require("./bd/conexion")

const app=express();
const PORT =3000;

app.use(express.json());
async function
probarconexion(){
    try {
        await pool.query("SELECT 1");
        console.log("conexion exitosa")
    } catch (error) {
        console.log(error.message)
    }
}

app.listen(PORT, async () => {
    console.log(`Servidor ejecuntandose en http://localhost:${PORT}`)
    await probarconexion()
})