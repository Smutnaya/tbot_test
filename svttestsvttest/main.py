from aiogram import Bot, types
from aiogram.utils import executor
import asyncio
from aiogram.dispatcher import Dispatcher
from aiogram.types import (ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,
                           InlineKeyboardButton)

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
import config  # импортируем файл config
import keyboard  # импортируем файл config keyboard
import logging  # модуль для вывода информации

storage = MemoryStorage()  # FSM
bot = Bot(token=config.botkey, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)  # Хранилище состояний в оперативной памяти
answers = 0
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO,
                    )


class test(StatesGroup):
    V1 = State()
    V2 = State()
    R = State()
    C = State()


class practic(StatesGroup):
    Chetnoe = State()
    Uniq = State()
    Upper = State()
    Book = State()
    Fibonachi = State()


class book_st(StatesGroup):
    Name = State()
    Author = State()
    Get_name = State()
    Get_author = State()


class Book:
    def __init__(self, author_book, name_book):
        self.author = author_book
        self.name = name_book

    def new_author(self, new_author):
        self.author = new_author

    def new_name(self, new_name):
        self.name = new_name


name = ''
author = ''
book = Book('', '')


@dp.message_handler(Command("start"), state=None)  # задаем название команды start
async def welcome(message):
    joinedFile = open("user.txt", "r")  # Создаем файл в который будем записывать id пользователя
    joinedUsers = set()
    for line in joinedFile:  # цикл в котором проверяем имеется ли такой id в файле user
        joinedUsers.add(line.strip())

    if not str(message.chat.id) in joinedUsers:  # Делаем запись в файл user нового id
        joinedFile = open("user.txt", "a")
        joinedFile.write(str(message.chat.id) + "\n")
        joinedUsers.add(message.chat.id)

    await bot.send_message(message.chat.id, f"Привет, *{message.from_user.first_name},* бот работает",
                           reply_markup=keyboard.start, parse_mode='Markdown')
    # После проверки и записи выводим сообщение с именем пользователя и отображаем кнопки


@dp.message_handler(commands=['rassilka'], state=None)
async def rassilka(message):
    if message.chat.id == config.admin:
        await bot.send_message(message.chat.id, f'*Рассылка началась '
                                                f'\nБот оповестит, когда закончит рассылку*', parse_mode='Markdown')
        receive_user, block_user = 0, 0
        joinedFile = open('user.txt', 'r')
        joinedUser = set()

        for line in joinedFile:
            joinedUser.add(line.strip())
        joinedFile.close()

        for user in joinedUser:
            try:
                await bot.send_photo(user, open('photo.jpg', 'rb'), message.text[message.text.find(' '):])
                receive_user += 1
            except:
                block_user += 1
            await asyncio.sleep(0.4)

        await bot.send_message(message.chat.id, f"*Рассылка была завершена \n*получили сообщение: *{receive_user}*\n"
                                                f"заблокировали бота: *{block_user}*", parse_mode='Markdown')


@dp.message_handler(content_types=['text'])
async def get_message(message):
    if message.text == "Информация":
        await message.answer("Возможно, она есть", reply_markup=keyboard.keyboard_)
    if message.text == "Статистика":
        await message.answer("Посмотреть статистику?", reply_markup=keyboard.stats)
    if message.text == "Разработчик":
        await message.answer("он спит")
    if message.text == "Покажи пользователя":
        await message.answer("Сделайте выбор!", reply_markup=keyboard.user)
    if message.text == "Тест":
        await message.answer("Решаем тест?", reply_markup=keyboard.test)
    if message.text == "Фото":
        await photo(message.chat.id)
    if message.text == "Четное/нечетное":
        await practic.Chetnoe.set()
        await message.answer("Введите число")
    if message.text == "Уникальные":
        await practic.Uniq.set()
        await message.answer("Введите данные через пробел")
    if message.text == "Верхний регистр":
        await practic.Upper.set()
        await message.answer("Введите текст")
    if message.text == "Книга":
        await book_st.Name.set()
        await message.answer("Введите название книги")
    if message.text == "Фибоначчи":
        await practic.Fibonachi.set()
        await message.answer("Введите число")
    if message.text == "Общаться с ботом":
        await test.C.set()
        await message.answer("Напишите боту")


