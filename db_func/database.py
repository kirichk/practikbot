import os
import sys
import sqlite3
import traceback
from sqlite3 import Error
from loguru import logger


@logger.catch
def post_sql_query(sql_query):
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'my.db')
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(sql_query)
        except Error as er:
            logger.info(sql_query)
            logger.info('SQLite error: %s' % (' '.join(er.args)))
            logger.info("Exception class is: ", er.__class__)
            logger.info('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            logger.info(traceback.format_exception(
                exc_type, exc_value, exc_tb))
            pass
        result = cursor.fetchall()
        return result


@logger.catch
def create_table():
    query = '''CREATE TABLE IF NOT EXISTS DATA
                        (user_id TEXT,
                        phone TEXT);'''
    post_sql_query(query)
    query = '''CREATE TABLE IF NOT EXISTS TASKS
                        (user_id TEXT,
                        counter TEXT);'''
    post_sql_query(query)


@logger.catch
def add_user(phone, user_id):
    sql_selection = f"SELECT * FROM DATA WHERE "\
                        f"user_id = '{user_id}';"
    rows = post_sql_query(sql_selection)
    if not rows:
        query = f"INSERT INTO DATA (phone, user_id) VALUES ('{phone}', "\
                f"'{user_id}');"
        logger.info(post_sql_query(query))
    else:
        query = f"UPDATE DATA SET phone = '{phone}', user_id = '{user_id}';"
        logger.info(post_sql_query(query))


@logger.catch
def add_task(user_id):
    sql_selection = f"SELECT * FROM TASKS WHERE "\
        f"user_id = '{user_id}';"
    rows = post_sql_query(sql_selection)
    if not rows:
        query = f"INSERT INTO TASKS (user_id, counter) VALUES ('{user_id}', '0');"
        post_sql_query(query)


@logger.catch
def task_list():
    query = f"SELECT * FROM TASKS;"
    result = post_sql_query(query)
    return result


@logger.catch
def add_counter(user_id, counter):
    counter = str(int(counter) + 1)
    query = f"UPDATE TASKS SET counter = '{counter}' WHERE user_id = '{user_id}';"
    post_sql_query(query)


@logger.catch
def delete_task(user_id):
    sql_selection = f"DELETE FROM TASKS WHERE "\
                        f"user_id = '{user_id}';"
    post_sql_query(sql_selection)
