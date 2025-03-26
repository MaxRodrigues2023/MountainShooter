import sqlite3
from typing import List, Dict, Tuple

class DBProxy:
    def __init__(self, db_name: str):
        self.connection = sqlite3.connect(f'{db_name}.db')
        self._create_table()

    def _create_table(self):
        self.connection.execute('''
            CREATE TABLE IF NOT EXISTS dados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                score INTEGER NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def save(self, score_dict: Dict[str, str]):
        try:
            self.connection.execute(
                'INSERT INTO dados (name, score, date) VALUES (:name, :score, :date)',
                score_dict
            )
            self.connection.commit()
        except Exception as e:
            print(f"Error saving score: {e}")
            raise

    def retrieve_top10(self) -> List[Tuple]:
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT id, name, score, date 
            FROM dados 
            ORDER BY score DESC 
            LIMIT 10
        ''')
        return cursor.fetchall()

    def close(self):
        self.connection.close()




# import sqlite3
#
# class DBProxy:
#
#
#         self.db_name = db_name
#         self.connection = sqlite3.connect(db_name)
#         self.connection.execute('''
#                                   CREATE TABLE IF NOT EXISTS dados(
#                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
#                                   name TEXT NOT NULL,
#                                   score INTEGER NOT NULL,
#                                   date TEXT NOT NULL)
#                                '''
#                                )
#
#     def save(self, score_dict: dict):
#         self.connection.execute('INSERT INTO dados (name, score, date) VALUES (:name, : score, : date)', score_dict)
#         self.connection.commit()
#     def retrieve_top10(self) -> list:
#         return self.connection.execute('SELECT * FROM dados ORDER BY score DESC LIMIT 10').fetchall()
#     def close(self):
#         return self.connection.close()