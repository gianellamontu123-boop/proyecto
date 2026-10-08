const express = require ("express");
const pool = require("./bd/conexion");
const routerAnimales = require("./rutas/animales");
const loginRouter = require("./rutas/login")
const ADOPCIONESRouter = require("./rutas/adopciones")

const app=express();
const PORT =3000;

app.use(express.json()); 

app.use("/api/animales", routerAnimales)
app.use("/api/login", loginRouter)
app.use("/api/adopciones", ADOPCIONESRouter)
async function probarconexion(){
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