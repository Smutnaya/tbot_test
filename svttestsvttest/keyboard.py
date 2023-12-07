from aiogram import Bot, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Основа для кнопок

info = types.KeyboardButton("Информация")  # Кнопка информации
stats = types.KeyboardButton("Статистика")  # Кнопка статистики
test = types.KeyboardButton("Тест")  # Кнопка теста
razrab = types.KeyboardButton("Разработчик")
user = types.KeyboardButton("Покажи пользователя")
photo = types.KeyboardButton("Фото")
chetnoe = types.KeyboardButton("Четное/нечетное")
uniq = types.KeyboardButton("Уникальные")
upper = types.KeyboardButton("Верхний регистр")
book = types.KeyboardButton("Книга")
fibonachi = types.KeyboardButton("Фибоначчи")
communication = types.KeyboardButton("Общаться с ботом")
start.add(test, stats, info, razrab, user, photo, chetnoe, uniq, upper, book, fibonachi, communication)  # добавляем кнопки в основу бота key

keyboard_ = InlineKeyboardMarkup()
btn1 = InlineKeyboardButton('Info', callback_data='Info-btn')
btn2 = InlineKeyboardButton('Python', callback_data='Python-btn')
keyboard_.add(btn1, btn2)

stats = InlineKeyboardMarkup()
stats.add(InlineKeyboardButton(f'Да', callback_data='join'))
stats.add(InlineKeyboardButton(f'Нет', callback_data='cancle'))

test = InlineKeyboardMarkup()
test.add(InlineKeyboardButton(f'Да', callback_data='tstart'))
test.add(InlineKeyboardButton(f'Нет', callback_data='cancle'))

t1 = InlineKeyboardMarkup(row_width=3)
# t1.add(InlineKeyboardButton(f'1', callback_data='t1_1'))
# t1.add(InlineKeyboardButton(f'2', callback_data='t1_2'))
# t1.add(InlineKeyboardButton(f'3', callback_data='t1_3'))
t1_1 = InlineKeyboardButton(text='1', callback_data="t1_1")
t1_2 = InlineKeyboardButton(text='2', callback_data="t1_2")
t1_3 = InlineKeyboardButton(text='3', callback_data="t1_3")
t1.add(t1_1, t1_2, t1_3)

t2 = InlineKeyboardMarkup(row_width=3)
t2.add(InlineKeyboardButton(f'7', callback_data='t2_1'))
t2.add(InlineKeyboardButton(f'6', callback_data='t2_2'))
t2.add(InlineKeyboardButton(f'4', callback_data='t2_3'))

result = InlineKeyboardMarkup(row_width=3)
result.add(InlineKeyboardButton(f'Результаты', callback_data='result'))

user = InlineKeyboardMarkup(row_width=3)
user.add(InlineKeyboardButton(f'Хочу увидеть id', callback_data='id'))
user.add(InlineKeyboardButton(f'Назад', callback_data='cancle'))
