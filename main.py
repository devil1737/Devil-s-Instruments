import asyncio

from config import *
import datetime
from aiogram import F, Bot, Dispatcher, types
from aiogram.filters.command import Command
from randomphraze import *
from random import choice

offset = datetime.timezone(datetime.timedelta(hours=3))

def user_start_working(user_id):
    current_datetime = datetime.datetime.now(offset)
    print(current_datetime.time())
    USERS[user_id] = [True, current_datetime]
    with open(f'users_log/{user_id}.log', 'a+', encoding='utf8') as file:
        file.write(f'Начал работу [{current_datetime}]\n')
        file.flush()

def user_end_working(user_id):
    last_time = USERS[user_id][1]
    last_time_d = [last_time.hour, last_time.day]
    current_datetime = datetime.datetime.now(offset)
    current_datetime_d = [current_datetime.hour, current_datetime.day]
    counted = current_datetime_d[0] - last_time_d[0]
    belyga = [counted]
    if counted >= 2:
        counted = 'Very Good'
    elif counted == 1:
        counted = 'So-so'
    elif counted == 0:
        counted = 'Bad'
    elif counted < 0:
        counted = 'Error'
    USERS[user_id] = [False, current_datetime]
    with open(f'users_log/{user_id}.log', 'a+', encoding='utf8') as file:
        file.write(f'Закончил работу ({belyga[0]}) [{current_datetime}]\n')
        file.flush()
    belyga.append(counted)
    return belyga

bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def start(msg: types.Message):
    kb = [
        [types.KeyboardButton(text="Начать работу")],
        [types.KeyboardButton(text="Закончить работу")],
        [types.KeyboardButton(text='Коммент в логах')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await msg.answer('Выберите действие:', reply_markup=keyboard)

@dp.message(F.text == 'Начать работу')
async def start_job(msg: types.Message):
    if msg.from_user.id in USERS and USERS[msg.from_user.id][0]:
        await msg.answer('Работа уже начата')
    else:
        user_start_working(msg.from_user.id)
        await msg.answer('✔️ Вы успешно начали работу!')

@dp.message(F.text == 'Закончить работу')
async def end_job(msg: types.Message):
    if msg.from_user.id in USERS and not USERS[msg.from_user.id][0]:
        await msg.answer('Прежде чем закончить работу - начните её (тварь, ёбань, чмо)')
    else:
        count = user_end_working(msg.from_user.id)
        print(count)
        await msg.answer('✔️ ' + choice(PHRAZES[count[1]]).format(count[0]))

@dp.message()
async def comment(msg: types.Message):
    current_datetime = datetime.datetime.now(offset)
    with open(f'users_log/{msg.from_user.id}.log', 'a+', encoding='utf8') as file:
        file.write(msg.text + ' [' + str(current_datetime) + ']\n')
        file.flush()
    await msg.answer('Бот не ебёт чё ты щас только что высрал, но отправил это в логи')

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())