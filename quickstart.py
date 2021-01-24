"""
Start timer?
1. Read score from arduino
2. Record that there was a score
3. Input data into google sheets
4. Either
    a. google sheets chart updating
    b. create user interface that shows score
5. If score changes send score to other player
6. Show led display other player has scored
"""
import mysql.connector
from mysql.connector import Error
import sys
import time
import serial

HOST = 'sql3.freemysqlhosting.net'
DATABASE = 'sql3388722'
USER = 'sql3388722'
PASSWORD = 'Ibu7TM7rtV'

def open_connection():
    connection = connect_sql()
    cursor = create_cursor(connection)
    return connection, cursor 

def close_connection(connection, cursor):
    connection.close()
    cursor.close()

def connect_sql():
    try:
        connection = mysql.connector.connect(host=HOST,
                                            database=DATABASE,
                                            user=USER,
                                            password=PASSWORD)
        return connection
    except Error as e: print("Error while connecting to MySQL", e)

def create_cursor(connection):
    try: return connection.cursor(buffered=True)
    except: print("Error creating cursor for connection.")

def create_table(connection, cursor):
    """ Create table for game
    """
    cursor.execute("CREATE TABLE IF NOT EXISTS Game (name VARCHAR(255), score int)")

def show_table(cursor):
    """ Displays all the rows in the table
    """
    cursor.execute("SELECT * FROM Game")
    result = cursor.fetchall()
    print("Player Scores: ")
    for row in result:
        print(row) 
        print(' | '.join(map(str, row)))
    return len(result)

def add_row(connection, cursor, name, score):
    """ Create a new row in the table
    """
    sql = 'INSERT INTO Game (name, score) VALUES (%s, %s)'
    val = (name, score)
    cursor.execute(sql, val)
    connection.commit()

def reset_scores(connection, cursor):
    """ Reset the score of both players to zero
    """
    cursor.execute("UPDATE Game SET score=0")
    connection.commit()

def update_score(connection, cursor, name, score):
    """ Change the score of a particular player in the table
    """
    sql = "UPDATE Game SET score = %s WHERE name = %s"
    val = (str(score), name)
    cursor.execute(sql, val)
    connection.commit()

def declare_winner(connection, cursor, name):
    """ Compares the scores of both players to determine who has won
    """
    cursor.execute("SELECT * FROM Game")
    result = cursor.fetchall()
    for tup in result:
        print(tup)
        if(tup[0] == name and tup[1] == 1):
            return True
    return False


def initialize_table(connection, cursor, name1, name2):
    """ Delete previous table and initialize name of two new players
    """
    cursor.execute("DROP TABLE Game")
    create_table(connection, cursor)
    add_row(connection, cursor, name1, 0)
    add_row(connection, cursor, name2, 0)

def test(): # Delete table to reset sql table
    connection, cursor = open_connection()
    initialize_table(connection, cursor, "player1", "player2")
    # cursor.execute("DROP TABLE Game")
    # create_table(connection, cursor)
    # add_row(connection, cursor, "Luisa", 0)
    # add_row(connection, cursor, "Faith", 0)
    cursor.execute("SELECT * FROM Game")
    result = cursor.fetchall()
    print(result)
    reset_scores(connection, cursor)
    print(declare_winner(connection, cursor, 'player1'))
    connection.commit()
    close_connection(connection, cursor)

def main():
    ser = serial.Serial('COM4', 9600)
    while 1:
        connection, cursor = open_connection()
        val = ser.readline()
        if val == "player1":
            cursor.execute("UPDATE Game SET score=1 WHERE name = player1")
        time.sleep(.5)
        if(declare_winner(connection, cursor, "player2")):
            ser.write("player2")
        close_connection(connection, cursor)


if __name__ == '__main__':
    main()