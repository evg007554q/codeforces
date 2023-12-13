import math
from pydoc import html
from typing import Optional

from aiogram import types, F, Router, flags
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder


from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton
from magic_filter import F

from func import db_manager


class DateTask():
    task_level = 0
    ftext = ''
    find_task_text = ''
    topic = ''
    task_topic = []
    task_list = []
    task_page = 0
    tpage = 0

    db=db_manager.DBManager()

    # for tn in range(29):
    #     nt = { 'id': tn, 'name': f'{find_task_text}  №{tn}', 'tags': f'tema task','solvedCount': 'решений шт.', 'rating': 'рейтинг/сложность' }
    #     task_list.append(nt)
    #
    # for tn in range(21):
    #         nt = {'name': f'{ftext} №{tn}', 'id': tn}
    #         task_topic.append(nt)


def update_list_task_topic():
    """обновляет список категорий"""
    if DateTask.task_level == 2:
        rating1=2600
        rating2=9999
    elif DateTask.task_level == 2:
        rating1=1600
        rating2=2600
    else:
        rating1=0
        rating2=1600

    ftext = DateTask.ftext
    task_topic = []
    qw = f"SELECT distinct problem_tags.tag "\
         "  FROM problem_tags "\
         "      inner join problem "\
         f"	        on problem_tags.id_problem = problem.id_problem "\
         f"where problem.rating>={rating1} and problem.rating<{rating2} and problem_tags.tag like '%{ftext}%'"
    data_qw = DateTask.db.qw(qw)
    for tag in data_qw:
        nt = {'name': tag[0], 'id': 0}
        task_topic.append(nt)

    # for tn in range(21):
    #     nt = {'name': f'{ftext} №{tn}', 'id': tn}
    #     task_topic.append(nt)
    DateTask.task_topic = task_topic

def update_list_task():
    """обновялет список задач"""
    if DateTask.task_level == 2:
        rating1=2600
        rating2=9999
    elif DateTask.task_level == 2:
        rating1=1600
        rating2=2600
    else:
        rating1=0
        rating2=1600

    find_task_text = DateTask.find_task_text
    topic = DateTask.topic
    # print('topic',topic)
    task_list = []
    qw = f"SELECT distinct problem.id_problem, name, solvedcount , url, rating" \
         "  FROM problem_tags " \
         "      inner join problem " \
         f"	        on problem_tags.id_problem = problem.id_problem " \
         f"where problem.rating>={rating1} and problem.rating<{rating2} and problem_tags.tag = '{topic}' and problem.name like '%{find_task_text}%'"
    # print(qw)
    data_qw = DateTask.db.qw(qw)
    for tn in data_qw:
        # print('tn',tn)
        nt = {'id': tn[0], 'name': tn[1], 'tags': topic, 'solvedCount': tn[2],'url': tn[3],'rating': tn[4]}
        # print(nt)
        task_list.append(nt)


    # for tn in range(3):
    #     nt = {'id': tn, 'name': f'{find_task_text}  №{tn}', 'tags': f'tema task', 'solvedCount': 'решений шт.',
    #           'rating': 'рейтинг/сложность'}
    #
    #     task_list.append(nt)
    DateTask.task_list = task_list

def get_keyboard_fab():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🥉 Легкие задачи ", callback_data=NumbersCallbackFactory(action="level", value=0, text="Легкие задачи")
    )
    builder.button(
        text="🥈 Обычные задачи", callback_data=NumbersCallbackFactory(action="level", value=1, text="Обычные задачи")
    )
    builder.button(
        text="🥇 Сложные задачи", callback_data=NumbersCallbackFactory(action="level", value=2, text="Сложные задачи")
    )

    return builder.as_markup()


def get_keyboard_topic():
    task_topic = DateTask.task_topic
    il=DateTask.tpage

    coiunItem = math.ceil(len(task_topic)/9)-1

    lastpage = il==coiunItem
    # notlastpage = il > 0

    sp_size = 8
    sp_list_task_topic = [task_topic[i:i+sp_size] for i in range(0, len(task_topic), sp_size)]
    if len(sp_list_task_topic) == 0:
        textfind='Нет таких категорий. Тык сюда 📥 поищим еще'
    else:
        textfind = "🔎 Поиск категории"

    builder = InlineKeyboardBuilder()
    for item in  sp_list_task_topic[il]:
        builder.button(
            text=item['name'], callback_data=NumbersCallbackFactory(action="task_topic", value=item['id'], text=item['name'])
        )
    builder.adjust(4)

    builder.row()

    # print('stn',il)

    if not il == 0:
        builder.button(
            text="⏪ Назад", callback_data=NumbersCallbackFactory(action="navigator", value=-1, text="-1")
        )

    builder.button(
        text=textfind, callback_data=NumbersCallbackFactory(action="find_topic", value=0, text="find")
    )
    if not lastpage:
        builder.button(
            text="⏩ Вперед", callback_data=NumbersCallbackFactory(action="navigator", value=1, text="+1")
        )
    builder.adjust(4)
    return builder.as_markup()

