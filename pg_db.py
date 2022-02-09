import psycopg2
from config_db import config
from time import gmtime, strftime
from psycopg2.extras import NamedTupleCursor


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        with conn.cursor() as cursor:
            conn.autocommit = True
            insert = cursor.execute("INSERT INTO users (id, nikname, firstname, lastname, email, psw, time) VALUES  ('8', 'ALA3', 'Almaty2', 'Kazakhstan2', 'ALA2', 'Almaty2', '2015')")
            print(insert)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def insert_log_phone(model, mac, number, tabnumber):
    timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(timenow)
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        with conn.cursor() as cursor:
            conn.autocommit = True

            postgres_insert_query = "INSERT INTO log_yealink (model, mac, number, tabnumber, adminowner, time) VALUES (%s,%s,%s,%s,%s,%s)"
            record_to_insert = (model, mac, number, tabnumber, 'admin', timenow)
            cursor.execute(postgres_insert_query, record_to_insert)
            # cursor.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def select_log_phone():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        with conn.cursor() as cursor:
            conn.autocommit = True
            postgres_select_query = "SELECT * FROM log_yealink ORDER BY time DESC;"
            cursor.execute(postgres_select_query,)

            # display the PostgreSQL database server version
            db_version = cursor.fetchall()
            print(db_version)
            return db_version

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

#temp
def select_dss_phone():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        with conn.cursor() as cursor:
            conn.autocommit = True
            postgres_select_query = "SELECT * FROM dssphone_hab;"
            cursor.execute(postgres_select_query)

            dss_phone = cursor.fetchall()
            print(dss_phone)
            print(type(dss_phone))
            print(type(dss_phone[0]))
            return dss_phone

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def update_dss_phone(key_number, label_number, value_number, module_number):
    timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(timenow)
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        with conn.cursor() as cursor:
            conn.autocommit = True

            postgres_insert_query = "UPDATE dssphone_hab SET label_number = (%s), value_number = (%s), time = (%s) WHERE key_number = (%s) AND module_number = (%s)"
            record_to_insert = (label_number, value_number, timenow, key_number, module_number)
            cursor.execute(postgres_insert_query, record_to_insert)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')





#temp
def insert_ad_users(model, mac, number, tabnumber):
    timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(timenow)
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        with conn.cursor() as cursor:
            conn.autocommit = True
            record_to_insert = ('str(model)', 'str(mac)', 'str(number)', 'str(tabnumber)', 'admin', '(dt.now())')

            postgres_insert_query = "INSERT INTO log_yealink (model, mac, number, tabnumber, adminowner, time) VALUES (%s,%s,%s,%s,%s,%s)"
            record_to_insert = (model, mac, number, tabnumber, 'admin', timenow)
            cursor.execute(postgres_insert_query, record_to_insert)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')



def insert_log_ami(CallerIDNum, CallerIDName, ConfbridgeTalking="", TimeStart="no information", TimeEnd="no information"):
    timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(timenow)
    print(CallerIDNum, CallerIDName, ConfbridgeTalking, TimeStart, TimeEnd)
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        with conn.cursor() as cursor:
            conn.autocommit = True
            postgres_insert_query = "INSERT INTO conf_36861 (CallerIDNum, CallerIDName, ConfbridgeTalking, TimeStart, TimeEnd) VALUES (%s,%s,%s,%s,%s)"
            record_to_insert = (CallerIDNum, CallerIDName, ConfbridgeTalking, TimeStart, TimeEnd)
            cursor.execute(postgres_insert_query, record_to_insert)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def update_log_ami_talk(CallerIDNum, CallerIDName, ConfbridgeTalking="", TimeStart="no information", TimeEnd="no information"):
    timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(timenow)
    print(CallerIDNum, CallerIDName, ConfbridgeTalking, TimeStart, TimeEnd)
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        with conn.cursor() as cursor:
            conn.autocommit = True
            postgres_insert_query = "UPDATE conf_36861 SET ConfbridgeTalking = (%s) WHERE CallerIDNum = (%s)"
            record_to_insert = (ConfbridgeTalking, CallerIDNum)
            cursor.execute(postgres_insert_query, record_to_insert)
            # cursor.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def delete_log_ami(CallerIDNum, CallerIDName, TimeStart="no information", TimeEnd="no information"):
    print(CallerIDNum, CallerIDName, TimeStart, TimeEnd)
    timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(timenow)
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        with conn.cursor() as cursor:
            conn.autocommit = True
            postgres_insert_query = """DELETE FROM conf_36861 WHERE CallerIDNum = %s"""
            record_to_insert = (CallerIDNum,)
            cursor.execute(postgres_insert_query, record_to_insert)
            print(cursor.execute(postgres_insert_query, record_to_insert))


    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def delete_all_log_ami(TimeStart="no information", TimeEnd="no information"):
    print(TimeStart, TimeEnd)
    timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(timenow)
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        with conn.cursor() as cursor:
            conn.autocommit = True
            postgres_insert_query = "DELETE FROM conf_36861"
            cursor.execute(postgres_insert_query)


    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')



def select_log_ami():
    timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(timenow)
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        with conn.cursor() as cursor:
            conn.autocommit = True
            postgres_select_query = "SELECT * FROM conf_36861 ORDER BY TimeStart DESC;"
            cursor.execute(postgres_select_query,)
            db_select_log_ami = cursor.fetchall()
            print(db_select_log_ami)
            return db_select_log_ami

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')



def insert_ad_users_new():
    timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(timenow)
    print(CallerIDNum, CallerIDName, ConfbridgeTalking, TimeStart, TimeEnd)
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        with conn.cursor() as cursor:
            conn.autocommit = True
            postgres_insert_query = "INSERT INTO ad_users (CallerIDNum, CallerIDName, ConfbridgeTalking, TimeStart, TimeEnd) VALUES (%s,%s,%s,%s,%s)"
            record_to_insert = (CallerIDNum, CallerIDName, ConfbridgeTalking, TimeStart, TimeEnd)
            cursor.execute(postgres_insert_query, record_to_insert)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

