from sql_logic import *


def add_task(name, deadline):
    """ Добавить задачу """
    sql_add_task(name, deadline)


def get_keyboard_task():
    """ получение инфы для создания клавиатуры """
    data = sql_get_all_tasks()
    all_tasks = {}
    for row in data:
        id_task = row[0]
        date = row[1]
        date_done = row[2]
        deadline = row[3]
        name_task = row[4]
        all_tasks[id_task] = {
                             'name': f'{name_task}',
                             'date_done': f'{date_done}',
                             'deadline': f'{deadline}',
                             'date_create': f'{date}'
                         }
    return all_tasks


def get_all_info_task(task_id):
    """ получение информации о задаче """
    sql_task_info = sql_get_all_info(task_id)
    task_info = {}
    for row in sql_task_info:
        date_create = row[0]
        date_done = row[1]
        deadline = row[2]
        name = row[3]
        if date_done == None:
            date_done = 'Нет'
        task_info = {
            'name': f'{name}',
            'date_create': f'{date_create}',
            'deadline': f'{deadline}',
            'date_done': f'{date_done}'
        }
    return task_info
