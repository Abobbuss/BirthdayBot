from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
)

from src.constants import message_constants
from src.keyboards import keyboards
from src.models import data
from src.models import  db_functions
from src.states.states import Form


form_router: Router = Router()
data = data.Data()

ADMINS = [1497337003]

@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.start)

    if not db_functions.user_exists(message.from_user.id):
        await message.answer(message_constants.welcome_message)
        await state.set_state(Form.name_registrate)
    else:
        if message.from_user.id in ADMINS:
            await message.answer("Привет админ",
                                 reply_markup=keyboards.main_keyboard)


@form_router.message(Form.name_registrate)
async def process_name(message: Message, state: FSMContext) -> None:
    user_name = message.text.strip()
    user_telegram_name = message.from_user.username
    telegram_id = message.from_user.id
    db_functions.add_user(telegram_id, user_name, user_telegram_name)

    await message.answer("Спасибо, ваше имя сохранено!")
    await state.clear()

    if message.from_user.id in ADMINS:
        await message.answer("Привет админ",
                             reply_markup=keyboards.main_keyboard)


@form_router.message(Command("Отмена"))
@form_router.message(F.text.casefold() == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Отмена",)
    await state.clear()
    await state.set_state(Form.start)

@form_router.message(Command("Создать поздравление"))
@form_router.message(F.text.casefold() == "создать поздравление")
async def create_present(message: Message, state: FSMContext) -> None:
    answer = "Введите имя телеграмм человека, которого будем поздравлять"
    await message.answer(
        answer,
        reply_markup=keyboards.cancel_keyboard,
    )
    await  state.set_state(Form.name_create_present)

@form_router.message(Form.name_create_present)
async def command_start(message: Message, state: FSMContext) -> None:
    person_id = db_functions.get_user_id_by_username(message.text.strip())

    if person_id is None:
        await message.answer(
            "Пользователь не найден, отменяю создание",
            reply_markup=keyboards.main_keyboard
        )
        await state.clear()
        return

    await state.update_data(person_id=person_id)
    fullname = db_functions.get_full_name_by_user_id(person_id)
    await message.answer(f"Будем скидываться для {fullname}\n Введите текст, который необходимо отправить всем пользователям\n"
                         f"Не забудьте прикрепить ссылку на оплату",
                         reply_markup=keyboards.cancel_keyboard)
    await state.set_state(Form.message_to_present)

@form_router.message(Form.message_to_present)
async def command_start(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    person_id = data.get("person_id")
    fullname = db_functions.get_full_name_by_user_id(person_id)
    message_present = message.text.strip()
    await state.update_data(message_present=message_present)
    answer = f"Я отправлю всем пользователям, кроме {fullname} следующее сообщение\n{message_present}\n Для отправки нажмите кнопку отправить"

    await message.answer(answer, reply_markup=keyboards.send_keyboard)
    await state.set_state(Form.wait_send)

@form_router.message(Command("Отправить"))
@form_router.message(F.text.casefold() == "отправить")
async def send_message_present(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    person_id = data.get("person_id")

    print(person_id)
    if person_id is None:
        await message.answer("Ошибка: не удалось получить данные именинника.")
        await state.clear()
        return

    message_text = data.get("message_present")
    print(message_text)
    if not message_text:
        await message.answer("Не удалось получить сообщение поздравление")
        await state.clear()
        return

    users = db_functions.get_all_users_except(person_id)
    print(users)

    for user in users:
        user_id = user['telegram_id']
        try:
            await message.bot.send_message(chat_id=user_id, text=message_text, reply_markup=keyboards.main_keyboard)
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

    await message.answer("Сообщение успешно отправлено всем пользователям.")
    await state.clear()