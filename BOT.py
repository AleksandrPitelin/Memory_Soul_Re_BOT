from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from Memory_Soul_Re_BOT.app import database as db, keyboards as kb
from random import choice
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher import FSMContext


storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv("TOKEN"))
pay = Bot(os.getenv('PAYMENT_TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)


async def on_startup(_):
    await db.db_start()
    print('Бот успешно запущен')



class NewOrder(StatesGroup):
    type = State()
    name = State()
    desc = State()
    price = State()
    photo = State()



@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await db.cmd_start_db(message.from_user.id)
    await message.answer_sticker('CAACAgIAAxkBAAPjZEJRG_UCPLPRfxw8VDH_hfdV7S4AAtUFAAL6C7YIBh9vLn4bP0ovBA')
    await message.answer(f"{message.from_user.first_name},Приветствую Вас у меня на канале!", reply_markup=kb.main)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы зарегистрировались как администратор!', reply_markup=kb.main_admin)


"""Проверка ID юзера"""
@dp.message_handler(commands=['id'])
async def cmd_id(message: types.Message):
    await message.answer(f'{message.from_user.id}')



"""Стикер в приветствие"""
@dp.message_handler(content_types=['sticker'])
async def check_sticker(message: types.Message):
    await message.answer(message.sticker.file_id)


@dp.message_handler(text='Каталог')
async def catalog(message: types.Message):
    await message.answer(f'Каталог пуст', reply_markup=kb.catalog_list)


@dp.message_handler(text='Корзина')
async def cart(message: types.Message):
    await message.answer(f'Корзина пуста')


@dp.message_handler(text='Контакты')
async def contacts(message: types.Message):
    await message.answer(f"Мой YouTube: https://www.youtube.com/@user-nd4uj8gt9p")



@dp.message_handler(text='Админ-панель')
async def contacts(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы вошли в админ-панель', reply_markup=kb.admin_panel)
    else:
        await message.reply("Я вас не понимаю")


@dp.message_handler(text='Добавить товар')
async def add_item(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await NewOrder.type.set()
        await message.answer(f"Выберите тип товара", reply_markup=kb.catalog_list)
    else:
        await message.reply("Я вас не понимаю")

@dp.callback_query_handler(state=NewOrder.type)
async def add_item_type(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = call.data
    await call.message.answer(f"Напишите название товара", reply_markup=kb.cancel)
    await NewOrder.next()


@dp.message_handler(state=NewOrder.name)
async def add_item_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer(f"Напишите описание товара")
    await NewOrder.next()


@dp.message_handler(state=NewOrder.desc)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await message.answer(f"Напишите цену товара")
    await NewOrder.next()


@dp.message_handler(state=NewOrder.price)
async def add_item_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer(f"Отправьте фото товара")
    await NewOrder.next()


@dp.message_handler(lambda message: not message.photo, state=NewOrder.photo)
async def add_item_photo_check(message: types.Message):
    await message.answer("Это не фотография!")


@dp.message_handler(content_types=['photo'],state=NewOrder.photo)
async def add_item_photo(message: types.Message, state: FSMContext):
    async with state.proxy()as data:
        data['photo'] = message.photo[0].file_id
    await db.add_item(state)
    await message.answer('Товар успешно создан!', reply_markup=kb.admin_panel)
    await state.finish()


# -----------   ОПЛАТА!!! ------------- #


@dp.message_handler(commands=['pay'])
async def start(message: types.Message):
    await bot.send_invoice(message.chat.id, "Покупка курса", "Описание курса", "invoice",
                           os.getenv("PAYMENT_TOKEN", "USD", [types.LabeledPrice("Покупка курса", 100 * 100)]))


# -----------------------------------#

async def answer(message: types.Message):
    await message.reply("Я вас не понимаю")



#-----------------------------------#

"""Хвалилка присланных фото"""

random_answer = ('Какая красивая фотография!',
'Очень хороший ракурс!',
'Цвета на этой фотографии просто потрясающие!',
'Я люблю, как эта фотография передает настроение!',
'Очень интересная композиция!',
'Я бы повесил эту фотографию на стене!',
'Очень талантливый фотограф!',
'Фотография просто изумительная!',
'Как хорошо, что у вас есть такой талант!'
)
@dp.message_handler(content_types=['photo'])
async def get_user_photo(message):
    await bot.send_message(message.chat.id, choice(random_answer))


@dp.callback_query_handler()
async def callback_query_keyboard(callback_query: types.CallbackQuery):
    if callback_query.data == "Курс":
        await bot.send_message(chat_id=callback_query.from_user.id, text="Вы выбрали курс")
    elif callback_query.data == "Погружение":
        await bot.send_message(chat_id=callback_query.from_user.id, text="Погружение")
    elif callback_query.data == "Женский круг":
        await bot.send_message(chat_id=callback_query.from_user.id, text="Женский круг")



if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)


