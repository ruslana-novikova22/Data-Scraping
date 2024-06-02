const express = require('express');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();

const app = express();
app.use(bodyParser.json());

// Підключення до існуючої бази даних
const db = new sqlite3.Database('university.db');

// API для отримання даних
app.get('/api/faculties', (req, res) => {
    db.all("SELECT * FROM Faculty", [], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(rows);
    });
});

app.get('/api/departments', (req, res) => {
    db.all("SELECT * FROM Department", [], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(rows);
    });
});

app.get('/api/staff', (req, res) => {
    db.all("SELECT * FROM Lecturer", [], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(rows);
    });
});

// API для збереження даних
app.post('/api/faculties', (req, res) => {
    const { name, url } = req.body;
    db.run("INSERT INTO faculties (name, url) VALUES (?, ?)", [name, url], function(err) {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.status(201).json({ message: 'Дані про факультет отримано', id: this.lastID });
    });
});

app.post('/api/departments', (req, res) => {
    const { name, url, faculty } = req.body;
    db.run("INSERT INTO departments (name, url, faculty) VALUES (?, ?, ?)", [name, url, faculty], function(err) {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.status(201).json({ message: 'Дані про кафедру отримано', id: this.lastID });
    });
});

app.post('/api/staff', (req, res) => {
    const { teacher, department, img_url, img_path } = req.body;
    db.run("INSERT INTO staff (teacher, department, img_url, img_path) VALUES (?, ?, ?, ?)", [teacher, department, img_url, img_path], function(err) {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.status(201).json({ message: 'Дані про працівника отримано', id: this.lastID });
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
