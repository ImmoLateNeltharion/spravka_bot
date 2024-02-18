from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kbm = InlineKeyboardMarkup(row_width=1)
buttonMonth = InlineKeyboardButton(text="Начало месяца", callback_data="half_a_month")
buttonMonth2 = InlineKeyboardButton(text="Середина месяца", callback_data="month")
kbm.add(buttonMonth, buttonMonth2)
