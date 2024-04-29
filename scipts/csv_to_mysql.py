import mysql.connector
from mysql.connector import errorcode
import csv
import os
import string

def get_title(areas_lst):   # Converts .csv file name to align with SQL table naming conventions
    title_space = areas_lst[i].split('.')[0].split()
    title = '_'.join(title_space)
    # Uses string library to construct translator object to remove punctuation from string
    translator = str.maketrans('', '', string.punctuation.replace('_', ''))
    return title.translate(translator)


# Connects to MySQL instance or displays associated error
try:
    cnx = mysql.connector.connect(
        host="localhost",
        user='root',
        password="******",
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Incorrect username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

# Establishes cursor and creates MySQL database if not present
try:
    cursor = cnx.cursor()
    cursor.execute("USE mp_areas")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        cursor.execute("CREATE DATABASE mp_areas")
        print('Created database: mp_areas')
        cursor.execute("USE mp_areas")
    else:
        print('err')
        exit()

# Gathers directory content
areas_lst = os.listdir('areas')

# Iterates through each .csv and creates new MySQL table for each
for i in range(len(areas_lst)):
    title = get_title(areas_lst)
    table_query = ('CREATE TABLE IF NOT EXISTS ' + title +
                   '(name1 varchar(255),'
                   'sub_area varchar(255),'
                   'area varchar(255),' 
                   'grade int,'
                   'star_count float,'
                   'popular int);')
    cursor.execute(table_query)
    cnx.commit()

    # Inserts .csv data into associated MySQL table
    try:
        with open(rf'areas\{areas_lst[i]}', 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            header = next(csv_reader)
            for line in csv_reader:
                ins_query = ('INSERT INTO ' + title +
                             '(name1, sub_area, area, grade, star_count, popular) '
                             'VALUES (%s, %s, %s, %s, %s, %s)')
                cursor.execute(ins_query, line)
                cnx.commit()
    except:
        print(f'Unable to import data for {title}')

