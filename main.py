
import telebot

from log import log


bot = telebot.TeleBot('')

buttons = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons.row(telebot.types.KeyboardButton('Комплексные'),
            telebot.types.KeyboardButton('Рациональные'),
            telebot.types.KeyboardButton('Еще не определился'))
buttons2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons2.row(telebot.types.KeyboardButton('+'),
            telebot.types.KeyboardButton('-'),
            telebot.types.KeyboardButton('*'),
            telebot.types.KeyboardButton('/'))

@bot.message_handler()
def hello(msg: telebot.types.Message):
    bot.send_message(chat_id=msg.from_user.id, 
                    text='Здравствуйте\n Выберите режим работы калькулятора',
                    reply_markup=buttons)
    bot.register_next_step_handler(msg, answer)

def answer(msg: telebot.types.Message):
    log(msg)
    # if msg.text == 'Комплексные':
    #     bot.register_next_step_handler(msg, complex_counter)
    #     bot.send_message(chat_id=msg.from_user.id, 
    #                     text='Введите два комплексных числа', 
    #                     reply_markup=telebot.types.ReplyKeyboardRemove())
    if msg.text == 'Рациональные':
        bot.register_next_step_handler(msg, take_first_number)
        bot.send_message(chat_id=msg.from_user.id, 
                        text='Введите первое число', 
                        reply_markup=telebot.types.ReplyKeyboardRemove())
    elif msg.text == 'Еще не определился':
        bot.register_next_step_handler(msg, answer)
        bot.send_message(chat_id=msg.from_user.id, text='Возвращайтесь, когда определитесь')
    else:
        bot.register_next_step_handler(msg, answer)
        bot.send_message(chat_id=msg.from_user.id, text='Используйте кнопки')

        bot.send_message(chat_id=msg.from_user.id, text='Выберите режим работы калькулятора', reply_markup=buttons)

def take_first_number(msg: telebot.types.Message):
    log(msg)
    if msg.text.isdigit():
        num1 = float(msg.text)
        bot.send_message(chat_id=msg.from_user.id, text='Введите второе число')
        bot.register_next_step_handler(message=msg, callback=take_second_number, num1=num1)
    else:
        bot.send_message(chat_id=msg.from_user.id, text='Введите первое число')
 
 
def take_second_number(msg: telebot.types.Message, num1):
    log(msg)
    if msg.text.isdigit():
        num2 = float(msg.text)
        bot.send_message(chat_id=msg.from_user.id, text='Введите операцию', reply_markup=buttons2)
        bot.register_next_step_handler(message=msg, callback=rational_counter, num1=num1, num2=num2)
        
    else:
        bot.send_message(chat_id=msg.from_user.id, text='Введите второе число')
 
 
def rational_counter(msg: telebot.types.Message, num1, num2):
    log(msg)
    if msg.text in {'+', '-', '*', '/'}:
        if msg.text == '+':
            sum_ = num1 + num2
        elif msg.text == '-':
            sum_ = num1 - num2
        elif msg.text == '*':
            sum_ = num1 * num2
        else:
            sum_ = num1 / num2
        bot.send_message(chat_id=msg.from_user.id, text=f'{sum_}')
    else:
        bot.send_message(chat_id=msg.from_user.id, text='Введите корректный оператор', reply_markup=buttons2)
        bot.register_next_step_handler(message=msg, callback=rational_counter, num1=num1, num2=num2)
 
 
bot.polling()