def get_keyboard_task():
    # print('topic', topic.text)
    task_list = DateTask.task_list
    il = DateTask.task_page

    coiunItem = math.ceil(len(task_list) / 10) - 1

    lastpage = il == coiunItem
    # notlastpage = il > 0

    sp_size = 10
    sp_list_task = [task_list[i:i + sp_size] for i in range(0, len(task_list), sp_size)]
    if len(sp_list_task) == 0:
        textfind = 'Нет таких задач. Тык сюда 📥 поищим еще'
    else:
        textfind = "Уточните поиск 🔎. "

    builder = InlineKeyboardBuilder()
    # for item in sp_list_task[il]:
    #     builder.button(
    #         text=item['name'],
    #         callback_data=NumbersCallbackFactory(action="task_topic", value=item['id'], text=item['name'])
    #     )
    builder.adjust(4)

    builder.row()

    # print('stn', il)

    if not il == 0:
        builder.button(
            text="⏪ Назад", callback_data=NumbersCallbackFactory(action="navigator_task", value=-1, text="-1")
        )

    builder.button(
        text=textfind, callback_data=NumbersCallbackFactory(action="find_task", value=0, text="find")
    )
    builder.button(
        text="Изменить категорию задач", callback_data=NumbersCallbackFactory(action="back_find_topic", value=0, text="find")
    )
    if not lastpage:
        builder.button(
            text="⏩ Вперед", callback_data=NumbersCallbackFactory(action="navigator_task", value=1, text="+1")
        )
    builder.adjust(4)
    return builder.as_markup()

def get_task():
    task_list = DateTask.task_list
    il = DateTask.task_page
    sp_size = 10
    sp_list_task = [task_list[i:i + sp_size] for i in range(0, len(task_list), sp_size)]

    # print('len',len(task_list))
    if len(task_list) == 0:
        tt = f'Не найдено задач выбранной сложности в категории {DateTask.topic}-{DateTask.find_task_text}'

    else:
        text_task = []
        for item in sp_list_task[il]:
            text_task.append(f"<b>{item['name']}</b>")
            text_task.append(f"<b>категория:</b> {item['tags']}")
            text_task.append(f"<b>решений:</b> {item['solvedCount']}")
            text_task.append(f"<b>сложность:</b> {item['rating']}")
            text_task.append(f"<b>URL:</b> <a href='{item['url']}'>тык</a>")
            text_task.append('')
        text_task.append('!!!')
        tt = '\n'.join(text_task)

    return tt



class Gen(StatesGroup):
    level = State()
    # findtopic = State()
    topic = State()
    task = State()

class NumbersCallbackFactory(CallbackData, prefix='fabnum'):
    action: str #имя активности
    value: Optional[int] = None #id в базе
    text: str #имя

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    """Старт"""
    text_rating = """Привет! Я бот из Кодовых сил. Я подберу для тебя задачи! Выберете уровень сложности"""

    await msg.answer(text_rating, reply_markup=get_keyboard_fab())
    await state.set_state(Gen.level)


@router.callback_query(Gen.level, NumbersCallbackFactory.filter(F.action == "level") )
async def level_selection(clbck: CallbackQuery, callback_data: NumbersCallbackFactory, state:  FSMContext):
    """обработка выбора уровня"""
    DateTask.task_level = callback_data.value
    update_list_task_topic()
    await state.update_data(level=callback_data)
    await state.set_state(Gen.topic)
    # print("easy_tasks", Gen.level)
    await clbck.answer(text=f'Выбран уровень: {callback_data.text} ')
    await clbck.message.answer(text=f'Уровень: {callback_data.text} ')

    await clbck.message.answer('По какой категории будем смотреть задачи', reply_markup=get_keyboard_topic())

# @router.message(
@router.callback_query(Gen.topic, NumbersCallbackFactory.filter(F.action == "navigator") )
async def listing_topic(clbck: CallbackQuery, callback_data: NumbersCallbackFactory, state:  FSMContext):
    """листаем список категорий +-8"""
    DateTask.tpage = DateTask.tpage + callback_data.value
    tt=f'  --- страница {DateTask.tpage} --- списка категорий'
    await clbck.message.answer(text=tt, reply_markup=get_keyboard_topic())

@router.callback_query(Gen.topic, NumbersCallbackFactory.filter(F.action == "find_topic") )
async def text_find_topic(clbck: CallbackQuery,  state:  FSMContext):
    """просим ввоести текст для поиска категории"""
    #Ждем ввода текста кагории
    # await state.set_state(Gen.findtopic)
    await clbck.message.answer(text='Какие темы задач вам интересны просто напишите это')

