import types

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_markup  = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text="Меню", callback_data='menu')
        ]
    ])