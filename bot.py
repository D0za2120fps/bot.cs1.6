# config.py

# Telegram
BOT_TOKEN = "8254854603:AAGGGOls7O-oXn5HtJ1QrY7DIxtbPzVTbCI"  # токен от BotFather
ADMIN_ID = 1734795991           # ваш числовой Telegram ID

# Оплата
CARD_NUMBER = "2202 2081 7115 4504"

# Привилегии и цены
PRIVILEGES = {
    'VIP': {'flags': 'ts', '7': 59, '30': 129, 'навсегда': 199},
    'Админ': {'flags': 'cdefijmts', '7': 149, '30': 299, 'навсегда': 499},
    'Супер Админ': {'flags': 'cdefijmtso', '7': 199, '30': 399, 'навсегда': 699},
    'Элитный Админ': {'flags': 'cdefijmtsop', '7': 249, '30': 499, 'навсегда': 899},
    'Вампир': {'flags': 'cdefijmtsopq', '7': 299, '30': 599, 'навсегда': 999},
    'Босс': {'flags': 'cdefijmtsopqn', '7': 399, '30': 799, 'навсегда': 1499},
    'Смотритель': {'flags': 'bcdefijmtsopqn', '7': 499, '30': 999, 'навсегда': 1999}
}

# FTP
FTP_HOST = '193.19.119.166'
FTP_USER = 'meHSHyRgqk'
FTP_PASS = 'maPInL8bGll0fmWnUoqp'
USERS_INI_PATH = 'addons\\amxmodx\\configs\\users.ini'

# RCON
RCON_HOST = '193.19.119.166'
RCON_PORT = 8888
RCON_PASS = 'R2013dkwdm3'
