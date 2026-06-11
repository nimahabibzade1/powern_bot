import mysql.connector
from config import *
import logging

version = '1.0.0'

logging.basicConfig(level=logging.INFO, filename='report.log', format=f"%(asctime)s - %(levelname)s - {version} - %(message)s")

def drop_n_create_database(db_name):
    logging.info('create data base daily_routin')
    conn = mysql.connector.connect(**database_config)
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {db_name};")
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
    conn.commit()
    cur.close()
    conn.close()
    print(f'database {db_name} created successfully')
    

def create_table_user(db_name):
    logging.info('create table user')
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor()
    SQL_Query = """
    CREATE TABLE USER (
        `ID`                INT    UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        `CID`               BIGINT UNSIGNED NOT NULL UNIQUE,
        `FIRST_NAME`        VARCHAR(50) NOT NULL,
        `LAST_NAME`         VARCHAR(50),
        `USERNAME`          VARCHAR(50),
        `REGISTER_DATE`     DATETIME DEFAULT CURRENT_TIMESTAMP,
        `LAST_UPDATE`       DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """
    cur.execute(SQL_Query)
    conn.commit()
    cur.close()
    conn.close()
    print(f'table USER created successfully')

def create_table_task(db_name):
    logging.info('create table task')
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor()
    SQL_Query = """
    CREATE TABLE TASK (
        `ID`                INT    UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        `CID`               BIGINT UNSIGNED NOT NULL,
        `TASK_ID`           SMALLINT UNSIGNED NOT NULL,
        `TASK_TITLE`        VARCHAR(50) NOT NULL,
        `DESCRIPTION`       VARCHAR(100),
        `NEED_TIME_IN_MIN`  SMALLINT UNSIGNED NOT NULL,
        `STATUS`            ENUM('NOT_TIME','PASSED_TIME','FINISHED','UNFINISHED'),
        `REGISTER_DATE`     DATETIME DEFAULT CURRENT_TIMESTAMP,
        `FINISHED_TIME`     DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (`CID`) REFERENCES USER(`CID`)
    );
    """
    cur.execute(SQL_Query)
    conn.commit()
    cur.close()
    conn.close()
    print('table TASK created successfully')


def create_table_result_task(db_name):
    logging.info('create table RESULT_TASK')
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor()
    SQL_Query = """
    CREATE TABLE RESULT_TASK (
        `CID`               BIGINT UNSIGNED PRIMARY KEY,
        `SUCCESS_TASK`      INT UNSIGNED NOT NULL DEFAULT 0,
        `NO_SUCCESS_TASK`   INT UNSIGNED NOT NULL DEFAULT 0,
        `SUCCESS_DAY`       SMALLINT UNSIGNED NOT NULL DEFAULT 0,
        `NO_SUCCESS_DAY`    SMALLINT UNSIGNED NOT NULL DEFAULT 0,
        `COIN`              SMALLINT UNSIGNED NOT NULL DEFAULT 0,
        `REGISTER_DATE`     DATETIME DEFAULT CURRENT_TIMESTAMP,
        `LAST_UPDATE`       DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (`CID`) REFERENCES USER(`CID`)
    );
    """
    cur.execute(SQL_Query)
    conn.commit()
    cur.close()
    conn.close()
    print('table RESULT_TASK created successfully')


def create_table_wakeup_sleep(db_name):
    logging.info('create table WAKEUP_SLEEP')
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor()
    SQL_Query = """
    CREATE TABLE WAKEUP_SLEEP(
        `CID`               BIGINT UNSIGNED PRIMARY KEY,
        `FIRST_NAME`        VARCHAR(50) NOT NULL,
        `LAST_NAME`         VARCHAR(50),
        `USERNAME`          VARCHAR(50),
        `TIME_WAKEUP`       TIME DEFAULT '07:00:00',
        `TIME_SLEEP`        TIME DEFAULT '21:00:00',
        `DIFFERENCE_MIN`    SMALLINT NOT NULL,
        `REGISTER_DATE`     DATETIME DEFAULT CURRENT_TIMESTAMP,
        `LAST_UPDATE`       DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (`CID`) REFERENCES USER(`CID`)
    );
    """
    cur.execute(SQL_Query)
    conn.commit()
    cur.close()
    conn.close()
    print(f'table WAKEUP_SLEEP created successfully')


def create_table_friend(db_name):
    logging.info('create table friend')
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor()
    SQL_Query = """
    CREATE TABLE FRIEND(
        `ID`                INT    UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        `CID`               BIGINT UNSIGNED NOT NULL,
        `FRIEND_CID`        BIGINT UNSIGNED NOT NULL ,
        `FIRST_NAME`        VARCHAR(50) NOT NULL,
        `FRIEND_FIRST_NAME` VARCHAR(50) NOT NULL,
        `history_permission` BOOLEAN DEFAULT FALSE,
        `START_FRIEND_DATE` DATETIME DEFAULT CURRENT_TIMESTAMP,
        `LAST_UPDATE`       DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (`CID`) REFERENCES USER(`CID`)
    );
    """
    cur.execute(SQL_Query)
    conn.commit()
    cur.close()
    conn.close()
    print(f'table FRIEND created successfully')


def create_table_note(db_name):
    logging.info('create table note')
    conn = mysql.connector.connect(**database_config, database=database_name)
    cur = conn.cursor()
    SQL_Query = """
    CREATE TABLE NOTE(
        `ID`                INT      UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        `CID`               BIGINT   UNSIGNED NOT NULL,
        `N_FROM`            ENUM('CHAT','TASK') NOT NULL,
        `FIRST_NAME`        VARCHAR(50) NOT NULL,
        `NOTE`              TEXT NOT NULL,
        `REGISTER_DATE`     DATETIME DEFAULT CURRENT_TIMESTAMP,
        `LAST_UPDATE`       DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (`CID`) REFERENCES USER(`CID`)
    );
    """
    cur.execute(SQL_Query)
    conn.commit()
    cur.close()
    conn.close()
    print(f'table NOTE created successfully')



if __name__ == "__main__":
    db_name = database_name
    drop_n_create_database(db_name)
    create_table_user(db_name)
    create_table_task(db_name)
    create_table_result_task(db_name)
    create_table_wakeup_sleep(db_name)
    create_table_friend(db_name)
    create_table_note(db_name)

    
