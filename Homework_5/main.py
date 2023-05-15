import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS clients (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(40) NOT NULL,
        last_name VARCHAR(40) NOT NULL,
        email VARCHAR(40) UNIQUE NOT NULL 
        );
        CREATE TABLE IF NOT EXISTS phones (
        client_id INTEGER NOT NULL REFERENCES clients (id) ON DELETE CASCADE,
        phone VARCHAR(40) UNIQUE NOT NULL,
        CONSTRAINT client_phone_pk PRIMARY KEY (client_id, phone)
        );
        ''')
        print('В базе данных созданы таблицы: "clients", "phones"')


def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO clients (first_name, last_name, email)
        VALUES (%s, %s, %s) RETURNING id;
        ''', (first_name, last_name, email))
        client_id = cur.fetchone()[0]
        print(f'В базу данных добавлен новый клиент c id - {client_id}')
        if phones:
            for phone in phones:
                add_phone(conn, client_id, phone)


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO phones (client_id, phone)
        VALUES (%s, %s);
        ''', (client_id, phone))
    print(f'В базу данных клиенту: {client_id} - добавлен телефон: {phone}')


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    info_dict = {'first_name': first_name, 'last_name': last_name, 'email': email}
    change_list = []
    for key, value in info_dict.items():
        if value:
            change_list.append(f"{key} = '{value}'")
    change_info = ",".join(change_list)
    sql_request = f'''
        UPDATE clients SET {change_info}
        WHERE id = {client_id};
        '''
    with conn.cursor() as cur:
        if change_info:
            cur.execute(sql_request)
        if phones:
            cur.execute('''
            SELECT phone FROM phones
            WHERE client_id=%s ''', (client_id,))
            client_phones = cur.fetchall()
            for i in (client_phones):
                for phones_numb in list(i):
                    if phones_numb == phones[0]:
                        cur.execute('''
                                    UPDATE phones SET phone=%s
                                    WHERE client_id=%s AND phone=%s;
                                    ''', (phones[1], client_id, phones[0]))
    print(f'В базе данных внесены изменения в данные клиента с id: {client_id} ')


def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute('''
        SELECT phone FROM phones
        WHERE client_id=%s AND phone=%s;
        ''', (client_id, phone))
        client_phones = cur.fetchall()
        if client_phones:
            cur.execute('''
            DELETE FROM phones 
            WHERE client_id=%s AND phone=%s;
            ''', (client_id, phone))
            print(f'Телефон {phone} клиента с id {client_id} - удален из базы данных')
        else:
            print(f'Телефон {phone} клиента с id {client_id} не существует в базе данных')


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute('''
        DELETE FROM clients WHERE id=%s;
        ''', (client_id,))
        print(f'Клиент с id {client_id} удален из базы данных')


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    info_dict = {'first_name': first_name, 'last_name': last_name, 'email': email, 'phone': phone}
    find_list = []
    for key, value in info_dict.items():
        if value:
            find_list.append(f"{key} = '{value}'")
    find_client = " AND ".join(find_list)
    sql_request = f'''
        SELECT DISTINCT c.id, c.first_name, c.last_name FROM phones AS p
        JOIN clients AS c ON p.client_id = c.id
        WHERE {find_client};
        '''
    with conn.cursor() as cur:
        cur.execute(sql_request)
        print(f'В базе данных найден клиент: {cur.fetchall()}')


if __name__ == '__main__':
    with psycopg2.connect(database='clientsbd', user='postgres', password='postgres') as connect:
        try:
            create_db(connect)
            add_client(connect, first_name='Анна', last_name='Каренина', email='a_karenina@gmail.com',
                       phones=('+799584624581', '+789995854671'))
            add_client(connect, first_name='Алексей', last_name='Вронский', email='vronsky@gmail.com')
            add_client(connect, first_name='Константин', last_name='Левин', email='klevin@gmail.com')
            add_client(connect, first_name='Алексей', last_name='Каренин', email='karenin_alexei@gmail.com')
            add_phone(connect, client_id=2, phone='+72123245875')
            add_phone(connect, client_id=3, phone='+79999215234')
            change_client(connect, client_id=3, last_name='Лёвин', email='levin@gmail.com')
            # Первый телефон в списке - тот, что заменяем, второй - на которой меняем
            change_client(connect, client_id=1, phones=['+789995854671', '+7498565866687'])
            delete_client(connect, client_id=4)
            delete_phone(connect, client_id=1, phone='+799584624581')
            find_client(connect, email='a_karenina@gmail.com')
        except psycopg2.Error as er:
            print(f'ERROR: {er}')
    connect.close()
