# import all necessary libraries
import telebot
import datetime
import botdatabase as bd
import os
from flask import Flask, request
import logging
from dotenv import load_dotenv

removeKeyboard = telebot.types.ReplyKeyboardRemove()  # to remove keyboard, so user can't press several buttons

""" all questions of the bot """


def q0(message):
    global current_question
    current_question = 0
    bot.send_message(message.from_user.id, 'Введите своё ФИО', reply_markup=removeKeyboard)  # send message to user


def q1(message):
    global current_question, current_column
    current_column = 1
    current_question = 1
    keyboard = telebot.types.InlineKeyboardMarkup()  # create keyboard
    btn1 = telebot.types.InlineKeyboardButton(text="Текущее", callback_data="now")  # create buttons, set
    # callback_data for processing user answer later
    btn2 = telebot.types.InlineKeyboardButton(text="Другое", callback_data="not_now")
    keyboard.row(btn1, btn2)  # add buttons to keyboard
    # send message with the keyboard
    bot.send_message(message.from_user.id, 'Укажите дату и время, когда произошла ситуация', reply_markup=keyboard)


def q2(message):
    global current_question, current_column
    current_column = 2
    current_question = 2
    bot.send_message(message.from_user.id, 'Какое конкретно событие, либо поток мыслей и/или образов, либо воспоминаний'
                                           ' пришли Вам на ум?', reply_markup=removeKeyboard)


def q3(message):
    global current_question, current_column
    current_column = 3
    current_question = 3
    keyboard = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton(text="Да", callback_data="yes_ph")
    btn2 = telebot.types.InlineKeyboardButton(text="Нет", callback_data="no_ph")
    keyboard.row(btn1, btn2)
    bot.send_message(message.from_user.id, 'Были ли у вас неприятные физические ощущения и если да, то какие именно?',
                     reply_markup=keyboard)


def q4(message):
    global current_question
    current_question = 4
    bot.send_message(message.from_user.id, 'Какие мысли и/или представления возникли у Вас?',
                     reply_markup=removeKeyboard)


def q5(message):
    global current_question, current_column
    current_column = 4
    current_question = 5
    bot.send_message(message.from_user.id, 'Насколько Вы были убеждены в их истинности в тот момент, '
                                           'когда они возникали? (в формате от 0 до 100%)', reply_markup=removeKeyboard)


def q6(message):
    global current_question, current_column
    current_column = 5
    current_question = 6
    bot.send_message(message.from_user.id, 'Какие эмоции Вы чувствовали в тот момент и насколько сильно была '
                                           'выражена каждая из них? (Введите в формате «Эмоция 0-100%», если эмоций '
                                           'несколько, перечислите их через запятую после %)',
                     reply_markup=removeKeyboard)


def q7(message):
    global current_question, current_column
    current_column = 6
    current_question = 7
    keyboard = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton(text="Продолжить", callback_data="continue")
    btn2 = telebot.types.InlineKeyboardButton(text="Завершить", callback_data="end")
    keyboard.row(btn1, btn2)
    bot.send_message(message.from_user.id, 'Желаете продолжить работу с бланком РДМ или Вы еще не владеете навыками для'
                                           ' дальнейшей проработки автоматических мыслей?', reply_markup=keyboard)


def q8(message):
    global current_question, current_column
    current_column = 6
    current_question = 8
    keyboard = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton(text="Да", callback_data="yes_cog")
    btn2 = telebot.types.InlineKeyboardButton(text="Нет", callback_data="no_cog")
    keyboard.row(btn1, btn2)
    bot.send_message(message.from_user.id, 'Можете ли указать когнитивное искажение, допущенное Вами?',
                     reply_markup=keyboard)


def q9(message):
    global current_question, current_column
    current_column = 6
    current_question = 9
    bot.send_message(message.from_user.id, 'Укажите допущенное искажение', reply_markup=removeKeyboard)


def q10(message):
    global current_question, current_column
    current_column = 7
    current_question = 10
    keyboard = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton(text="Да", callback_data="yes_adap")
    btn2 = telebot.types.InlineKeyboardButton(text="Нет", callback_data="no_adap")
    keyboard.row(btn1, btn2)
    bot.send_message(message.from_user.id, 'Используя вопросы для формулировки адаптивного ответа, сформулируйте '
                                           'ответ на автоматическую мысль. Ответьте на максимально возможное '
                                           'количество вопросов или на такое количество, чтобы почувствовать '
                                           'улучшение состояния. Вывести список вопросов?', reply_markup=keyboard)


