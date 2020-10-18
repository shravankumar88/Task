import mysql.connector
from mysql.connector import Error
import os

#
# def get_db_connection():
#     try:
#         print ('host',os.environ)
#         print ('user',os.getenv('user_mysql'))
#         print ('database_mysql',os.getenv('database_mysql'))
#         db_conn = mysql.connector.connect(host = os.getenv('host_mysql'), database = os.getenv('database_mysql'),
#                                             user = os.getenv('user_mysql'),
#                                             password = os.getenv('password_mysql'),
#                                             auth_plugin = 'mysql_native_password')
#         if db_conn.is_connected:
#             db_info = db_conn.get_server_info()
#             print(" connected to :: ",db_info )
#             return db_conn
#     except Error as e:
#         print("Exception ", e.msg)
#         return None

def get_db_connection():
    try:
        db_conn = mysql.connector.connect(host = "localhost", database = "UserImages",
                                            user = "mysql_user",
                                            password = "password",
                                            auth_plugin = 'mysql_native_password')
        if db_conn.is_connected:
            db_info = db_conn.get_server_info()
            print(" connected to :: ",db_info )
            return db_conn
    except Error as e:
        print("Exception ", e.msg)
        return None

def insert_into_table(insertquery, req_data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        records_list = form_db_record(req_data)
        cursor.executemany(insertquery,records_list)
        conn.commit()
        print("records inserted successfully")

    except Error as e:
        print("Exception :: ",e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def retrive_from_table_by_id(select_query):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(select_query)
        record = cursor.fetchone()
        print("row count ", cursor.rowcount)
        return record
    except Error as e:
        print("Exception :: ", e)
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
def retrive_all(select_query):
    try:
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(select_query)
        records = cursor.fetchall()
        for row in records:
            print(row)
        print("row count :: ",cursor.rowcount)
        return records
    except Error as e:
        print("Exception :: ", e)
        return None  
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def form_db_record(req_data):
    users = []
    for user in req_data:
        print(user)
        users.append((
            user['first_name'],
            user['last_name']
        ))
    for userfmt in users:
        print(userfmt)
    return users


