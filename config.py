from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
import random
from db import DataBase
token = "**********"
vk_session = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk_session, '**********')
vk = vk_session.get_api()
admin_user_id = **********
basa = DataBase()
def get_random_id():
    return random.randint(0,1000000)