@dp.message_handler(content_types=['text'], state=test.C)
async def upp(message, state: FSMContext):
    text = message.text.lower()
    if 'прив' in text or 'здравст' in text:
        await message.answer("Привет")
    elif 'как дел' in text or 'у тебя дел' in text or 'как ты' in text or 'как вы' in text:
        await message.answer("Все идет стабильно. Как ты сам")
    elif 'у меня' in text or 'мои дел' in text or 'хорош' in text or 'плох' in text or 'норм' in text:
        await message.answer(
            "Ты живой и это прекрасно. нет повода для грусти. могу рассказать анекдот. Если хочешь, напиши - анекдот в чат")
    elif 'анекдот' in text:
        await message.answer("Марк Соломонович... совсем плох и диктует нотариусу завещание:"
                             "— Моей жене, Розе, которая всю жизнь мечтала о бриллиантовом колье и норковой шубе, "
                             "я завещаю свое старое, но очень крепкое, кресло — качалку, в нем хорошо мечтается... ")
    elif 'пока' in text or 'прощай' in text or 'до свидания' in text or 'стоп' in text:
        await message.answer("Ну и прощай!")
        await state.finish()
    else:
        await message.answer("моя не понимать, что ты пишешь")


@dp.message_handler(content_types=['text'], state=book_st.Name)
async def upp(message):
    global name
    name = message.text
    await book_st.Author.set()
    await message.answer("Введите автора книги")


@dp.message_handler(content_types=['text'], state=book_st.Author)
async def upp(message):
    global author
    global book
    author = message.text
    book = Book(name, author)
    await message.answer(f'Книга "{book.name}" создана, автор: {book.author}')
    await message.answer(f'изменим название и автора. Введите новое название')
    await book_st.Get_name.set()


@dp.message_handler(content_types=['text'], state=book_st.Get_name)
async def upp(message):
    global book
    new_name = message.text
    book.new_name(new_name)
    await message.answer(f'Название книги "{name}" изменено на: {book.name}')
    await message.answer(f'Введите название автора для изменения')
    await book_st.Get_author.set()


@dp.message_handler(content_types=['text'], state=book_st.Get_author)
async def upp(message, state: FSMContext):
    global book
    new_author = message.text
    book.new_name(new_author)
    await message.answer(f'Название книги "{author}" изменено на: {book.author}\n'
                         f'->>книга "{book.name}" автор: {book.author}\nсостояние сброшено')
    await state.finish()


@dp.message_handler(content_types=['text'], state=practic.Upper)
async def upp(message, state: FSMContext):
    str = message.text
    await message.answer(f'{str.upper()}\nсостояние сброшено')
    await state.finish()


@dp.message_handler(content_types=['text'], state=practic.Chetnoe)
async def chet(message, state: FSMContext):
    number = int(message.text)
    if number % 2 == 0:
        mes = f"число {number} четное"
    else:
        mes = f"число {number} не четное"
    mes += ". состояние сброшено"
    await state.finish()
    await message.answer(mes)


@dp.message_handler(content_types=['text'], state=practic.Upper)
async def upp(message, state: FSMContext):
    str = message.text
    await message.answer(f'{str.upper()}\nсостояние сброшено')
    await state.finish()


@dp.message_handler(content_types=['text'], state=practic.Uniq)
async def unic(message, state: FSMContext):
    str = message.text.split()
    await message.answer(f'старый список {str}')
    await message.answer(f'новый список {set(str)}\nсостояние сброшено')
    await state.finish()


@dp.message_handler(content_types=['text'], state=practic.Fibonachi)
async def fib(message, state: FSMContext):
    mes = get_fib(int(message.text))

    await message.answer(f' {mes}\nсостояние сброшено')
    await state.finish()


