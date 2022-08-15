import pandas as pd
import telebot
import json
from telebot import types

bot = telebot.TeleBot('')  # вставить токен


def write_json_data(jsoni):
    with open('agro_data.json', 'w', encoding='utf-8') as f:
        json.dump(jsoni, f)


def get_menu_keyboard():
    markup = types.ReplyKeyboardMarkup()
    markup.row_width = 1
    btn1 = types.KeyboardButton("Курсы по моим интересам")
    btn2 = types.KeyboardButton("Поиск вуза специально для меня")
    btn3 = types.KeyboardButton('Мои интересы')
    btn4 = types.KeyboardButton("Найти подходящую стажировку")
    btn5 = types.KeyboardButton('Пройти тест заново')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    json_data = json.load(open('agro_data.json', encoding='utf-8'))
    id = str(message.from_user.id)
    if id in list(json_data['users'].keys()):  # не забываем, что айдишник по умолчанию - инт!
        if message.text == "Начать тест" and json_data['users'][id]['curr_status'] == "new":  # Первый вопрос
            json_data['users'][id]['testInfo'] = {'stage': 0, 'ended': False, "is_versatile": 1,
                                                  'curr_stage_info': {'used': [], 'not_used': [], 'ended': False},
                                                  "full_test_body": {}}
            json_data['users'][id]["isTestRightnow"] = True
            markup = types.ReplyKeyboardMarkup(row_width=2)
            itembtn1 = types.KeyboardButton('Да')
            itembtn2 = types.KeyboardButton('Нет')
            markup.add(itembtn1, itembtn2)
            bot.send_message(message.chat.id, "Ты считаешь себя разносторонним человеком?", reply_markup=markup)
            write_json_data(json_data)
            return
        if 'testInfo' in json_data['users'][id]:  # Тело теста
            print(json_data['users'][id]['favorite'])
            if json_data['users'][id]['testInfo']['stage'] == 0:  # Ответ на первый вопрос
                if message.text == 'Да':
                    json_data['users'][id]['testInfo']["is_versatile"] = 'ver'
                    json_data['users'][id]['testInfo']['full_test_body'] = \
                        json.load(open("test_content.json", encoding='utf-8'))['not_ver']
                    json_data['users'][id]['testInfo']['stage'] = 1
                    answers = json_data['users'][id]['testInfo']['full_test_body']["1"]
                    markup = types.ReplyKeyboardMarkup()
                    markup.row_width = 1
                    btn1 = types.KeyboardButton(answers[0][0])
                    btn2 = types.KeyboardButton(answers[1][0])
                    btn3 = types.KeyboardButton(answers[2][0])
                    btn4 = types.KeyboardButton(answers[3][0])
                    markup.add(btn1, btn2, btn3, btn4)
                    bot.send_message(message.chat.id, "Правила просты: выбирай то, что больше всего нравится",
                                     reply_markup=markup)
                    write_json_data(json_data)
                elif message.text == "Нет":
                    json_data['users'][id]['testInfo']["is_versatile"] = 'not_ver'
                    json_data['users'][id]['testInfo']['full_test_body'] = \
                        json.load(open("test_content.json", encoding='utf-8'))['ver']
                    json_data['users'][id]['testInfo']['stage'] = 1
                    answers = json_data['users'][id]['testInfo']['full_test_body']["1"]
                    markup = types.ReplyKeyboardMarkup()
                    markup.row_width = 1
                    btn1 = types.KeyboardButton(answers[0][0])
                    btn2 = types.KeyboardButton(answers[1][0])
                    btn3 = types.KeyboardButton(answers[2][0])
                    btn4 = types.KeyboardButton(answers[3][0])
                    markup.add(btn1, btn2, btn3, btn4)
                    bot.send_message(message.chat.id,
                                     "Правила просты: Выбирай то, что больше всего нравится",
                                     reply_markup=markup)
                    write_json_data(json_data)
                else:
                    markup = types.ReplyKeyboardMarkup(row_width=2)
                    itembtn1 = types.KeyboardButton('Да')
                    itembtn2 = types.KeyboardButton('Нет')
                    markup.add(itembtn1, itembtn2)
                    bot.send_message(message.chat.id, "Так ты считаешь себя разносторонним человеком? Да или нет?",
                                     reply_markup=markup)

            elif json_data['users'][id]['testInfo']['stage'] == 1:
                answers = json_data['users'][id]['testInfo']['full_test_body']["1"]
                if message.text in [i[0] for i in answers]:
                    json_data['users'][id]['testInfo']['stage'] = 2
                    answers = json_data['users'][id]['testInfo']['full_test_body']["2"]
                    json_data['users'][id]['favorite'].append(message.text)
                    markup = types.ReplyKeyboardMarkup()
                    markup.row_width = 1
                    btn1 = types.KeyboardButton(answers[0][0])
                    btn2 = types.KeyboardButton(answers[1][0])
                    btn3 = types.KeyboardButton(answers[2][0])
                    btn4 = types.KeyboardButton(answers[3][0])
                    btn5 = types.KeyboardButton('Шаг назад')
                    markup.add(btn1, btn2, btn3, btn4, btn5)
                    bot.send_message(message.chat.id, "Правила просты: выбирай то, что больше всего нравится",
                                     reply_markup=markup)
                    write_json_data(json_data)
                elif message.text == 'Шаг  назад':
                    json_data['users'][id]['testInfo']['stage'] = 4
                    answers = json_data['users'][id]['testInfo']['full_test_body']["4"]
                    del json_data['users'][id]['favorite'][-1]
                    markup = types.ReplyKeyboardMarkup()
                    markup.row_width = 1
                    btn1 = types.KeyboardButton(answers[0][0])
                    btn2 = types.KeyboardButton(answers[1][0])
                    btn3 = types.KeyboardButton(answers[2][0])
                    btn4 = types.KeyboardButton(answers[3][0])
                    btn5 = types.KeyboardButton('Шаг назад')
                    markup.add(btn1, btn2, btn3, btn4, btn5)
                    bot.send_message(message.chat.id,
                                     "Откатились! Правила просты: выбирай то, что больше всего нравится",
                                     reply_markup=markup)
                    write_json_data(json_data)
                else:
                    markup = types.ReplyKeyboardMarkup()
                    markup.row_width = 1
                    btn1 = types.KeyboardButton(answers[0][0])
                    btn2 = types.KeyboardButton(answers[1][0])
                    btn3 = types.KeyboardButton(answers[2][0])
                    btn4 = types.KeyboardButton(answers[3][0])
                    markup.add(btn1, btn2, btn3, btn4)
                    bot.send_message(message.chat.id,
                                     "Правила просты: выбирай то, что больше всего нравится.",
                                     reply_markup=markup)
            elif json_data['users'][id]['testInfo']['stage'] == 2:
                answers = json_data['users'][id]['testInfo']['full_test_body']["2"]
                if message.text in [i[0] for i in answers]:
                    json_data['users'][id]['testInfo']['stage'] = 3
                    answers = json_data['users'][id]['testInfo']['full_test_body']["3"]
                    json_data['users'][id]['favorite'].append(message.text)
                    markup = types.ReplyKeyboardMarkup()
                    markup.row_width = 1
                    btn1 = types.KeyboardButton(answers[0][0])
                    btn2 = types.KeyboardButton(answers[1][0])
                    btn3 = types.KeyboardButton(answers[2][0])
                    btn4 = types.KeyboardButton(answers[3][0])
                    btn5 = types.KeyboardButton('Шаг назад')
                    markup.add(btn1, btn2, btn3, btn4, btn5)
                    bot.send_message(message.chat.id, "Правила просты: выбирай то, что больше всего нравится",
                                     reply_markup=markup)
                    write_json_data(json_data)
                elif message.text == 'Шаг назад':
                    json_data['users'][id]['testInfo']['stage'] = 1
                    answers = json_data['users'][id]['testInfo']['full_test_body']["1"]
                    del json_data['users'][id]['favorite'][-1]
                    markup = types.ReplyKeyboardMarkup()
                    markup.row_width = 1
                    btn1 = types.KeyboardButton(answers[0][0])
                    btn2 = types.KeyboardButton(answers[1][0])
                    btn3 = types.KeyboardButton(answers[2][0])
                    btn4 = types.KeyboardButton(answers[3][0])
                    markup.add(btn1, btn2, btn3, btn4)
                    bot.send_message(message.chat.id,
                                     "Откатились! Правила просты: выбирай то, что больше всего нравится",
                                     reply_markup=markup)
                    write_json_data(json_data)
                else:
                    markup = types.ReplyKeyboardMarkup()
                    markup.row_width = 1
                    btn1 = types.KeyboardButton(answers[0][0])
                    btn2 = types.KeyboardButton(answers[1][0])
                    btn3 = types.KeyboardButton(answers[2][0])
                    btn4 = types.KeyboardButton(answers[3][0])
                    btn5 = types.KeyboardButton('Шаг назад')
                    markup.add(btn1, btn2, btn3, btn4, btn5)
                    bot.send_message(message.chat.id,
                                     "Правила просты: выбирай то, что больше всего нравится.",
                                     reply_markup=markup)
            elif json_data['users'][id]['testInfo']['stage'] == 3:
                answers = json_data['users'][id]['testInfo']['full_test_body']["3"]
                if message.text in [i[0] for i in answers]:
                    json_data['users'][id]['testInfo']['stage'] = 4
                    answers = json_data['users'][id]['testInfo']['full_test_body']["4"]
                    json_data['users'][id]['favorite'].append(message.text)
                    markup = types.ReplyKeyboardMarkup()
                    markup.row_width = 1
                    btn1 = types.KeyboardButton(answers[0][0])
                    btn2 = types.KeyboardButton(answers[1][0])
                    btn3 = types.KeyboardButton(answers[2][0])
                    btn4 = types.KeyboardButton(answers[3][0])
                    btn5 = types.KeyboardButton('Шаг назад')
                    markup.add(btn1, btn2, btn3, btn4, btn5)
                    bot.send_message(message.chat.id, "Правила просты: выбирай то, что больше всего нравится",
                                     reply_markup=markup)
                    write_json_data(json_data)
                elif message.text == 'Шаг назад':
                    json_data['users'][id]['testInfo']['stage'] = 2
                    answers = json_data['users'][id]['testInfo']['full_test_body']["2"]
                    del json_data['users'][id]['favorite'][-1]
                    markup = types.ReplyKeyboardMarkup()
                    markup.row_width = 1
                    btn1 = types.KeyboardButton(answers[0][0])
                    btn2 = types.KeyboardButton(answers[1][0])
                    btn3 = types.KeyboardButton(answers[2][0])
                    btn4 = types.KeyboardButton(answers[3][0])
                    btn5 = types.KeyboardButton('Шаг назад')
                    markup.add(btn1, btn2, btn3, btn4, btn5)
                    bot.send_message(message.chat.id,
                                     "Откатились! Правила просты: выбирай то, что больше всего нравится",
                                     reply_markup=markup)
                    write_json_data(json_data)
                else:
                    markup = types.ReplyKeyboardMarkup()
                    markup.row_width = 1
                    btn1 = types.KeyboardButton(answers[0][0])
                    btn2 = types.KeyboardButton(answers[1][0])
                    btn3 = types.KeyboardButton(answers[2][0])
                    btn4 = types.KeyboardButton(answers[3][0])
                    btn5 = types.KeyboardButton('Шаг назад')
                    markup.add(btn1, btn2, btn3, btn4, btn5)
                    bot.send_message(message.chat.id,
                                     "Правила просты: выбирай то, что больше всего нравится.",
                                     reply_markup=markup)
            elif json_data['users'][id]['testInfo']['stage'] == 4:
                answers = json_data['users'][id]['testInfo']['full_test_body']["4"]
                if message.text in [i[0] for i in answers]:
                    json_data['users'][id]['testInfo']['stage'] = 5
                    answers = json_data['users'][id]['testInfo']['full_test_body']["5"]
                    json_data['users'][id]['favorite'].append(message.text)
                    markup = types.ReplyKeyboardMarkup()
                    markup.row_width = 1
                    btn1 = types.KeyboardButton(answers[0][0])
                    btn2 = types.KeyboardButton(answers[1][0])
                    btn3 = types.KeyboardButton(answers[2][0])
                    btn4 = types.KeyboardButton(answers[3][0])
                    btn5 = types.KeyboardButton('Шаг назад')
                    markup.add(btn1, btn2, btn3, btn4, btn5)
                    bot.send_message(message.chat.id, "Правила просты: выбирай то, что больше всего нравится",
                                     reply_markup=markup)
                    write_json_data(json_data)
                elif message.text == 'Шаг назад':
                    json_data['users'][id]['testInfo']['stage'] = 3
                    answers = json_data['users'][id]['testInfo']['full_test_body']["3"]
                    del json_data['users'][id]['favorite'][-1]
                    markup = types.ReplyKeyboardMarkup()
                    markup.row_width = 1
                    btn1 = types.KeyboardButton(answers[0][0])
                    btn2 = types.KeyboardButton(answers[1][0])
                    btn3 = types.KeyboardButton(answers[2][0])
                    btn4 = types.KeyboardButton(answers[3][0])
                    btn5 = types.KeyboardButton('Шаг назад')
                    markup.add(btn1, btn2, btn3, btn4, btn5)
                    bot.send_message(message.chat.id,
                                     "Откатились! Правила просты: выбирай то, что больше всего нравится",
                                     reply_markup=markup)
                    write_json_data(json_data)
                else:
                    markup = types.ReplyKeyboardMarkup()
                    markup.row_width = 1
                    btn1 = types.KeyboardButton(answers[0][0])
                    btn2 = types.KeyboardButton(answers[1][0])
                    btn3 = types.KeyboardButton(answers[2][0])
                    btn4 = types.KeyboardButton(answers[3][0])
                    btn5 = types.KeyboardButton('Шаг назад')
                    markup.add(btn1, btn2, btn3, btn4, btn5)
                    bot.send_message(message.chat.id,
                                     "Правила просты: выбирай то, что больше всего нравится.",
                                     reply_markup=markup)
            elif json_data['users'][id]['testInfo']['stage'] == 5:
                answers = json_data['users'][id]['testInfo']['full_test_body']["5"]
                if message.text in [i[0] for i in answers]:
                    del json_data['users'][id]['testInfo']
                    json_data['users'][id]['favorite'].append(message.text)
                    markup = types.ReplyKeyboardMarkup()
                    markup.row_width = 1
                    btn1 = types.KeyboardButton("Вернуться в меню")
                    markup.add(btn1)
                    bot.send_message(message.chat.id, "Тест окончен, в меню появилась куча интересного!",
                                     reply_markup=markup)
                    json_data['users'][id]['isNew'] = False
                    json_data['users'][id]['curr_status'] = 'in_menu'
                    write_json_data(json_data)
                elif message.text == 'Шаг назад':
                    json_data['users'][id]['testInfo']['stage'] = 4
                    answers = json_data['users'][id]['testInfo']['full_test_body']["4"]
                    del json_data['users'][id]['favorite'][-1]
                    markup = types.ReplyKeyboardMarkup()
                    markup.row_width = 1
                    btn1 = types.KeyboardButton(answers[0][0])
                    btn2 = types.KeyboardButton(answers[1][0])
                    btn3 = types.KeyboardButton(answers[2][0])
                    btn4 = types.KeyboardButton(answers[3][0])
                    btn5 = types.KeyboardButton('Шаг назад')
                    markup.add(btn1, btn2, btn3, btn4, btn5)
                    bot.send_message(message.chat.id,
                                     "Откатились! Правила просты: выбирай то, что больше всего нравится",
                                     reply_markup=markup)
                    write_json_data(json_data)
                else:
                    markup = types.ReplyKeyboardMarkup()
                    markup.row_width = 1
                    btn1 = types.KeyboardButton(answers[0][0])
                    btn2 = types.KeyboardButton(answers[1][0])
                    btn3 = types.KeyboardButton(answers[2][0])
                    btn4 = types.KeyboardButton(answers[3][0])
                    btn5 = types.KeyboardButton('Шаг назад')
                    markup.add(btn1, btn2, btn3, btn4, btn5)
                    bot.send_message(message.chat.id,
                                     "Правила просты: выбирай то, что больше всего нравится.",
                                     reply_markup=markup)
        else:
            if json_data['users'][id]['curr_status'] == "new":
                pass
            if json_data['users'][id]['curr_status'] == "in_menu":
                if message.text == "Мои интересы":
                    specs = json_data['users'][id]['favorite']
                    bot.send_message(message.chat.id,
                                     f"Последний тест показал, что тебе интересны следующие специальности:\n\n\u2022{specs[0]}\n\n\u2022{specs[1]}\n\n\u2022{specs[2]}\n\n\u2022{specs[3]}\n\n\u2022{specs[4]}",
                                     )
                if message.text == "Пройти тест заново":
                    del json_data['users'][id]
                    write_json_data(json_data)
                    markup = types.ReplyKeyboardMarkup()
                    markup.row_width = 1
                    btn1 = types.KeyboardButton("Начать тест")
                    markup.add(btn1)
                    bot.send_message(message.chat.id, "Данные удалены", reply_markup=markup
                                     )
                elif message.text == 'Курсы по моим интересам':
                    json_data['users'][id]['curr_status'] = 'looking for courses'
                    json_data['users'][id]['stage'] = 1
                    write_json_data(json_data)
                    markup = types.ReplyKeyboardMarkup()
                    markup.row_width = 1
                    answers = json_data['users'][id]['favorite']
                    btn1 = types.KeyboardButton(answers[0])
                    btn2 = types.KeyboardButton(answers[1])
                    btn3 = types.KeyboardButton(answers[2])
                    btn4 = types.KeyboardButton(answers[3])
                    btn5 = types.KeyboardButton(answers[4])
                    markup.add(btn1, btn2, btn3, btn4, btn5)
                    bot.send_message(message.chat.id, "Курсы в какой области ты ищешь?",
                                     reply_markup=markup)
                elif message.text == 'Найти подходящую стажировку':
                    json_data['users'][id]['curr_status'] = 'looking for stages'
                    json_data['users'][id]['stage'] = 1
                    write_json_data(json_data)
                    markup = types.ReplyKeyboardMarkup()
                    markup.row_width = 1
                    answers = json_data['users'][id]['favorite']
                    btn1 = types.KeyboardButton(answers[0])
                    btn2 = types.KeyboardButton(answers[1])
                    btn3 = types.KeyboardButton(answers[2])
                    btn4 = types.KeyboardButton(answers[3])
                    btn5 = types.KeyboardButton(answers[4])
                    markup.add(btn1, btn2, btn3, btn4, btn5)
                    bot.send_message(message.chat.id, "Стажировки в какой области ты ищешь?",
                                     reply_markup=markup)
                elif message.text == 'Поиск вуза специально для меня':
                    json_data['users'][id]['curr_status'] = 'looking_for_vuz'
                    json_data['users'][id]['stage'] = 1
                    write_json_data(json_data)
                    markup = types.ReplyKeyboardMarkup()
                    markup.row_width = 1
                    answers = json_data['users'][id]['favorite']
                    btn1 = types.KeyboardButton(answers[0])
                    btn2 = types.KeyboardButton(answers[1])
                    btn3 = types.KeyboardButton(answers[2])
                    btn4 = types.KeyboardButton(answers[3])
                    btn5 = types.KeyboardButton(answers[4])
                    markup.add(btn1, btn2, btn3, btn4, btn5)
                    bot.send_message(message.chat.id, "Какое направление тебя интересует?",
                                     reply_markup=markup)

            elif json_data['users'][id]['curr_status'] == 'looking for courses':
                if message.text in json_data['users'][id]['favorite'] and json_data['users'][id]['stage'] == 1:
                    bot.send_message(message.chat.id,
                                     f"Тебе точно будет интересно  посмотреть это:\n\nhttps://stepik.org/catalog/search?q={'%20'.join(message.text.split())}",
                                     reply_markup=get_menu_keyboard())
                    del json_data['users'][id]['stage']
                    json_data['users'][id]['curr_status'] = 'in_menu'
                    write_json_data(json_data)


            elif json_data['users'][id]['curr_status'] == 'looking for stages':
                if message.text in json_data['users'][id]['favorite'] and json_data['users'][id]['stage'] == 1:
                    stages_data = json.load(open("spec_info.json"))[message.text]['stages']
                    bot.send_message(message.chat.id,
                                     f"Вот стажировки по твоему профилю:\n\n{stages_data[0]}\n\n{stages_data[1]}\n\n{stages_data[2]}",
                                     reply_markup=get_menu_keyboard())
                    del json_data['users'][id]['stage']
                    json_data['users'][id]['curr_status'] = 'in_menu'
                    write_json_data(json_data)


            elif json_data['users'][id]['curr_status'] == 'looking_for_vuz':
                if message.text in json_data['users'][id]['favorite'] and json_data['users'][id]['stage'] == 1:
                    markup = types.ReplyKeyboardMarkup()
                    markup.row_width = 1
                    answers = ["Баллы ЕГЭ (сначала большие)", "Баллы ЕГЭ (сначала маленькие)", "Ближайшие ко мне вузы"]
                    btn1 = types.KeyboardButton(answers[0])
                    btn2 = types.KeyboardButton(answers[1])
                    btn3 = types.KeyboardButton(answers[2])
                    markup.add(btn1, btn2, btn3)
                    bot.send_message(message.chat.id,
                                     f"Как сортировать?",
                                     reply_markup=markup)
                    json_data['users'][id]['stage'] = 2
                    json_data['users'][id]['need_info_about'] = message.text
                    write_json_data(json_data)

                elif message.text in ["Баллы ЕГЭ (сначала большие)", "Баллы ЕГЭ (сначала маленькие)",
                                      "Ближайшие ко мне вузы"] and json_data['users'][id]['stage'] == 2:
                    BASA = pd.read_excel(r"FINALDATA.xlsx")
                    new_data = []
                    for i in range(len(BASA['url'])):
                        if BASA["Main program name"][i] == json_data['users'][id]['need_info_about']:
                            new_data.append(BASA.iloc[i])
                    if message.text.split()[0] == "Баллы":
                        new_data = list(sorted(new_data, key=lambda x: x['Mid ege'], reverse="большие" in message.text))
                        text_1 = f"1.\n\nСПЕЦИАЛЬНОСТЬ:\n{new_data[0]['Main program name']}\n\nПАРАМЕТРЫ ПРОГРАММЫ:\n{new_data[0]['Program parametrs']}\n\nИНДИВИДУАЛЬНЫЕ ДОСТИЖЕНИЯ:\n{new_data[0]['IDS']}\n\nПРОХОДНОЙ БАЛЛ ПРОШЛЫХ ЛЕТ:\n{new_data[0]['Points info']}\n\nПОЗВОНИТЬ:\n{new_data[0]['phones']}\n\nССЫЛКИ:\n{new_data[0]['urls']}\n{new_data[0]['url']}"
                        text_2 = f"2.\n\nСПЕЦИАЛЬНОСТЬ:\n{new_data[1]['Main program name']}\n\nПАРАМЕТРЫ ПРОГРАММЫ:\n{new_data[1]['Program parametrs']}\n\nИНДИВИДУАЛЬНЫЕ ДОСТИЖЕНИЯ:\n{new_data[1]['IDS']}\n\nПРОХОДНОЙ БАЛЛ ПРОШЛЫХ ЛЕТ:\n{new_data[1]['Points info']}\n\nПОЗВОНИТЬ:\n{new_data[1]['phones']}\n\nССЫЛКИ:\n{new_data[1]['urls']}\n{new_data[1]['url']}"
                        bot.send_message(message.chat.id,
                                         text_1)
                        bot.send_message(message.chat.id,
                                         text_2, reply_markup=get_menu_keyboard())
                        del json_data['users'][id]['need_info_about']
                        del json_data['users'][id]['stage']
                        json_data['users'][id]['curr_status'] = 'in_menu'
                        write_json_data(json_data)

                else:
                    del json_data['users'][id]['stage']
                    try:
                        del json_data['users'][id]['need_info_about']
                    except Exception:
                        pass
                    json_data['users'][id]['curr_status'] = 'in_menu'
                    write_json_data(json_data)
            if id in json_data['users']:
                if json_data['users'][id]['curr_status'] == 'in_menu':
                    bot.send_message(message.chat.id,
                                     "МЕНЮ",
                                     reply_markup=get_menu_keyboard())





    else:
        try:
            json_data['users'][message.from_user.id] = {'isTestCompleted': False, 'isTestRightnow': False,
                                                        'favorite': [], 'isNew': True, "curr_status": "new"}
            with open('agro_data.json', 'w', encoding='utf-8') as f:
                json.dump(json_data, f)
        except Exception as e:
            print(e.args)
            json_data['users'] = {}
            json_data['users'][message.from_user.id] = {'isTestCompleted': False, 'isTestRightnow': False,
                                                        'testInfo': {}, 'favorite': [], 'isNew': True,
                                                        "curr_status": "new"}
            with open('agro_data.json', 'w', encoding='utf-8') as f:
                json.dump(json_data, f)
        markup = types.ReplyKeyboardMarkup()
        item1 = types.KeyboardButton("Начать тест")
        markup.add(item1)
        bot.send_message(message.chat.id, "Привет, дружище, начинай скорее тест!", reply_markup=markup)


# Проверка на наличие БД

try:
    open('agro_data.json', encoding='utf-8')
except Exception:
    with open('agro_data.json', 'w') as f:
        json.dump({'users': {}}, f)

bot.polling(none_stop=True, interval=0)
