import telebot
from time import time

def log(msg: telebot.types.Message):
    file = open('db.txt', 'a')
    file.write(f'{msg.from_user.id}, {msg.text}, {time}\n')
    file.close