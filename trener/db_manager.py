import sqlite3
import os

DB_PATH = "training_history.db"

def init_db():
    """Створює таблицю, якщо вона ще не існує."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS training_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            duration_sec INTEGER,
            reps_done INTEGER,
            target_reps INTEGER,
            error_count INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_session(duration, reps_done, target_reps, error_count):
    """Зберігає результати тренування у БД."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO training_sessions (duration_sec, reps_done, target_reps, error_count)
        VALUES (?, ?, ?, ?)
    ''', (int(duration), int(reps_done), int(target_reps), int(error_count)))
    conn.commit()
    conn.close()

def get_all_sessions():
    """Повертає всі записи відсортовані від найновіших до найстаріших."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, date_time, duration_sec, reps_done, target_reps, error_count 
        FROM training_sessions ORDER BY date_time DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_records(ids_to_delete):
    """Видаляє вибрані записи за їх ID."""
    if not ids_to_delete: 
        return
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    placeholders = ','.join('?' for _ in ids_to_delete)
    cursor.execute(f'DELETE FROM training_sessions WHERE id IN ({placeholders})', ids_to_delete)
    conn.commit()
    conn.close()