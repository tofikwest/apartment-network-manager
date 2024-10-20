import asyncio
import logging
import os
import re
from aiogram.types.keyboard_button import KeyboardButton
from typing_extensions import Text
from decouple import config
from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import (
    MenuButtonCommands,
    BotCommand,
    Message,
    CallbackQuery,
    MenuButtonWebApp,
    WebAppInfo,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from messages import START_USER_ALREADY_IN_SYSTEM, WELCOME_MESSAGE


router = Router()

APARTMENTS = ["1205 Surf ave.", "800 E 14 street"]

user_data = {}

def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="📋 Правила проживания"))
    builder.add(KeyboardButton(text="🗑️ Куда выбрасывать мусор"))
    builder.add(KeyboardButton(text="📅 Кто дежурит на этой неделе?"))
    builder.add(KeyboardButton(text="ℹ️ Моя информация"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

@router.message(Command(commands=['start']))
async def start(msg: Message, bot: Bot):
   user_id = msg.chat.id

   if user_id in user_data:
       await msg.answer(
                   f"С возвращением, {user_data[user_id]['name']}!",
                   reply_markup=get_main_keyboard())
       return

   builder = InlineKeyboardBuilder()

   for apt in APARTMENTS: builder.button(text=apt, callback_data=f"apt:{apt}")

   builder.adjust(2)

   await bot.send_message(
        chat_id=msg.chat.id,
        text=WELCOME_MESSAGE,
        parse_mode="HTML",
        reply_markup=builder.as_markup()
    )

@router.message(Command(commands=['info']))
async def info(msg: Message, bot: Bot):
    user_id = msg.chat.id
    print('asd')
    await bot.send_message(
        chat_id=user_id,
        text=str(user_data)
    )

@router.callback_query(F.data.startswith("apt:"))
async def process_apartment_choice(callback: CallbackQuery):
    print(callback.data);

    user_id = callback.from_user.id
    apartment = callback.data.split(":")[1]
    user_data[user_id] = {"apartment": apartment}

    await callback.message.edit_text(f"Вы выбрали {apartment}. Теперь, пожалуйста, напишите ваше имя.")
    user_data[user_id]["waiting_for_name"] = True

@router.message(F.text)
async def process_name(msg: Message):
    user_id = msg.chat.id

    if user_id in user_data and user_data[user_id].get('waiting_for_name'):
        name = msg.text
        user_data[user_id]['name'] = name
        user_data[user_id]['waiting_for_name'] = False

        await msg.answer(
            f"Спасибо, {name}! Ваши данные:\nКвартира: {user_data[user_id]['apartment']}\nИмя: {name}",
            reply_markup=get_main_keyboard()
        )

    else:
        await msg.answer('Пожалуйста, используйте команду /start для начала работы с ботом.')