def q11(message):
    questions = "1. Каковы доказательства истинности этой автоматической мысли?\n2. Каковы доказательства " \
                "обратного?\n3. Существует пи альтернативное объяснение? \n4. Что самое худшее может произойти?\n5. " \
                "Смогу ли я пережить это?\n6. Каков самый лучший исход?\n7. Каков самый реалистичный вариант развития " \
                "событий?\n8. Каковы последствия моей убежденности в истинности этой автоматической мысли?\n9. Что " \
                "произойдет, если я изменю свое мышление?\n10. Что я могу сделать?\n11. Если бы в подобной ситуации " \
                "оказался мой близкий и у него были подобные мысли, что я мог бы сказать ему? "
    global current_question, current_column
    current_column = 7
    current_question = 11
    bot.send_message(message.from_user.id, 'Введите свои ответы и насколько Вы уверены в каждом из них, с указанием '
                                           'номера вопроса в формате: «1. Текст ответа 0-100%». Каждый следующий '
                                           'ответ начинайте с новой строки.', reply_markup=removeKeyboard)
    bot.send_message(message.from_user.id, questions, reply_markup=removeKeyboard)


def q12(message):
    global current_question, current_column
    current_column = 8
    current_question = 12
    bot.send_message(message.from_user.id, 'Насколько теперь Вы убеждены в истинности автоматической мысли? Укажите '
                                           'какие эмоции Вы сейчас испытываете и их интенсивность. Введите в формате:'
                                           ' «0-100%, эмоция 0-100%', reply_markup=removeKeyboard)


def q13(message):
    global current_question, current_column
    current_column = 9
    current_question = 13
    bot.send_message(message.from_user.id, 'Каковы будут Ваши дальнейшие действия (или что Вы сделали в данной '
                                           'ситуации)?', reply_markup=removeKeyboard)


def end_of_session(message):
    global current_question
    current_question = 14
    bot.send_message(message.from_user.id, 'Запись внесена в бланк. До встречи!', reply_markup=removeKeyboard)


client_id = 'PERSONAL CLIENT ID'
client_sheet = 'PERSONAL CLIENT SHEET'

# array of bot questions
arr = [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, end_of_session]
current_question = 0  # variable for number of current question, so user can choose a question that they want to answer
# variables current_row and current_column are needed to feel database
user_id, user_name, current_row, current_column, text = None, None, -1, -1, ''
bot = telebot.TeleBot('BOT TOKEN')


@bot.message_handler(commands=['start'])  # function to start session
def start_session(message):
    global user_id, current_row
    user_id = message.from_user.id
    if bd.check_user(user_id) == 'none':  # check if user is in database; if not, ask for a name and add datasheet
        global current_question
        current_row = 2
        current_question = 0
        arr[0](message)
    else:  # if user is already in the database, just start the session with the first question
        global user_name
        user_name = bd.check_user(user_id)
        current_row = bd.get_row(user_name)
        arr[1](message)


@bot.message_handler(commands=['cogn'])  # process a command
def cognitive_list(message):
    global current_question
    current_question = -1
    cogn_list = "Когнитивные искажения (ошибки мышления):\n1.Полярное мышление (черно-белое мышление) – только две " \
                "категории в оценки событий: хорошо или плохо;\n2.Катастрофизация – предсказание будущего " \
                "исключительно негативно, без учета других, более вероятных исходов\n3.Обесценивание позитивного " \
                "\n4.Эмоциональное обоснование – убеждение, что нечто должно быть правдой потому что вы так " \
                "«чувствуете», игнорирую или обесцениваете факты реальности;\n5.Навешивание ярлыков – наделение " \
                "безусловными, глобальными характеристиками себя или окружающих, без учета, что оценка всех фактов " \
                "может с большей вероятностью привести к менее негативным исходам;\n6.Магнификация/минимизация – " \
                "оценка событий с преувеличением негативного и/или преуменьшением позитивного;\n7.Мысленный фильтр (" \
                "туннельное мышление) – безосновательный учет только негативных аспектов ситуации, без оценки полной " \
                "картины происходящего;\n8.«Чтение мыслей» - уверенность человека, что он знает мысли окружающих, " \
                "или наоборот;\n9.Сверхгенерализация – формулирование обобщающих негативных выводов, выходящих далеко " \
                "за пределы текущей ситуации;\n10.Персонализация – представление о себе, как о главной причине " \
                "негативного поведения других людей. Уверенность, что ошибки человека находятся в центре внимания " \
                "окружающих;\n11.Должествование – мышления по принципу «я должен…» "
    bot.send_message(message.from_user.id, cogn_list, reply_markup=removeKeyboard)


