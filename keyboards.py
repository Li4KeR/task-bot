from aiogram import types
from aiogram.types import InlineKeyboardButton

from logic import get_keyboard_task

main = types.InlineKeyboardMarkup(row_width=2) # основная клавиатура
back_to_main = types.InlineKeyboardMarkup() # клавиатура возращения в главное меню


def create_all_tasks_keyboard():
    all_tasks = get_keyboard_task()
    if all_tasks != {}:
        all_tasks_keyboard = types.InlineKeyboardMarkup(row_width=2)
        for key, value in all_tasks.items():
            id_task = key
            name = value.get('name')
            all_tasks_keyboard.add(InlineKeyboardButton(text=f'{name}', callback_data=f'taskid_{id_task}'))
            print(name)
            print(id_task)
    else:
        all_tasks_keyboard = []
    return all_tasks_keyboard


""" кнопки основного меню """
main.add(
    InlineKeyboardButton(text="Все задачи", callback_data="menu_all_tasks"),
    InlineKeyboardButton(text="Добавить задачу", callback_data="menu_add_task")
)


""" кнопки возврата в главное меню """
back_to_main.add(
    InlineKeyboardButton(text="Главное меню", callback_data="main")
)


