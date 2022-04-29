import getpass
import pg8000
import csv

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

#get rid of any preexisting tables
cursor.execute(
    """
    DROP TABLE IF EXISTS movie cascade;
    DROP TABLE IF EXISTS movie_release cascade;
    """
)

#create the movie_info table
cursor.execute(
    """CREATE TABLE movie_info
    (
        name TEXT,
        rating TEXT,
        genre TEXT,
        director TEXT,
        writer TEXT,
        star TEXT,
        country TEXT,
        budget BIGINT,
        gross BIGINT,
        company TEXT,
        runtime INT,

        primary key (name, director)
    )
    """
)

#create the movie_release table
cursor.execute(
    """CREATE TABLE movie_release
    (
        movie_info_name TEXT,
        movie_info_director TEXT,
        release NUMERIC(4, 0),
        score NUMERIC(2,1),
        votes INT,

        foreign key (movie_info_name, movie_info_director) references movie_info(name, director)
    )
    """
)

#helper function that transforms raw data into psql formatted integers
def make_int(string):
    if len(string) > 0:
        return string[:-2]
    else:
        return None

#helper function that transforms raw data into psql formatted numeric
def make_num(string):
    try:
        float(string)
        return string
    except:
        return None

#put data into psql database

#open the csv
with open("movies.csv", 'r') as csvfile:
    print("OPENING CSV")
    reader = csv.reader(csvfile)

    #skip the header file
    next(reader)

    query_movie_info = """INSERT INTO movie_info
        (name, rating, genre, director, writer, star, country, budget, gross, company, runtime)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    query_movie_releases = """INSERT INTO movie_release
        (movie_info_name, movie_info_director, release, score, votes)
        VALUES
        (%s, %s, %s, %s, %s)
        """

    count = 0

    #for every line in the csv
    for row in reader:
        #[0:name, 1:rating, 2:genre, 3:year, 4:released,
        # 5:score, 6:votes, 7:director, 8:writer, 9:star,
        # 10:country, 11:budget, 12:gross, 13:company, 14:runtime]

        #add appropriate data to movie_info
        cursor.execute(query_movie_info, (row[0], row[1], row[2], row[7], row[8],
                                        row[9], row[10], make_int(row[11]), make_int(row[12]),
                                        row[13], make_int(row[14]), ))

        #add appropriate data to movie_release
        cursor.execute(query_movie_releases, (row[0], row[7], make_num(row[3]), make_num(row[5]), make_int(row[6]), ))

        count += 1
        if (count % 100 == 0):
            print(count)

cursor.close()
db.commit()
db.close()