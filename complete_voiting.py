import requests
from time import sleep
from config import basa
import datetime


def voiting():
    while True:
        data = basa.get_user_resolution_comlite()

        for d in data:
            if d[3]!= None:
                t = get_data(d)
                if t < datetime.datetime.now():
                    try:
                        za, protiv = basa.itog_voiting(d[0])

                        za_p = int(za / (za + protiv) * 100)
                        text = "❗❗❗ Инициатива: " + str(d[1]) + "\n\n 📋 Описание инициативы: " + str(d[2]) + "\n\n📄 Ссылка на документ: " + str(
                            d[4]) + "\n\n👍 Проголосовало \"За\": " + str(za) + " чел. - " + str(za_p) + "%" + "\n👎 Проголосовало \"Против\": " + str(protiv) + " чел. - " + str(100 - za_p) + "%"
                        post(text)
                    except ZeroDivisionError:
                        voiting()
        sleep(30)


def get_data(data):
    dat = data[3].split(".")
    d = datetime.date(int(dat[2]), int(dat[1]), int(dat[0]))
    t = datetime.time(int(dat[3]), int(dat[4]))
    return datetime.datetime.combine(d, t)


def post(text):
    token = "**********"

    params = (
        ('owner_id', '**********'),
        ('from_group', '1'),
        ('message', text),
        ('access_token', token),
        ('v', '5.70'),
    )

    response = requests.get('https://api.vk.com/method/wall.post', params=params)
