import getpass
import pg8000
import csv
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

result = cursor.execute("""SELECT mr.release as release_date,SUM(mr.score) AS score_sum, COUNT(mr.release) FROM movie_release AS mr GROUP BY release_date ORDER BY release_date;""")

film_db = {}

for i in result.fetchall():
    film_db[i[0]] = i[1] / i[2]
fig = plt.figure(figsize = (10, 5))

plt.bar(film_db.keys(), film_db.values(), color ='maroon',
        width = 0.4)
plt.xlabel("Year Released")
plt.ylabel("Average imdb score")
plt.title("Average Film Score In Each Year")
plt.show()

cursor.close()
db.close()
