from aiogram.types import ReplyKeyboardMarkup,InlineKeyboardMarkup,InlineKeyboardButton



main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Каталог').add('Корзина').add('Контакты')


main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Каталог').add('Корзина').add('Контакты').add('Админ-панель')


admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Добавить товар').add('Удалить товар').add('Сделать расслыку')


catalog_list =InlineKeyboardMarkup(row_width=2)
catalog_list.add(InlineKeyboardButton(text='Курс',callback_data='Курс'),
                 InlineKeyboardButton(text='Погружение',callback_data='Погружение'),
                 InlineKeyboardButton(text='Женский круг',callback_data='Женский круг'))

cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add("Отмена")