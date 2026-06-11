import mysql.connector
from config import *

import logging
version = '1.0.0'
logging.basicConfig(level=logging.INFO, filename='report.log', format=f"%(asctime)s - %(levelname)s - {version} - %(message)s")



def get_note_data(CID,N_FROM):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor(dictionary=False)
    if N_FROM == 'CHAT':
        SQL_QUERY = f"SELECT NOTE FROM NOTE WHERE CID = %s AND N_FROM = %s ;"
        cur.execute(SQL_QUERY, (CID,N_FROM))
        data = cur.fetchall()
    elif N_FROM == 'TASK':
        # SQL_QUERY = f"SELECT NOTE FROM NOTE WHERE CID = %s AND N_FROM = %s ;"
        # cur.execute(SQL_QUERY, (CID,N_FROM))
        SQL_QUERY = F'SELECT DESCRIPTION FROM TASK WHERE CID = %s;'
        cur.execute(SQL_QUERY, (CID,))
        data = cur.fetchall()
    elif N_FROM == 'ALL':
        SQL_QUERY = f"SELECT NOTE , N_FROM FROM NOTE WHERE CID = %s ;"
        cur.execute(SQL_QUERY, (CID,))
        data = cur.fetchall()
    logging.info(f'user {CID} use fucn get_note_data with arguman : {N_FROM} and return data : {data}')
    conn.commit()
    cur.close()
    conn.close()
    return data





def get_wakeup_sleep_time(CID):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor(dictionary=False)
    SQL_QUERY = f"SELECT TIME_WAKEUP,TIME_SLEEP,DIFFERENCE_MIN FROM WAKEUP_SLEEP WHERE CID = %s;"
    cur.execute(SQL_QUERY, (CID,))
    data = cur.fetchone()
    logging.info(f'user {CID} use fucn get_wakeup_sleep_time and return data : {data}')
    conn.commit()
    cur.close()
    conn.close()
    return data

# a,b,c=get_wakeup_sleep_time()
# print()
def is_login_wakeup_sleep_time(CID):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor(dictionary=False)
    SQL_QUERY = f"SELECT CID FROM WAKEUP_SLEEP WHERE CID = %s;"
    cur.execute(SQL_QUERY, (CID,))
    data = cur.fetchone()
    result = True
    if data == None:
        result= False
    else:
        result = True
    logging.info(f'user {CID} use fucn is_login_wakeup_sleep_time and return data : {result}')
    conn.commit()
    cur.close()
    conn.close()
    return result


def is_login_user(CID):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor(dictionary=False)
    SQL_QUERY = f"SELECT CID FROM USER WHERE CID = %s;"
    cur.execute(SQL_QUERY, (CID,))
    data = cur.fetchone()
    result = True
    if data == None:
        result= False
    logging.info(f'user {CID} use fucn is_login_user and return data : {result}')
    conn.commit()
    cur.close()
    conn.close()
    return result





def is_enter_task(CID):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor(dictionary=False)
    SQL_QUERY = f"SELECT CID FROM TASK WHERE CID = %s;"
    cur.execute(SQL_QUERY, (CID,))
    data = cur.fetchall()
    result = True
    if len(data) == 0:
        result= False
    logging.info(f'user {CID} use fucn is_enter_task and return data : {result}')
    conn.commit()
    cur.close()
    conn.close()
    return result




def get_name_from_user(CID):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor(dictionary=False)
    SQL_QUERY = f"SELECT FIRST_NAME FROM USER WHERE CID = %s;"
    cur.execute(SQL_QUERY, (CID,))
    data = cur.fetchone()
    logging.info(f'user {CID} use fucn get_name_from_user and return data : {data}')
    conn.commit()
    cur.close()
    conn.close()
    return data


def get_user_date_with_id(ID):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor(dictionary=False)
    SQL_QUERY = f"SELECT CID , FIRST_NAME , LAST_NAME , USERNAME  FROM USER WHERE ID = %s;"
    cur.execute(SQL_QUERY, (ID,))
    data = cur.fetchone()
    logging.info(f'user {ID} use fucn get_user_date_with_id and return data : {data}')
    conn.commit()
    cur.close()
    conn.close()
    return data




def get_user_date_with_cid(CID):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor(dictionary=False)
    SQL_QUERY = f"SELECT ID , FIRST_NAME , LAST_NAME , USERNAME  FROM USER WHERE CID = %s;"
    cur.execute(SQL_QUERY, (CID,))
    data = cur.fetchone()
    logging.info(f'user {CID} use fucn get_user_date_with_cid and return data : {data}')
    conn.commit()
    cur.close()
    conn.close()
    return data




def get_result_task_data(CID):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor(dictionary=False)
    SQL_QUERY = f"SELECT SUCCESS_TASK,NO_SUCCESS_TASK,SUCCESS_DAY,NO_SUCCESS_DAY,COIN FROM RESULT_TASK WHERE CID = %s;"
    cur.execute(SQL_QUERY, (CID,))
    data = cur.fetchone()
    logging.info(f'user {CID} use fucn get_result_task_data and return data : {data}')
    conn.commit()
    cur.close()
    conn.close()
    return data



