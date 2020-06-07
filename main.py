from vk_api.bot_longpoll import VkBotEventType
from config import longpoll , vk_session , vk, get_random_id, admin_user_id
from _thread import start_new_thread
from admin import Admin
from user import userClass
from complete_voiting import voiting

def main():
     start_new_thread(voiting, ())
     print("Зашло")
     for event in longpoll.listen():
         if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text == "Начать":
             if event.obj.from_id == admin_user_id:
                 start_new_thread(Admin, (event.obj.from_id, ))
             else:
                 start_new_thread(userClass, (event.obj.from_id, ))



if __name__ == '__main__':

    main()