# не буду добавлять состояние ввод текста поиска
# любой текст в состоянии topic расценивается как текст для поиска категории
# @router.message(Gen.findtopic)
@router.message(Gen.topic)
@flags.chat_action("typing")
async def listing_topic(msg: Message, state:  FSMContext):
    """обновляем список категорий по слову поиска, выводим категории после поиска"""
    DateTask.ftext = msg.text
    DateTask.tpage=0;
    update_list_task_topic()

    # await state.update_data(findtopic=DateTask.ftext )

    await msg.answer('Нашли такие категории: ', reply_markup=get_keyboard_topic())

@router.callback_query(Gen.topic, NumbersCallbackFactory.filter(F.action == "task_topic") )
async def select_topic(clbck: CallbackQuery, callback_data: NumbersCallbackFactory, state:  FSMContext):
    """обработка выбора категории"""
    await state.update_data(topic=callback_data)
    # перевод в состояние задачи
    await state.set_state(Gen.task)

    data_task_topic = await state.get_data()
    topic = data_task_topic['topic']
    DateTask.topic = callback_data.text

    update_list_task()

    # print(get_task())

    tt=f'  --- задачи из категории {callback_data.text} --- '
    await clbck.message.answer(text=tt, parse_mode="HTML")
    await clbck.message.answer(text=get_task(),parse_mode="HTML")

    tt = f'  --- страница {DateTask.task_page} --- списка задач по {topic.text}'
    await clbck.message.answer(text=tt, reply_markup=get_keyboard_task())

@router.callback_query(Gen.task, NumbersCallbackFactory.filter(F.action == "navigator_task") )
async def navigator_task(clbck: CallbackQuery, callback_data: NumbersCallbackFactory, state:  FSMContext):
    """листаем задачи +-10"""
    data_task_topic = await state.get_data()
    topic=data_task_topic['topic']
    DateTask.task_page = DateTask.task_page + callback_data.value


    await clbck.message.answer(text=get_task(), parse_mode="HTML")

    tt=f'  --- страница {DateTask.task_page} --- списка задач по #{topic.text}#{DateTask.find_task_text}'
    await clbck.message.answer(text=tt, reply_markup=get_keyboard_task())

@router.callback_query(Gen.task, NumbersCallbackFactory.filter(F.action == "back_find_topic") )
async def back_find_topic(clbck: CallbackQuery, callback_data: NumbersCallbackFactory, state:  FSMContext):
    """назад к выбору категории"""
    DateTask.task_page = 0
    DateTask.tpage = 0
    await state.set_state(Gen.topic)
    await clbck.message.answer('По какой категории будем смотреть задачи', reply_markup=get_keyboard_topic())

@router.callback_query(Gen.task, NumbersCallbackFactory.filter(F.action == "find_task") )
async def find_task(clbck: CallbackQuery,  state:  FSMContext):
    """просим ввести текст для поиска"""
    #Ждем ввода текста
    # await state.set_state(Gen.findtopic)
    await clbck.message.answer(text='Уточните какую задачу искать')

# любой текст в состоянии task расценивается как текст для поиска задачи
@router.message(Gen.task)
@flags.chat_action("typing")
async def listing_topic(msg: Message, state:  FSMContext):
    """обновляем список задач по слову поиска, выводим что нашли """
    DateTask.find_task_text = msg.text
    DateTask.task_page = 0
    update_list_task()

    data_task_topic = await state.get_data()
    topic = data_task_topic['topic']

    await msg.answer(text=get_task(), parse_mode="HTML")

    tt = f'  --- страница {DateTask.task_page} --- списка задач по #{topic.text} #{DateTask.find_task_text}'

    await msg.answer(tt, reply_markup=get_keyboard_task())

# @router.message(F.text == "Сложность")
# @router.message(F.text == "сложность")
# @router.message(F.text == "Меню")
# async def menu(msg: Message):
#     await msg.answer('Главное меню', reply_markup=tg_menu.menu1)
#     print(Gen.level)
#

# import collections
#
# import os
# from pathlib import Path
# from dotenv import load_dotenv
# from aiogram import Bot, Dispatcher, types, executor
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher.filters.state import State, StatesGroup
#
# from telegram import Bot
#
#
#
# BASE_DIR = Path(__file__).resolve().parent.parent
#
# load_dotenv(BASE_DIR / '.env')
#
#
#
#
# class DialogBot:
#     """Bot - для подбора задачь"""
#
#     def __init__(self):
#         self.bot = Bot(token=os.getenv('BOT_TG_TOKEN'), parse_mode=types.ParseMode.HTML )
#         # Инициализация хранилища состояний
#         self.storage = MemoryStorage()
#         # Инициализация диспетчера
#         self.dp = Dispatcher(self, storage=self.storage)
#
# class MyStates(StatesGroup):
#     # Определение состояния "name"
#     name = State()
#     # Определение состояния "age"
#     age = State()
#     # Определение состояния "email"
#     email = State()
#
# @dp.message_handler(commands=['start'])
# async def cmd_start(message: types.Message):
#     # При начале обработки команды "start" переводим бота в состояние "name"
#     await MyStates.name.set()
#     await message.reply("Привет! Напиши свое имя.")

