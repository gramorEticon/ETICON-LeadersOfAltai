import psycopg2
import Levenshtein

class DataBase:
    def __init__(self):

        try:
            self.conn = psycopg2.connect(dbname="**********",
                                         user="**********",
                                         password="**********",
                                         host="**********",
                                         port=5432)

            self.cursor = self.conn.cursor()
            print("Connection sucsesfull!")

        except psycopg2.Error as err:
            print("Connection error: {}".format(err))


    def registration_user(self, name, family, description, vk_id, telephone):

        self.cursor.execute(f"""INSERT INTO
                                    public.users(name, description, vk_id, telephone, family)
                                VALUES
                                    ('{name}', '{description}', '{vk_id}', '{telephone}', '{family}');""")

        self.conn.commit()


    def get_user(self, vk_id):

        self.cursor.execute(f"""SELECT *
                                FROM 
                                    public.users
                                WHERE
                                    vk_id = '{vk_id}';""")
        data = self.cursor.fetchone()
        return data


    def new_resolution_admin(self, name, desc, date, link, chat_id):

        self.cursor.execute(f"""INSERT INTO
                                    resolution(name, description, date, link, admin_invite, finish, chat_id)
                                VALUES
                                    ('{name}', '{desc}', '{date}', '{link}', true, false, '{chat_id}');""")

        self.conn.commit()


    def new_resolution_user(self, name, desc, link, chat_id):

        self.cursor.execute(f"""INSERT INTO
                                    resolution(name, description, admin_invite, finish, link, chat_id)
                                VALUES
                                    ('{name}', '{desc}', false, false, '{link}', '{chat_id}');""")

        self.conn.commit()


    def accept_resolution(self, resolution_id, date):

        self.cursor.execute(f"""UPDATE
                                    resolution
                                SET
                                    admin_invite = true,
                                    date = '{date}'
                                WHERE
                                    id = {resolution_id};""")
        self.conn.commit()


    def delete_resolution(self, resolution_id):

        self.cursor.execute(f"""DELETE FROM
                                    resolution
                                WHERE
                                    id = {resolution_id};""")

        self.conn.commit()


    def new_document(self, chat_id, file_link, name):

        self.cursor.execute(f"""INSERT INTO
                                    document(chat_id, file_link, name)
                                VALUES
                                    ('{chat_id}','{file_link}','{name}');""")

        self.conn.commit()


    def chek_user(self, user_id):

        self.cursor.execute(f"""SELECT *
                                FROM
                                    public.users
                                WHERE
                                    vk_id = '{user_id}';""")

        data = self.cursor.fetchone()

        if data is None:
            return False
        else:
            return True


    def chek_voice(self, user_id):

        self.cursor.execute(f"""SELECT *
                                FROM
                                    voice
                                WHERE
                                    voice_who = '{user_id}';""")

        data = self.cursor.fetchone()

        if data is None:
            return True
        else:
            return False


    def give_voite(self, who_id, to_id):

        if not self.chek_voice(who_id):

            self.cursor.execute(f"""INSERT INTO
                                        voice(voice_who, voice_to)          
                                    VALUES
                                        ('{who_id}','{to_id + ","}');""")
        else:

            self.cursor.execute(f"""INSERT INTO
                                        voice(voice_who, voice_to)
                                    VALUES
                                       ('{who_id}','{to_id + ","}');""")

            self.cursor.execute(f"""SELECT 
                                        voice_who, voice_to
                                    FROM
                                        voice;""")

            data = self.cursor.fetchall()

            for elem in data:
                if elem[1].split(',')[-2] == who_id:
                    self.cursor.execute(f"""UPDATE
                                                voice
                                            SET
                                                voice_to = '{elem[1] + to_id + ","}'
                                            WHERE
                                                voice_who = '{elem[0]}';""")

        self.conn.commit()




    def pickup_voice(self, who_id):

        self.cursor.execute(f"""DELETE FROM
                                    voice
                                WHERE
                                    voice_who = '{who_id}';""")

        self.cursor.execute(f"""SELECT 
                                    voice_who, voice_to
                                FROM
                                    voice;""")

        data = self.cursor.fetchall()
        for elem in data:
            arr = elem[1].split(',')
            if who_id in arr:
                index = arr.index(who_id)
                arr = arr[:index + 1]
                s = ""
                for item in arr:
                    s = s + item + ","

                self.cursor.execute(f"""UPDATE
                                            voice
                                        SET
                                            voice_to = '{s}'
                                        WHERE
                                            voice_who = '{elem[0]}';""")

        self.conn.commit()




    def voiting(self, user_id, resolution_id, za):

        if za:
            string = 'true'
        else:
            string = 'false'

        self.cursor.execute(f"""INSERT INTO
                                    voiting(user_id, resolution_id, za)
                                VALUES
                                    ('{user_id}','{resolution_id}', {string});""")

        self.conn.commit()


    def who_give_voice(self, user_id):

        self.cursor.execute(f"""SELECT 
                                    voice_to
                                FROM
                                    voice
                                WHERE
                                    voice_who = '{user_id}';""")

        data = self.cursor.fetchone()[0]
        return data

    def to_give_voice(self, user_id):

        self.cursor.execute(f"""SELECT 
                                    voice_who, voice_to
                                FROM
                                    voice;""")

        data = self.cursor.fetchall()
        arr = []

        for elem in data:
            if elem[1].split(',')[-2] == user_id:
                arr.append(elem[0])

        return arr


    def count_giving(self, user_id):

        self.cursor.execute(f"""SELECT 
                                    voice_to
                                FROM
                                    voice;""")

        data = self.cursor.fetchall()
        count = 1
        for elem in data:
            if elem[0].split(',')[-2] == user_id:
                count = count + 1

        return count



    def get_user_resolution(self):

        self.cursor.execute(f"""SELECT *
                                FROM
                                    resolution
                                WHERE
                                    admin_invite = false;""")
        data = self.cursor.fetchall()
        return data

    def get_user_resolution_comlite(self):

        self.cursor.execute(f"""SELECT *
                                FROM
                                    resolution
                                WHERE
                                    admin_invite = true AND finish = false;""")
        data = self.cursor.fetchall()
        return data

    def get_all_resolution(self, user_id):

        self.cursor.execute(f"""SELECT *
                                FROM
                                    resolution
                                WHERE
                                    finish = false;""")
        data = self.cursor.fetchall()

        self.cursor.execute(f"""SELECT
                                    resolution_id
                                FROM
                                    voiting
                                WHERE
                                    user_id = '{user_id}';""")
        ids = self.cursor.fetchall()

        arr = []
        for elem in ids:
            arr.append(elem[0])

        z =[]
        for elem in data:
            if elem[0] not in arr:
                z.append(elem)
        return z


    def itog_voiting(self, resolution_id):
        za = 0
        protiv = 0

        self.cursor.execute(f"""SELECT
                                    user_id
                                FROM
                                    voiting
                                WHERE
                                    resolution_id = {resolution_id}
                                    AND 
                                    za = true;""")

        data = self.cursor.fetchall()
        for elem in data:
            za = za + self.count_giving(elem[0])

        self.cursor.execute(f"""SELECT
                                    user_id
                                FROM
                                    voiting
                                WHERE
                                    resolution_id = {resolution_id}
                                    AND 
                                    za = false;""")

        data = self.cursor.fetchall()
        for elem in data:
            protiv = protiv + self.count_giving(elem[0])

        self.cursor.execute(f"""UPDATE
                                    resolution
                                SET
                                    finish = true
                                WHERE
                                    id = {resolution_id};""")
        self.conn.commit()

        return za, protiv



    def best_of_the_best(self):

        self.cursor.execute("""SELECT *
                                FROM
                                    public.users;""")

        data = self.cursor.fetchall()
        a = []

        for elem in data:
            count = self.count_giving(elem[0])
            loc = []
            loc.append(count)
            d = {}
            d['id'] = elem[0]
            d['decription'] = elem[1]
            d['name'] = elem[2]
            d['telephone'] = elem[3]
            d['family'] = elem[4]
            loc.append(d)
            if len(a) > 1:
                for i in range(0, len(a) - 1, 1):
                    if count < a[-1][0]:
                        a.append(loc)
                        break
                    if count > a[0][0]:
                        a.insert(0, loc)
                        break
                    if count < a[i][0] and count >= a[i + 1][0]:
                        a.insert(i + 1, loc)
                        break
                    if count <= a[i][0] and count >= a[i + 1][0]:
                        a.insert(i + 1, loc)
                        break
            elif len(a) == 1:
                if count <= a[0][0]:
                    a.append(loc)
                    continue
                else:
                    a.insert(0, loc)
                    continue
            else:
                a.append(loc)
                continue
        return a


    def user_resolution(self, user_id):
        self.cursor.execute(f"""SELECT
                                    r.name, r.description,v.za, r.id
                                FROM
                                    resolution AS r
                                INNER JOIN
                                    voiting AS v
                                ON
                                    r.id = v.resolution_id
                                WHERE
                                    v.user_id = '{user_id}';""")
        data = self.cursor.fetchall()
        arr = []
        for elem in data:
            d = {}
            d["name"] = elem[0]
            d["description"] = elem[1]
            d["result"] = elem[2]
            d["id"] = elem[3]
            arr.append(d)

        return arr

    def find_user(self, family):
        self.cursor.execute(f"""SELECT *
                                FROM 
                                    public.users;""")
        data = self.cursor.fetchall()

        arr =[]

        for elem in data:
            if Levenshtein.ratio(elem[4], family) > 0.6:
                arr.append(elem)

        return arr


    def get_all_id(self):
        try:
            self.cursor.execute(f"""SELECT vk_id
                                    FROM 
                                        public.users;""")
            id_ = self.cursor.fetchall()

            self.cursor.execute(f"""SELECT 
                                        voice_who
                                    FROM 
                                        voice;""")

            who = self.cursor.fetchall()

            ids = []
            for elem in who:
                ids.append(elem[0])

            arr =[]

            for elem in id_:
                if elem[0] not in ids:
                    arr.append(int(elem[0]))

            return arr
        except psycopg2.ProgrammingError:
            self.get_all_id()

    def get_resolution(self, id_):

        self.cursor.execute(f"""SELECT *
                                FROM
                                    resolution
                                WHERE
                                    id = {id_};""")
        data = self.cursor.fetchone()
        return data














