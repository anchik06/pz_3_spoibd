import mysql.connector


class SQL:
    def __init__(self, db_config, table_name):
        self.conn = mysql.connector.connect(**db_config)
        self.db_config = db_config
        self.table_name = table_name
        self.cursor = self.conn.cursor()
        self.columns = []

    # создаём таблицу, если она не существует, с автоматически увеличивающимся первичным ключом
    def create_table(self, columns):
        column_definition = ', '.join(f"`{name}` {type}" for name, type in columns.items())
        query = f'''
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
             {column_definition}
                )
                '''
        cursor = self.conn.cursor()
        try:
            cursor.execute(query)
            self.conn.commit()
        finally:
            cursor.close()
        print(f"таблица '{self.table_name}' cсоздана с колонаками {self.columns}")

    # получает список колонок
    def update_column(self):
        query = f"SHOW COLUMNS FROM {self.table_name}"
        self.cursor.execute(query)
        self.columns = [row[0] for row in self.cursor.fetchall()]

    # ищет похожую таблицу, если она есть
    def check_table_exist(self, table_name):
        query = f"SHOW TABLES LIKE '{self.table_name}'"
        self.cursor.execute(query)
        return self.cursor.fetchone() is not None

    # удаляет таблицу
    def drop_table(self):
        cursor = self.conn.cursor()
        try:
            query = f"DROP TABLE IF EXISTS {self.table_name}"
            cursor.execute(query)
            self.conn.commit()
        finally:
            cursor.close()
        print(f"таблтца '{self.table_name}' удалена")

    # чтение данных
    def select_table(self, columns='*', where=None):
        query = f"SELECT {columns} FROM `{self.table_name}`"
        if where:
            query += f" WHERE {where}"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"ошибка при выборке данных: {err}")
            return []

    # заполняем таблицу
    def insert(self, data):
        if not data:
            print("нет данных для вставки")
            return
        columns = ', '.join(f"`{key}`" for key in data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO `{self.table_name}` ({columns}) VALUES ({placeholders})"
        try:
            self.cursor.execute(query, tuple(data.values()))
            self.conn.commit()
            print(f"добавлена запись в таблицу '{self.table_name}'")
        except mysql.connector.Error as err:
            print(f"что-то пошло не так: {err}")

    def close (self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()



db_config = {
    'host': "srv221-h-st.jino.ru",
    'database': "j30084097_137",
    'user': "j30084097_137",
    'password': "Gruppa137"}

if __name__ == "__main__":
    db = SQL(db_config, "fridge")
    cols = {
        "type_of_product": "VARCHAR(50)",
        "product": "VARCHAR(100)",
        "quantity": "INT"
    }
    db.create_table(cols)

    db.insert({"type_of_product": "молочка", "product": "йогурт", "quantity": 5})
    db.insert({"type_of_product": "овощи", "product": "помидор", "quantity": 3})
    db.insert({"type_of_product": "фрукты", "product": "банан", "quantity": 2})

    db.close()