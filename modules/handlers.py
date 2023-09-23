from aiogram import types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup

from .run import bot, dp
from config.config import id_admin
from config.message import start
from database.database import (
    sql_start,
    sql_stop,
    add_admin,
    add_operator,
    add_order,
    check_adm,
    check_order,
    delete_order,
    take_op,
    get_sum,
)


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
            "Введите id человека которого хотите сделать администратором"
        )
        await admin.tg_id.set()
    else:
        await message.answer(
            "Ошибка!\nЧтобы добавить админа нужно самому быть администратором."
        )


@dp.message_handler(state=admin.tg_id)
async def set_id(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    data = await state.get_data()
    add_admin(data["id"])
    await message.answer("Администратор добавлен!")
    await state.finish()


# Добавление оператора
class operator(StatesGroup):
    name = State()
    tg_id = State()


@dp.message_handler(Command("add_op"))
async def command_add_adm(message: Message):
    if check_adm(message.from_user.id):
        await message.answer("Введите имя оператора")
        await operator.name.set()

    else:
        await message.answer(
            "Ошибка!\nЧтобы добавить оператора нужно быть администратором."
        )


@dp.message_handler(state=operator.name)
async def set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    print("123")
    await message.answer("Отлично!\nТеперь напишите его id телеграмма")
    await operator.next()


@dp.message_handler(state=operator.tg_id)
async def set_id(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    data = await state.get_data()
    add_operator(data["name"], data["id"])
    await message.answer("Данные оператора добавлены!")
    await state.finish()


# Начало получения справки
class info(StatesGroup):
    address = State()
    date = State()


@dp.message_handler(Command("spravk"))
async def command_spravka(message: Message):
    print("123")
    await message.answer("Укажите адрес помещения")
    await info.address.set()


@dp.message_handler(state=info.address)
async def set_add(message: Message, state: FSMContext):
    await state.update_data(add=message.text)
    await message.answer("Отлично!\nТеперь напишите дату")
    await info.next()


@dp.message_handler(state=info.date)
async def set_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    data = await state.get_data()
    # Формула для расчета суммы оплаты
    sum = 0
    await message.answer(f"Сумма оплаты состовляет - {sum}")
    add_order(message.from_user.id, sum)
    await state.finish()
    await message.answer(f"Пришлите фотографию чека оплаты")


@dp.message_handler(content_types=["photo"])
async def get_photo(message: Message):
    if check_order(message.from_user.id):
        file_id = message.photo[-1].file_id
        await bot.send_photo(chat_id=take_op(), photo=file_id)
        await message.reply(
            "Отправили Ваш чек на рассмотрение оператору, ожидайте ответа!"
        )
        await op_answer(message, message.from_user.id, take_op())


async def op_answer(message: Message, id, id_op):
    button = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text=f"Да", callback_data=f"ans_yes_{id}_{id_op}")
    button2 = InlineKeyboardButton(text=f"Нет", callback_data=f"ans_no_{id}_{id_op}")
    button.row(button1, button2)
    sum = get_sum(id)
    st = f"Чек пришел на сумму {sum}?"
    await bot.send_message(chat_id=id_op, text=st, reply_markup=button)


@dp.callback_query_handler(text_startswith="ans_")
async def process(call: types.CallbackQuery):
    ans = call.data.split("_")[1]
    id = call.data.split("_")[2]
    id_op = call.data.split("_")[3]
    delete_order(id)
    if ans == "yes":
        await bot.send_message(chat_id=id, text="Ваш чек подтвержден")
    else:
        await negative_ans(id, id_op)


class negative(StatesGroup):
    reason = State()
    id = State()


async def negative_ans(id, id_op):
    await bot.send_message(chat_id=id_op, text="Напишите причину отказа")
    negative.id = id
    await negative.reason.set()


@dp.message_handler(state=negative.reason)
async def set_date(message: Message, state: FSMContext):
    await state.update_data(reason=message.text)
    data = await state.get_data()
    temp = data["reason"]
    txt = f"Вам отказал оператор по причине - {temp}"
    await bot.send_message(chat_id=negative.id, text=txt)
    await state.finish()
