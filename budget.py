import getpass
import pg8000
import matplotlib.pyplot as plt

#Question: How does budget affect a movie's gross and score?

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

query = """SELECT budget, gross, score
        FROM movie_info, movie_release
        WHERE movie_info_name = name AND movie_info_director = director
            AND budget IS NOT NULL 
            AND gross IS NOT NULL
            AND score IS NOT NULL
        ORDER BY budget
        """
cursor.execute(query)
results = cursor.fetchall()
budget = []
gross = []
score = []

for arr in results:
    budget += [arr[0]]
    gross += [arr[1]]
    score += [arr[2]]

figure, axis = plt.subplots(1, 2)
axis[0].scatter(budget, gross, color='green', alpha = 0.1)
axis[0].xlabel("budget ($)")
axis[0].ylabel("gross ($)")
axis[0]

axis[1].scatter(budget, score, color='red', alpha=0.1)
plt.show()

cursor.close()
db.close()