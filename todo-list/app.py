from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os


app = Flask(__name__)
DB_PATH = 'tasks.db'


def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        with open('database/schema.sql', 'r') as f:
            conn.executescript(f.read())
        conn.close()


@app.route('/')
def index():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    tasks = conn.execute('SELECT * FROM habits ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)


# ... остальные функции с 2 пустыми строками между ними ...


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


