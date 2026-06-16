import pytest
import tempfile
import os
import sys
import sqlite3

# Добавляем текущую директорию в PYTHONPATH
sys.path.insert(0, '.')

from app import app, DB_PATH  # Теперь импорт работает


@pytest.fixture
def client():
    """Создаёт тестовый клиент Flask с временной БД"""
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    
    app.config['TESTING'] = True
    app.config['DATABASE'] = db_path
    
    with app.test_client() as client:
        with app.app_context():
            # Инициализируем БД
            conn = sqlite3.connect(db_path)
            conn.execute('''
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    completed INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()
        yield client
    
    os.close(db_fd)
    os.unlink(db_path)


def test_index_page(client):
    """Проверяет, что главная страница загружается"""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'To-Do List' in rv.data


def test_add_task(client):
    """Проверяет добавление задачи"""
    rv = client.post('/add', data={'title': 'Test Task'}, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Test Task' in rv.data


def test_toggle_task(client):
    """Проверяет переключение статуса задачи"""
    # Сначала добавляем задачу
    client.post('/add', data={'title': 'Toggle Me'})
    
    # Получаем ID задачи из БД
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.execute('SELECT id FROM habits WHERE title = ?', ('Toggle Me',))
    task_id = cursor.fetchone()[0]
    conn.close()
    
    # Переключаем статус
    rv = client.get(f'/toggle/{task_id}', follow_redirects=True)
    assert rv.status_code == 200


def test_delete_task(client):
    """Проверяет удаление задачи"""
    # Сначала добавляем задачу
    client.post('/add', data={'title': 'Delete Me'})
    
    # Получаем ID задачи
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.execute('SELECT id FROM habits WHERE title = ?', ('Delete Me',))
    task_id = cursor.fetchone()[0]
    conn.close()
    
    # Удаляем задачу
    rv = client.get(f'/delete/{task_id}', follow_redirects=True)
    assert rv.status_code == 200

