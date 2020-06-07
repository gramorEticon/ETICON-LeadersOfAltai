from config import vk, vk_session, get_random_id, longpoll, basa as db
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotEventType
import re
import math
from datetime import  datetime, timedelta

class userClass():

    def __init__(self, user_id):
        userInBD = db.chek_user(user_id)
        if userInBD == True:
            self.user_menu(user_id)
        elif userInBD == False:
            self.register_user(user_id)

    def register_user(self, user_id):
        user_profile = {
            "phone": None,
            "first_name": None,
            "last_name": None,
            "info": None
        }
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("Да ☑", color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button("Нет ❌", color=VkKeyboardColor.NEGATIVE)
        profile = vk.users.get(user_ids=user_id, fields="contacts")
        full_info = profile[0]
        user_profile["first_name"] = profile[0]["first_name"]
        user_profile["last_name"] = profile[0]["last_name"]
        if "mobile_phone" in full_info:
            telephone = profile[0]["mobile_phone"]
            user_name = profile[0]["first_name"] + " " + profile[0]["last_name"]
            user_first_name = profile[0]["first_name"]
            vk.messages.send(message=f"{user_first_name}, это ваш телефон - {telephone}?",
                            peer_id=user_id,
                            random_id=get_random_id(),
                            keyboard=keyboard.get_keyboard())
        else:
            self.get_phone(user_id, user_profile)

        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Да ☑" and event.obj.text != "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                user_profile["phone"] = telephone
                self.get_user_information(user_id, user_profile)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Нет ❌" and event.obj.text != "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.get_phone(user_id, user_profile)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and (event.obj.text == "Начать" or event.obj.text == 'В стартовое меню ➡') and event.obj.from_id == user_id:
                break

    def get_phone(self,user_id, user_profile):
        vk.messages.send(message='📞 Введите свой номер телефона:',
                         random_id=get_random_id(),
                         peer_id=user_id)

        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.from_id == user_id and event.obj.text != "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡':
                regular = r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
                phone = re.fullmatch(regular, event.obj.text)
                if phone != None:
                    user_profile["phone"] = event.obj.text
                    self.get_user_information(user_id, user_profile)
                    break
                else:
                    vk.messages.send(message='‼ Номер телефона введен неверно, повторите ввод',
                                     random_id=get_random_id(),
                                     peer_id=user_id)
                    self.get_phone(user_id)
                    break

    def get_user_information(self, user_id, user_profile):
        vk.messages.send(message=f"😄 Расскажите немного о себе",
                         peer_id=user_id,
                         random_id=get_random_id()
                         )
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW  and event.obj.text != "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                user_profile["info"] = event.obj.text
                db.registration_user(user_profile["first_name"],user_profile["last_name"],user_profile["info"],user_id,user_profile["phone"])
                self.user_menu(user_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and (event.obj.text == "Начать" or event.obj.text == 'В стартовое меню ➡') and event.obj.from_id == user_id:
                break

    def user_menu(self, user_id):
        keyboard = VkKeyboard(one_time=False)

        golos = db.chek_voice(user_id)
        if golos == True:
            keyboard.add_button("🤝 Отдать голос", color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button("🙋‍🙋‍♂️ Проголосовать", color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button("📈 Топ лидеров мнений", color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button("🙌 Кто мне доверяет", color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button("🆕 Предложить инициативу", color=VkKeyboardColor.PRIMARY)
        if golos == False:
            keyboard.add_button("🙅‍♂️ Забрать голос", color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button("📈 Топ лидеров мнений", color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button("🙌 Кому отдал свой голос", color=VkKeyboardColor.PRIMARY)
        vk.messages.send(message = "Добро пожаловать в главное меню",
                         peer_id = user_id,
                         random_id = get_random_id(),
                         keyboard = keyboard.get_keyboard())
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "🤝 Отдать голос" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.giftChoice(user_id, 0, 1)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "🙋‍🙋‍♂️ Проголосовать" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.choice(user_id, 0, 1)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "🆕 Предложить инициативу" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.creat_iniziative(user_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "📈 Топ лидеров мнений" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.top_leaders(user_id, 0, 1)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "🙌 Кто мне доверяет" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.kto_dover(user_id, 0, 1)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "🙅‍♂️ Забрать голос" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.cancel_golos(user_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "🙌 Кому отдал свой голос" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                lead_id  =   db.who_give_voice(user_id)
                lead_id = lead_id.strip(",")
                leader = db.get_user(lead_id)
                self.leader_info(user_id , 0 , 1, leader[0])
                break
            if event.type == VkBotEventType.MESSAGE_NEW and (event.obj.text == "Начать" or event.obj.text == 'В стартовое меню ➡') and event.obj.from_id == user_id:
                break

    def cancel_golos(self, user_id):
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("Да", color=VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_button("Нет", color=VkKeyboardColor.POSITIVE)
        sender = db.who_give_voice(user_id)
        sender.split(",")
        vk.messages.send(message=f"Вы хотите забрать свой голос у https://vk.com/id{sender}?",
                             peer_id=user_id,
                             random_id=get_random_id(),
                             keyboard=keyboard.get_keyboard())

        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Да" and event.obj.text != "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                db.pickup_voice(user_id)
                self.user_menu(user_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Нет" and event.obj.text != "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.user_menu(user_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and (event.obj.text == "Начать" or event.obj.text == 'В стартовое меню ➡') and event.obj.from_id == user_id:
                break

    def iniciativesLeader(self, user_id, counter, stranica):
        who = db.who_give_voice(user_id)
        user = db.get_user(who)
        project = db.user_resolution(who)
        keyboard = VkKeyboard(one_time=False)
        project = ["проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект","проект"]
        schetchik = counter
        while schetchik < counter+8:
            if schetchik < len(project):
                keyboard.add_button(project[schetchik], color=VkKeyboardColor.POSITIVE)
                keyboard.add_line()
                schetchik=schetchik+1
            else:
                break
        if counter+8 < len(project) and counter-8 >= 0:
            keyboard.add_button("⬅ Назад", color=VkKeyboardColor.POSITIVE)
            keyboard.add_button("Вперед ➡", color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.POSITIVE)
        if counter - 8 >= 0 and counter + 8 >= len(project):
            keyboard.add_button("⬅ Назад", color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.POSITIVE)
        if counter+8 < len(project) and counter == 0:
            keyboard.add_button("Вперед ➡", color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.POSITIVE)
        if counter+8 >= len(project) and counter-8 <= 0:
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.POSITIVE)
            pass
        vk.messages.send(message=f"Список предложенных инициатив\nСтраница {stranica} из {math.ceil(len(project)/8)}",
                         peer_id=user_id,
                         random_id=get_random_id(),
                         keyboard=keyboard.get_keyboard())

        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Вперед ➡" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:

                self.iniciativesLeader(user_id, counter+8, stranica+1)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.iniciativesLeader(user_id, counter-8, stranica+1)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and (event.obj.text == "Начать" or event.obj.text == 'В стартовое меню ➡') and event.obj.from_id == user_id:
                break

    def giftChoice(self, user_id, counter, stranica):
        keyboard = VkKeyboard(one_time=False)
        project = db.best_of_the_best()
        schetchik = counter
        idser = []
        namer = []
        while schetchik < counter+7:
            if schetchik < len(project):
                if project[schetchik][1]["id"] != str(user_id):
                    keyboard.add_button(project[schetchik][1]["family"] + " " + project[schetchik][1]["name"], color=VkKeyboardColor.POSITIVE)
                    namer.append(project[schetchik][1]["family"] + " " + project[schetchik][1]["name"])
                    idser.append(project[schetchik][1]["id"])
                    keyboard.add_line()
                    schetchik=schetchik+1
                elif project[schetchik][1]["id"] == str(user_id):
                    schetchik = schetchik + 1
                    continue
            else:
                break
        if counter+7 < len(project) and counter-7 >= 0:
            keyboard.add_button("⬅ Назад", color=VkKeyboardColor.DEFAULT)
            keyboard.add_button("Вперед ➡", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔎 Поиск", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        elif counter - 7 >= 0 and counter + 7 >= len(project):
            keyboard.add_button("⬅ Назад", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔎 Поиск", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        elif counter+7 < len(project) and counter == 0:
            keyboard.add_button("Вперед ➡", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔎 Поиск", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        elif counter+7 >= len(project) and counter-7 <= 0:
            keyboard.add_button("🔎 Поиск", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
            pass
        vk.messages.send(message=f"🔶 Список предложенных инициатив\n🔷 Страница {stranica} из {math.ceil(len(project)/7)}",
                         peer_id=user_id,
                         random_id=get_random_id(),
                         keyboard=keyboard.get_keyboard())

        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text in namer and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                indexer = namer.index(event.obj.text)
                self.gift_choice_for_user(user_id,counter,stranica,idser[indexer])

                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Вперед ➡" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:

                self.giftChoice(user_id, counter+7, stranica+1)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.giftChoice(user_id, counter-7, stranica-1)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "🔎 Поиск" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.search_user_for_gift(user_id, counter, stranica)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "🔙 В меню" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.user_menu(user_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and (event.obj.text == "Начать" or event.obj.text == 'В стартовое меню ➡') and event.obj.from_id == user_id:
                break

    def search_user_for_gift(self, user_id, counter, stranica):
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("⬅ Назад")
        vk.messages.send(message=f"🔶 Отправьте фамилию кандидата",
                         peer_id=user_id,
                         random_id=get_random_id(),
                         keyboard = keyboard.get_keyboard()
                         )
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.giftChoice(user_id,counter,stranica)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text != "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                project = db.find_user(event.obj.text)
                self.search_result(user_id, 0, 1, event.obj.text, project)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and (event.obj.text == "Начать" or event.obj.text == 'В стартовое меню ➡') and event.obj.from_id == user_id:
                break

    def search_result(self, user_id, counter, stranica, family, search_list):
        keyboard = VkKeyboard(one_time=False)
        project = search_list
        schetchik = counter
        idser = []
        namer = []
        while schetchik < counter+7:
            if schetchik < len(project):
                keyboard.add_button(project[schetchik][4] + " " + project[schetchik][2], color=VkKeyboardColor.POSITIVE)
                idser.append(project[schetchik][0])
                namer.append(project[schetchik][4] + " " + project[schetchik][2])
                keyboard.add_line()
                schetchik=schetchik+1
            else:
                break
        if counter+7 < len(project) and counter-7 >= 0:
            keyboard.add_button("⬅ Назад", color=VkKeyboardColor.DEFAULT)
            keyboard.add_button("Вперед ➡", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("Поиск", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        elif counter - 7 >= 0 and counter + 7 >= len(project):
            keyboard.add_button("⬅ Назад", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("Поиск", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        elif counter+7 < len(project) and counter == 0:
            keyboard.add_button("Вперед ➡", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("Поиск", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        elif counter+7 >= len(project) and counter-7 <= 0:
            keyboard.add_button("Поиск", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)

        if len(project) == 0:
            vk.messages.send(message=f"Мы не нашли людей по вашему запросу 😕",
                         peer_id=user_id,
                         random_id=get_random_id(),
                         keyboard=keyboard.get_keyboard())
        else:
            vk.messages.send(message=f"🔶Список найденых людей\n🔷Страница {stranica} из {math.ceil(len(project) / 7)}",
                             peer_id=user_id,
                             random_id=get_random_id(),
                             keyboard=keyboard.get_keyboard())

        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text in namer and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                checker = namer.index(event.obj.text)
                idus = idser[checker]
                self.gift_choice_for_user(user_id,counter,stranica,idus)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Вперед ➡" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.search_result(user_id, counter+7, stranica+1, family, search_list)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.search_result(user_id, counter-7, stranica-1, family, search_list)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Поиск" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.search_user_for_gift(user_id, counter,stranica)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "🔙 В меню" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.user_menu(user_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and (event.obj.text == "Начать" or event.obj.text == 'В стартовое меню ➡') and event.obj.from_id == user_id:
                break

    def gift_choice_for_user(self, user_id, counter, stranica, to_id):
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("Да", color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button("Нет", color=VkKeyboardColor.NEGATIVE)
        profile = vk.users.get(user_ids=to_id)
        user_name = profile[0]["first_name"] + " " + profile[0]["last_name"]
        vk.messages.send(message=f"🔶 Вы хотите отдать свой голос в пользу {user_name}\n🌐 Ссылка: https://vk.com/id{to_id}\n❓ Вы в этом уверены?",
                         peer_id=user_id,
                         random_id=get_random_id(),
                         keyboard=keyboard.get_keyboard())

        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.giftChoice(user_id, counter, stranica)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Да" and event.obj.text != "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                db.give_voite(user_id, to_id)
                self.user_menu(user_id)
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Нет" and event.obj.text != "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.giftChoice(user_id, counter, stranica)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and (event.obj.text == "Начать" or event.obj.text == 'В стартовое меню ➡') and event.obj.from_id == user_id:
                break

    def top_leaders(self, user_id, counter, stranica):
        keyboard = VkKeyboard(one_time=False)
        project = db.best_of_the_best()
        schetchik = counter
        namer = []
        idser = []
        while schetchik < counter+8:
            if schetchik < len(project):
                keyboard.add_button(project[schetchik][1]["family"] + " " + project[schetchik][1]["name"] + " " + f"№{schetchik+1}", color=VkKeyboardColor.POSITIVE)
                namer.append(project[schetchik][1]["family"] + " " + project[schetchik][1]["name"] + " " + f"№{schetchik+1}")
                idser.append(project[schetchik][1]["id"])
                keyboard.add_line()
                schetchik=schetchik+1
            else:
                break
        if counter+8 < len(project) and counter-8 >= 0:
            keyboard.add_button("⬅ Назад", color=VkKeyboardColor.DEFAULT)
            keyboard.add_button("Вперед ➡", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        elif counter - 8 >= 0 and counter + 8 >= len(project):
            keyboard.add_button("⬅ Назад", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        elif counter+8 < len(project) and counter == 0:
            keyboard.add_button("Вперед ➡", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        elif counter+8 >= len(project) and counter-8 <= 0:
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
            pass

        if len(project) == 0:
            vk.messages.send(message=f"Мы не нашли людей по вашему запросу 😕",
                         peer_id=user_id,
                         random_id=get_random_id(),
                         keyboard=keyboard.get_keyboard())
        else:
            vk.messages.send(message=f"🔶 Список найденых людей\n🔷 Страница {stranica} из {math.ceil(len(project) / 8)}",
                             peer_id=user_id,
                             random_id=get_random_id(),
                             keyboard=keyboard.get_keyboard())

        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text in namer and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                induxer = namer.index(event.obj.text)
                self.leader_info2(user_id, counter,  stranica, induxer)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Вперед ➡" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.top_leaders(user_id, counter+8, stranica+1)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.top_leaders(user_id, counter-8, stranica-1)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and (event.obj.text == "Начать" or event.obj.text == 'В стартовое меню ➡') and event.obj.from_id == user_id:
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "🔙 В меню" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.user_menu(user_id)
                break

    def leader_info(self, user_id, counter, stranica, indexer):
        keyboard = VkKeyboard(one_time=False)

        keyboard.add_button("📑 Просмотр инициатив", color=VkKeyboardColor.DEFAULT)
        keyboard.add_line()
        keyboard.add_button("🙋‍♂️ Просмотр поддержавших", color=VkKeyboardColor.DEFAULT)
        keyboard.add_line()
        keyboard.add_button("⬅ Назад", color=VkKeyboardColor.DEFAULT)
        project = db.best_of_the_best()

        for user_chec_id in project:
            if user_chec_id[1]['id'] == indexer:
                a = project.index(user_chec_id)
                break

        vk.messages.send(message=f"🙋‍♂️ {project[a][1]['family']} {project[a][1]['name']}\n🌐 Ссылка: https://vk.com/id{project[a][1]['id']}\n📃 Краткая информация: {project[a][1]['decription']}\n\n🙋‍♂️ Количество голосов: {project[a][0]}",
                         peer_id=user_id,
                         random_id=get_random_id(),
                         keyboard=keyboard.get_keyboard())

        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "📑 Просмотр инициатив" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.leader_projects(user_id,counter, project[a][1]['id'])
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "🙋‍♂️ Просмотр поддержавших" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.kto_dover_leader(user_id, 0, 1, project[a][1]['id'])
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.user_menu(user_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and (event.obj.text == "Начать" or event.obj.text == 'В стартовое меню ➡') and event.obj.from_id == user_id:
                break

    def leader_info2(self, user_id, counter, stranica, indexer):
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("📑 Просмотр инициатив", color=VkKeyboardColor.DEFAULT)
        keyboard.add_line()
        keyboard.add_button("🙋‍♂️ Просмотр поддержавших", color=VkKeyboardColor.DEFAULT)
        keyboard.add_line()
        keyboard.add_button("⬅ Назад", color=VkKeyboardColor.DEFAULT)
        project = db.best_of_the_best()

        vk.messages.send(message=f"🙋‍♂️ {project[indexer][1]['family']} {project[indexer][1]['name']}\n🌐 Ссылка: https://vk.com/id{project[indexer][1]['id']}\n📃 Краткая информация: {project[indexer][1]['decription']}\n\n🙋‍♂️ Количество голосов: {project[indexer][0]}",
                         peer_id=user_id,
                         random_id=get_random_id(),
                         keyboard=keyboard.get_keyboard())

        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "📑 Просмотр инициатив" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.leader_projects(user_id,counter, project[indexer][1]['id'])
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "🙋‍♂️ Просмотр поддержавших" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.kto_dover_leader(user_id, 0, 1, project[indexer][1]['id'])
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.user_menu(user_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and (event.obj.text == "Начать" or event.obj.text == 'В стартовое меню ➡') and event.obj.from_id == user_id:
                break

    def kto_dover(self, user_id, counter, stranica):
        keyboard = VkKeyboard(one_time=False)
        project = db.to_give_voice(str(user_id))

        schetchik = counter
        info = ""
        while schetchik < counter + 20:
            if schetchik < len(project):
                name = db.get_user(project[schetchik])
                info = info + f"🔵 [id{project[schetchik]}|{name[4]} {name[2]}] "+ "\n"
                schetchik = schetchik + 1
            else:
                break

        if counter + 20 < len(project) and counter - 20 >= 0:
            keyboard.add_button("⬅ Назад", color=VkKeyboardColor.DEFAULT)
            keyboard.add_button("Вперед ➡", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        elif counter - 20 >= 0 and counter + 20 >= len(project):
            keyboard.add_button("⬅ Назад", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        elif counter + 20 < len(project) and counter == 0:
            keyboard.add_button("Вперед ➡", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        elif counter + 20 >= len(project) and counter - 20 <= 0:
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        if len(project) == 0:
            keyboard = VkKeyboard(one_time=False)
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
            vk.messages.send(message="Вас ни кто не поддерживает 😟",
                                 peer_id=user_id,
                                 random_id=get_random_id(),
                                 keyboard=keyboard.get_keyboard())
        else:
            vk.messages.send(message=f"🔶 Страница {stranica}\n\n" + info,
                             peer_id=user_id,
                             random_id=get_random_id(),
                             keyboard=keyboard.get_keyboard())

        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Вперед ➡" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.kto_dover(user_id, counter + 20, stranica + 1)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.kto_dover(user_id, counter - 20, stranica - 1)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "🔙 В меню" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.user_menu(user_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and (event.obj.text == "Начать" or event.obj.text == 'В стартовое меню ➡') and event.obj.from_id == user_id:
                break


    def choice(self, user_id, counter, stranica):
        keyboard = VkKeyboard(one_time=False)
        project = db.get_user_resolution_comlite()
        schetchik = counter
        name_list = []
        id_list = []
        while schetchik < counter + 7:
            if schetchik < len(project):
                keyboard.add_button(project[schetchik][1], color=VkKeyboardColor.POSITIVE)
                keyboard.add_line()
                name_list.append(project[schetchik][1])
                id_list.append(project[schetchik][0])
                schetchik = schetchik + 1

            else:
                break

        if counter + 7 < len(project) and counter - 7 >= 0:
            keyboard.add_button("⬅ Назад", color=VkKeyboardColor.DEFAULT)
            keyboard.add_button("Вперед ➡", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        elif counter - 7 >= 0 and counter + 7 >= len(project):
            keyboard.add_button("⬅ Назад", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        elif counter + 7 < len(project) and counter == 0:
            keyboard.add_button("Вперед ➡", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        elif counter + 7 >= len(project) and counter - 7 <= 0:
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)

        if len(project) == 0:
            vk.messages.send(message=f"Мы не нашли новых инициатив 😕",
                             peer_id=user_id,
                             random_id=get_random_id(),
                             keyboard=keyboard.get_keyboard())
        else:
            vk.messages.send(message=f"🔶 Список найденых инициатив\n🔷 Страница {stranica} из {math.ceil(len(project) / 7)}",
                             peer_id=user_id,
                             random_id=get_random_id(),
                             keyboard=keyboard.get_keyboard())

        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Вперед ➡" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.choice(user_id, counter + 7, stranica + 1)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.choice(user_id, counter - 7, stranica - 1)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "🔙 В меню" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.user_menu(user_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and ( event.obj.text == "Начать" or event.obj.text == 'В стартовое меню ➡') and event.obj.from_id == user_id:
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text in name_list and (event.obj.text != "Начать" or event.obj.text != 'В стартовое меню ➡') and event.obj.from_id == user_id:
                self.choice_accept(user_id, id_list[name_list.index(event.obj.text)], counter , stranica)
                break


    def choice_accept(self, user_id, rez_id, counter, stranica):
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("👍 Я за инициативу", color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button("👎 Я против", color=VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_button("⬅ Назад", color=VkKeyboardColor.DEFAULT)
        keyboard.add_line()
        keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        info = db.get_resolution(rez_id)

        vk.messages.send(message=f"🔶 {info[1]}\n\n🔶{info[2]}\n\n🔶 Ссылка на чат: {info[7]}\n\n 🔶Ссылка на документы: {info[4]}\n\n🔶 Вы хотите отдвать свой голос за проект?",
                         peer_id=user_id,
                         random_id=get_random_id(),
                         keyboard=keyboard.get_keyboard())

        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "👍 Я за инициативу" and event.obj.text != "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                db.voiting(user_id, rez_id, True)
                self.user_menu(user_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "👎 Я против" and event.obj.text != "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                db.voiting(user_id, rez_id, False)
                self.user_menu(user_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and (event.obj.text == "Начать" or event.obj.text == 'В стартовое меню ➡') and event.obj.from_id == user_id:
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "🔙 В меню" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.user_menu(user_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.choice(user_id, counter, stranica)
                break

    def get_res_info(self, name , res):
        for d in res:
            if name == d["name"]:
                return d

        return 0

    def get_us_list(self, data):
        res_list = []
        for d in data:
            res_list.append(d["name"])
        return res_list

    def get_leader_id(self, name , data):
        ud = name.split(" ")
        for d in data:
            if ud[0] == d["name"] and ud[1] ==d["family"]:
                return d

        return 0

    def get_leader_data(self, data):
        leaders = []
        names_list = []
        for d in data:
            l = d[1]
            l["count"] = d[0]
            names_list.append( d[1]["name"] + " " + d[1]["family"])
            leaders.append(l)

    def leader_s(self, dat):
        info = {}
        info = dat[1]
        info["count"] = dat[0]
        return info

    def kto_dover_leader(self, user_id, counter, stranica, leader):
        keyboard = VkKeyboard(one_time=False)
        project = db.to_give_voice(str(leader))
        schetchik = counter

        info = ""
        while schetchik < counter + 20:
            if schetchik < len(project):
                name = db.get_user(project[schetchik])
                info = info + f"🔵 [id{project[schetchik]}|{name[4]} {name[2]}]" + "\n"
                schetchik = schetchik + 1
            else:
                break
        if counter + 20 < len(project) and counter - 20 >= 0:
            keyboard.add_button("⬅ Назад", color=VkKeyboardColor.DEFAULT)
            keyboard.add_button("Вперед ➡", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        elif counter - 20 >= 0 and counter + 20 >= len(project):
            keyboard.add_button("⬅ Назад", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        elif counter + 20 < len(project) and counter == 0:
            keyboard.add_button("Вперед ➡", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        elif counter + 20 >= len(project) and counter - 20 <= 0:
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        if len(project) == 0:
            keyboard = VkKeyboard(one_time=False)
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
            vk.messages.send(message="Вас ни кто не поддерживает 😕",
                                 peer_id=user_id,
                                 random_id=get_random_id(),
                                 keyboard=keyboard.get_keyboard())
        else:
            vk.messages.send(message=info,
                             peer_id=user_id,
                             random_id=get_random_id(),
                             keyboard=keyboard.get_keyboard())

        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Вперед ➡" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.kto_dover(user_id, counter + 20, stranica + 1)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.kto_dover(user_id, counter - 20, stranica - 1)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "🔙 В меню" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.user_menu(user_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and (event.obj.text == "Начать" or event.obj.text == 'В стартовое меню ➡') and event.obj.from_id == user_id:
                break

    def leader_projects(self, user_id , counter, leader ):
        user_res = db.user_resolution(leader)
        user_res_list = self.get_us_list(user_res)
        keyboard = VkKeyboard(one_time=False)

        s = counter
        while s < counter + 5:
            if s < len(user_res_list):
                keyboard.add_button(user_res_list[s], color=VkKeyboardColor.POSITIVE)
                keyboard.add_line()
                s = s + 1
            else:
                break
        if counter + 5 < len(user_res_list) and counter - 5 >= 0:
            keyboard.add_button("⬅ Назад", color=VkKeyboardColor.DEFAULT)
            keyboard.add_button("Вперед ➡", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        elif counter - 5 >= 0 and counter + 5 >= len(user_res_list):
            keyboard.add_button("⬅ Назад", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        elif counter + 5 < len(user_res_list) and counter == 0:
            keyboard.add_button("Вперед ➡", color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)
        elif counter + 5 >= len(user_res_list) and counter <= 0:
            keyboard.add_button("🔙 В меню", color=VkKeyboardColor.DEFAULT)

        vk.messages.send(
            message=f"🔶 Cписок принятых решений",
            peer_id=user_id,
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard()
        )

        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "⬅ Назад" and event.obj.text != "🔙 В меню" and event.obj.text != "Начать" and user_id == event.obj.from_id:
                self.leader_info2(user_id, counter - 5 , leader)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Вперед ➡" and event.obj.text != "🔙 В меню" and event.obj.text != "Начать" and user_id == event.obj.from_id:
                self.leader_info2(user_id, counter + 5, leader)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "🔙 В меню"  and event.obj.text != "Начать" and user_id == event.obj.from_id:
                self.user_menu(user_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text in user_res_list and event.obj.text != "Начать" and user_id == event.obj.from_id:
                res = self.get_res_info(event.obj.text, user_res)

                vk.messages.send(message = f"""🔶 Название:{res["name"]} \n🔷 Описание{res["description"]} \n🔷 Проголосовал:{ "За" if res["result"] else "Против"}""",
                                 peer_id = user_id ,
                                 random_id = get_random_id(),
                                 keyboard = keyboard.get_keyboard())

    def creat_iniziative(self, user_id):
        iniziative = {}
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("⬅ Назад", color = VkKeyboardColor.DEFAULT)
        vk.messages.send(message = "📃 Введите название инициативы",
                         peer_id = user_id,
                         random_id = get_random_id(),
                         )
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text and event.obj.text != "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                iniziative["name"] = event.obj.text
                self.get_discrition(user_id , iniziative)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Начать" and event.obj.from_id == user_id:
                break

    def get_discrition(self, user_id , iniziative):
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("⬅ Назад", color=VkKeyboardColor.DEFAULT)
        vk.messages.send(message="💬 Опишите суть инициативы",
                         peer_id=user_id,
                         random_id=get_random_id(),
                         )
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text and event.obj.text != "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                iniziative["discription"] = event.obj.text
                self.get_link(user_id, iniziative)
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Начать" and event.obj.from_id == user_id:
                break

    def get_link(self, user_id, iniziative):
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("⬅ Назад", color=VkKeyboardColor.NEGATIVE)
        vk.messages.send(message="📕 Введите ссылку на документ/презентацию",
                         peer_id=user_id,
                         random_id=get_random_id(),
                         )
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text and event.obj.text != "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                iniziative["doc_link"] = event.obj.text
                self.get_link_chat(user_id, iniziative)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Начать" and event.obj.from_id == user_id:
                break

    def get_link_chat(self, user_id , iniziative):
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("⬅ Назад", color=VkKeyboardColor.DEFAULT)
        vk.messages.send(message="💬 Введите ссылку на беседу",
                         peer_id=user_id,
                         random_id=get_random_id(),
                         )
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text and event.obj.text != "⬅ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                iniziative["chat_link"] = event.obj.text

                db.new_resolution_user(iniziative["name"], iniziative["discription"], iniziative["doc_link"], iniziative["chat_link"])
                vk.messages.send(message="Инициатива была успешно создана и отправлена на модерацию 🎉🎉🎉",
                                 peer_id=user_id,
                                 random_id=get_random_id(),
                                 )
                self.user_menu(user_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Начать" and event.obj.from_id == user_id:
                break


