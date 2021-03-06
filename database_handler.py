
from objects import House
import sqlite3

class DatabaseHandler(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.__database__ = 'example.db'


    def is_comment_answered(self, comment_id):
        connection = sqlite3.connect(self.__database__)
        cursor = connection.cursor()

        t = (comment_id,)
        cursor.execute('SELECT* FROM answered_comments WHERE comment_id=?', t)
        row = cursor.fetchone()

        connection.close()

        return row != None

    def set_comment_as_answered(self, comment_id):
        connection = sqlite3.connect(self.__database__)
        cursor = connection.cursor()

        t = (comment_id,)
        cursor.execute('INSERT INTO answered_comments VALUES (?)', t)
        connection.commit()

        connection.close()

    def get_houses(self, houseName):
        connection = sqlite3.connect(self.__database__)

        #Encapsulate the rows so we can index with strings later on
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        #Create a tuple so we can use the safe ?-method
        t = (houseName+'%',)
        cursor.execute('SELECT* FROM house WHERE name LIKE ?', t)

        rows = cursor.fetchall()

        houses = []

        for row in rows:
            if row != None:
                house = None
                house = House()
                house.name = row['name']
                house.coat_of_arms = row['coat_of_arms']
                house.words = row['words']
                house.cadet_branch = row['cadet_branch']
                house.seat = row['seat']
                house.current_lord = row['current_lord']
                house.region = row['region']
                house.title = row['title']
                house.heir = row['heir']
                house.overlord = row['overlord']
                house.founder = row['founder']
                house.founded = row['founded']
                houses.append(house)

        connection.close()

        return houses