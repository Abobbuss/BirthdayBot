from aiogram import Router, types, Dispatcher
from aiogram.types import Message

router: Router = Router()


@router.message()
async def process_picture(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.answer('picture')

    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


@Dispatcher.message_handler(commands='start')
async def start(message: types.Message):
    bot_started = False
    your_id = message.from_id
    chat_id = message.chat.id
    your_name = message.from_user.username
    if bot_started:
        await message.answer(f"Еще раз привет, {your_name}, айди {chat_id}!")
    else:
        bot_started = True
        await message.answer(f"Привет, {your_name} айди {chat_id}!")