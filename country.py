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

result = cursor.execute("""SELECT mi.country, AVG(mr.score) AS score_avg FROM movie_info AS mi, movie_release AS mr WHERE mi.name = mr.movie_info_name GROUP BY mi.country HAVING COUNT(*) > 5 ORDER BY AVG(mr.score) DESC;""")

film_db = {}

# print(result.fetchall())

for i in result.fetchall():
    # print(i[1])
    film_db[i[0]] = i[1]
fig = plt.figure(figsize = (10, 7))

plt.bar(film_db.keys(), film_db.values(), color ='maroon',
        width = 0.4)
plt.xticks(rotation='vertical')
plt.ylabel("IMDB Score")
plt.xlabel("Country")
plt.title("Average Film Score By Country")
plt.show()

cursor.close()
db.close()
