from aiogram import types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup

from .run import bot, dp
from .keyboard import kbm
from config.config import id_admin
from config.message import start
from certificate.edit import edit_cert
from database.database import (
    sql_start,
    sql_stop,
    add_admin,
    add_operator,
    check_adm,
    add_debt,
    add_order,
    check_order,
    delete_order,
    get_addr_order,
    take_op,
    get_sum,
    get_debt,
    update_debt,
    check_adr,
    add_month,
    get_month,
)


async def send_to_adm_su(dp):
    sql_start()
    await bot.send_message(chat_id=id_admin, text="Bot is running")


async def send_to_adm_sd(dp):
    sql_stop()
    await bot.send_message(chat_id=id_admin, text="Bot disable")


@dp.message_handler(Command("start"))
async def command_start(message: Message):
    await message.answer(
        f"Здравствуйте, {message.from_user.first_name}!\n{start}", reply_markup=kbm
    )


@dp.callback_query_handler(text="half_a_month")
async def cb_half_a_month(call: types.CallbackQuery):
    add_month(call.message.chat.id, 0)
    await set_addr(call)


@dp.callback_query_handler(text="month")
async def cb_month(call: types.CallbackQuery):
    add_month(call.message.chat.id, 1)
    await set_addr(call)


class addr(StatesGroup):
    add = State()
    debt = State()


@dp.message_handler(Command("add_debt"))
async def command_add_debt(message: Message):
    if check_adm(message.from_user.id):
        await message.answer("Напишите адрес")
        await addr.add.set()
    else:
        await message.answer("Ошибка!\n")
    pass


@dp.message_handler(state=addr.add)
async def set_adr(message: Message, state: FSMContext):
    await state.update_data(adr=message.text)
    await message.answer("Напишите долг (В случае его отсутствия напишите 0)")
    await addr.next()


@dp.message_handler(state=addr.debt)
async def set_id(message: Message, state: FSMContext):
    await state.update_data(debt=message.text)
    data = await state.get_data()
    add_debt(data["adr"], data["debt"])
    await message.answer("Данные адресса добавлены!")
    await state.finish()


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
    square = State()


@dp.callback_query_handler(text="spravka")
async def set_addr(call: types.CallbackQuery):
    await call.message.answer("Укажите полный адрес помещения")
    await info.address.set()


@dp.message_handler(state=info.address)
async def set_square(message: Message, state: FSMContext):
    await state.update_data(addr=message.text)
    await message.answer("Напишите номер помещения")
    await info.square.set()


@dp.message_handler(state=info.square)
async def get_addr_spr(message: Message, state: FSMContext):
    await state.update_data(sqr=message.text)
    data = await state.get_data()
    if check_adr(data["addr"]):
        rate = 1000
        data = await state.get_data()
        debt = get_debt(data["addr"])
        check_month = get_month(message.from_user.id)
        curr_sum = rate * int(data["sqr"])
        print(curr_sum)
        if check_month != 1:
            curr_sum /= 2
        print(curr_sum)
        if debt < curr_sum:
            await message.answer(f"Сумма оплаты составляет - {curr_sum - debt}")
            add_order(message.from_user.id, curr_sum - debt, data["addr"])
            await state.finish()
            await message.answer(f"Пришлите фотографию чека оплаты")
        else:
            file = edit_cert(data["addr"])
            await message.reply_document(document=open(f"{file}", "rb"))
            await message.answer("Вот ваша справка об отсутствии задолженности.")
    else:
        await state.finish()
        await message.answer(
            f"Не можем найти Ваш адрес в нашей базе данных.\nПроверьте правильность введенных данных и попробуйте ещё раз.",
        )
        await command_start(message)


@dp.message_handler(content_types=["photo"])
async def get_photo(message: Message):
    if check_order(message.from_user.id):
        file_id = message.photo[-1].file_id
        await bot.send_photo(chat_id=take_op(), photo=file_id)
        await message.reply(
            "Отправили Ваш чек на рассмотрение оператору, ожидайте ответа!"
        )
        await op_answer(message.from_user.id, take_op())


async def op_answer(id, id_op):
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
    if ans == "yes":
        await bot.send_message(chat_id=id, text="Ваш чек подтвержден")
        address = get_addr_order(id)
        print(address)
        update_debt(address, get_sum(id))
        file = edit_cert(get_addr_order(id))
        await call.message.reply_document(document=open(f"{file}", "rb"))
        await call.message.answer("Вот ваша справка об отсутствии задолженности.")
    else:
        await negative_ans(id, id_op)
    delete_order(id)


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
