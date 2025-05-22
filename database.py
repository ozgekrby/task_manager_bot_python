import sqlite3

DEFAULT_DB_NAME = "tasks.db" 

def get_db_connection(db_name=None):
    """Belirtilen veritabanına veya varsayılana bir bağlantı kurar."""
    name_to_use = db_name if db_name is not None else DEFAULT_DB_NAME
    conn = sqlite3.connect(name_to_use)
    return conn

def init_db(db_name=None):
    """Veritabanını ve görevler tablosunu oluşturur (eğer yoksa)."""
    conn = get_db_connection(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            completed INTEGER DEFAULT 0 -- 0: incomplete, 1: completed
        )
    ''')
    conn.commit()
    conn.close()

def add_task_db(description: str, db_name=None):
    """Veritabanına yeni bir görev ekler."""
    conn = get_db_connection(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (description) VALUES (?)", (description,))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def get_tasks_db(db_name=None):
    """Tüm görevleri veritabanından alır."""
    conn = get_db_connection(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, completed FROM tasks ORDER BY id ASC")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_task_db(task_id: int, db_name=None) -> bool:
    """Belirli bir ID'ye sahip görevi siler. Başarılıysa True döner."""
    conn = get_db_connection(db_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()
    return deleted_rows > 0

def complete_task_db(task_id: int, db_name=None) -> bool:
    """
    Belirli bir ID'ye sahip görevi tamamlandı olarak işaretler.
    Görev bulunamazsa veya zaten tamamlanmışsa False döner.
    Başarıyla tamamlandı olarak işaretlenirse True döner.
    """
    conn = get_db_connection(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT completed FROM tasks WHERE id = ?", (task_id,))
    task_status = cursor.fetchone()

    if not task_status:
        conn.close()
        return False
    
    if task_status[0] == 1:
        conn.close()
        return False

    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    updated_rows = cursor.rowcount
    conn.close()
    return updated_rows > 0

def get_task_by_id_db(task_id: int, db_name=None):
    """Belirli bir ID'ye sahip görevi alır."""
    conn = get_db_connection(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, completed FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    return task

def clear_tasks_table(db_name=None):
    """Belirtilen veritabanındaki tasks tablosunu temizler ve ID sayacını sıfırlar."""
    target_db = db_name if db_name is not None else DEFAULT_DB_NAME
    conn = get_db_connection(db_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='tasks'")
    conn.commit()
    conn.close()