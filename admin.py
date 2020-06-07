from config import vk, vk_session, get_random_id, longpoll, basa
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotEventType
from datetime import datetime , timedelta
class Admin():
    MINUTES = 2
    def __init__(self, user_id):
        self.admin_menu(user_id)

    def admin_menu(self, user_id):

        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("📋 Создать инициативу", color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button("🏆 Список лидеров", color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button("✅ Одобрить предложенную инициативу", color=VkKeyboardColor.PRIMARY)
        vk.messages.send(message = "Выберете пункт меню",
                         peer_id = user_id,
                         random_id = get_random_id(),
                         keyboard = keyboard.get_keyboard())
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "📋 Создать инициативу" and event.obj.text != "◀ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.creat_iniziative(user_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "🏆 Список лидеров" and event.obj.text != "◀ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                data = basa.best_of_the_best()
                leaders , names_list = self.get_leader_data(data)
                self.leader_ceck(user_id, 0, leaders , names_list)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "✅ Одобрить предложенную инициативу" and event.obj.text != "◀ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                self.user_resolution_choise(user_id, 0 )
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Начать" and event.obj.from_id == user_id:
                break


    def creat_iniziative(self, user_id):
        iniziative = {}
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("◀ Назад", color = VkKeyboardColor.NEGATIVE)
        vk.messages.send(message = "✏ Введите название инициативы",
                         peer_id = user_id,
                         random_id = get_random_id(),
                         )
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text and event.obj.text != "◀ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                iniziative["name"] = event.obj.text
                self.get_discrition(user_id , iniziative)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Начать" and event.obj.from_id == user_id:
                break


    def get_discrition(self, user_id , iniziative):
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("◀ Назад", color=VkKeyboardColor.NEGATIVE)
        vk.messages.send(message="✏ Кратко опишите суть инициативы",
                         peer_id=user_id,
                         random_id=get_random_id(),
                         )
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text and event.obj.text != "◀ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                iniziative["discription"] = event.obj.text
                self.get_link(user_id, iniziative)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Начать" and event.obj.from_id == user_id:
                break

    def get_link(self, user_id, iniziative):
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("◀ Назад", color=VkKeyboardColor.NEGATIVE)
        vk.messages.send(message="📄 Введите ссылку на документ",
                         peer_id=user_id,
                         random_id=get_random_id(),
                         )
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text and event.obj.text != "◀ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                iniziative["doc_link"] = event.obj.text
                self.get_link_chat(user_id, iniziative)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Начать" and event.obj.from_id == user_id:
                break

    def get_link_chat(self, user_id , iniziative):
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("◀ Назад", color=VkKeyboardColor.NEGATIVE)
        vk.messages.send(message="👥 Введите ссылку на беседу",
                         peer_id=user_id,
                         random_id=get_random_id(),
                         )
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text and event.obj.text != "◀ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                iniziative["chat_link"] = event.obj.text
                iniziative["date"] = self.get_data_str()

                basa.new_resolution_admin(iniziative["name"], iniziative["discription"], iniziative["date"], iniziative["doc_link"], iniziative["chat_link"])
                vk.messages.send(message="👍 Инициатива была успешно создана",
                                 peer_id=user_id,
                                 random_id=get_random_id(),
                                 )
                users = basa.get_all_id()
                self.get_rassilka(text = f"❗❗❗ Инициатива {iniziative['name']} доступна для голосования в течении 7 дней.\n\n 👥  Для обсуждения инициативы перейдите в беседу:\n {iniziative['chat_link']} ", users = users)
                self.admin_menu(user_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Начать" and event.obj.from_id == user_id:
                break


    def get_data_str(self):
        now = datetime.now() + timedelta(minutes=self.MINUTES)
        d = ""
        d = d + str(now.day) + "." + str(now.month) + "." + str(now.year) + "." + str(now.hour) + "." + str(now.minute)

        return d


    def get_id(self, el , res_us):
        us_id = 0
        for i in range(0,len(res_us)):
            if el == res_us[i]["name"]:
                us_id = i
                return us_id
        return us_id

    def user_resolution_parser(self):
        data = basa.get_user_resolution()
        resolution_users = []
        res_name = []
        if len(data) == 0:
            return 0 , 0
        for d in data:
            resolution_users.append({"id": d[0], "name":d[1], "desc":d[2], "date":d[3], "doc_linc": d[4], "chat_link":d[7] })
            res_name.append(d[1])

        return  resolution_users, res_name


    def user_resolution_choise(self, user_id, counter):
       res_us , res_name =  self.user_resolution_parser()
       if res_us == 0 and res_name == 0:


           vk.messages.send(message="☹ Новых инициатив нет, вы будете возвращены в главное меню",
                            peer_id=user_id,
                            random_id=get_random_id(),
                            )
           self.admin_menu(user_id)
       keyboard = VkKeyboard(one_time=False)
       for r in res_us:
           keyboard.add_button(r["name"], color = VkKeyboardColor.POSITIVE)
           keyboard.add_line()
       if counter + 8 <len(res_us) and counter-8 >=0:
           keyboard.add_button("◀ Назад", color = VkKeyboardColor.POSITIVE)
           keyboard.add_button("Вперед ▶", color=VkKeyboardColor.POSITIVE)
       if counter - 8 < len(res_us) and counter + 8 >= len(res_us):
           keyboard.add_button("Вперед ▶", color=VkKeyboardColor.POSITIVE)
       if counter + 8 < len(res_us) and counter == 0:
           keyboard.add_button("Вперед ▶", color=VkKeyboardColor.POSITIVE)

       keyboard.add_line()
       keyboard.add_button('В стартовое меню ➡', color=VkKeyboardColor.PRIMARY)
       vk.messages.send(message="🤔 Выбирете интересующюю Вас инициативу",
                        peer_id=user_id,
                        random_id=get_random_id(),
                        keyboard = keyboard.get_keyboard()
                        )
       for event in longpoll.listen():
           if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Вперед ▶" and event.obj.from_id == user_id and event.obj.text != "◀ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' :
               self.user_resolution_choise(user_id, counter + 8)
               break
           if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "◀ Назад" and event.obj.from_id == user_id and event.obj.text != "◀ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' :
               self.user_resolution_choise(user_id, counter - 8)
               break
           if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text in res_name and event.obj.from_id == user_id and event.obj.text != "◀ Назад" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' :
               us_id = self.get_id(event.obj.text , res_us)
               self.res_yn(user_id, res_us[us_id])
               break
           if event.type == VkBotEventType.MESSAGE_NEW and (event.obj.text == 'В стартовое меню ➡' or event.obj.text == "Начать"):
                break




    def res_yn(self, user_id , res):
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("👍 Одобряю", color = VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button("👎 Не одобряю", color = VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_button("В стартовое меню ➡", color= VkKeyboardColor.PRIMARY)
        vk.messages.send(message=f"""{res["name"]} \n {res["desc"]} \n Ссылка на документ: {res["doc_linc"]} \n Ссылка на {res["chat_link"]}""",
                         peer_id=user_id,
                         random_id=get_random_id(),
                         keyboard=keyboard.get_keyboard()
                         )
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "👍 Одобряю"  and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                data = self.get_data_str()
                basa.accept_resolution(res["id"], data)
                users = basa.get_all_id()
                self.get_rassilka(
                    text=f"Инициатива {res['name']} доступна для голосования в течении 7 дней.\n Для обсуждения инициативы перейдите в беседу:\n {res['chat_link']}  \n Ссылка на документ: {res['doc_linc']}",
                    users=users)

                self.admin_menu(user_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "👎 Не одобряю" and event.obj.text != "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                basa.delete_resolution(res["id"])
                self.admin_menu(user_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW  and event.obj.text == "Начать" and event.obj.text != 'В стартовое меню ➡' and event.obj.from_id == user_id:
                break



    def get_leader_data(self, data):
        leaders = []
        names_list = []
        for d in data:
            l = d[1]
            l["count"] = d[0]
            names_list.append( d[1]["name"] + " " + d[1]["family"])
            leaders.append(l)


        return leaders, names_list

    def leader_ceck(self, user_id , counter ,data , name_list):
        keyboard = VkKeyboard(one_time=False)
        s = counter
        while s < counter + 5:
            if s < len(name_list):
                keyboard.add_button(name_list[s], color = VkKeyboardColor.POSITIVE)
                keyboard.add_line()
                s = s +1
            else:
                break
        if counter+5 < len(name_list) and counter-5 >=0:
            keyboard.add_button("◀ Назад", color=VkKeyboardColor.POSITIVE)
            keyboard.add_button("Вперед ▶", color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button('В стартовое меню ➡', color= VkKeyboardColor.NEGATIVE)
        if counter - 5 >=0 and counter + 5 >= len(name_list):
            keyboard.add_button("◀ Назад", color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button('В стартовое меню ➡', color=VkKeyboardColor.NEGATIVE)
        if counter + 5 < len(name_list)  and counter == 0 :
            keyboard.add_button("Вперед ▶", color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button('В стартовое меню ➡', color=VkKeyboardColor.NEGATIVE)
        if counter + 5 >= len(name_list) and counter <= 0:
            keyboard.add_button('В стартовое меню ➡', color=VkKeyboardColor.NEGATIVE)

        vk.messages.send(
            message=f"""Список лидеров, для подробной информации выберете интересующего Вас человека """,
            peer_id=user_id,
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard()
            )
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Вперед ▶" and event.obj.text != 'В стартовое меню ➡' and event.obj.text != "Начать" and user_id == event.obj.from_id:
                self.leader_ceck(user_id, counter+ 5 , data , name_list)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "◀ Назад" and event.obj.text != 'В стартовое меню ➡' and event.obj.text != "Начать" and user_id == event.obj.from_id:
                self.leader_ceck(user_id, counter - 5, data, name_list)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == 'В стартовое меню ➡'  and event.obj.text != "Начать" and user_id == event.obj.from_id:
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text in name_list and event.obj.text != 'В стартовое меню ➡' and event.obj.text != "Начать" and user_id == event.obj.from_id:
                us_id = self.get_leader_id(event.obj.text, data)
                self.leader_info(user_id , 0 ,  us_id)
                break


    def leader_info(self, user_id , counter,  us_id):
        user_res = basa.user_resolution(us_id["id"])
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
            keyboard.add_button("◀ Назад", color=VkKeyboardColor.POSITIVE)
            keyboard.add_button("Вперед ▶", color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button('В стартовое меню ➡', color=VkKeyboardColor.NEGATIVE)
        if counter - 5 >= 0 and counter + 5 >= len(user_res_list):
            keyboard.add_button("◀ Назад", color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button('В стартовое меню ➡', color=VkKeyboardColor.NEGATIVE)
        if counter + 5 < len(user_res_list) and counter == 0:
            keyboard.add_button("Вперед ▶", color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button('В стартовое меню ➡', color=VkKeyboardColor.NEGATIVE)
        if counter + 5 >= len(user_res_list) and counter <= 0:
            keyboard.add_button('В стартовое меню ➡', color=VkKeyboardColor.NEGATIVE)

        vk.messages.send(
            message=f"""🙂 Имя:{us_id["name"]} \n🙂 Фамилия: {us_id["family"]}\n 📱 Номер телефона: {us_id["telephone"]}\n ℹ Информация о лидере: {us_id["decription"]}\n\n⬇ Ниже представлен список принятых решений \n""",
            peer_id=user_id,
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard()
        )
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Вперед ▶" and event.obj.text != 'В стартовое меню ➡' and event.obj.text != "Начать" and user_id == event.obj.from_id:
                self.leader_info(user_id, counter + 5 , us_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "◀ Назад" and event.obj.text != 'В стартовое меню ➡' and event.obj.text != "Начать" and user_id == event.obj.from_id:
                self.leader_info(user_id, counter + 5, us_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == 'В стартовое меню ➡'  and event.obj.text != "Начать" and user_id == event.obj.from_id:
                self.admin_menu(user_id)
                break
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text in user_res_list and event.obj.text != "Начать" and user_id == event.obj.from_id:
                res = self.get_res_info(event.obj.text, user_res)
                vk.messages.send(message = f"""Название:{res["name"]} \n Описание{res["description"]} \n """,
                                 peer_id = user_id ,
                                 random_id = get_random_id(),
                                 keyboard = keyboard.get_keyboard())
                break





    def get_leader_id(self, name , data):
        ud = name.split(" ")
        for d in data:
            if ud[0] == d["name"] and ud[1] ==d["family"]:
                return d

        return 0

    def get_us_list(self, data):
        res_list = []
        for d in data:
            res_list.append(d["name"])
        return res_list

    def get_res_info(self, name , res):
        for d in res:
            if name == d["name"]:
                return d

        return 0


    def get_rassilka(self, text, users):
        users.remove(164893000)
        vk.messages.send(
                message = text,
                peer_ids = users,
                random_id = get_random_id()
            )
































