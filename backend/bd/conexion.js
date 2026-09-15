const mysql = requiere("mysql2/promise");

const pool = mysql.createpool({
    host: "localhost",
    port:3306,
    user: "root",
    password: "1234",
    database: "arca_bd"
})
