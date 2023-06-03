# from app import *
# import os
# import types
# from dotenv import *
# from TELEGRAM_BOT.BOT import bot, Dispatcher as dp


# load_dotenv()

# @dp.message_handler(commands=['pay'])
# async def start(message: types.Message):
#     await bot.send_invoice(message.chat.id, "Покупка курса", "Описание курса", "invoice",
#                            os.getenv("PAYMENT_TOKEN", "USD", [types.LabeledPrice("Покупка курса", 100 * 100)]))

