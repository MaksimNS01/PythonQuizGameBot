from aiogram import types, F, Router
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.quiz_data import quiz_data
from app.functions import new_quiz, get_quiz_index, update_quiz_index, get_question

router = Router()

# Dictionary for storing user results
user_results = {}

# Handler for the /start command
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Start the game"))
    builder.add(types.KeyboardButton(text="Statistics"))
    await message.answer(f"Welcome to the Python quiz! There are {len(quiz_data)} questions waiting for you, ready to get started?", reply_markup=builder.as_markup(resize_keyboard=True))


# Handler for /quiz
@router.message(F.text=="Start the game")
@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Start again"))
    builder.add(types.KeyboardButton(text="Statistics"))
    await message.answer(f"Let's start the quiz!", reply_markup=builder.as_markup(resize_keyboard=True))
    await new_quiz(message)

    user_id = message.from_user.id
    # Save the initial game state for the user
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
    # Updates the current question number in the database
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer(f"That was the last question. The quiz is over!")


@router.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Retrieve the current question from the user state dictionary
    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']

    await callback.message.answer(f"Incorrect. Correct answer: {quiz_data[current_question_index]['options'][correct_option]}")

    # Updates the current question number in the database
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("That was the last question. The quiz is over!")


# Handler on pressing the “Statistics” button
@router.message(lambda message: message.text == "Statistics")
async def show_statistics(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_results:
        score = user_results[user_id]["score"]
        await message.answer(f"Your last result: {score} out of {len(quiz_data)}")
    else:
        await message.answer("You have not started the game yet. Click 'Start Game' to get started.")

# Handler to press the button “Again”
@router.message(lambda message: message.text == "Start again")
async def restart_game(message: types.Message):
    user_id = message.from_user.id
    # Reset the game state for the user
    user_results[user_id] = {"score": 0, "current_question": 0}
    
    builder = types.ReplyKeyboardMarkup(resize_keyboard=True)
    builder.add(types.KeyboardButton(text="Start again"))
    builder.add(types.KeyboardButton(text="Statistics"))
    await message.answer("Game on again! Good luck!", reply_markup=builder)
