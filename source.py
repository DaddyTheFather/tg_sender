from telebot import TeleBot
from secret import TOKEN, MY_TG_ID
from colorama import init
from faker import Faker
from random import seed
from googleapiclient.errors import HttpError
from httplib2.error import ServerNotFoundError
from ssl import SSLEOFError
from socket import gaierror


WELCOME_BTNS = ('Разовые заявки 1️⃣',
                'Автоматические заявки ⏳',
                'Авторизация аккаунтов 🔐',
                'Активные аккаунты 🦾',
                'Покупка аккаунтов 💰')
CANCEL_BTN = ('В меню ↩️',)
AUTO_CHOICE = ('Просмотры 👀',
               'Репосты 📢',
               CANCEL_BTN[0])
AUTO_BTNS = ('Добавление 📌',
             'Удаление ❌',
             'Активные 📅',
             CANCEL_BTN[0])
SINGLE_BTNS = ('Активные 📅',
               'Выполненные заявки 📋',
               'Подписки 🔔',
               'Просмотры 👀',
               'Репосты 📢',
               'Удаление ❌',
               'Реакции 😍',
               CANCEL_BTN[0])
BNT_NUM_OPERATION = ('💬 Проверить СМС',
                     '🅾️ Отменить номер')
CREATE_APP_BTN = ('Создать приложение 📱',)

BOT = TeleBot(TOKEN)
REQS_QUEUE = []
ACCOUNTS = []
FINISHED_REQS = []
CUR_REQ = {}
AUTO_SUBS_DICT = {}
AUTO_REPS_DICT = {}
CODE = None
NEW_ROW_TO_ADD = None
NEW_CHAT_ID = MY_TG_ID
FAKER = Faker()
init()
seed()
LONG_SLEEP = 15
SHORT_SLEEP = 1
LINK_FORMAT = r'https://t\.me/'
MAX_MINS = 300
TIME_FORMAT = '%Y-%m-%d %H:%M'
ADMIN_CHAT_ID = MY_TG_ID
MAX_WAIT_CODE = 180
LINK_DECREASE_RATIO = 3
LIMIT_DIALOGS = 1000
MAX_MINS_REQ = 20
SHEET_NAME = 'Тестирование'
EXTRA_SHEET_NAME = 'Дополнительные'
MAX_ACCOUNTS_BUY = 5
URL_SIM = 'https://onlinesim.io/api/'
URL_GET_TARIFFS = URL_SIM + 'getTariffs.php'
URL_BUY = URL_SIM + 'getNum.php'
URL_SMS = URL_SIM + 'getState.php'
URL_CANCEL = URL_SIM + 'setOperationOk.php'
URL_TG = 'https://my.telegram.org/'
URL_API_GET_CODE = URL_TG + 'auth/send_password'
URL_API_LOGIN = URL_TG + 'auth/login'
URL_API_CREATE_APP = URL_TG + 'apps/create'
URL_API_GET_APP = URL_TG + 'apps'
MAX_RECURSION = 25
NUMBER_LAST_FIN = 10
LEFT_CORNER = 'A2'
RIGHT_CORNER = 'H500'
SMALL_RIGHT_CORNER = 'D300'
CONN_ERRORS = (TimeoutError, ServerNotFoundError, gaierror, HttpError, SSLEOFError)
FILE_FINISHED = 'finished.json'
FILE_AUTO_VIEWS = 'auto_views.json'
FILE_AUTO_REPS = 'auto_reps.json'
IMG_PATH = 'random_image.jpg'