def get_fib(int_):
    if int_ == 0:
        result = 0
    elif int_ in (1, 2):
        result = 1
    else:
        result = get_fib(int_ - 1) + get_fib(int_ - 2)
    return result


async def photo(user_id):
    await bot.send_photo(user_id, open('photo.jpg', 'rb'))


@dp.callback_query_handler(lambda x: x.data == 'Info-btn')
async def topics_btn(callback_query: types.CallbackQuery):
    text = f'инф\nее нет'

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=text)


@dp.callback_query_handler(lambda x: x.data == 'Python-btn')
async def topics_btn2(callback_query: types.CallbackQuery):
    text = f'А Python нужно учить самому'

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=text)


@dp.callback_query_handler(lambda x: x.data == 'id')
async def topics_btn2(callback_query: types.CallbackQuery):
    text = callback_query.from_user.id

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=text)


@dp.callback_query_handler(text_contains='join')
async def join(call: types.CallbackQuery):
    if call.message.chat.id == config.admin:
        d = sum(1 for line in open('user.txt'))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'Статистика: *{d}* человек', parse_mode='Markdown')
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='У вас нет админки', parse_mode='Markdown')


@dp.callback_query_handler(text_contains='cancle')
async def cancle(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Возврат в главное меню', parse_mode='Markdown')


@dp.callback_query_handler(text_contains='tstart')
async def join(call: types.CallbackQuery):
    await test.V1.set()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'1+1=', reply_markup=keyboard.t1)


# @dp.callback_query_handler(text_contains='t1_1')
# @dp.callback_query_handler(text_contains='t1_2')
# @dp.callback_query_handler(text_contains='t1_3')
# @dp.callback_query_handler(text_contains='t2_1')
# @dp.callback_query_handler(text_contains='t2_2')
# @dp.callback_query_handler(text_contains='t2_3')
# @dp.callback_query_handler(text_contains='result')
# async def qr_message(call: types.CallbackQuery):
#     code = call.data
#     global answers
#     if code == "t1_1" or code == "t1_3":
#         await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                     text=f'Ответ не верный, ответ: 2\n\n2+2=',
#                                     reply_markup=keyboard.t2)
#     if code == "t1_2":
#         answers += 1
#         await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                     text=f'Правильно!\n\n2+2=', reply_markup=keyboard.t2)
#
#     if code == "t2_1" or code == "t2_2":
#         await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                     text=f'Ответ не верный, ответ: 4',
#                                     reply_markup=keyboard.result)
#     if code == "t2_3":
#         answers += 1
#         await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                     text=f'Правильно!', reply_markup=keyboard.result)
#     if code == "result":
#         await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                     text=f'Правильных ответов: *{answers}* ({answers * 100 / 2}% правильных ответов)',
#                                     parse_mode='Markdown')


@dp.callback_query_handler(state=test.V1)
async def answer_v1(call: types.CallbackQuery):
    code = call.data
    global answers
    await test.V2.set()
    mess = 'Ответ не верный, ответ: 2'
    if code == "t1_2":
        answers += 1
        mess = 'Правильно!'
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'{mess}\n\n2+2=',
                                reply_markup=keyboard.t2)


@dp.callback_query_handler(state=test.V2)
async def answer_v2(call: types.CallbackQuery):
    code = call.data
    global answers
    await test.R.set()
    mess = 'Ответ не верный, ответ: 4'
    if code == "t2_3":
        answers += 1
        mess = 'Правильно!'
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'{mess}', reply_markup=keyboard.result)


@dp.callback_query_handler(state=test.R)
async def answer_v1(call: types.CallbackQuery, state: FSMContext):
    code = call.data
    global answers
    await state.finish()
    if code == "result":
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'Правильных ответов: *{answers}* ({answers * 100 / 2}% правильных ответов)',
                                    parse_mode='Markdown')
    answers = 0


if __name__ == '__main__':
    print('Бот запущен!')  # Чтобы бот работал всегда с выводом в начале вашего любого текста
    executor.start_polling(dp, skip_updates=True)
