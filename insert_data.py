import mysql.connector
from config import *
from edit_data import add_coin_to_user

import logging
version = '1.0.0'
logging.basicConfig(level=logging.INFO, filename='report.log', format=f"%(asctime)s - %(levelname)s - {version} - %(message)s")




def insert_user_data(CID, FIRST_NAME, LAST_NAME, USERNAME):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor()
    SQL_QUERY = f"SELECT CID FROM USER WHERE CID=%s;"
    cur.execute(SQL_QUERY, (CID,))
    data = cur.fetchall()
    if not len(data) != 0:
        SQL_QUERY = f"INSERT INTO USER (CID, FIRST_NAME, LAST_NAME, USERNAME) VALUES (%s, %s, %s, %s);"
        cur.execute(SQL_QUERY, (CID, FIRST_NAME, LAST_NAME, USERNAME))
        print(f'user {CID} info inserted successfully')
        logging.info(f'user {CID} data insert successfully with func insert_user_data')
    else:
        print(f'user {CID} exists in table')
    conn.commit()
    cur.close()
    conn.close()
    return True

def insert_wakeup_sleep_data(CID, FIRST_NAME, LAST_NAME, USERNAME, TIME_WAKEUP, TIME_SLEEP,DIFFERENCE_MIN):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor()
    SQL_QUERY = "SELECT CID FROM WAKEUP_SLEEP WHERE CID=%s ;"
    cur.execute(SQL_QUERY, (CID,))
    data = cur.fetchall()
    if not len(data) != 0:    
        SQL_QUERY = f"INSERT INTO WAKEUP_SLEEP (CID, FIRST_NAME, LAST_NAME, USERNAME, TIME_WAKEUP, TIME_SLEEP , DIFFERENCE_MIN) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        cur.execute(SQL_QUERY, (CID, FIRST_NAME, LAST_NAME, USERNAME, TIME_WAKEUP, TIME_SLEEP ,DIFFERENCE_MIN) )
        print(f'user {CID} wakeup_sleep time inserted successfully')
        logging.info(f'user {CID} data insert successfully with func insert_wakeup_sleep_data')
    else:
        print(f'user {CID} exists in wakeup_sleep table')
    conn.commit()
    cur.close()
    conn.close()
    return True



# ENUM('CHAT','TASK')
def insert_note_data(CID,N_FROM,FIRST_NAME,NOTE):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor()
    SQL_QUERY = "INSERT INTO NOTE (CID,N_FROM,FIRST_NAME,NOTE) VALUES (%s ,%s ,%s ,%s ) ;"
    cur.execute(SQL_QUERY, (CID,N_FROM,FIRST_NAME,NOTE))
    logging.info(f'user {CID} note data insert successfully with func insert_note_data')
    print('note added')
    conn.commit()
    cur.close()
    conn.close()
    return True




def insert_friend_data(CID,FRIEND_CID,FIRST_NAME,FRIEND_FIRST_NAME):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor()
    SQL_QUERY = 'SELECT FRIEND_CID FROM FRIEND WHERE CID = %s;'
    cur.execute(SQL_QUERY, (CID,))
    data = cur.fetchall()
    result=True
    for friend in data:
        print(friend[0],FRIEND_CID , type(friend[0]),type(FRIEND_CID))
        if int(friend[0]) == int(FRIEND_CID):
            result = False 
    if result:
        SQL_QUERY = "INSERT INTO FRIEND (CID,FRIEND_CID,FIRST_NAME,FRIEND_FIRST_NAME) VALUES (%s ,%s ,%s ,%s ) ;"
        cur.execute(SQL_QUERY, (CID,FRIEND_CID,FIRST_NAME,FRIEND_FIRST_NAME))
        SQL_QUERY = "INSERT INTO FRIEND (CID,FRIEND_CID,FIRST_NAME,FRIEND_FIRST_NAME) VALUES (%s ,%s ,%s ,%s ) ;"
        cur.execute(SQL_QUERY, (FRIEND_CID,CID,FRIEND_FIRST_NAME,FIRST_NAME))
        add_coin_to_user(CID,10)
        add_coin_to_user(FRIEND_CID,10)
        print(f'Now user {CID} and user {FRIEND_CID} are friend!')
        message=f'You invited with {FRIEND_FIRST_NAME}'
        logging.info(f'user {CID} and friedn {FRIEND_CID} data insert successfully with func insert_friend_data')
    else:
        print('you are friend!')
        message=f'You friend with {FRIEND_FIRST_NAME}'
    conn.commit()
    cur.close()
    conn.close()
    return message



def insert_result_task_default_data(CID):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor()
    SQL_QUERY = 'SELECT CID FROM RESULT_TASK WHERE CID = %s;'
    cur.execute(SQL_QUERY, (CID,))
    data = cur.fetchone()
    if data == None:
        SQL_QUERY = "INSERT INTO RESULT_TASK (CID,SUCCESS_TASK,NO_SUCCESS_TASK,SUCCESS_DAY,NO_SUCCESS_DAY,COIN) VALUES (%s ,%s ,%s ,%s ,%s , %s) ;"
        if CID == 1134412960 :
            cur.execute(SQL_QUERY, (CID,1000,0,1000,0,10000))
            logging.info(f'admin data insert successfully with func insert_result_task_default_data')
        else:
            cur.execute(SQL_QUERY, (CID,0,0,0,0,0))
            logging.info(f'user {CID} data insert successfully with func insert_result_task_default_data')
        print(f'result_task user {CID}  inserted successfully')
    else:
        print(f'user {CID} exist in RESULT_TASK')
    conn.commit()
    cur.close()
    conn.close()


# insert_task_data(cid,tittle,description,required_min,ID)
def insert_task_data(CID,TASK_TITLE,DESCRIPTION,NEED_TIME_IN_MIN,TASK_ID):
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor()
    SQL_QUERY = "INSERT INTO TASK (CID,TASK_TITLE,DESCRIPTION,NEED_TIME_IN_MIN,TASK_ID,STATUS) VALUES (%s ,%s ,%s ,%s ,%s ,%s) ;"
    cur.execute(SQL_QUERY, (CID,TASK_TITLE,DESCRIPTION,NEED_TIME_IN_MIN,TASK_ID,'NOT_TIME'))
    print(f'task user {CID}  inserted successfully')
    logging.info(f'user {CID} data insert successfully with func insert_task_data')
    conn.commit()
    cur.close()
    conn.close()


# # 'NOT_TIME','PASSED_TIME','FINISHED','UNFINISHED'
# insert_task_data(1134412960,"unsuccessfull","desc4",60,4)

# if __name__ == "__main__":
#     insert_user_data(11,'hasan', 'dsff','fdf11')
#     insert_task_data(11,'game','dl;fkjsd',10,3)
#     insert_task_data(11,'readig','studing lesson',60)
#     insert_friend_data(11,1134412960,'hasan','nima')
#     insert_result_task_default_data(11)
#     insert_task_data(12,'SECOND','DLKFJDLK',10)
#     insert_result_task_default_data(11)
#     insert_note_data(1134412960,'TASK','nima','سلام هبییی')
#     insert_wakeup_sleep_data(11,'nima','habib','power11100',"25:00","12:00:00")