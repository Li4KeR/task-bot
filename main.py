from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

from keyboards import *
from logic import *
from sql_logic import *


""" настройки """
token = '6254363282:AAGQJkntDkeqFsycS3e-Rx5nJp7fwG7pPiM'
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class TaskModel(StatesGroup):
    """ модель задач """
    name = State()
    deadline = State()


@dp.message_handler(commands="start")
async def menu_start(message: types.Message):
    """ стартовое меню """
    await message.answer("Доброе пожаловать, хозяин! <3", reply_markup=main)


@dp.callback_query_handler(lambda call: "main" in call.data)
async def next_keyboard(call: types.CallbackQuery):
    """ возвращение в стартовое меню """
    await call.message.edit_text(text="Доброе пожаловать, хозяин! <3")
    await call.message.edit_reply_markup(reply_markup=main)
    await call.answer()


@dp.callback_query_handler(lambda call: "menu_all_tasks" in call.data)
async def menu_all_tasks(call: types.CallbackQuery):
    """ меню со всеми задачами """
    keyboard_task = create_all_tasks_keyboard()
    if keyboard_task != []:
        await call.message.edit_text(text="Мои задачи:")
        await call.message.edit_reply_markup(reply_markup=keyboard_task)
    else:
        await call.message.edit_text(text="У меня нет задач")
        await call.message.edit_reply_markup(reply_markup=back_to_main)
    await call.answer()


@dp.callback_query_handler(lambda call: 'menu_add_task' in call.data)
async def menu_add_task(call: types.CallbackQuery):
    """ начало добавления задачи, запуск фсм """
    await call.message.edit_text(text="Введите имя задачи:")
    await call.message.edit_reply_markup(reply_markup=main)
    await TaskModel.name.set()


@dp.message_handler(state=TaskModel.name)
async def menu_enter_deadline(message: types.Message, state: FSMContext):
    """ ввод дедлайна и присвоение поля ИМЯ фсм """
    answer = message.text
    await state.update_data(name=answer)
    await message.answer('Срок')
    await TaskModel.deadline.set()


@dp.message_handler(state=TaskModel.deadline)
async def menu_create_task(message: types.Message, state: FSMContext):
    """ присвоение дедлайна и остановка фсм """
    answer = message.text
    await state.update_data(deadline=answer)
    data = await state.get_data()
    await state.finish()
    name = data['name']
    deadline = data['deadline']
    add_task(name, deadline)
    await message.answer('Задача добавлена', reply_markup=back_to_main)


@dp.callback_query_handler(Text(startswith="taskid_"))
async def all_info_task(call: types.CallbackQuery):
    """ вывод информации о задаче """
    task_id = call.data.split("_")[1]
    info_task = get_all_info_task(task_id)
    info_task_keyboard = types.InlineKeyboardMarkup(row_width=2)
    info_task_keyboard.add(
        InlineKeyboardButton(text="Завершить", callback_data=f"task_done_{task_id}"),
        InlineKeyboardButton(text="Удалить", callback_data=f"delete_task_{task_id}"),
        InlineKeyboardButton(text="Главное меню", callback_data='main')
    )
    await call.message.edit_text(text=f"Задача: {info_task.get('name')}\n"
                                      f"Создана: {info_task.get('date_create')}\n"
                                      f"Дедлайн: {info_task.get('deadline')}\n"
                                      f"Завершена: {info_task.get('date_done')}")
    await call.message.edit_reply_markup(reply_markup=info_task_keyboard)


@dp.callback_query_handler((Text(startswith='task_done')))
async def task_done(call: types.CallbackQuery):
    """ завершение задачи """
    task_id = call.data.split('_')[2]
    sql_task_done(task_id)
    await call.message.edit_text(f"Задача завершена")
    await call.message.edit_reply_markup(reply_markup=back_to_main)


@dp.callback_query_handler((Text(startswith='delete_task_')))
async def task_done(call: types.CallbackQuery):
    """ удаление задачи """
    task_id = call.data.split('_')[2]
    sql_delete_task(task_id)
    await call.message.edit_text(f"Задача удалена")
    await call.message.edit_reply_markup(reply_markup=back_to_main)


if __name__ == '__main__':
    check_sql()
    executor.start_polling(dp, skip_updates=True)