@bot.message_handler(commands=['question'])
def questions_list(message):
    global current_question
    current_question = -1
    q_list = "1.Укажите дату и время, когда произошла ситуация \n2.Какое конкретно событие, либо поток мыслей и/или " \
             "образов, либо воспоминаний пришли Вам на ум? \n3.Были ли вас неприятные физические ощущения и если " \
             "да, то какие именно? \n4.Какие мысли и/или представления возникли у Вас?\n5.Насколько Вы были убеждены " \
             "в их истинности в тот момент, когда они возникали? (в формате от 0 до 100%) \n6.Какие эмоции Вы " \
             "чувствовали в тот момент и насколько сильно они была выражена каждая из них? (Введите в формате «Эмоция " \
             "0-100%», если эмоций несколько перечислите их через запятую после %) \n7.Желаете продолжить работу с " \
             "бланком РДМ или Вы еще не владеете навыками для дальнейшей проработки автоматических мыслей?\n8.Можете " \
             "ли указать когнитивное искажение, допущенное Вами? \n9.Используя вопросы для формулировки адаптивного " \
             "ответа, сформулируйте ответ на автоматическую мысль. Ответьте на максимально возможное количество " \
             "вопросов или на такое количество, чтобы почувствовать улучшение состояния. Вывести список вопросов? " \
             "\n10.Введите свои ответы и насколько Вы уверены в каждом из них, с указанием номера вопроса в формате: " \
             "«1. Текст ответа 0-100%». Каждый следующий ответ начинайте с новой строки. \n11.Насколько теперь Вы " \
             "убеждены в истинности автоматической мысли? Укажите какие эмоции Вы сейчас испытываете и их " \
             "интенсивность. Введите в формате: «0-100%, эмоция 0-100%» \n12.Каковы будут Ваши дальнейшие действия (" \
             "или что Вы сделали в данной ситуации)? "
    bot.send_message(message.from_user.id, q_list, reply_markup=removeKeyboard)


@bot.message_handler(commands=['emotions'])
def emotions_list(message):
    global current_question
    current_question = -1
    em_list = "1.Злость (обида, недовольство, досада);\n2.Страх (тревога, беспокойство, нервозность);\n3.Грусть (" \
              "подавленность, отчаяние, боль);\n4.Стыд (неловкость, смущение);\n5.Вина (сожаление, " \
              "раскаяние);\n6.Любовь (интерес, вдохновение, привязанность);\n7.Радость (удовлетворение, возбуждение, " \
              "гордость). "
    bot.send_message(message.from_user.id, em_list, reply_markup=removeKeyboard)


@bot.message_handler(commands=['next'])  # process a command to send next question
def next_question(message):
    global current_question
    current_question += 1
    arr[current_question](message)


@bot.message_handler(commands=['back'])  # process a command to return to the previous question
def previous_question(message):
    global current_question
    if current_question != 0 and current_question <= 14:
        current_question -= 1
        arr[current_question](message)
    elif current_question == 0:
        start_session(message)
    else:
        bot.send_message(message.from_user.id, "Невозможно вернуться назад. Пожалуйста, введите номер вопроса или "
                                               "начните ссесию сначала.", reply_markup=removeKeyboard)


@bot.message_handler(commands=['number'])  # a command for choosing a number of question
def num_of_question(message):
    global current_question
    current_question = 15
    try:
        num = int(message.text.replace('/number', ''))
        if 0 < num < 14:
            arr[num](message)
        else:
            bot.send_message(message.from_user.id, "Нет такого вопроса. Введите номер вопроса от 1 до 13.",
                             reply_markup=removeKeyboard)
            questions_list(message)
    except ValueError:  # exception for wrong input
        bot.send_message(message.from_user.id, "Введите в формате «/number номер вопроса» (например, «/number 3»)",
                         reply_markup=removeKeyboard)


@bot.message_handler(commands=['last'])
def next_section(message):
    q8(message)


@bot.message_handler(commands=['columns'])  # a command to choose a column to fill in
def columns(message):
    global current_question
    current_question = -1
    keyboard = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton(text="Дата и время", callback_data="date")
    btn2 = telebot.types.InlineKeyboardButton(text="Ситуация", callback_data="situation")
    btn3 = telebot.types.InlineKeyboardButton(text="Физиологический ответ", callback_data="physiological")
    btn4 = telebot.types.InlineKeyboardButton(text="Автоматические мысли", callback_data="automatic")
    btn5 = telebot.types.InlineKeyboardButton(text="Эмоции", callback_data="emotions")
    btn6 = telebot.types.InlineKeyboardButton(text="Когнитивное искажение", callback_data="cognitive")
    btn7 = telebot.types.InlineKeyboardButton(text="Адаптивный ответ", callback_data="adaptive")
    btn8 = telebot.types.InlineKeyboardButton(text="Результат", callback_data="result")
    btn9 = telebot.types.InlineKeyboardButton(text="Действие", callback_data="action")
    keyboard.add(btn1, btn2)
    keyboard.add(btn3)
    keyboard.add(btn4)
    keyboard.add(btn5)
    keyboard.add(btn6)
    keyboard.add(btn7)
    keyboard.add(btn8, btn9)
    bot.send_message(message.from_user.id, "Выберете название столбца, который хотите заполнить.",
                     reply_markup=keyboard)


