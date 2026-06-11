import mysql.connector
from config import *

import logging
version = '1.0.0'
logging.basicConfig(level=logging.INFO, filename='report.log', format=f"%(asctime)s - %(levelname)s - {version} - %(message)s")




def edit_wakeup_sleep_data(CID,TIME_WAKEUP, TIME_SLEEP,DIFFERENCE_MIN):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor()
    SQL_QUERY = "UPDATE WAKEUP_SLEEP SET TIME_WAKEUP = %s , TIME_SLEEP = %s , DIFFERENCE_MIN =%s WHERE CID = %s ;"
    cur.execute(SQL_QUERY, (TIME_WAKEUP,TIME_SLEEP,DIFFERENCE_MIN,CID))
    print(f'wakeup and sleep user {CID} updated!')
    conn.commit()
    cur.close()
    conn.close()
    return True



def add_coin_to_user(CID, COIN):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor()
    SQL_QUERY = "SELECT COIN FROM RESULT_TASK WHERE CID = %s ;"
    cur.execute(SQL_QUERY,(CID ,))
    data = cur.fetchone()
    COINS = data[0] + COIN
    if  COINS < 65000:
        SQL_QUERY = "UPDATE RESULT_TASK SET COIN = %s WHERE CID = %s ;"
        cur.execute(SQL_QUERY, (COINS,CID))
        print(f'{COIN} ADDED TO USER {CID} !')
    else:
        print(f'user {CID} , your coins are full!')
    conn.commit()
    cur.close()
    conn.close()
    return True



def edit_sleep_time(CID,SLEEP_TIME,MIN_ADD):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor()
    SQL_QUERY = "SELECT DIFFERENCE_MIN FROM WAKEUP_SLEEP WHERE CID = %s ;"
    cur.execute(SQL_QUERY,(CID ,))
    data = cur.fetchone()
    MINS_ADD = data[0] + MIN_ADD
    SQL_QUERY = "UPDATE WAKEUP_SLEEP SET TIME_SLEEP = %s , DIFFERENCE_MIN = %s WHERE CID = %s ;"
    cur.execute(SQL_QUERY, (SLEEP_TIME,MINS_ADD,CID))
    print(f'Time sleep user {CID} changed to {SLEEP_TIME}!')
    conn.commit()
    cur.close()
    conn.close()
    return True




def edit_status_task(CID,ID,STATUS):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor()
    SQL_QUERY = "UPDATE TASK SET STATUS = %s WHERE CID = %s AND ID = %s;"
    cur.execute(SQL_QUERY, (STATUS,CID,ID))
    print(f'status task with id {ID} changed to {STATUS} !')
    conn.commit()
    cur.close()
    conn.close()
    return True







def add_success_work_to_user(CID):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor()
    SQL_QUERY = "SELECT SUCCESS_TASK FROM RESULT_TASK WHERE CID = %s;"
    cur.execute(SQL_QUERY,(CID ,))
    data = cur.fetchone()
    success_task = data[0] +1
    SQL_QUERY = "UPDATE RESULT_TASK SET SUCCESS_TASK = %s WHERE CID = %s ;"
    cur.execute(SQL_QUERY, (success_task,CID))
    print(f'user {CID} did one success task!')
    conn.commit()
    cur.close()
    conn.close()
    



def add_unsuccess_work_to_user(CID):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor()
    SQL_QUERY = "SELECT NO_SUCCESS_TASK FROM RESULT_TASK WHERE CID = %s;"
    cur.execute(SQL_QUERY,(CID ,))
    data = cur.fetchone()
    unsuccess_task = data[0] +1
    SQL_QUERY = "UPDATE RESULT_TASK SET NO_SUCCESS_TASK = %s WHERE CID = %s ;"
    cur.execute(SQL_QUERY, (unsuccess_task,CID))
    print(f'user {CID} did one unsuccess task!')
    conn.commit()
    cur.close()
    conn.close()
    







def add_success_day_to_user(CID):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor()
    SQL_QUERY = "SELECT SUCCESS_DAY FROM RESULT_TASK WHERE CID = %s;"
    cur.execute(SQL_QUERY,(CID ,))
    data = cur.fetchone()
    success_day = data[0] +1
    SQL_QUERY = "UPDATE RESULT_TASK SET SUCCESS_DAY = %s WHERE CID = %s ;"
    cur.execute(SQL_QUERY, (success_day,CID))
    print(f'user {CID} did one success day!')
    conn.commit()
    cur.close()
    conn.close()
    





    
def add_unsuccess_day_to_user(CID):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor()
    SQL_QUERY = "SELECT NO_SUCCESS_DAY FROM RESULT_TASK WHERE CID = %s;"
    cur.execute(SQL_QUERY,(CID ,))
    data = cur.fetchone()
    unsuccess_day = data[0] +1
    SQL_QUERY = "UPDATE RESULT_TASK SET NO_SUCCESS_DAY = %s WHERE CID = %s ;"
    cur.execute(SQL_QUERY, (unsuccess_day,CID))
    print(f'user {CID} did one unsuccess day!')
    conn.commit()
    cur.close()
    conn.close()
    






def change_history_permission(CID,FRIEND_CID,BOOL):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor()
    SQL_QUERY = "SELECT history_permission FROM FRIEND WHERE CID = %s AND FRIEND_CID = %s;"
    cur.execute(SQL_QUERY,(CID,FRIEND_CID))
    data = cur.fetchone()
    past_bool = data[0]
    if BOOL != past_bool :
        SQL_QUERY = "UPDATE FRIEND SET history_permission = %s WHERE CID = %s AND FRIEND_CID = %s;"
        cur.execute(SQL_QUERY, (BOOL,CID,FRIEND_CID))
        print(f'history_permission USER {CID} AND {FRIEND_CID} CHANGED TO {BOOL}!')
        back_data = True
    else:
        print(f'history_permission USER {CID} AND {FRIEND_CID} already is {BOOL}!')
        back_data = False
    conn.commit()
    cur.close()
    conn.close()
    return back_data







