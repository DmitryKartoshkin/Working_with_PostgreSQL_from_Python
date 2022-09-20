mport psycopg2
class Table:
    # Блок с приватными методами
    # Методы добавления
    def _add_personality(first_name, last_name):
        # Метод добавляет имя и фамилию
        cur.execute("""INSERT INTO notebook(first_name, last_name)
        VALUES (%s, %s);""", (first_name, last_name))
        conn.commit()
    def _add_email(email):
        # Функция добавляет email
        cur.execute("""INSERT INTO email(email) VALUES (%s);""", (email,))
        conn.commit()
    def _add_phone(phone_number):
        # Функция добавляет номер телефона
        cur.execute("""INSERT INTO phone(phone_number)
        VALUES (%s);""", (phone_number,))
        conn.commit()
    def _add_id_email_data(first_name, last_name, email):
        # Функция добавляет связь межу ФИО и email
        cur.execute("""INSERT INTO email_data(id_personality, id_email)
        VALUES(%s, %s);""",
        (Table._search_id_personality(first_name, last_name),
        Table._seach_id_email(email)))
        conn.commit()
    def _add_id_phone_data(first_name, last_name, phone_number):
        # Функция добавляет связь межу ФИО и телефонным номером
        cur.execute("""INSERT INTO phone_data(id_personality, id_phone)
        VALUES(%s, %s);""",
        (Table._search_id_personality(first_name, last_name),
         Table._search_id_phone(phone_number,)))
        conn.commit()
    # Методы поиска
    def _search_id_personality(first_name, last_name):
        # Функция находит id по указанным имени и фамилии
        cur.execute("""SELECT id_personality FROM notebook
        WHERE first_name = %s AND last_name = %s;""", (first_name, last_name))
        personality_id = cur.fetchone()[0]
        return personality_id
    def _seach_id_email(email):
        # Функция находит id по указанному email
        cur.execute("""SELECT id_email FROM email
        WHERE email = %s;""", (email,))
        email_id = cur.fetchone()[0]
        return email_id
    def _search_id_phone(phone_number):
        # Функция находит id по указанному номеру телефонаf
        cur.execute("""SELECT id_phone FROM phone
        WHERE phone_number = %s;""", (phone_number,))
        phone_id = cur.fetchone()[0]
        return phone_id
    def _search_id_phone_personality(first_name, last_name):
        # Метод находит id телефонного номера по указанным имени и фамилии
        cur.execute("""SELECT id_phone
        FROM notebook n 
        FULL JOIN phone_data pd USING(id_personality)
        FULL JOIN phone p USING(id_phone)
        WHERE first_name = %s AND last_name = %s;""", (first_name, last_name))
        phone_id = cur.fetchone()[0]
        return phone_id
    def _search_id_email_personality(first_name, last_name):
        # Метод находит id email по указанным имени и фамилии
        cur.execute("""SELECT id_email
        FROM notebook n
        FULL JOIN email_data ed USING(id_personality)
        FULL JOIN email e USING(id_email)
        WHERE first_name = %s AND last_name = %s;""", (first_name, last_name))
        email_id = cur.fetchone()
        return email_id
        # Методы обнавления
    def _update_phone(first_name, last_name, phone_number):
        # Метод обновления телефонного номера
        cur.execute("""UPDATE phone SET phone_number = %s
        WHERE id_phone = %s;""",
        (phone_number, Table._search_id_phone_personality(first_name, last_name)))
        conn.commit()
    def _update_email(first_name, last_name, email):
        # Метод обновления email
        cur.execute("""UPDATE email SET email = %s WHERE id_email = %s;""",
        (email, Table._search_id_email_personality(first_name, last_name)))
        conn.commit()

    # Основной блок
    def __init__(self, first_name=None, last_name=None, phone_number=None, email=None):
        """  При инициализации экземпляра класса в базу данных вносится
        принятые аргументы, согласно прописанной логике."""
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        if self.email == None and self.phone_number == None:
            Table._add_personality(first_name, last_name)
            conn.commit()
        elif self.email == None and self.phone_number != None:
            Table._add_personality(first_name, last_name)
            Table._add_phone(phone_number)
            conn.commit()
            Table._add_id_phone_data(first_name, last_name, phone_number)

            conn.commit()
        elif self.email != None and self.phone_number == None:
            Table._add_personality(first_name, last_name)
            Table._add_email(email)
            conn.commit()
            Table._add_id_email_data(first_name, last_name, email)
            conn.commit()
        else:
            Table._add_personality(first_name, last_name)
            Table._add_email(email)
            Table._add_phone(phone_number)
            conn.commit()
            Table._add_id_phone_data(first_name, last_name, phone_number)
            Table._add_id_email_data(first_name, last_name, email)
            conn.commit()
        print('Данные внесены')
    def customer_base():
        """Функция, создающая структуру БД (таблицы)"""
        cur.execute("""CREATE TABLE IF NOT EXISTS notebook(
                               id_personality SERIAL PRIMARY KEY,
                               first_name VARCHAR(20) NOT null,
                               last_name VARCHAR(20) NOT null);"""
                    )
        cur.execute("""CREATE TABLE IF NOT EXISTS email(
                               id_email SERIAL PRIMARY KEY,
                               email VARCHAR(30) UNIQUE);"""
                    )
        cur.execute("""CREATE TABLE IF NOT EXISTS phone(
                               id_phone SERIAL PRIMARY KEY,
                               phone_number BIGINT UNIQUE);"""
                    )
        conn.commit()
        cur.execute("""CREATE TABLE IF NOT EXISTS email_data(
                               id_personality INTEGER,
                               id_email INTEGER,
                               FOREIGN KEY (id_personality) REFERENCES notebook(id_personality),
                               FOREIGN KEY (id_email) REFERENCES email(id_email) OON DELETE CASCADE);"""
                    )
        cur.execute("""CREATE TABLE IF NOT EXISTS phone_data(
                               id_personality INTEGER,
                               id_phone INTEGER,
                               FOREIGN KEY (id_personality) REFERENCES notebook(id_personality),
                               FOREIGN KEY (id_phone) REFERENCES phone(id_phone) ON DELETE CASCADE);"""
                    )
        conn.commit()
        print('Структура БД создана')
    def add_phone_personality(first_name, last_name, phone_number):
        """Метод, позволяющая добавить телефон для существующего клиента"""
        Table._add_phone(phone_number)
        conn.commit()
        Table._search_id_phone(phone_number)
        Table._add_id_phone_data(first_name, last_name, phone_number)
        conn.commit()
        print('Номер телефона добавлен')
    def update_personality(first_name, last_name, email=None, phone_number=None):
        """Метод, позволяющая изменить данные о клиенте согласно принятым аргументам"""
        if email == None and phone_number == None:
            return "Нет данных для изменения"
        elif email == None and phone_number != None:
            Table._update_phone(first_name, last_name, phone_number)
            conn.commit()
            return 'Данные обновлены'
        elif email != None and phone_number == None:
            Table._update_email(first_name, last_name, email)
            conn.commit()
            return 'Данные обновлены'
        else:
            Table._update_phone(first_name, last_name, phone_number)
            Table._update_email(first_name, last_name, email)
            conn.commit()
            return 'Данные обновлены'
    def delet_phone(first_name, last_name):
        """Метод, позволяющий удалить номер телефона для клиента"""

        cur.execute("""DELETE FROM phone WHERE id_phone = %s;""",
        (Table._search_id_phone_personality(first_name, last_name),))
        conn.commit()
    def delet_personality(first_name, last_name):
        """Метод, позволяющий удалить клиента из базы данных"""
        cur.execute("""DELETE FROM phone WHERE id_phone = %s;""",
        (Table._search_id_phone_personality(first_name, last_name),))
        cur.execute("""DELETE FROM email WHERE id_email = %s;""",
        (Table._search_id_email_personality(first_name, last_name),))
        cur.execute("""DELETE FROM notebook WHERE id_personality = %s;""",
        (Table._search_id_personality(first_name, last_name),))
        conn.commit()
    def search_data(first_name= None, last_name = None, phone_number=None, email=None):
        """ Функция, позволяющая найти клиента по его данным (имени, фамилии, email или телефону)"""
        if email == None and phone_number == None:
            cur.execute("""SELECT n.first_name, n.last_name, p.phone_number, e.email 
            FROM notebook n 
            FULL JOIN email_data ed USING(id_personality) 
            FULL JOIN email e USING(id_email) 
            FULL JOIN phone_data pd USING(id_personality)
            FULL JOIN phone p USING(id_phone)
            WHERE first_name = %s AND last_name = %s;""", (first_name, last_name))
            data = cur.fetchall()
            return data
        elif email != None:
            cur.execute("""SELECT n.first_name, n.last_name, p.phone_number, e.email 
            FROM notebook n 
            FULL JOIN email_data ed USING(id_personality) 
            FULL JOIN email e USING(id_email) 
            FULL JOIN phone_data pd USING(id_personality)
            FULL JOIN phone p USING(id_phone)
            WHERE email = %s;""", (email,))
            data = cur.fetchall()
            return data
        elif phone_number != None:
            cur.execute("""SELECT n.first_name, n.last_name, p.phone_number, e.email 
            FROM notebook n 
            FULL JOIN email_data ed USING(id_personality) 
            FULL JOIN email e USING(id_email) 
            FULL JOIN phone_data pd USING(id_personality)
            FULL JOIN phone p USING(id_phone)
            WHERE phone_number = %s;""", (phone_number,))
            data = cur.fetchall()
            return data

with open('password.txt', 'r') as file_object:
    password_data_base = file_object.readline().strip()


conn = psycopg2.connect(database='netologu_db', user='postgres', password=password_data_base)
print("База данных успешно открыта")
with conn.cursor() as cur:

conn.close()
