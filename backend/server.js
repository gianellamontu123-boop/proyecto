const express = require ("express");

const app=express();
const PORT =3000;

app.use(express.json());

app.listen(PORT, async () => {
    console.log(`Servidor ejecuntandose en http://localhost:${PORT}`)
})