from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup

from run import bot, dp
from config import id_admin
from message import start
from database import sql_start, sql_stop, add_admin, check_adm, add_operator


async def send_to_adm_su(dp):
    sql_start()
    await bot.send_message(chat_id=id_admin, text="Bot is running")


async def send_to_adm_sd(dp):
    sql_stop()
    await bot.send_message(chat_id=id_admin, text="Bot disable")


@dp.message_handler(Command("start"))
async def command_start(message: Message):
    await message.answer(f"Здравствуйте, {message.from_user.first_name}!\n{start}")


@dp.message_handler(Command("spravka"))
async def command_spravka(messgae: Message):
    pass


# Добавление администратора
class admin(StatesGroup):
    tg_id = State()


@dp.message_handler(Command("add_adm"))
async def command_add_adm(message: Message):
    if check_adm(message.from_user.id):
        await message.answer(
            "Ошибка!\nЧтобы добавить админа нужно самому быть администратором."
        )
    else:
        await message.answer(
            "Введите id человека которого хотите сделать администратором"
        )
        await admin.id.set()


@dp.message_handler(state=admin.name)
async def set_id(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    data = await state.get_data()
    add_admin(data["id"])
    await message.answer("Администратора добавлены!")
    await state.finish()


# Добавление оператора
class operator(StatesGroup):
    name = State()
    tg_id = State()


@dp.message_handler(Command("add_adm"))
async def command_add_adm(message: Message):
    if check_adm(message.from_user.id):
        await message.answer(
            "Ошибка!\nЧтобы добавить оператора нужно быть администратором."
        )
    else:
        await message.answer("Введите имя оператора")
        await operator.name.set()


@dp.message_handler(state=admin.name)
async def set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.txt)
    await message.answer("Отлично!\nТеперь напишите его id телеграмма")
    await operator.next()


@dp.message_handler(state=admin.tg_id)
async def set_id(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    data = await state.get_data()
    add_operator(data["name"], data["id"])
    await message.answer("Данные оператора добавлены!")
    await state.finish()
