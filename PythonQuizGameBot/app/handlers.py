from aiogram import types, F, Router
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.quiz_data import quiz_data
from app.functions import new_quiz, get_quiz_index, update_quiz_index, get_question

router = Router()

# Словарь для хранения результатов пользователей
user_results = {}

# Хэндлер на команду /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    builder.add(types.KeyboardButton(text="Статистика"))
    await message.answer(f"Добро пожаловать в квиз по Python! Вас ждёт {len(quiz_data)} вопросов, готовы начать?", reply_markup=builder.as_markup(resize_keyboard=True))


# Хэндлер на команду /quiz
@router.message(F.text=="Начать игру")
@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать заново"))
    builder.add(types.KeyboardButton(text="Статистика"))
    await message.answer(f"Давайте начнем квиз!", reply_markup=builder.as_markup(resize_keyboard=True))
    await new_quiz(message)

    user_id = message.from_user.id
    # Сохраняем начальное состояние игры для пользователя
    user_results[user_id] = {"score": 0, "current_question": 0}
    

@router.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):

    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    user_id = callback.from_user.id
    user_results[user_id]["score"] += 1

    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']
    await callback.message.answer(f"{quiz_data[current_question_index]['options'][correct_option]}. Верно!")
    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        # await callback.message.answer(f"Это был последний вопрос. Квиз завершен! Вы набрали {user_results[user_id]["score"]}/{len(quiz_data)}")
        await callback.message.answer(f"Это был последний вопрос. Квиз завершен!")


@router.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']

    await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")


# Хэндлер на нажатие кнопки "Статистика"
@router.message(lambda message: message.text == "Статистика")
async def show_statistics(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_results:
        score = user_results[user_id]["score"]
        await message.answer(f"Ваш последний результат: {score} из {len(quiz_data)}")
    else:
        await message.answer("Вы еще не начинали игру. Нажмите 'Начать игру', чтобы начать.")

# Хэндлер на нажатие кнопки "Заново"
@router.message(lambda message: message.text == "Заново")
async def restart_game(message: types.Message):
    user_id = message.from_user.id
    # Сбрасываем состояние игры для пользователя
    user_results[user_id] = {"score": 0, "current_question": 0}
    
    builder = types.ReplyKeyboardMarkup(resize_keyboard=True)
    builder.add(types.KeyboardButton(text="Заново"))
    builder.add(types.KeyboardButton(text="Статистика"))
    await message.answer("Игра началась заново! Удачи!", reply_markup=builder)