# ENUM('NOT_TIME','PASSED_TIME','FINISHED','UNFINISHED')
def get_task_data(CID,STATUS):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor(dictionary=False)
    SQL_QUERY = f"SELECT TASK_TITLE , DESCRIPTION , STATUS , NEED_TIME_IN_MIN , ID FROM TASK WHERE CID = %s AND STATUS = %s; "
    cur.execute(SQL_QUERY, (CID,STATUS))
    data = cur.fetchall()
    logging.info(f'user {CID} use fucn get_task_data and with arguman : {STATUS} and with return data : {data}')
    conn.commit()
    cur.close()
    conn.close()
    return data



def get_all_task_data(CID):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor(dictionary=False)
    SQL_QUERY = f"SELECT TASK_TITLE , DESCRIPTION , STATUS , NEED_TIME_IN_MIN , ID FROM TASK WHERE CID = %s ; "
    cur.execute(SQL_QUERY, (CID,))
    data = cur.fetchall()
    logging.info(f'user {CID} use fucn get_all_task_data with return data : {data}')
    conn.commit()
    cur.close()
    conn.close()
    return data








def get_all_friend_data(CID):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor(dictionary=False)
    SQL_QUERY = f"SELECT FRIEND_CID , FRIEND_FIRST_NAME , START_FRIEND_DATE FROM FRIEND WHERE CID = %s; "
    cur.execute(SQL_QUERY, (CID,))
    data = cur.fetchall()
    logging.info(f'user {CID} use fucn get_all_friend_data with return data : {data}')
    conn.commit()
    cur.close()
    conn.close()
    return data



def get_friend_data(CID,FRIEND_CID):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor(dictionary=False)
    SQL_QUERY = f"SELECT  FRIEND_FIRST_NAME , START_FRIEND_DATE FROM FRIEND WHERE CID = %s AND FRIEND_CID = %s; "
    cur.execute(SQL_QUERY, (CID,FRIEND_CID))
    data = cur.fetchone()
    logging.info(f'user {CID} use fucn get_friend_data with arguman : {FRIEND_CID} and with return data : {data}')
    conn.commit()
    cur.close()
    conn.close()
    return data




#after_delete_schedule_list_get_every_cid_have_task              استفاده نشد
def after_delete_schedule_list():
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor(dictionary=False)
    SQL_QUERY = f"SELECT DISTINCT  CID FROM TASK WHERE STATUS = 'NOT_TIME' "
    cur.execute(SQL_QUERY)
    data = cur.fetchall()
    logging.info(f'user func after_delete_schedule_list with return data : {data}')
    conn.commit()
    cur.close()
    conn.close()
    return data


#view_users_for_admin(admin cid , start id  , end id)
#view_users_for_admin(admin cid , 0  , 2)     ===>          [(id = 1 , ....)]
def view_users_for_admin(admin_cid,start_cid,end_cid):
    if admin_cid == 1134412960 : 
        conn = mysql.connector.connect(**database_config, database=database_name)
        cur = conn.cursor(dictionary=False)
        if start_cid == end_cid:
            SQL_QUERY = f"SELECT ID , CID , FIRST_NAME , LAST_NAME , USERNAME ,REGISTER_DATE , LAST_UPDATE FROM USER WHERE ID = %s;"
            cur.execute(SQL_QUERY,(start_cid,))
            data = cur.fetchone()
        else:            
            SQL_QUERY = f"SELECT ID , CID , FIRST_NAME , LAST_NAME , USERNAME ,REGISTER_DATE , LAST_UPDATE FROM USER WHERE ID > %s AND ID < %s;"
            cur.execute(SQL_QUERY,(start_cid,end_cid))
            data = cur.fetchall()
        logging.info(f'admin {admin_cid} use fucn view_users_for_admin with arguman : {start_cid} and : {end_cid} and with return data : {data}')
        conn.commit()
        cur.close()
        conn.close()
        return data
    




def get_all_users_id():
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor(dictionary=False)
    SQL_QUERY = f"SELECT ID FROM USER ;"
    cur.execute(SQL_QUERY,)
    data = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return data




def get_history_permission(CID,FRIEND_CID):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor(dictionary=False)
    SQL_QUERY = f"SELECT history_permission FROM FRIEND WHERE CID = %s AND FRIEND_CID = %s ;"
    cur.execute(SQL_QUERY,(CID,FRIEND_CID))
    data = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return data








# print(view_users_for_admin(1134412960,0,3))


# print(get_task_data(11))
# print(get_friend_data(1134412960,1139674003))
# print(get_friend_data(1134412960))
# print(is_login_wakeup_sleep_time(1))
# print(get_name_from_user(10))

# print(get_friend_data(1134412960)[0][2])
# print(get_task_data(13))
# print(get_wakeup_sleep_time(113441290))
# print(get_task_data(12))

