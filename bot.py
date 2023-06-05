import logging
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import Message


logging.basicConfig(level=logging.INFO)  # Установка уровня логирования

API_TOKEN = "ВАШ ТОКЕН"  # Сделать токен своего бота можно тут - https://t.me/BotFather
ADMIN = None  # Узнать свой ID аккаунта можно тут - https://t.me/getmyid_bot

Start_Photo, Help_Photo, Vacancy_Photo, Events_Photo, Spam_Photo = "photo/Menu.jpg", "photo/Help.jpg", \
    "photo/Vacancy.jpg", "photo/Events.jpg", "photo/Spam.jpg"  # Конфиг всех фото которые используются

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Создание баз данных (database1 - для рассылок, админки и прочего. database2 - для добавлений вакансий. database3 - для добавлений мероприятий)
conn1 = sqlite3.connect('db/database1.db')
cur1 = conn1.cursor()
cur1.execute("""CREATE TABLE IF NOT EXISTS bot(
   user_id INTEGER);
""")
conn1.commit()
conn1.commit()
conn2 = sqlite3.connect('db/database2.db')
cursor2 = conn2.cursor()
cursor2.execute('''CREATE TABLE IF NOT EXISTS bot2
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   job TEXT);''')
conn2.commit()
conn3 = sqlite3.connect('db/database3.db')
cursor3 = conn3.cursor()
cursor3.execute('''CREATE TABLE IF NOT EXISTS bot3
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   event TEXT);''')
conn3.commit()


# Определение состояний для FSM (Finite State Machine)
class AdminStates(StatesGroup):
    ADDING_SPAM = State()
    ADDING_JOB = State()
    ADDING_EVENTS = State()
    REMOVE_EVENTS = State()
    REMOVE_JOB = State()


