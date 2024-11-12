from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отмена"),
        ]
    ],
    resize_keyboard=True
)

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Создать поздравление"),
        ]
    ],
    resize_keyboard=True
)

send_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text="Отправить"),
        KeyboardButton(text="Отмена")
        ]
    ],
    resize_keyboard=True
)