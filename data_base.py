import sqlite3

class DataBase:
    def __init__(self):
        self.db_path = "bd_sqlite.db"
        self.table_name = "rankings"
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_path) as conexion:
            conexion.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} (id integer primary key autoincrement not null, player TEXT,score INTEGER);")

    def insert_score(self, player, score):
        try:
            with sqlite3.connect(self.db_path) as conexion:
                conexion.execute(f"INSERT INTO {self.table_name}(player, score) VALUES('{player}', '{score}')")
                conexion.commit()
                print("piola")
        except sqlite3.Error as e:
            print(f"Error al ejecutar INSERT: {e}")

    def select_scores(self):
        cursor = None
        try:
            with sqlite3.connect(self.db_path) as conexion:
                cursor = conexion.execute(f"SELECT player, score FROM {self.table_name} ORDER BY score DESC LIMIT 5;")
                score_list = cursor.fetchall()
                return score_list
        except sqlite3.Error as e:
            print(f"Error al ejecutar SELECT: {e}")
            return None
        finally:
            if cursor:
                cursor.close()