# Обработчик команды /start
@dp.message_handler(Command('start'))
async def cmd_start(message: types.Message):
    if message.from_user.id == ADMIN:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка 📝"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить вакансию ➕"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить мероприятие ➕"))
        keyboard.add(types.InlineKeyboardButton(text="Удалить мероприятие ❌"))
        keyboard.add(types.InlineKeyboardButton(text="Удалить вакансию ❌"))
        keyboard.add(types.InlineKeyboardButton(text="Помощь ❔"))
        await message.answer(
            '🔄 <b> Чат-бот Волонтёры Лангепаса </b> - ЗАПУСКАЕТСЯ, ПОЖАЛУЙСТА, ПОДОЖДИТЕ... 🔄',
            parse_mode='HTML')
        with open(Start_Photo, 'rb') as file:
            file.seek(0)
            await message.answer_photo(photo=file)
            file.close()
            await message.answer(
                """
Добро пожаловать, <b>Администратор</b>. Выберите то, что вы хотите сделать.
                """, parse_mode="HTML", reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Посмотреть вакансии 💼‍"))
        keyboard.add(types.InlineKeyboardButton(text="Посмотреть мероприятия 📋"))
        keyboard.add(types.InlineKeyboardButton(text="Помощь ❔"))
        await message.answer(
            '🔄 <b> Чат-бот Волонтёры Лангепаса </b> - ЗАПУСКАЕТСЯ, ПОЖАЛУЙСТА, ПОДОЖДИТЕ... 🔄',
            parse_mode='HTML')
        with open(Start_Photo, 'rb') as file:
            file.seek(0)
            await message.answer_photo(photo=file)
            file.close()
            await message.answer(
                """
Добро пожаловать, <b>Пользователь</b>. Выберите то, что вы хотите сделать.
                """, parse_mode="HTML", reply_markup=keyboard)


# Обработчик команды Рассылка 📝
@dp.message_handler(content_types=['text'], text='Рассылка 📝')
async def text_spam(message: Message):
    if message.from_user.id == ADMIN:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Назад 🔄️"))
        await AdminStates.ADDING_SPAM.set()
        await message.answer(
            """
🔄️ Действие <b>выполняется</b>, подождите... 🔄️
            """, parse_mode="HTML")
        with open(Spam_Photo, 'rb') as file:
            file.seek(0)
            await message.answer_photo(photo=file)
            file.close()
            await message.answer(
                """
Напишите <b>текст</b>, чтобы начать <b>рассылку</b> всем пользователям, которые пользовались чат-ботом.
                """, parse_mode="HTML", reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Назад 🔄️"))
        await message.answer(
            """
🔄️ Действие <b>выполняется</b>, подождите... 🔄️
            """, parse_mode="HTML")
        with open(Spam_Photo, 'rb') as file:
            file.seek(0)
            await message.answer_photo(photo=file)
            file.close()
            await message.answer(
                """
Вы не являетесь <b>администратором</b>.
                """, parse_mode="HTML", reply_markup=keyboard)


# Выполнение действия рассылки
@dp.message_handler(state=AdminStates.ADDING_SPAM)
async def process_spam(message: Message, state: FSMContext):
    if message.text == 'Назад 🔄️':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка 📝"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить вакансию ➕"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить мероприятие ➕"))
        keyboard.add(types.InlineKeyboardButton(text="Удалить мероприятие ❌"))
        keyboard.add(types.InlineKeyboardButton(text="Удалить вакансию ❌"))
        keyboard.add(types.InlineKeyboardButton(text="Помощь ❔"))
        await message.answer(
            """
🔄️ Действие <b>выполняется</b>, подождите... 🔄️
            """, parse_mode="HTML")
        with open(Start_Photo, 'rb') as file:
            file.seek(0)
            await message.answer_photo(photo=file)
            file.close()
            await message.answer(
                """
Вы вернулись в <b>главное меню</b>.
                """, parse_mode="HTML", reply_markup=keyboard)
        await state.finish()
    else:
        cur1.execute(f'''SELECT user_id FROM bot''')
        spam_base = cur1.fetchall()
        print(spam_base)
        for z in range(len(spam_base)):
            print(spam_base[z][0])
        for z in range(len(spam_base)):
            await bot.send_message(spam_base[z][0], message.text)
            await message.answer(
                """
Рассылка завершена <b>успешно</b>. ✅
                """, parse_mode="HTML")
        await state.finish()


# Обработчик команды Добавить вакансию ➕
@dp.message_handler(content_types=['text'], text='Добавить вакансию ➕')
async def text_adding_job(message: types.Message):
    if message.chat.id == ADMIN:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Назад 🔄️"))
        await message.answer(
            """
🔄️ Действие <b>выполняется</b>, подождите... 🔄️
            """, parse_mode="HTML")
        with open(Vacancy_Photo, 'rb') as file:
            file.seek(0)
            await message.answer_photo(photo=file)
            file.close()
            await message.answer(
                """
💼Чтобы добавить <b>вакансию</b>, напишите текст по такому формату:

📋<b>(РАБОТА | ОПИСАНИЕ РАБОТЫ | КОНТАКТЫ)</b>

⚠️<b>Обязательно</b> соблюдайте формат добавления вакансии!
                """, parse_mode="HTML", reply_markup=keyboard)
        await AdminStates.ADDING_JOB.set()


# Выполнение действия добавлений вакансии
@dp.message_handler(state=AdminStates.ADDING_JOB)
async def process_add_text(message: types.Message, state: FSMContext):
    if message.text == 'Назад 🔄️':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка 📝"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить вакансию ➕"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить мероприятие ➕"))
        keyboard.add(types.InlineKeyboardButton(text="Удалить мероприятие ❌"))
        keyboard.add(types.InlineKeyboardButton(text="Удалить вакансию ❌"))
        keyboard.add(types.InlineKeyboardButton(text="Помощь ❔"))
        await message.answer(
            """
🔄️ Действие <b>выполняется</b>, подождите... 🔄️
            """, parse_mode="HTML")
        with open(Start_Photo, 'rb') as file:
            file.seek(0)
            await message.answer_photo(photo=file)
            file.close()
            await message.answer(
                """
Вы вернулись в <b>главное меню</b>.
                """, parse_mode="HTML", reply_markup=keyboard)
        await state.finish()
    else:
        admin_text = message.text
        # Сохранение текста в базе данных
        cur2 = conn2.cursor()
        cur2.execute("INSERT INTO bot2 (job) VALUES (?)", (admin_text,))
        conn2.commit()
        await state.finish()
        await message.answer('✅ Вакансия успешно <b>добавлена</b>.', parse_mode="HTML")


# Обработчик команды Посмотреть вакансии 💼‍
@dp.message_handler(content_types=['text'], text='Посмотреть вакансии 💼‍')
async def view_job(message: types.Message):
    # Получение вакансий из базы данных
    cur2 = conn2.cursor()
    cur2.execute("SELECT job FROM bot2")
    job = cur2.fetchall()
    if job:
        response = '<b>💼 Актуальные вакансии:</b>\n'
        for text in job:
            response += f'- {text[0]}\n'
    else:
        response = '💼 Вакансии <b>отсутствуют</b>.'
    await message.answer(
        """
🔄️ Действие <b>выполняется</b>, подождите... 🔄️
        """, parse_mode="HTML")
    with open(Vacancy_Photo, 'rb') as file:
        file.seek(0)
        await message.answer_photo(photo=file)
        file.close()
        await message.answer(response, parse_mode="HTML")


# Обработчик команды Удалить вакансию ❌
@dp.message_handler(content_types=['text'], text='Удалить вакансию ❌')
async def remove_job(message: types.Message):
    # Запрос на выборку всех вакансий
    cur2 = conn2.cursor()
    cur2.execute("SELECT id, job FROM bot2")
    vacancies = cur2.fetchall()
    # Проверка, есть ли вакансии в базе данных
    if vacancies:
        # Формирование списка вакансий для вывода пользователю
        vacancies_list = "\n".join([f"{v[0]}. {v[1]}" for v in vacancies])
        # Отправка пользователю список вакансий
        await message.answer("Выберите <b>номер</b> вакансии для удаления:\n" + vacancies_list, parse_mode="HTML")
        # Ожидание ввода номера вакансии от пользователя
        await AdminStates.REMOVE_JOB.set()
    else:
        await message.answer(
            """
В базе данных <b>отсутствуют</b> вакансии.
            """, parse_mode="HTML")


# Выполнение удаления вакансии
@dp.message_handler(state=AdminStates.REMOVE_JOB)
async def process_add_text(message: types.Message, state: FSMContext):
    if message.text == 'Назад 🔄️':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка 📝"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить вакансию ➕"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить мероприятие ➕"))
        keyboard.add(types.InlineKeyboardButton(text="Удалить мероприятие ❌"))
        keyboard.add(types.InlineKeyboardButton(text="Удалить вакансию ❌"))
        keyboard.add(types.InlineKeyboardButton(text="Помощь ❔"))
        await message.answer(
            """
🔄️ Действие <b>выполняется</b>, подождите... 🔄️
            """, parse_mode="HTML")
        with open(Start_Photo, 'rb') as file:
            file.seek(0)
            await message.answer_photo(photo=file)
            file.close()
            await message.answer(
                """
Вы вернулись в <b>ГЛАВНОЕ МЕНЮ</b>.
                """, parse_mode="HTML", reply_markup=keyboard)
        await state.finish()
    else:
        # Получение введенного пользователем номера вакансии
        vacancy_id = message.text.strip()
        # Проверка, является ли введенный номер корректным
        cur2 = conn2.cursor()
        cur2.execute("SELECT id FROM bot2")
        available_ids = [v[0] for v in cur2.fetchall()]
        if vacancy_id.isdigit() and int(vacancy_id) in available_ids:
            vacancy_id = int(vacancy_id)
            # Удаление выбранной вакансии из базы данных
            cur2.execute(f"DELETE FROM bot2 WHERE id = {vacancy_id}")
            conn2.commit()
            await message.answer(
                """
Вакансия успешно <b>удалена</b>.
                """, parse_mode="HTML")
        else:
            await message.answer(
                """
<b>Некорректный</b> номер вакансии.
                """, parse_mode="HTML")
        # Сброс состояния
        await state.finish()


# Обработчик команды Добавить мероприятие ➕
@dp.message_handler(content_types=['text'], text='Добавить мероприятие ➕')
async def text_adding_events(message: types.Message):
    if message.chat.id == ADMIN:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Назад 🔄️"))
        await message.answer(
            """
🔄️ Действие <b>выполняется</b>, подождите... 🔄️
            """, parse_mode="HTML")
        with open(Events_Photo, 'rb') as file:
            file.seek(0)
            await message.answer_photo(photo=file)
            file.close()
            await message.answer(
                """
🧩 Чтобы добавить <b>мероприятие</b>, напишите текст по такому формату:

📋<b>(НАЗВАНИЕ МЕРОПРИЯТИЯ | МЕСТО ПРОВЕДЕНИЯ | ДАТА | ВРЕМЯ)</b>

⚠️<b>Обязательно</b> соблюдайте формат добавления мероприятия!
                """, parse_mode="HTML", reply_markup=keyboard)
        await AdminStates.ADDING_EVENTS.set()


# Выполнение добавления мероприятия
@dp.message_handler(state=AdminStates.ADDING_EVENTS)
async def process_adding_events(message: types.Message, state: FSMContext):
    if message.text == 'Назад 🔄️':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка 📝"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить вакансию ➕"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить мероприятие ➕"))
        keyboard.add(types.InlineKeyboardButton(text="Удалить мероприятие ❌"))
        keyboard.add(types.InlineKeyboardButton(text="Удалить вакансию ❌"))
        keyboard.add(types.InlineKeyboardButton(text="Помощь ❔"))
        await message.answer(
            """
🔄️ Действие <b>выполняется</b>, подождите... 🔄️
            """, parse_mode="HTML")
        with open(Start_Photo, 'rb') as file:
            file.seek(0)
            await message.answer_photo(photo=file)
            file.close()
            await message.answer(
                """
Вы вернулись в <b>ГЛАВНОЕ МЕНЮ</b>.
                """, parse_mode="HTML", reply_markup=keyboard)
        await state.finish()
    else:
        admin_text = message.text
        cur3 = conn3.cursor()
        cur3.execute("INSERT INTO bot3 (event) VALUES (?)", (admin_text,))
        conn3.commit()
        await state.finish()
        await message.answer(
            """
Мероприятие успешно <b>добавлено</b>.
            """, parse_mode="HTML")


# Обработчик команды Посмотреть мероприятия 📋
@dp.message_handler(content_types=['text'], text='Посмотреть мероприятия 📋')
async def view_job(message: types.Message):
    # Получение мероприятий из базы данных
    cur3 = conn3.cursor()
    cur3.execute("SELECT event FROM bot3")
    job = cur3.fetchall()
    if job:
        response = '🧩 Актуальные мероприятия:\n'
        for text in job:
            response += f'- {text[0]}\n'
    else:
        response = '🧩 Мероприятия отсутствуют.'
    await message.answer(
        """
🔄️ Действие <b>выполняется</b>, подождите... 🔄️
        """, parse_mode="HTML")
    with open(Events_Photo, 'rb') as file:
        file.seek(0)
        await message.answer_photo(photo=file)
        file.close()
        await message.answer(response, parse_mode="HTML")


# Обработчик команды Удалить мероприятие ❌
@dp.message_handler(content_types=['text'], text='Удалить мероприятие ❌')
async def remove_job(message: types.Message):
    # Запрос на выборку всех мероприятий
    cur3 = conn3.cursor()
    cur3.execute("SELECT id, event FROM bot3")
    event = cur3.fetchall()
    # Проверка, есть ли вакансии в базе данных
    if event:
        # Формирование списка мероприятия для вывода пользователю
        event_list = "\n".join([f"{v[0]}. {v[1]}" for v in event])
        # Отправка пользователю список мероприятий
        await message.answer("Выберите номер мероприятия для удаления:\n" + event_list)
        # Ожидание ввода номера мероприятия от пользователя
        await AdminStates.REMOVE_EVENTS.set()
    else:
        await message.answer("В базе данных нет мероприятий.")


# Выполнение удаления мероприятия
@dp.message_handler(state=AdminStates.REMOVE_EVENTS)
async def process_add_text(message: types.Message, state: FSMContext):
    if message.text == 'Назад 🔄️':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка 📝"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить вакансию ➕"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить мероприятие ➕"))
        keyboard.add(types.InlineKeyboardButton(text="Удалить мероприятие ❌"))
        keyboard.add(types.InlineKeyboardButton(text="Удалить вакансию ❌"))
        keyboard.add(types.InlineKeyboardButton(text="Помощь ❔"))
        await message.answer(
            """
🔄️ Действие <b>выполняется</b>, подождите... 🔄️
            """, parse_mode="HTML")
        with open(Start_Photo, 'rb') as file:
            file.seek(0)
            await message.answer_photo(photo=file)
            file.close()
            await message.answer(
                """
Вы вернулись в <b>главное меню</b>.
                """, parse_mode="HTML", reply_markup=keyboard)
        await state.finish()
    else:
        # Получение введенного пользователем номера мероприятия
        event_id = message.text.strip()
        # Проверка, является ли введенный номер корректным
        cur3 = conn3.cursor()
        cur3.execute("SELECT id FROM bot3")
        available_ids = [v[0] for v in cur3.fetchall()]
        if event_id.isdigit() and int(event_id) in available_ids:
            event_id = int(event_id)
            # Удаление выбранного мероприятия из базы данных
            cur3.execute(f"DELETE FROM bot3 WHERE id = {event_id}")
            conn3.commit()
            await message.answer("Мероприятие успешно удалено.")
        else:
            await message.answer("Некорректный номер мероприятия.")
        # Сброс состояния
        await state.finish()


# Обработчик команды Помощь ❔
@dp.message_handler(content_types=['text'], text='Помощь ❔')
async def help(message: types.Message):
    if message.chat.id == ADMIN:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка 📝"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить вакансию ➕"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить мероприятие ➕"))
        keyboard.add(types.InlineKeyboardButton(text="Удалить мероприятие ❌"))
        keyboard.add(types.InlineKeyboardButton(text="Удалить вакансию ❌"))
        keyboard.add(types.InlineKeyboardButton(text="Помощь ❔"))
        await message.answer(
            """
🔄️ Действие <b>выполняется</b>, подождите... 🔄️
            """, parse_mode="HTML")
        with open(Help_Photo, 'rb') as file:
            file.seek(0)
            await message.answer_photo(photo=file)
            file.close()
            await message.answer(
                """
🛠️ Подробная инструкция для <b>АДМИНИСТРАТОРА</b> чат-бота. 🛠️


<b>Рассылка</b> 📝 - Команда, которая по определённому тексту отправляет всем сообщение, кто пользовался чат-ботом.

<b>Добавить вакансию</b> ➕ - Команда, которая добавляет вакансию. Обычный пользователь будет видеть вашу добавленную вакансию.

<b>Добавить мероприятие</b> ➕ - Команда, которая добавляет мероприятие. Обычный пользователь будет видеть ваше добавленное мероприятие.

<b>Удалить мероприятие</b> ❌ - Команда, которая удаляет мероприятие. У пользователя также пропадёт мероприятие.

<b>Удалить вакансию</b> ❌ - Команда, которая удаляет вакансию. У пользователя также пропадёт вакансия.

<b>Помощь</b> ❔ - Подробная инструкция для пользования чат-ботом.
                """, parse_mode="HTML", reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Посмотреть вакансии 💼‍"))
        keyboard.add(types.InlineKeyboardButton(text="Посмотреть мероприятия 📋"))
        keyboard.add(types.InlineKeyboardButton(text="Помощь ❔"))
        await message.answer(
            """
🔄️ Действие <b>выполняется</b>, подождите... 🔄️
            """, parse_mode="HTML")
        with open(Help_Photo, 'rb') as file:
            file.seek(0)
            await message.answer_photo(photo=file)
            file.close()
            await message.answer(
                """
🛠️ Подробная инструкция для <b>ПОЛЬЗОВАТЕЛЯ</b> чат-бота. 🛠️


<b>Посмотреть вакансии</b> 💼 - Команда, которая позволяет смотреть все активные вакансии волонтёра.

<b>Посмотреть мероприятия</b> 📋 - Команда, которая позволяет смотреть все активные мероприятия.

<b>Помощь</b> ❔ - Подробная инструкция для пользования чат-ботом.
                """, parse_mode="HTML", reply_markup=keyboard)


if __name__ == '__main__':
    # Запуск бота
    executor.start_polling(dp)
