import getpass
import pg8000
import matplotlib.pyplot as plt

# Used from Project 8
login = input('login: ')
secret = getpass.getpass('password: ')

credentials = {'user'    : login, 
               'password': secret, 
               'database': 'csci403',
               'port'    : 5433,
               'host'    : 'codd.mines.edu'}

try:
    db = pg8000.connect(**credentials)
except pg8000.Error as e:
    print('Database error: ', e.args[0]["M"])
    exit()

cursor = db.cursor()