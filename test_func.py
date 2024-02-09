from aiogram import types
from initial import bot


class TestClass:
    async def func_1(self, msg: types.Message):
        await msg.reply("Привет!\nНапиши мне что-нибудь!")

    async def func_2(self, msg: types.Message):
        await msg.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")

    async def func_3(self, msg: types.Message):
        await bot.send_message(msg.from_user.id, msg.text)