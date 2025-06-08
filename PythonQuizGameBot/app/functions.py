import aiosqlite
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.quiz_data import quiz_data

# Set the name of the database
DB_NAME = 'quiz_bot.db'


async def get_question(message, user_id):
    # Retrieve the current question from the user state dictionary
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)


async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index)
    await get_question(message, user_id)


async def get_quiz_index(user_id):
     # Connecting to the database
     async with aiosqlite.connect(DB_NAME) as db:
        # Get the record for the specified user
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0


async def update_quiz_index(user_id, index):
    # Create a connection to the database (if it does not exist, it will be created)
    async with aiosqlite.connect(DB_NAME) as db:
        # Insert a new entry or replace it if a user_id already exists.
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        # Save the changes
        await db.commit()


async def create_table():
    # Create a connection to the database (if it does not exist, it will be created)
    async with aiosqlite.connect(DB_NAME) as db:
        # Create a table
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        # Save the changes
        await db.commit()


def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()

    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data="right_answer" if option == right_answer else "wrong_answer")
        )
    
    builder.adjust(1)
    return builder.as_markup()
