import sqlite3
from datetime import datetime


def check_sql():
    """ создаем бд """
    try:
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS tasks(
                    id INTEGER PRIMARY KEY,
                    date_create TEXT NOT NULL,
                    date_done TEXT,
                    deadline TEXT,
                    name TEXT NOT NULL);
                    """)

        conn.commit()
        cursor.close()
        return True
    except sqlite3.Error as error:
        error_text = "Ошибка при работе с SQLite ", error
        print(error_text)
        return False


def sql_get_all_tasks():
    """ возвращает информацию о всех задачах """
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    data = cursor.execute(f"SELECT id, date_create, date_done, deadline, name from tasks").fetchall()
    conn.close()
    return data


def sql_add_task(name, deadline):
    """ добавить задачу """
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    date = datetime.now()
    cursor.execute(f"INSERT INTO tasks(date_create, deadline, name) VALUES('{date}', '{deadline}', '{name}')")
    conn.commit()


def sql_get_all_info(task_id):
    """ вся информация о задаче по id """
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    task_info = cursor.execute(f"SELECT date_create, date_done, deadline, name from tasks where id='{task_id}'").fetchall()
    return task_info


def sql_task_done(task_id):
    """ завершение задачи по id """
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    date = datetime.now()
    cursor.execute(f"UPDATE tasks SET date_done='{date}' WHERE id='{task_id}'")
    conn.commit()


def sql_delete_task(task_id):
    """ удаления задачи по id """
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM tasks WHERE id='{task_id}'")
    conn.commit()

