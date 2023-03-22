import sqlite3
from sqlite3 import Error

database = "sciencedb.db"


# Connection to SQLite database
# return type <connection>
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


# get all authors as tuple()
def select_all_authors():
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM authors")
    return cur.fetchall()


# create new author
def createAuthor(data):
    conn = create_connection(database)
    cur = conn.cursor()
    sql = '''
    insert into authors(name, hindex, i10index, imgUrl, resource)
    values(?, ?, ?, ?, ?)
    '''
    cur.execute(sql, data)
    conn.commit()


# update author by id
def updateAuthor(data):
    conn = create_connection(database)
    cur = conn.cursor()
    sql = '''
        update authors set hindex = ?, i10index = ?, imgUrl = ? where id = ?
        '''
    cur.execute(sql, data)
    conn.commit()


# filter authors by i10Index, hIndex
def filterAuthors(filterKey):
    conn = create_connection(database)
    cur = conn.cursor()
    if filterKey == "i10index":
        cur.execute("select * from authors ORDER by i10index DESC")
        return cur.fetchall()
    elif filterKey == "hindex":
        cur.execute("select * from authors ORDER by hindex DESC")
        return cur.fetchall()
    else:
        return []


def findAuthorById(author_id):
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("select * from authors where id = ?", (author_id,))
    return cur.fetchall()


def findAuthorByNameContains(author_name):
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("select * from authors where name like ?", ('%' + author_name + '%',))
    return cur.fetchall()