# functions to process button pressing


@bot.callback_query_handler(func=lambda
        call: call.data == 'date' or call.data == 'situation' or call.data == 'physiological' or call.data == 'automatic' or call.data == 'emotions' or call.data == 'cognitive' or call.data == 'adaptive' or call.data == 'result' or call.data == 'action')
def chose_column(call):
    if call.data == 'date':
        q1(call)
    elif call.data == 'situation':
        q2(call)
    elif call.data == 'physiological':
        q3(call)
    elif call.data == 'automatic':
        q4(call)
    elif call.data == 'emotions':
        q6(call)
    elif call.data == 'cognitive':
        q8(call)
    elif call.data == 'adaptive':
        q11(call)
    elif call.data == 'result':
        q12(call)
    elif call.data == 'action':
        q13(call)


@bot.callback_query_handler(func=lambda call: call.data == 'now' or call.data == 'not_now')
def set_data(call):  # function to set date
    global current_question, user_name, current_row, current_column
    if call.data == 'now':
        today = datetime.date.today()
        bd.add_date(user_name, today.strftime('%d.%m.%Y'))
        current_question = 2
        arr[current_question](call)
    else:
        current_question = 1
        bot.send_message(call.message.chat.id, "Введите нужную дату в формате дд.мм.гг (например, 23.03.2021)",
                         reply_markup=removeKeyboard)


@bot.message_handler(content_types=['text'])  # process text send by user and fill needed columns
def dialogue(message):
    global current_question, user_name, user_id, current_row, current_column
    if current_question == 0:
        check_id = message.from_user.id
        if bd.check_user(check_id) == 'none':  # if there is no such user in the database
            user_name = message.text
            bd.create_worksheet(check_id, user_name)  # create their personal sheet
    elif current_question == 1:
        global current_row
        current_row = bd.add_date(user_name, message.text)
    elif current_question == 15:
        try:
            num = int(message.text)
            arr[num](message)
            return
        except ValueError:
            num_of_question(message)
            return
    elif current_question <= -1:
        return
    elif current_question == 4 or current_question == 5:
        global text
        if current_question == 4:
            text = message.text + '\n'
        else:
            text += message.text
        bd.add_info(user_name, current_row, current_column, text)
    else:
        bd.add_info(user_name, current_row, current_column, message.text)
    try:
        current_question += 1
        arr[current_question](message)
    except IndexError:
        bot.send_message(message.from_user.id, "Сессия завершена. Воспользуйтесь одной из команд, чтобы изменить "
                                               "ответы или начать новую сессию.", reply_markup=removeKeyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'yes_ph' or call.data == "no_ph")
def physical(call):
    global current_question
    if call.data == 'yes_ph':
        current_question = 3
        bot.send_message(call.message.chat.id, 'Введите текст', reply_markup=removeKeyboard)
    elif call.data == "no_ph":
        global user_name, current_row
        bd.add_info(user_name, current_row, 3, ' - ')
        current_question = 4
        arr[current_question](call)


@bot.callback_query_handler(func=lambda call: call.data == "continue" or call.data == "end")
def next_part(call):
    global current_question, current_column, current_row, user_name
    if call.data == 'end':
        for i in range(current_column, 10):
            bd.add_info(user_name, current_row, i, '-')
        current_question = 14
        end_of_session(call)
    elif call.data == 'continue':
        current_question = 8
        arr[current_question](call)


@bot.callback_query_handler(func=lambda call: call.data == 'yes_cog' or call.data == 'no_cog')
def cognitive(call):
    global current_question, user_name, current_row, current_column
    if call.data == 'yes_cog':
        current_question = 9
    if call.data == 'no_cog':
        bd.add_info(user_name, current_row, current_column, '-')
        current_question = 10
    arr[current_question](call)


@bot.callback_query_handler(func=lambda call: call.data == 'yes_adap' or call.data == 'no_adap')
def adaptive(call):
    global current_question, user_name, current_row, current_column
    if call.data == 'yes_adap':
        current_question = 11
    if call.data == 'no_adap':
        bd.add_info(user_name, current_row, current_column, '-')
        current_question = 12
    arr[current_question](call)


# set webhook for our bot so it never dies on HEROKU
if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)
    load_dotenv('.env')
    server = Flask(__name__)


    @server.route("/", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200


    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url="URL to your bot on heroku")
        return "?", 200


    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    # if there is no environment variable HEROKU, then bot is running from local computer
    # delete webhook for sure and run with usual polling
    bot.remove_webhook()
    bot.polling(none_stop=True)


