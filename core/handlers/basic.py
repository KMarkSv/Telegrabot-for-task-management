
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, InputFile
import sqlite3

from id import dp, bot


async def add_tasks (message:Message):
    await message.answer('Введите задачу, и сроки:\n<b>пример:</b> <code>Помыть посуду - 07.12.2024 10.47</code>', parse_mode="HTML")
    try:
        await dp.message.register(getting_text, F.text)  # вызов следующей функции
    except TypeError:
        print('TypeError')




async def get_start(message: Message, bot: Bot):
    user_name = message.from_user.username
    welcome_text = """
    <b>Привет! 👋</b>\nЯ — твой персональный помощник для управления задачами.\nВместе мы справимся со всеми делами! 🎯

    Вот что я могу:
    - 📋 <b>Добавить задачу</b>: просто введи её текст и дедлайн.
    - ✅ <b>Отметить выполненное</b>: закрой задачу, если она готова.
    - ❌ <b>Удалить задачу</b>: избавься от лишнего.
    - 🔔 <b>Напомнить о дедлайне</b>: если время поджимает.

    📚 <b>Команды для работы:</b>
    - <code>/add</code> — добавить новую задачу.
    - <code>/list</code> — посмотреть список всех задач.
    - <code>/done &lt;номер задачи&gt;</code> — отметить задачу выполненной.
    - <code>/delete &lt;номер задачи&gt;</code> — удалить задачу.
    - <code>/clear</code> — очистить весь список задач.
    \n🎯 <b>Начни планировать уже сейчас!</b>\nВведи команду, чтобы приступить.
    """

    await message.answer(text=welcome_text, parse_mode="HTML")




async def getting_text(message: Message, bot: Bot):
    user_id = message.from_user.id  # Получаем ID пользователя
    table_name = f"user_{user_id}"  # Уникальное имя таблицы для каждого пользователя

    # Подключаемся к базе данных (создается, если её нет)
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Создаем таблицу для пользователя, если она еще не существует
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Не выполнено'
    )
    """)

    # Разделяем текст на части
    list_med = message.text.split('-')
    print(message.text)
    print(list_med)

    # Проверяем корректность данных и записываем в таблицу
    if len(list_med) == 2:
        task = list_med[0].strip()
        date = f'До {list_med[1].strip()}'
        status = "Не выполнено"  # По умолчанию статус задачи "Не выполнено"

        # Записываем данные в таблицу
        cursor.execute(f"INSERT INTO {table_name} (task, date, status) VALUES (?, ?, ?)", (task, date, status))

        # Сохраняем изменения и подтверждаем пользователю
        conn.commit()
        await message.answer(f"Задача: '{task}' с датой: '{date}' добавлена в базу данных со статусом '{status}'.")
    else:
        await message.answer("Ошибка: формат ввода некорректный. Пример: 'Помыть посуду - 07.12.2024 10:47'")

    # Закрываем соединение
    conn.close()











async def user_list(message: Message, bot: Bot):
    user_id = message.from_user.id  # Получаем ID пользователя
    table_name = f"user_{user_id}"  # Уникальное имя таблицы для каждого пользователя

    # Подключаемся к базе данных
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    try:
        # Извлекаем все записи из таблицы пользователя
        cursor.execute(f"SELECT id, task, date, status FROM {table_name}")
        tasks = cursor.fetchall()

        # Если задач нет
        if not tasks:
            await message.answer("Ваш список задач пуст.")
        else:
            # Формируем строку со списком задач
            tasks_text = "\n\n".join(
                [f"<b>Задача #{row[0]}:</b>\n<b>Описание:</b> {row[1]}\n<b>Дата:</b> {row[2]}\n<b>Статус:</b> {row[3]}"
                 for row in tasks]
            )
            await message.answer(f"<b>Ваш список задач:</b>\n\n{tasks_text}", parse_mode="HTML")

    except sqlite3.OperationalError:
        # Если таблицы для пользователя нет
        await message.answer("У вас еще нет добавленных задач.")
    finally:
        # Закрываем соединение
        conn.close()




async def done_number(message: Message, bot: Bot):
    user_id = message.from_user.id  # ID пользователя
    table_name = f"user_{user_id}"  # Таблица пользователя
    command = message.text.split()  # Разделяем сообщение на части

    if len(command) != 2 or not command[1].isdigit():
        await message.answer("Пожалуйста, используйте команду в формате: /done <номер задачи>")
        return

    task_id = int(command[1])  # Получаем номер задачи

    # Подключение к базе данных
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    try:
        # Проверяем, существует ли задача с таким ID
        cursor.execute(f"SELECT task FROM {table_name} WHERE id = ?", (task_id,))
        task = cursor.fetchone()

        if not task:
            await message.answer(f"Задача с номером {task_id} не найдена.")
        else:
            # Обновляем статус задачи
            cursor.execute(f"UPDATE {table_name} SET status = ? WHERE id = ?", ("Выполнено", task_id))
            conn.commit()
            await message.answer(f"Задача #{task_id} успешно отмечена как выполненная.")
    except sqlite3.OperationalError:
        # Обработка случая, если таблицы пользователя нет
        await message.answer("У вас еще нет добавленных задач.")
    finally:
        # Закрытие соединения
        conn.close()





async def delete_task(message: Message):
    # Проверяем, что пользователь ввёл корректный номер задачи
    command_parts = message.text.split()
    if len(command_parts) != 2 or not command_parts[1].isdigit():
        await message.reply("Введите команду в формате: /delete <номер задачи>")
        return

    task_number = int(command_parts[1])  # Получаем номер задачи
    user_id = message.from_user.id  # Идентификатор пользователя
    table_name = f"user_{user_id}"  # Имя таблицы для пользователя

    # Подключение к базе данных
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    try:
        # Получаем задачу, чтобы проверить её существование
        cursor.execute(f"SELECT rowid, * FROM {table_name}")
        tasks = cursor.fetchall()

        if task_number < 1 or task_number > len(tasks):
            await message.reply(f"Задачи с номером {task_number} не существует.")
            return

        # Удаляем задачу
        task_id = tasks[task_number - 1][0]  # Получаем rowid для удаления
        cursor.execute(f"DELETE FROM {table_name} WHERE rowid = ?", (task_id,))
        conn.commit()

        await message.reply(f"Задача №{task_number} успешно удалена!")
    except sqlite3.OperationalError:
        await message.reply("У вас пока нет задач.")
    finally:
        conn.close()




async def clear_tasks(message: Message):
    user_id = message.from_user.id  # Идентификатор пользователя
    table_name = f"user_{user_id}"  # Имя таблицы для пользователя

    # Подключение к базе данных
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    try:
        # Проверяем, есть ли таблица для данного пользователя
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cursor.fetchone():
            await message.reply("У вас нет задач, которые можно очистить.")
            return

        # Очищаем таблицу пользователя
        cursor.execute(f"DELETE FROM {table_name}")
        conn.commit()

        await message.reply("Ваш список задач был успешно очищен!")
    except sqlite3.OperationalError as e:
        await message.reply("Произошла ошибка при попытке очистить задачи.")
        print(f"Ошибка: {e}")
    finally:
        conn.close()