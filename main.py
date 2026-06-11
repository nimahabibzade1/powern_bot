import threading
import schedule
import telebot
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from telebot.util import antiflood
from datetime import datetime , timedelta
import os
import time
# from text import fa
import random
import string
from insert_data import insert_user_data , insert_wakeup_sleep_data , insert_note_data , insert_friend_data ,insert_result_task_default_data , insert_task_data
from get_data import get_note_data ,get_wakeup_sleep_time , get_name_from_user , get_result_task_data , get_task_data , get_all_friend_data , is_login_wakeup_sleep_time , get_friend_data , is_enter_task , after_delete_schedule_list , get_all_task_data ,view_users_for_admin ,is_login_user,get_all_users_id , get_user_date_with_id , get_user_date_with_cid ,get_history_permission
from edit_data import edit_wakeup_sleep_data , add_coin_to_user , edit_sleep_time ,edit_status_task ,add_success_work_to_user , add_unsuccess_work_to_user ,add_unsuccess_day_to_user , add_success_day_to_user ,change_history_permission
import logging
from config import *







#                       :  باگ ها 


#                  :   یاد آوری ها
#            if result > 0 :     416
#ساخت کارکرد هر دکمه پروژه در کاغذ
# باید فارسی بشه در جلسه هشتم توضیح
#اضافه کردن لاگ به سه تا فایل فانکشن های دیتا بیس




telebot.apihelper.API_URL = 'https://tapi.bale.ai/bot{0}/{1}'

# API_TOKEN = ''

version = '1.0.0'

logging.basicConfig(level=logging.INFO, filename='report.log', format=f"%(asctime)s - %(levelname)s - {version} - %(message)s")

bot = telebot.TeleBot(API_TOKEN)

commands    =    {
    "start"         :           "start the bot" ,
    "help"          :           "introduce bot" ,
}


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        # print(m)
        if m.content_type == 'text':
            print(f"{m.chat.first_name} [{str(m.chat.id)}]: {m.text}")
        elif m.content_type == 'photo':
            print(f"{m.chat.first_name} [{str(m.chat.id)}]: New photo recieved")
        elif m.content_type == 'document':
            print(f"{m.chat.first_name} [{str(m.chat.id)}]: New document recieved")
        elif m.content_type == 'contact':
            print(f"{m.chat.first_name} [{str(m.chat.id)}]: New contact recieved")
        elif m.content_type == 'location':
            print(f"{m.chat.first_name} [{str(m.chat.id)}]: New location recieved")


bot.set_update_listener(listener)  # register listener

CHANNEL_CID= 6361909505

message_ids_from_channel = {
    'start'     :       1777385932742 ,

}

photos      ={

    'david_gogins'      :       "1134412960:7438061736443518720:0:31d2b545c1133a783c7b7805ace94705",
    'david_gogins1'     :       '1134412960:7644069700217478915:0:7efe9eef31dbef1942481d2d6b6daa541a9ec6f7595b78a8',
    'home_pic'          :       '1134412960:-809446379693859070:0:7efe9eef31dbef1940ddf4a74caf81991a9ec6f7595b78a8',
    'note'              :       "1134412960:993398229999427329:0:27b86d0b3b1b3700a0ed7a98ed791c31",
    'view_note'         :       '1134412960:6140075873305370369:0:7efe9eef31dbef1907f01e569553ff1e1a9ec6f7595b78a8',
    'friend'            :       '1134412960:5355114359573323522:0:7efe9eef31dbef192fa722ae86c765551a9ec6f7595b78a8',
    'history'           :       '1134412960:-193566478589354239:0:7efe9eef31dbef19fa6b055f138b54ae3c7b7805ace94705',

}

admin      =       1134412960

admins = [1134412960]

logins      =     []     # [cid , ...]

user_steps   =     {}     # {cid: step, ...}

wakeup_sleep_time     =     []     # [cid , ...]

user_wakeup_sleep_time = {}     # {cid  :[wakuptime, sleeptime]}

change_wakeup_sleep_time_list       =       []

SECRET = 7222018858

task_ID = {}

all_task_min = {}             #The sum of all task minutes

user_hour_list = {}             #every user message by scheule        {cid:{wakeup_cid_wakeup:12:00,sleep_cid_sleep:00:00,task1:time_taskname}}

time_line_list = {}                 # for deleting task             {cid:{wakeup:'12:00',sleep:'23:00',tasks:[task_id,task_id]}}

is_send_wakeup_message = {}         #برای اینکه اگه وقت بیداره گذشته و وقت بقیه تسک ها یا خوابیدن رسیده پیام نده و بزاره برای وقتی که اول پیام بیداری رو بده بعد                {cid:True}

time_line_message_for_del = {}       #وقتی که صف تایم لاین رو به کاربر نشون میده همینو سیو میکنه وقتی که کاربر میخاد با آیدی تسک کار رو حذف کنه دوباره نشون میده که ایدی رو انتخاب کنه     {cid:message}

delete_task_id = {}                 #ایدی تسک هایی که کنسل شدن داخل اینه                {cid:[]}

ban_user_cid = {}                   #سی ای دی کسایی که بن شدن                       {cid:schedule_obj}

support_user_username = 'powern1100'

invite_user_list = {}               #هر کسی که میخاد در بخش دوست هیستوری دوستشو ببینه باید اول درخواست بده برای اینکه چند بار نتونه درخواست بده این لیست ساخته شده                  {cid:friend_cid,cid:friend_cid,cid:friend_cid,...}





def login_user(cid,first_name,last_name,username):
    logging.info(f'fucn login_user for {cid}')
    if not cid in logins:
        if insert_user_data(cid,first_name,last_name,username):
            logins.append(cid)
    else:
        print(f'user {cid} info exists in list')



def wakeup_sleep_time_user(cid, first_name, last_name, username, time_wakeup , time_sleep ,difference_min):
    logging.info(f'fucn wakeup_sleep_time_user for {cid}')
    if not cid in wakeup_sleep_time:
        if insert_wakeup_sleep_data(cid, first_name, last_name, username, time_wakeup , time_sleep,difference_min):
            wakeup_sleep_time.append(cid)
    else:
        print(f'user {cid} wakeup sleep time exists in list')



def take_wakeup_time(cid):
    logging.info(f'fucn take_wakeup_time for {cid}')
    if not cid in wakeup_sleep_time:
        bot.send_message(cid,'first you must enter wakeup and sleep time !\nPlease enter waking up time :(HH:MM)')
        user_steps[cid] = 'wakeup_sleep_A'
    else:
        print('user in lisy')


def gen_invite_link(cid):
    logging.info(f'fucn gen_invite_link for {cid}')
    num1 = random.randint(10,99)
    num2 = random.randint(10,99)
    link = str(num1)+str((cid * 3) + SECRET)+str(num2)
    return int(link)

def dec_invite_link(value):
    logging.info(f'fucn dec_invite_link ')
    value = str(value)
    link1 = value[2:]
    link2 = link1[:-2]
    cid = (int(link2)-SECRET) // 3
    return str(cid)



def time_difference(wakeup_time,sleep_time):
    logging.info(f'fucn time_difference ')
    wakeup_hour,wakeup_min=wakeup_time.split(':')
    sleep_hour,sleep_min=sleep_time.split(':')
    wakeup_minutes=0
    wakeup_minutes+=int(wakeup_hour)*60
    wakeup_minutes+=int(wakeup_min)
    sleep_minutes=0
    sleep_minutes+=int(sleep_hour)*60
    sleep_minutes+=int(sleep_min)
    if wakeup_minutes > sleep_minutes:
        sleep_minutes += 60 * 24
    data_in_min=sleep_minutes-wakeup_minutes
    data_in_hour=data_in_min//60
    return data_in_hour , data_in_min


def give_wakeup_sleep_time(cid):
    logging.info(f'fucn give_wakeup_sleep_time for {cid}')
    data=get_wakeup_sleep_time(cid)
    wakeup_time , sleep_time , time_have_in_min = data
    wakeup_time = str(wakeup_time)
    sleep_time = str(sleep_time)
    time_have_in_min = str(time_have_in_min)
    return wakeup_time , sleep_time ,time_have_in_min


def give_result_task_data(cid,owner=None,friend_name=None):
    logging.info(f'fucn give_result_task_data for {cid}')
    func_data =get_result_task_data(cid)
    if owner == None:
        data=f"""
You finished {func_data[0]} tasks successfuly!
You finished {func_data[1]} tasks unsuccessfuly!
You finished {func_data[2]} day successfuly!
You finished {func_data[3]} day unsuccessfuly!
Overall you have {func_data[4]} coins!
"""
    else:
        data=f"""
{friend_name} finished {func_data[0]} tasks successfuly!
{friend_name} finished {func_data[1]} tasks unsuccessfuly!
{friend_name} finished {func_data[2]} day successfuly!
{friend_name} finished {func_data[3]} day unsuccessfuly!
Overall {friend_name} have {func_data[4]} coins!
"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('HOME',callback_data="home"))
    return markup , data






def add_time(base_time_str,min_add):  # a and b for checking if %H:%M:%S :change it to %H:%M
    logging.info(f'fucn add_time')
    base_time_str = str(base_time_str)
    a=base_time_str.split(':') 
    b=[]
    b.append(a[0])
    b.append(a[1])
    base_time_str = ':'.join(b)
    base_time = datetime.strptime(base_time_str,"%H:%M")
    new_time =base_time + timedelta(minutes=min_add)
    return(new_time.strftime("%H:%M"))





def check_time_true_format (time): #    %H : %M
    logging.info(f'fucn check_time_true_format')
    time = str(time)
    time_list = time.split(":")
    main_time_list = []
    main_time_list.append(time_list[0].zfill(2))
    main_time_list.append(time_list[1].zfill(2))
    main_time = ':'.join(main_time_list)
    return main_time






def return_task_markup():
    logging.info(f'fucn return_task_markup')
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('unSuccessfully tasks',callback_data='uncompleted_tasks'),InlineKeyboardButton('Successfully tasks',callback_data='completed_tasks'))
    markup.add(InlineKeyboardButton('Pending tasks',callback_data='Pending_tasks'),InlineKeyboardButton('passed tasks',callback_data='finished_tasks'))
    markup.add(InlineKeyboardButton('ALL',callback_data='all_tasks_result'))
    markup.add(InlineKeyboardButton('HOME',callback_data='home'))
    return markup




# time_line_list[cid]['sleep']=sleep
# time_line_list[cid]['tasks'][task_id]=task_obj
def delete_all_time_line_task(cid):
    logging.info(f'fucn delete_all_time_line_task for cid {cid}')
    for task in time_line_list[cid]:
        if task == 'wakeup':
            wakeup_obj = time_line_list[cid][task]
            schedule.cancel_job(wakeup_obj)
        elif task == 'sleep':
            sleep_obj = time_line_list[cid][task]
            schedule.cancel_job(sleep_obj)
        elif task == 'tasks':
            for each_task in time_line_list[cid][task]:
                task_obj = time_line_list[cid]['tasks'][each_task]
                schedule.cancel_job(task_obj)
    time_line_list.pop(cid)
    print(f'all task of user {cid} deleted')





def give_user_id_list():
    logging.info(f'fucn give_user_id_list')
    func_data = get_all_users_id()
    user_id_list = []
    for user in func_data:
        user_id_list.append(user[0])
    return user_id_list



# def invite_friend_to_allow_history(cid , friend_cid):
#     logging.info(f'fucn invite_friend_to_allow_history for user {cid} and friend {friend_cid}')
#     markup = InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton('YES',callback_data=f'allowed_premiss_{cid}_{friend_cid}'),InlineKeyboardButton('NO',callback_data=f'view_friends'))









@bot.message_handler(commands=['start'])
def start_command(message):
    cid = message.chat.id
    logging.info(f'user {cid} started bot!')
    first_name=message.chat.first_name
    last_name=message.chat.last_name
    username=message.chat.username
    login_user(cid,first_name,last_name,username)
    insert_result_task_default_data(cid)
    if not cid in ban_user_cid:
        if len(message.text.split()) > 1 and len(str(message.text.split()[-1])) >= 14:
            invite_cid_dec = str(message.text.split()[-1])
            friend_cid=dec_invite_link(invite_cid_dec)
            if friend_cid != str(cid):
                print(f'dec cid : {friend_cid}')
                friend_first_name = get_name_from_user(friend_cid)[0]
                caption = insert_friend_data(cid,friend_cid,first_name,friend_first_name)
                bot.send_message(cid,caption)
        markup=InlineKeyboardMarkup()
        if cid in admins:
            markup.add(InlineKeyboardButton('ADMIN',callback_data='admin'))
        markup.add(InlineKeyboardButton('Help',callback_data='help_command'))
        # bot.copy_message(cid, CHANNEL_CID, message_ids_from_channel['start'])
        bot.reply_to(message,'Welcome to our bot!', reply_markup=markup)








@bot.callback_query_handler(func=lambda call: True)#چک کن که برای همشون انسر کال بک کوری زده باشم
def callback_handler(call):
    # print(call)
    call_id = call.id
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data
    username=call.message.chat.username
    first_name=call.message.chat.first_name
    last_name=call.message.chat.last_name
    logging.info(f'user {cid} press button with data {data}!')
    if not is_login_user(cid):
        insert_user_data(cid, first_name, last_name, username)
    print(f'call id: {call_id}, cid: {cid}, mid: {mid}, data: {data}')
    if data.startswith('help_command'):
        if not cid in ban_user_cid:
            bot.answer_callback_query(call_id,'You press button HELP')
            bot.edit_message_reply_markup(cid,mid,reply_markup=None)
            caption="""This bot can give you ROUTIN and DISCIPLINE
First you must insert your routin and set waking up & sleep time
STAY HARD!!
"""
            if is_login_wakeup_sleep_time(cid):
                wakeup_sleep_time.append(cid)
            if not cid in wakeup_sleep_time:
                bot.send_photo(cid,photos['david_gogins'],caption=caption)
                take_wakeup_time(cid)
            else:
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('HOME', callback_data='home'))
                bot.send_photo(cid,photos['david_gogins'],caption=caption, reply_markup=markup)
    elif data.startswith('wakeup_sleep_A_'):
        bot.answer_callback_query(call_id,'')
        if not cid in ban_user_cid:
            data_list=data.split('_')
            answer = data_list[-1]
            if answer == 'yes':
                wakeup_time = data_list[-2]
                user_wakeup_sleep_time.setdefault(cid, []).append(wakeup_time)
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('YES ✅',callback_data=f'nothing'),InlineKeyboardButton('NO',callback_data='nothing'))
                bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
                bot.send_message(cid,'Please enter sleeping time :(HH:MM)')
                user_steps[cid] = 'wakeup_sleep_B'
            elif answer == 'no':
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('YES',callback_data=f'nothing'),InlineKeyboardButton('NO ❎',callback_data='nothing'))
                bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
                take_wakeup_time(cid)
    elif data.startswith('wakeup_sleep_B_'):#پاک کردن step
        if not cid in ban_user_cid:
            bot.answer_callback_query(call_id,'')
            data_list=data.split('_')
            answer = data_list[-1]
            if answer == 'yes':
                user_steps.pop(cid)
                time_wakeup=user_wakeup_sleep_time[cid][0]
                time_sleep= data_list[-2]
                if time_sleep.startswith('24'):
                    check_hour,check_min=time_sleep.split(':')
                    time_sleep='00'+':'+check_min
                result,difference_min=time_difference(time_wakeup,time_sleep)
                if result >= 0 or result <= 0:#if result > 0 : اصلش اینه بخاطر اینکه اصلش نمیزاره روزت کمتر از یک ساعت باشه برای تست اینو برمیدارم و شرطی میزارم که حتی روزت بشه 5 دقیقه هم باشه تا بتونیم پایان روز هم مشاهده کنیم
                    if cid in change_wakeup_sleep_time_list :
                        markup=InlineKeyboardMarkup()
                        markup.add(InlineKeyboardButton('YES ✅',callback_data=f'nothing'),InlineKeyboardButton('NO',callback_data='nothing'))
                        bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
                        markup=InlineKeyboardMarkup()
                        markup.add(InlineKeyboardButton('HOME',callback_data='home'))
                        text=f"""
You change wake up and sleep data!
Now you can set your task and have plan for tomorrow!
SO you wake up at *{time_wakeup}* and sleep at *{time_sleep}*.
You almost have *{result}* hour to do what ever you want!
bot will message you at these times when you enter your task first!
*you can change this time every time!*
"""
                        if cid in time_line_list and len(time_line_list[cid])  > 0:
                            if 'wakeup' in time_line_list[cid]:
                                past_wakeup_time , past_sleep_time , past_diffrence =get_wakeup_sleep_time(cid)
                                if time_wakeup == past_wakeup_time :
                                    if time_sleep != past_sleep_time :
                                        if int(difference_min) > int(past_diffrence):
                                            sleep_obj = time_line_list[cid]['sleep']
                                            schedule.cancel_job(sleep_obj)
                                            time_line_list[cid].pop('sleep')
                                            markup1 = 'yes_sleep'
                                            sleep_time_message  = 'Good job💫\nYou finished your day!\nhope to had good day!!\nTomorrow will start again!\nBUT YOU CAN CANCEL IT!!\nDid you finish it successfully?'
                                            task_id='sleep_wakeup'
                                            sleep = schedule.every().day.at(check_time_true_format(add_time(time_sleep,1))).do(job,cid=cid,message=sleep_time_message,markup=markup1,task_id=task_id)
                                            time_line_list[cid]['sleep'] = sleep
                                            edit_wakeup_sleep_data(cid,time_wakeup,time_sleep,difference_min)
                                            bot.send_message(cid,'wake up time are same!but sleep time changed!!')
                                            bot.send_message(cid,text,parse_mode='MarkdownV2',reply_markup=markup)
                                        else:
                                            edit_wakeup_sleep_data(cid,time_wakeup,time_sleep,difference_min)
                                            bot.send_message(cid,'wake up time are same!but sleep time changed!but Changes do not affect the time of already entered tasks. To make changes, you must delete all tasks and re-enter your tasks again!')
                                            bot.send_message(cid,text,parse_mode='MarkdownV2',reply_markup=markup)
                                    else:
                                        bot.send_message(cid,'The times you entered had already been recorded and will not be changed.')
                                        bot.send_message(cid,text,parse_mode='MarkdownV2',reply_markup=markup)
                                else:
                                    delete_all_time_line_task(cid)
                                    edit_wakeup_sleep_data(cid,time_wakeup,time_sleep,difference_min)
                                    bot.send_message(cid,'wake-up and sleep time changed!!And all task time changed to!!So When your new wake-up time arrives, the tasks will start after that.')
                                    bot.send_message(cid,text,parse_mode='MarkdownV2',reply_markup=markup)
                                    insert_user_hour_list(cid)
                            elif 'sleep' in time_line_list[cid]:
                                sleep_obj = time_line_list[cid]['sleep']
                                schedule.cancel_job(sleep_obj)
                                time_line_list[cid].pop('sleep')
                                markup1 = 'yes_sleep'
                                sleep_time_message  = 'Good job💫\nYou finished your day!\nhope to had good day!!\nTomorrow will start again!\nBUT YOU CAN CANCEL IT!!\nDid you finish it successfully?'
                                task_id='sleep_wakeup'
                                sleep = schedule.every().day.at(check_time_true_format(add_time(time_sleep,1))).do(job,cid=cid,message=sleep_time_message,markup=markup1,task_id=task_id)
                                time_line_list[cid]['sleep'] = sleep
                                edit_wakeup_sleep_data(cid,time_wakeup,time_sleep,difference_min)
                                bot.send_message(cid,'wake-up and sleep time changed!but Changes do not affect on the wake-up time because already wake-up time passed. To make changes, you must delete all tasks and re-enter your tasks again!')
                                bot.send_message(cid,text,parse_mode='MarkdownV2',reply_markup=markup)
                            else:
                                edit_wakeup_sleep_data(cid,time_wakeup,time_sleep,difference_min)
                                bot.send_message(cid,text,parse_mode='MarkdownV2',reply_markup=markup)
                        else:
                            edit_wakeup_sleep_data(cid,time_wakeup,time_sleep,difference_min)
                            bot.send_message(cid,text,parse_mode='MarkdownV2',reply_markup=markup)
                    else:
                        user_wakeup_sleep_time.setdefault(cid, []).append(time_sleep)
                        markup=InlineKeyboardMarkup()
                        markup.add(InlineKeyboardButton('YES ✅',callback_data=f'nothing'),InlineKeyboardButton('NO',callback_data='nothing'))
                        bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
                        markup=InlineKeyboardMarkup()
                        markup.add(InlineKeyboardButton('HOME',callback_data='home'))
                        text=f"""
GOOD JOB!
You finish first step!
Now you can set your task and have plan for tomorrow!
SO you wake up at *{time_wakeup}* and sleep at *{time_sleep}*.
You almost have *{result}* hour to do what ever you want!
*you can change this time every time!*
    """
                        bot.send_message(cid,text,parse_mode='MarkdownV2',reply_markup=markup)
                        wakeup_sleep_time_user(cid, first_name, last_name, username, time_wakeup , time_sleep,difference_min)
                        user_wakeup_sleep_time.pop(cid)
                else:
                    bot.send_message(cid,'differences of these time must be more than *1* hour!\n Start again!!',parse_mode='MarkdownV2')
            elif answer == 'no' :
                user_steps.pop(cid)
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('YES',callback_data=f'nothing'),InlineKeyboardButton('NO ❎',callback_data='nothing'))
                bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
                bot.send_message(cid,'Please enter sleeping time :(HH:MM)')
                user_steps[cid] = 'wakeup_sleep_B'
    elif data == 'home':
        bot.answer_callback_query(call_id,'HOME')
        if not cid in ban_user_cid:
            markup=InlineKeyboardMarkup()
            bot.edit_message_reply_markup(cid,mid,reply_markup=None)
            bot.delete_message(cid,mid)
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('TASK',callback_data='task'),InlineKeyboardButton('TIMES',callback_data='wakeup_sleep_time_part'))
            markup.add(InlineKeyboardButton('NOTE',callback_data='note'),InlineKeyboardButton('EVALUATION',callback_data='history'),InlineKeyboardButton('FRIEND',callback_data='friend'))
            bot.send_photo(cid,photos['home_pic'],caption=f'Welcome *{first_name}* !',parse_mode='MarkdownV2',reply_markup=markup)
    elif data == 'task':
        bot.answer_callback_query(call_id,'TASK')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            if cid in user_steps:
                user_steps.pop(cid)
            all_task_data =[]
            other_func_data=get_task_data(cid,'PASSED_TIME')
            all_task_data.extend(other_func_data)
            other_func_data=get_task_data(cid,'FINISHED')
            all_task_data.extend(other_func_data)
            other_func_data=get_task_data(cid,'UNFINISHED')
            all_task_data.extend(other_func_data)
            func_data=get_task_data(cid,'NOT_TIME')
            if len(func_data) != 0 and cid in user_hour_list:
                markup = return_task_markup()
                markup.add(InlineKeyboardButton('VIEW ALL TASKS THAT ARE GOING TO SEND YOU A MESSAGE',callback_data='view_all_task_will_send'))
                bot.send_message(cid,'In this part you can check you tasks!!',reply_markup=markup)
            elif len(func_data) != 0 and not cid in user_hour_list:
                insert_user_hour_list(cid)
                markup = return_task_markup()
                markup.add(InlineKeyboardButton('VIEW ALL TASKS THAT ARE GOING TO SEND YOU A MESSAGE',callback_data='view_all_task_will_send'))
                bot.send_message(cid,'In this part you can check you tasks!!',reply_markup=markup)
            elif cid in time_line_list and 'sleep' in time_line_list[cid]:
                markup = return_task_markup()
                markup.add(InlineKeyboardButton('VIEW ALL TASKS THAT ARE GOING TO SEND YOU A MESSAGE',callback_data='view_all_task_will_send_just_sleep'))
                bot.send_message(cid,'In this part you can check you tasks!!',reply_markup=markup)
            elif len(all_task_data) != 0 and len(func_data) == 0:
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('INSERT NEW TASK',callback_data='insert_new_task'),InlineKeyboardButton('CHECK TASKS',callback_data='check_all_tasks'))
                markup.add(InlineKeyboardButton('HOME',callback_data='home'))
                bot.send_message(cid,"Do you want to insert new task or check tasks?",reply_markup=markup)
            elif len(func_data) == 0 and len(all_task_data) == 0:
                _,__,min_have = get_wakeup_sleep_time(cid)
                text =f"""
You have {min_have} min this day to do your tasks!
In here you must insert your task in this forman\n
*task tittle*
*Task description*
*The task required time in minutes*\n
If your tasks is finish and you want to stop this just send *STOP* to finish!
"""
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('READY',callback_data='main_task'))
                markup.add(InlineKeyboardButton('HOME',callback_data='home'))
                bot.send_message(cid,text,reply_markup=markup)
    elif data == 'view_all_task_will_send':
        bot.answer_callback_query(call_id,'CHECK TASKS')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            message = ''
            if cid in time_line_list:
                if len(time_line_list[cid]) != 0 :
                    wakeup_time , sleep_time , __ = get_wakeup_sleep_time(cid)
                    message+='you will do these tasks at these moment\n\n'
                    wakeup_message=''
                    sleep_message=''
                    task_message=''
                    check_wakeup=f'wakeup_{cid}_wakeup'
                    check_sleep=f'sleep_{cid}_sleep'
                    for task in user_hour_list[cid]:
                        if task == check_wakeup:
                            if 'wakeup' in time_line_list[cid] :
                                wakeup_message+=f'you will wake-up and start your day at {wakeup_time}\n\n'
                            else:
                                wakeup_message+=f'you woke-up and started your day at {wakeup_time}\n\n'
                        elif task == check_sleep:
                            if 'sleep' in time_line_list[cid] :
                                sleep_message+=f'you will sleep and finish your day at {add_time(sleep_time,1)}\n\n'
                            else:
                                sleep_message+=f'you sleep and finished your day at {add_time(sleep_time,1)}\n\n'
                        else:
                            time , x , task_id = user_hour_list[cid][task]
                            if 'tasks' in time_line_list[cid] and len(time_line_list[cid]['tasks']) != 0 :
                                if task_id in time_line_list[cid]['tasks'] :
                                    task_message +=f'you will finish task : ({task}) with ID : ({task_id}) at {time}\n\n'
                                elif cid in delete_task_id:
                                    if task_id in delete_task_id[cid]:
                                        message+=f'you deleted ({task})'
                                else:
                                    task_message +=f'you finished ({task}) at {time}\n\n'
                            else:
                                    task_message +=f'you finished ({task}) at {time}\n\n'
                    message+=wakeup_message
                    message+=task_message
                    message+=sleep_message
                    time_line_message_for_del[cid]=message
                    markup= InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton('DELETE ALL TASK',callback_data='delete_all_task_time_line'))
                    markup.add(InlineKeyboardButton('DELETE TASK BY SELECTION',callback_data='delete_task_by_Selection'))
                    markup.add(InlineKeyboardButton('BACK',callback_data='task'))
                    bot.send_message(cid,message,reply_markup=markup)
            else:
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('HOME',callback_data='home'))
                bot.send_message(cid,'There is no doing list in here!!',reply_markup=markup)
    elif data == 'view_all_task_will_send_just_sleep':
        bot.answer_callback_query(call_id,'DELETE ALL TASKS')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            if cid in user_steps:
                user_steps.pop(cid)
            message = ''
            if cid in time_line_list:
                if len(time_line_list[cid]) != 0 :
                    wakeup_time , sleep_time , __ = get_wakeup_sleep_time(cid)
                    message+='you will do these tasks at these moment\n\n'
                    wakeup_message=''
                    sleep_message=''
                    task_message=''
                    check_wakeup=f'wakeup_{cid}_wakeup'
                    check_sleep=f'sleep_{cid}_sleep'
                    for task in user_hour_list[cid]:
                        if task == check_wakeup:
                            if 'wakeup' in time_line_list[cid] :
                                wakeup_message+=f'you will wake-up and start your day at {wakeup_time}\n\n'
                            else:
                                wakeup_message+=f'you woke-up and started your day at {wakeup_time}\n\n'
                        elif task == check_sleep:
                            if 'sleep' in time_line_list[cid] :
                                sleep_message+=f'you will sleep and finish your day at {add_time(sleep_time,1)}\n\n'
                            else:
                                sleep_message+=f'you sleep and finished your day at {add_time(sleep_time,1)}\n\n'
                        else:
                            time , x , task_id = user_hour_list[cid][task]
                            if 'tasks' in time_line_list[cid] and len(time_line_list[cid]['tasks']) != 0 :
                                if task_id in time_line_list[cid]['tasks'] :
                                    task_message +=f'you will finish task : ({task}) with ID : ({task_id}) at {time}\n\n'
                                elif cid in delete_task_id:
                                    if task_id in delete_task_id[cid]:
                                        message+=f'you deleted ({task})'
                                else:
                                    task_message +=f'you finished ({task}) at {time}\n\n'
                            else:
                                    task_message +=f'you finished ({task}) at {time}\n\n'
                    message+=wakeup_message
                    message+=task_message
                    message+=sleep_message
                    markup= InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton('DELETE ALL TASK',callback_data='delete_all_task_time_line'))
                    markup.add(InlineKeyboardButton('BACK',callback_data='task'))
                    bot.send_message(cid,message,reply_markup=markup)
    elif data == 'delete_all_task_time_line':
        bot.answer_callback_query(call_id,'DELETE ALL TASKS')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            if cid in user_steps:
                user_steps.pop(cid)
            for task in time_line_list[cid]:
                if task == 'wakeup':
                    wakeup_obj = time_line_list[cid]['wakeup']
                    schedule.cancel_job(wakeup_obj)
                elif task == 'sleep':
                    sleep_obj = time_line_list[cid]['sleep']
                    schedule.cancel_job(sleep_obj)
                else:
                    for task_id in time_line_list[cid][task]:
                        task_obj = time_line_list[cid][task][task_id]
                        schedule.cancel_job(task_obj)
                        edit_status_task(cid,task_id,'PASSED_TIME')
            if 'sleep' in time_line_list[cid]:
                time_line_list[cid].pop('sleep')
            if 'wakeup' in time_line_list[cid]:
                time_line_list[cid].pop('wakeup')
            if 'tasks' in time_line_list[cid]:
                time_line_list[cid].pop('tasks')
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('HOME',callback_data='home'))
            message="""
You will no longer receive any messages for tasks, wake-up reminders, or sleep reminders or task reminders! Your account has now been set to the "Passed" status.
To start receiving reminders again and create new tasks, please go to the Tasks section and add your tasks first.
"""
            bot.send_message(cid,message,reply_markup=markup)
    elif data == 'delete_task_by_Selection':
        bot.answer_callback_query(call_id,'DELETE TASK')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            message = time_line_message_for_del[cid]
            bot.send_message(cid,message)
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('BACK',callback_data='task'))
            bot.send_message(cid,'Please enter the ID of the task you want to delete.',reply_markup=markup)
            user_steps[cid]='get_task_id_for_deleting'
    elif data == 'check_all_tasks':
        bot.answer_callback_query(call_id,'CHECK TASKS')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            markup = return_task_markup()
            bot.send_message(cid,'In this part you can check you tasks!!',reply_markup=markup)
    elif data == 'insert_new_task':
        bot.answer_callback_query(call_id,'INSERT NEW TASK')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            _,__,min_have = get_wakeup_sleep_time(cid)
            text =f"""
You have {min_have} in this day to do your tasks!
In here you must insert your task in this forman\n
*task tittle*
*Task description*
*The task required time in minutes*\n
If your tasks is finish and you want to stop this just send *STOP* to finish!
"""
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('READY',callback_data='main_task'))
            markup.add(InlineKeyboardButton('HOME', callback_data='home'))
            bot.send_message(cid,text,reply_markup=markup)
    elif data =='main_task':
        bot.answer_callback_query(call_id,'TASK')
        if not cid in ban_user_cid:
            bot.edit_message_reply_markup(cid,mid,reply_markup=None)
            if not cid in task_ID:
                task_ID[cid]=0
                task_ID[cid]+=1
            if not cid in all_task_min:
                all_task_min[cid]=0
            markup = ReplyKeyboardMarkup()
            markup.add('STOP')
            bot.send_message(cid,f'Based on the format above, send your {task_ID[cid]} task\nEnter your first/next task or finish it with sending STOP ! :',reply_markup=markup)
            user_steps[cid]=f'receive_task_{task_ID[cid]}'
    elif data == 'wakeup_sleep_time_part':
        bot.answer_callback_query(call_id,'WAKEUP SLEEP TIME')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            if get_wakeup_sleep_time(cid) == None:
                if cid in wakeup_sleep_time:
                    wakeup_sleep_time.remove(cid)
                take_wakeup_time(cid)
            else:
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('CHANGE',callback_data='change_wakeup_sleep_time'))
                markup.add(InlineKeyboardButton('HOME',callback_data='home'))
                wakeup_time , sleep_time , time_have_in_min= give_wakeup_sleep_time(cid)
                caption = f"""
You entered {wakeup_time} for waking up and
{sleep_time} for sleeping!
So you have {time_have_in_min} minutes or around {int(time_have_in_min)//60} hours to do your plan!
Do you want to change this times or not?
"""
                bot.send_message(cid,caption,reply_markup=markup)
    elif data == 'change_wakeup_sleep_time':
        bot.answer_callback_query(call_id,'CHANGE WAKE UP AND SLEEP TIME')
        if not cid in ban_user_cid:
            if cid in user_steps:
                user_steps.pop(cid)
            bot.delete_message(cid,mid)
            if cid in wakeup_sleep_time:
                wakeup_sleep_time.remove(cid)
            if cid in user_wakeup_sleep_time:
                user_wakeup_sleep_time.pop(cid)
            change_wakeup_sleep_time_list.append(cid)
            take_wakeup_time(cid)
    elif data == 'note':
        if cid in user_steps:
            user_steps.pop(cid)
        bot.answer_callback_query(call_id,'NOTE')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('ADD NOTE', callback_data='add_note'))
            markup.add(InlineKeyboardButton('VIEW NTOE', callback_data='view_note'))
            markup.add(InlineKeyboardButton('HOME',callback_data='home'))
            # bot.send_message(cid,'NOTE',reply_markup=markup)
            bot.send_photo(cid,photos['note'],caption='note tools:',reply_markup=markup)#  بعضی مواقع عکس فرستادن در بله مشکل داره
    elif data == 'history':
        bot.answer_callback_query(call_id,'HISTORY')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            caption = 'Do you want to check your evaluation ?'
            markup =  InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('EVALUATION',callback_data='evaluation'),InlineKeyboardButton('EXPLANATIONS',callback_data='explanations'))
            markup.add(InlineKeyboardButton('HOME',callback_data='home'))
            bot.send_photo(cid,photos['history'],caption=caption,reply_markup=markup)
    elif data=='explanations':
        bot.answer_callback_query(call_id,'EVALUATION')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)#invite_link =f'https://ble.ir/powern_bot?start={gen_invite_link(cid)}'
            caption=f"""You can use the bot by entering your sleep and wake times, as well as your tasks for the day. When the message for the end of each task arrives, you can collect coins by selecting whether you successfully completed. At the end of the day, by specifying whether you successfully finished your day, you can also collect coins. Also bot has up to a 2 minutes delay!!
Additionally, you can collect coins by inviting your friends, and you can also view your friend's evaluation section.\n
For support and cooperation with our support team, contact us: [support](https://ble.ir/{support_user_username})
"""
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("HOME",callback_data='home'))
            bot.send_message(cid,caption,parse_mode='MarkdownV2',reply_markup=markup)
    elif data == 'evaluation':
        bot.answer_callback_query(call_id,'EVALUATION')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            markup , caption =give_result_task_data(cid)
            bot.send_message(cid,caption,reply_markup=markup)
    elif data == 'friend':
        bot.answer_callback_query(call_id,'FRIEND')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('FRIENDS',callback_data='view_friends'))
            markup.add(InlineKeyboardButton('INVITE LINK', callback_data='give_invite_link'))
            markup.add(InlineKeyboardButton('HOME',callback_data='home'))
            bot.send_photo(cid,photos['friend'],reply_markup=markup)
    elif data == 'view_friends':
        bot.answer_callback_query(call_id,'VIEW FRIEND')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            if cid in user_steps:
                user_steps.pop(cid)
            func_data = get_all_friend_data(cid)
            markup = InlineKeyboardMarkup()
            for friend in func_data:
                markup.add(InlineKeyboardButton(friend[1],callback_data=f'view_friend_data_{friend[0]}'))
            markup.add(InlineKeyboardButton('HOME',callback_data='home'))
            bot.send_message(cid,'These are your friends:\n',reply_markup=markup)
    elif data.startswith('view_friend_data_'):
        if not cid in ban_user_cid:
            friend_cid=int(data.split('_')[-1])
            friend=get_friend_data(cid,friend_cid)
            friend_name = friend[0]
            friend_date = friend[1]
            bot.answer_callback_query(call_id,f'view {friend_name}')
            bot.delete_message(cid,mid)
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('HISTORY',callback_data=f'friend_history_{friend_cid}'),InlineKeyboardButton('EVALUATION',callback_data=f'friend_evaluation_{friend_cid}'))
            markup.add(InlineKeyboardButton('BACK',callback_data='view_friends'))
            text = f"""
You get friend with  *{friend_name}*  at   *{friend_date}*
Do you want to view history or evaluation ?
"""
            bot.send_message(cid,text,reply_markup=markup,parse_mode='MarkdownV2')
    elif data.startswith('friend_history_'):
        if not cid in ban_user_cid:
            friend_cid=int(data.split('_')[-1])
            bot.delete_message(cid,mid)
            func_data = get_history_permission(cid,friend_cid)
            premiss_history = func_data[0]
            friend_name=get_name_from_user(friend_cid)[0]
            bot.answer_callback_query(call_id,f'HISTORY {friend_name}')
            friend_first_name = get_name_from_user(int(friend_cid))[0]
            if premiss_history:
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('CHANGE PREMISSION',callback_data=f'change_premiss_to_false_{friend_cid}'))
                markup.add(InlineKeyboardButton('SHOW HISTORY',callback_data=f'show_history_friend_{friend_cid}'))
                markup.add(InlineKeyboardButton('HOME',callback_data='home'))
                bot.send_message(cid,f'check history user {friend_first_name}',reply_markup=markup)
            else:
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('YES',callback_data=f'allowed_premiss_{cid}'),InlineKeyboardButton('NO',callback_data=f'not_allowed_premiss_{cid}'))
                bot.send_message(cid,f'Your request has been sent to user {friend_first_name}. When user {friend_first_name} responds positively to your request, you can view the other part of the history as well')
                user_first_name = get_name_from_user(cid)[0]
                bot.send_message(friend_cid,f'Do you want your history information to be shared with user {user_first_name} ?',reply_markup=markup)
                invite_user_list[cid]=friend_cid
    elif data.startswith('show_history_friend_'):
        if not cid in ban_user_cid:
            bot.answer_callback_query(call_id,f'SHOW HISTORY OF FRIEND')
            bot.delete_message(cid,mid)
            friend_cid=int(data.split('_')[-1])
            all_task_data =[]
            other_func_data=get_task_data(friend_cid,'PASSED_TIME')
            all_task_data.extend(other_func_data)
            other_func_data=get_task_data(friend_cid,'FINISHED')
            all_task_data.extend(other_func_data)
            other_func_data=get_task_data(friend_cid,'UNFINISHED')
            all_task_data.extend(other_func_data)
            other_func_data=get_task_data(friend_cid,'NOT_TIME')
            all_task_data.extend(other_func_data)
            if len(all_task_data) == 0:
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('HOME',callback_data='home'))
                bot.send_message(cid,'your friend has not any finished or unfinished task!',reply_markup=markup)
            else:
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('unSuccessfully tasks',callback_data=f'uncompleted_tasks_{friend_cid}'),InlineKeyboardButton('Successfully tasks',callback_data=f'completed_tasks_{friend_cid}'))
                markup.add(InlineKeyboardButton('Pending tasks',callback_data=f'Pending_tasks_{friend_cid}'),InlineKeyboardButton('passed tasks',callback_data=f'finished_tasks_{friend_cid}'))
                markup.add(InlineKeyboardButton('ALL',callback_data=f'all_tasks_result_{friend_cid}'))
                markup.add(InlineKeyboardButton('HOME',callback_data='home'))
                bot.send_message(cid,'all task of your friend',reply_markup=markup)
    elif data.startswith('uncompleted_tasks_'):
        if not cid in ban_user_cid:
            bot.answer_callback_query(call_id,f'UNCOMPLETED TASKS')
            bot.delete_message(cid,mid)
            friend_cid=int(data.split('_')[-1])
            func_data=get_task_data(friend_cid,'UNFINISHED')
            message = "These are the tasks that your friend completed unsuccessfully :\n\n\n"
            for task in func_data:
                message +=f"TASK NAME : {task[0]}\n"
                message +=f"TASK DESCRIPTION :\n{task[1]}\n"
                message +=f"Task minutes required : {task[3]}\n\n\n"
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('BACK',callback_data=f'view_friend_data_{friend_cid}'))
            bot.send_message(cid,message,reply_markup=markup)

    elif data.startswith('completed_tasks_'):
        if not cid in ban_user_cid:
            bot.answer_callback_query(call_id,f'COMPLETED TASKS')
            bot.delete_message(cid,mid)
            friend_cid=int(data.split('_')[-1])
            func_data=get_task_data(friend_cid,'FINISHED')
            message = "These are the tasks that your friend completed successfully :\n\n\n"
            for task in func_data:
                message +=f"TASK NAME : {task[0]}\n"
                message +=f"TASK DESCRIPTION :\n{task[1]}\n"
                message +=f"Task minutes required : {task[3]}\n\n\n"
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('BACK',callback_data=f'view_friend_data_{friend_cid}'))
            bot.send_message(cid,message,reply_markup=markup)

    elif data.startswith('Pending_tasks_'):
        if not cid in ban_user_cid:
            bot.answer_callback_query(call_id,f'PENDING TASKS')
            bot.delete_message(cid,mid)
            friend_cid=int(data.split('_')[-1])
            func_data=get_task_data(friend_cid,'NOT_TIME')
            message = "These are the tasks that your friend are pending and whose time has not come yet :\n\n\n"
            for task in func_data:
                message +=f"TASK NAME : {task[0]}\n"
                message +=f"TASK DESCRIPTION :\n{task[1]}\n"
                message +=f"Task minutes required : {task[3]}\n\n\n"
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('BACK',callback_data=f'view_friend_data_{friend_cid}'))
            bot.send_message(cid,message,reply_markup=markup)

    elif data.startswith('finished_tasks_'):
        if not cid in ban_user_cid:
            bot.answer_callback_query(call_id,f'FINISHED TASKS')
            bot.delete_message(cid,mid)
            friend_cid=int(data.split('_')[-1])
            func_data=get_task_data(friend_cid,'PASSED_TIME')
            message = "These are the tasks that was passed, and your friend has not said they are finished or not :\n\n\n"
            for task in func_data:
                message +=f"TASK NAME : {task[0]}\n"
                message +=f"TASK DESCRIPTION :\n{task[1]}\n"
                message +=f"Task minutes required : {task[3]}\n\n\n"
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('BACK',callback_data=f'view_friend_data_{friend_cid}'))
            bot.send_message(cid,message,reply_markup=markup)

    elif data.startswith('all_tasks_result_'):
        if not cid in ban_user_cid:
            bot.answer_callback_query(call_id,f'ALL TASKS')
            bot.delete_message(cid,mid)
            friend_cid=int(data.split('_')[-1])
            func_data = get_all_task_data(friend_cid)
            message = "These are all of your friend tasks :\n\n\n"
            for task in func_data:
                message +=f"TASK NAME : {task[0]}\n"
                message +=f"TASK STATUS : {task[2]}\n"
                message +=f"TASK DESCRIPTION :\n{task[1]}\n"
                message +=f"Task minutes required : {task[3]}\n\n\n"
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('BACK',callback_data=f'view_friend_data_{friend_cid}'))
            main_message=message.replace("NOT_TIME","PENDING").replace("PASSED_TIME","PASSED").replace("FINISHED","SUCCESSFULL COMPLETED").replace("UNFINISHED","UNSUCCESSFULL COMPLETED")
            bot.send_message(cid,main_message,reply_markup=markup)

    elif data.startswith('change_premiss_to_false'):
        if not cid in ban_user_cid:
            bot.answer_callback_query(call_id,f'DELETE PREMISSION')
            bot.delete_message(cid,mid)
            friend_cid = int(data.split('_')[-1])
            change_history_permission(cid,friend_cid,False)
            change_history_permission(friend_cid,cid,False)
            friend_name=get_name_from_user(friend_cid)[0]
            my_name=get_name_from_user(cid)[0]
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('HOME',callback_data='home'))
            bot.send_message(cid,f'now your friend {friend_name} cant to check your history',reply_markup=markup)
            bot.send_message(friend_cid,f'your friend {my_name} delete premission of check eack other history now for checking history again you must send request again!',reply_markup=markup)
    elif data.startswith('not_allowed_premiss_'):
        if not cid in ban_user_cid:
            friend_cid = int(data.split('_')[-1])
            friend_name=get_name_from_user(friend_cid)[0]
            bot.answer_callback_query(call_id,f'FAILED REQUEST USER {friend_name}')
            bot.delete_message(cid,mid)
            my_name=get_name_from_user(cid)[0]
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('HOME',callback_data='home'))
            bot.send_message(cid,f'FAILED REQUEST {friend_name} !',reply_markup=markup)
            bot.send_message(friend_cid,f'USER {my_name} not allowed!',reply_markup=markup)
    elif data.startswith('allowed_premiss_'):
        if not cid in ban_user_cid:
            friend_cid = int(data.split('_')[-1])
            friend_name=get_name_from_user(friend_cid)[0]
            bot.answer_callback_query(call_id,f'ALLOWED TO USER {friend_name}')
            bot.delete_message(cid,mid)
            my_name=get_name_from_user(cid)[0]
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('HOME',callback_data='home'))
            bot.send_message(cid,f'Now you can check history of user {friend_name}',reply_markup=markup)
            bot.send_message(friend_cid,f'user {my_name} accept your request? Now you can check history of user {my_name} !',reply_markup=markup)
            change_history_permission(cid,friend_cid,True)
            change_history_permission(friend_cid,cid,True)
    elif data.startswith('friend_evaluation_'):
        if not cid in ban_user_cid:
            friend_cid=int(data.split('_')[-1])
            bot.delete_message(cid,mid)
            friend_name=get_name_from_user(friend_cid)[0]
            bot.answer_callback_query(call_id,f'EVALUATION {friend_name}')
            markup , data = give_result_task_data(friend_cid,True,friend_name)
            bot.send_message(cid,data,reply_markup=markup)
    elif data == 'give_invite_link':
        bot.answer_callback_query(call_id,'INVITE LINK')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            login_user(cid,first_name,last_name,username)
            invite_link =f'https://ble.ir/powern_bot?start={gen_invite_link(cid)}'
            bot.send_message(cid,f'Here is your invite link:\n{invite_link}')
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('HOME',callback_data='home'))
            bot.send_message(cid,'Lets goooo!', reply_markup=markup)
    elif data =='add_note':
        bot.answer_callback_query(call_id,'ADD NOTE')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('BACK',callback_data='note'))
            bot.send_message(cid,'send your note to save!',reply_markup=markup)
            user_steps[cid]='save_chat_note'
    elif data =='view_note':
        bot.answer_callback_query(call_id,'VIEW NOTE')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('VIEW NOTES',callback_data='view_chat_notes'),InlineKeyboardButton('DESCRIPTION OF TASK',callback_data='view_task_notes'))
            # markup.add(InlineKeyboardButton('ALL NOTES', callback_data='view_all_notes'))
            markup.add(InlineKeyboardButton('BACK',callback_data='note'))
            # bot.send_message(cid,'Choose the category !', reply_markup=markup)
            bot.send_photo(cid,photos['view_note'],caption='Choose the category !',reply_markup=markup)
    elif data == 'view_chat_notes':
        bot.answer_callback_query(call_id,'VIEW CHAT NOTES')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            notes=get_note_data(cid,'CHAT')
            if is_enter_task:
                view_chat_note='This is all of your note from chat! :\n\n'
                for each_note in notes:
                    view_chat_note+=each_note[0]
                    view_chat_note+='\n\n\n'
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('HOME',callback_data='home'))
                bot.send_message(cid,view_chat_note,reply_markup=markup)
            else:
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('HOME',callback_data='home'))
                bot.send_message(cid,'Dont have any task to show their description!',reply_markup=markup)
    elif data == 'view_task_notes':
        bot.answer_callback_query(call_id,'VIEW TASK NOTES')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            notes=get_note_data(cid,'TASK')
            if len(notes) != 0:
                view_chat_note='These are all the descriptions of your tasks! :\n\n'
                for each_note in notes:
                    view_chat_note+=each_note[0]
                    view_chat_note+='\n\n\n'
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('HOME',callback_data='home'))
                bot.send_message(cid,view_chat_note,reply_markup=markup)
            else:
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('HOME',callback_data='home'))
                bot.send_message(cid,'you dont have any task to view their descriptions !!',reply_markup=markup)
    elif data == 'view_all_notes':
        bot.answer_callback_query(call_id,'VIEW ALL NOTES')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            notes=get_note_data(cid,'ALL')
            if len(notes) != 0:
                view_chat_note='This is your notes! :\n\n'
                for each_note in notes:
                    view_chat_note+=each_note[0]+'('+each_note[1]+')'
                    view_chat_note+='\n\n\n'
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('HOME',callback_data='home'))
                bot.send_message(cid,view_chat_note,reply_markup=markup)
            else:
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('HOME',callback_data='home'))
                bot.send_message(cid,'The notes is empty!',reply_markup=markup)
    elif data == 'admin':
        bot.answer_callback_query(call_id,'ADMIN')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            if cid in admins :
                if cid in user_steps:
                    bot.edit_message_reply_markup(cid,mid,reply_markup=None)
                    user_steps.pop(cid)
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('VIEW USERS',callback_data='view_users_for_admin'))
                markup.add(InlineKeyboardButton('VIEW BANNED USERS',callback_data='view_banned_user'))
                if cid == admin :
                    markup.add(InlineKeyboardButton('SUB ADMINS',callback_data='sub_admins'))
                    markup.add(InlineKeyboardButton('CHANGE SUPPORT USERNAME',callback_data='change_support_username'))
                bot.send_message(cid,'ADMIN TOOLS:',reply_markup=markup)
    elif data == 'change_support_username':
        bot.answer_callback_query(call_id,'ADMIN')
        if cid == admin:
            bot.delete_message(cid,mid)
            user_steps[cid]='give_username_for_support'
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('BACK',callback_data='cancel_admin_tool'))
            bot.send_message(cid,'please send the username of user that you want to become support team',reply_markup=markup)
    elif data == 'sub_admins':
        bot.answer_callback_query(call_id,'ADMIN')
        if not cid in ban_user_cid:
            bot.edit_message_reply_markup(cid,mid,reply_markup=None)
            if cid == admin :
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('PROMOTING USER TO ADMIN',callback_data='change_user_to_admin'))
                markup.add(InlineKeyboardButton('VIEW ADMINS',callback_data='view_admins'))
                bot.send_message(cid,'CHOOSE 👨‍💻',reply_markup=markup)
    elif data == 'view_admins':
        bot.answer_callback_query(call_id,'ADMIN')
        if not cid in ban_user_cid:
            bot.edit_message_reply_markup(cid,mid,reply_markup=None)
            if cid == admin :
                if len(admins) > 1 :
                    for admin_cid in admins:
                        if admin_cid != admin:
                            admin_info = get_user_date_with_cid(admin_cid)
                            admin_id = admin_info[0]
                            admin_first_name = admin_info[1]
                            admin_last_name = admin_info[2]
                            admin_username = admin_info[3]
                            markup = InlineKeyboardMarkup()
                            markup.add(InlineKeyboardButton('REMOVE FROM ADMINS',callback_data=f'remove_from_admins_{admin_cid}'))
                            bot.send_message(cid,f'ADMIN ID : {admin_id}\nUSER CID : {admin_cid}\nADMIN FIRST NAME : {admin_first_name}\nADMIN LAST NAME : {admin_last_name}\nADMIN USERNAME : {admin_username}',reply_markup=markup)
                    markup = InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton('BACK',callback_data='cancel_admin_tool'))
                    bot.send_message(cid,'these are all of your admins!',reply_markup=markup)
                else:
                    markup=InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton('BACK',callback_data='cancel_admin_tool'))
                    bot.send_message(cid,"You are the only admin we have !!",reply_markup=markup)
    elif data.startswith('remove_from_admins_'):
        bot.answer_callback_query(call_id,'ADMIN')
        if not cid in ban_user_cid:
            bot.edit_message_reply_markup(cid,mid,reply_markup=None)
            admin_cid = int(data.split('_')[-1])
            if admin_cid in admins :
                admins.remove(admin_cid)
                bot.send_message(cid,f'user {admin_cid} removed from admins!')
                bot.send_message(admin_cid,'You are no longer an admin!')
            else:
                bot.send_message(cid,f"user {admin_cid} already not admin!")
    elif data == 'change_user_to_admin':
        bot.answer_callback_query(call_id,'ADMIN')
        if not cid in ban_user_cid:
            bot.edit_message_reply_markup(cid,mid,reply_markup=None)
            if cid == admin :
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('BACK',callback_data='cancel_admin_tool'))
                user_steps[cid]='become_admin'
                bot.send_message(cid,"In the 'VIEW USERS' section, send the user ID of the person you want to become an admin.",reply_markup=markup)
    elif data == 'view_banned_user':
        bot.answer_callback_query(call_id,'ADMIN')
        if not cid in ban_user_cid:
            bot.edit_message_reply_markup(cid,mid,reply_markup=None)
            if len(ban_user_cid) != 0 :
                for user in ban_user_cid:
                    first_name = get_name_from_user(user)[0]
                    markup=InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton('UNBAN USER',callback_data=f'unban_user_{user}'))
                    bot.send_message(cid,f'first name : {first_name}\ncid : {user}',reply_markup=markup)
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('BACK',callback_data='cancel_admin_tool'))
                bot.send_message(cid,'these are all of banned users!!',reply_markup=markup)
            else:
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('BACK',callback_data='cancel_admin_tool'))
                bot.send_message(cid,"don't have banned users!!",reply_markup=markup)
    elif data.startswith('unban_user_'):
        bot.answer_callback_query(call_id,'ADMIN')
        if not cid in ban_user_cid:
            bot.edit_message_reply_markup(cid,mid,reply_markup=None)
            user_cid = int(data.split('_')[-1])
            ban_obj = ban_user_cid[user_cid]
            if user_cid in ban_user_cid:
                schedule.cancel_job(ban_obj)
                ban_user_cid.pop(user_cid)
                bot.send_message(user_cid,'The bot admin has removed you from the ban list.')
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('BACK',callback_data='cancel_admin_tool'))
            bot.send_message(cid,f'user {user_cid} unbanned!!',reply_markup=markup)
    elif data == 'view_users_for_admin':
        bot.answer_callback_query(call_id,'ADMIN')
        if not cid in ban_user_cid:
            bot.edit_message_reply_markup(cid,mid,reply_markup=None)
            bot.delete_message(cid,mid)
            if cid in admins:
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('BACK',callback_data='cancel_admin_tool'))
                user_steps[cid]='view_users_admin'
                bot.send_message(cid,'Enter the start ID and the end ID to view their information.\nLike that:\n\nSTART ID\nEND ID',reply_markup=markup)
    elif data == 'cancel_admin_tool':
        bot.answer_callback_query(call_id,'ADMIN')
        if not cid in ban_user_cid:
            bot.edit_message_reply_markup(cid,mid,reply_markup=None)
            if cid in user_steps:
                user_steps.pop(cid)
            bot.edit_message_reply_markup(cid,mid,reply_markup=None)
            bot.send_message(cid,'/start again!')
    elif data.startswith('ban_user_'):
        bot.answer_callback_query(call_id,'ADMIN')
        if not cid in ban_user_cid:
            bot.edit_message_reply_markup(cid,mid,reply_markup=None)
            user_cid = data.split('_')[-1]
            user_first_name=get_name_from_user(user_cid)[0]
            user_steps[cid]=f'get_min_for_ban_{user_cid}'
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('BACK',callback_data='cancel_admin_tool'))
            bot.send_message(cid,f'How many minutes do you want to ban the user {user_first_name} for?\njust enter minutes:',reply_markup=markup)
    elif data.startswith('change_time_sleep_'):
        bot.answer_callback_query(call_id,'ADMIN')
        if not cid in ban_user_cid:
            bot.edit_message_reply_markup(cid,mid,reply_markup=None)
            _,__,___,tittle,description,required_min,ID,time_sleep,min_need=data.split('_')
            edit_sleep_time(cid,str(time_sleep),int(min_need))
            insert_task_data(cid,tittle,description,required_min,ID)
            hideboard=ReplyKeyboardRemove()
            bot.send_message(cid,'sleep time changed!!',reply_markup=hideboard)
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('HOME',callback_data='home'))
            bot.send_message(cid,'All of your tasks have been saved !',reply_markup=markup)
            insert_user_hour_list(cid)
            all_task_min.pop(cid)
            task_ID.pop(cid)
    elif data.startswith('change_task_time_'):
        bot.answer_callback_query(call_id,'CHANGE TASK TIME')
        if not cid in ban_user_cid:
            bot.edit_message_reply_markup(cid,mid,reply_markup=None)
            _,__,___,tittle,description,required_min,ID,time_sleep=data.split('_')
            insert_task_data(cid,tittle,description,required_min,ID)
            hideboard=ReplyKeyboardRemove()
            bot.send_message(cid,'task time changed!!',reply_markup=hideboard)
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('HOME',callback_data='home'))
            bot.send_message(cid,'All of your tasks have been saved !',reply_markup=markup)
            insert_user_hour_list(cid)
            all_task_min.pop(cid)
            task_ID.pop(cid)
    elif data == 'completed_tasks':
        bot.answer_callback_query(call_id,'VIEW COMPLETED TASKS')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            func_data=get_task_data(cid,'FINISHED')
            message = "These are the tasks you have successfully completed :\n\n\n"
            for task in func_data:
                message +=f"TASK NAME : {task[0]}\n"
                message +=f"TASK DESCRIPTION :\n{task[1]}\n"
                message +=f"Task minutes required : {task[3]}\n\n\n"
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('BACK',callback_data='task'))
            bot.send_message(cid,message,reply_markup=markup)
    elif data == 'uncompleted_tasks':
        bot.answer_callback_query(call_id,'VIEW UNCOMPLETED TASKS')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            func_data=get_task_data(cid,'UNFINISHED')
            message = "These are the tasks you completed unsuccessfully :\n\n\n"
            for task in func_data:
                message +=f"TASK NAME : {task[0]}\n"
                message +=f"TASK DESCRIPTION :\n{task[1]}\n"
                message +=f"Task minutes required : {task[3]}\n\n\n"
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('BACK',callback_data='task'))
            bot.send_message(cid,message,reply_markup=markup)
    elif data == 'finished_tasks':
        bot.answer_callback_query(call_id,'VIEW FINISHED TASKS')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            func_data=get_task_data(cid,'PASSED_TIME')
            message = "These are the tasks that was passed, and you have not said they are finished or not :\n\n\n"
            for task in func_data:
                message +=f"TASK NAME : {task[0]}\n"
                message +=f"TASK DESCRIPTION :\n{task[1]}\n"
                message +=f"Task minutes required : {task[3]}\n\n\n"
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('BACK',callback_data='task'))
            bot.send_message(cid,message,reply_markup=markup)
    elif data == 'Pending_tasks':
        bot.answer_callback_query(call_id,'VIEW PENDING TASKS')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            func_data=get_task_data(cid,'NOT_TIME')
            message = "These are the tasks that are pending and whose time has not come yet :\n\n\n"
            for task in func_data:
                message +=f"TASK NAME : {task[0]}\n"
                message +=f"TASK DESCRIPTION :\n{task[1]}\n"
                message +=f"Task minutes required : {task[3]}\n\n\n"
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('BACK',callback_data='task'))
            bot.send_message(cid,message,reply_markup=markup)
    elif data == 'all_tasks_result':
        bot.answer_callback_query(call_id,'VIEW ALL TASKS')
        if not cid in ban_user_cid:
            bot.delete_message(cid,mid)
            func_data = get_all_task_data(cid)
            message = "These are all of your tasks :\n\n\n"
            for task in func_data:
                message +=f"TASK NAME : {task[0]}\n"
                message +=f"TASK STATUS : {task[2]}\n"
                message +=f"TASK DESCRIPTION :\n{task[1]}\n"
                message +=f"Task minutes required : {task[3]}\n\n\n"
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('BACK',callback_data='task'))
            main_message=message.replace("NOT_TIME","PENDING").replace("PASSED_TIME","PASSED").replace("FINISHED","SUCCESSFULL COMPLETED").replace("UNFINISHED","UNSUCCESSFULL COMPLETED")
            bot.send_message(cid,main_message,reply_markup=markup)
    elif data.startswith('successful_work_'):
        bot.answer_callback_query(call_id,'GOOD JOB')
        if not cid in ban_user_cid:
            _,__,task_id = data.split("_")
            edit_status_task(cid,int(task_id),'FINISHED')
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('GOOD JOB',callback_data='nothing'))
            markup.add(InlineKeyboardButton('HOME',callback_data='home'))
            bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
            add_success_work_to_user(cid)
            add_coin_to_user(cid,1)
    elif data.startswith('unsuccessful_work_'):
        bot.answer_callback_query(call_id,'TRY HARDER')
        if not cid in ban_user_cid:
            _,__,task_id = data.split("_")
            edit_status_task(cid,task_id,'UNFINISHED')
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('TRY HARDER',callback_data='nothing'))
            markup.add(InlineKeyboardButton('HOME',callback_data='home'))
            bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
            add_unsuccess_work_to_user(cid)
    elif data.startswith('successful_day'):
        bot.answer_callback_query(call_id,'GOOD JOB')
        if not cid in ban_user_cid:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('GOOD JOB',callback_data='nothing'))
            markup.add(InlineKeyboardButton('HOME',callback_data='home'))
            bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
            add_success_day_to_user(cid)
            add_coin_to_user(cid,2)
    elif data.startswith('unsuccessful_day'):
        bot.answer_callback_query(call_id,'TRY HARDER')
        if not cid in ban_user_cid:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('TRY HARDER',callback_data='nothing'))
            markup.add(InlineKeyboardButton('HOME',callback_data='home'))
            bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
            add_unsuccess_day_to_user(cid)
    elif data.startswith('get_admin_'):
        bot.answer_callback_query(call_id,'TRY HARDER')
        if not cid in ban_user_cid:
            bot.edit_message_reply_markup(cid,mid,reply_markup=None)
            if cid == admin:
                user_cid = int(data.split('_')[-1])
                admins.append(user_cid)
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('BACK',callback_data='cancel_admin_tool'))
                bot.send_message(cid,f'user with cid {user_cid} is admin now!!',reply_markup=markup)
                bot.send_message(user_cid,'You have been made an admin by the main bot admin!!')
    elif data == 'nothing':
        bot.answer_callback_query(call_id,'NOTHING')







@bot.message_handler(func= lambda message: user_steps.get(message.chat.id) == 'wakeup_sleep_A')
def step_wakeup_sleep_A_handle(message):
    cid=message.chat.id
    logging.info(f'user step {user_steps[cid]} for user {cid}')
    time = message.text
    w_t = time.split(":")
    if len(w_t) == 2 :
        time_list=[]
        if w_t[0].isdigit() and w_t[1].isdigit():
            hour = w_t[0]
            minute = w_t[1]
            if 0 <= int(hour) < 25 and  0 <= int(minute) < 60:
                time_list.append(str(hour).zfill(2))
                time_list.append(str(minute).zfill(2))
                wakup_time = ':'.join(time_list)
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('YES',callback_data=f'wakeup_sleep_A_{wakup_time}_yes'),InlineKeyboardButton('NO',callback_data='wakeup_sleep_A_no'))
                bot.send_message(cid,f'Do you mean {wakup_time} ?',reply_markup=markup)
            else:
                bot.send_message(cid,'Enter it correctly\nEnter again!')
                user_steps.pop(cid)
                take_wakeup_time(cid)
        else:
            bot.send_message(cid,'Enter number like  12:00\nEnter again!')
            user_steps.pop(cid)
            take_wakeup_time(cid)
    else:
        bot.send_message(cid,'Enter hour:minute\nEnter again!')
        user_steps.pop(cid)
        take_wakeup_time(cid)







@bot.message_handler(func= lambda message: user_steps.get(message.chat.id) == 'wakeup_sleep_B')
def step_wakeup_sleep_B_handle(message):
    cid=message.chat.id
    logging.info(f'user step {user_steps[cid]} for user {cid}')
    time = message.text
    w_t = time.split(":")
    if len(w_t) == 2 :
        time_list=[]
        if w_t[0].isdigit() and w_t[1].isdigit():
            hour = w_t[0]
            minute = w_t[1]
            if 0 <= int(hour) < 25 and  0 <= int(minute) < 60:
                time_list.append(str(hour).zfill(2))
                time_list.append(str(minute).zfill(2))
                wakup_time = ':'.join(time_list)
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('YES',callback_data=f'wakeup_sleep_B_{wakup_time}_yes'),InlineKeyboardButton('NO',callback_data='wakeup_sleep_B_no'))
                bot.send_message(cid,f'Do you mean {wakup_time} ?',reply_markup=markup)
            else:
                bot.send_message(cid,'Enter it correctly\nEnter again!')
                user_steps.pop(cid)
                bot.send_message(cid,'Please enter sleeping time :(HH:MM)')
                user_steps[cid] = 'wakeup_sleep_B'
        else:
            bot.send_message(cid,'Enter number like  12:00\nEnter again!')
            user_steps.pop(cid)
            bot.send_message(cid,'Please enter sleeping time :(HH:MM)')
            user_steps[cid] = 'wakeup_sleep_B'
    else:
        bot.send_message(cid,'Enter hour:minute\nEnter again!')
        user_steps.pop(cid)
        bot.send_message(cid,'Please enter sleeping time :(HH:MM)')
        user_steps[cid] = 'wakeup_sleep_B'









@bot.message_handler(func= lambda message: user_steps.get(message.chat.id) == 'save_chat_note')
def step_save_chat_note_handle(message):
    cid=message.chat.id
    logging.info(f'user step {user_steps[cid]} for user {cid}')
    from_note='CHAT'
    mid = message.message_id
    first_name=message.chat.first_name
    note=message.text
    # bot.edit_message_reply_markup(cid,mid,reply_markup=None)
    insert_note_data(cid,from_note,first_name,note)
    print('note saved')
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('HOME',callback_data='home'))
    bot.send_message(cid,'your message saved successfully!')
    bot.send_message(cid,'Lets gooo!', reply_markup=markup)




@bot.message_handler(func =lambda message: user_steps.get(message.chat.id) == f'receive_task_{task_ID.get(message.chat.id)}')
def step_save_chat_note_handle(message):
    global all_task_min
    cid=message.chat.id
    logging.info(f'user step {user_steps[cid]} for user {cid}')
    time_wake , time_sleep , min_have =get_wakeup_sleep_time(cid)
    answer = message.text
    if answer.lower() == 'stop':
        hideboard=ReplyKeyboardRemove()
        bot.send_message(cid,f'You enter {task_ID[cid]-1} task!',reply_markup=hideboard)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('HOME',callback_data='home'))
        bot.send_message(cid,f'Tasks will start soon!!',reply_markup=markup)
        user_steps.pop(cid)
        if task_ID[cid] != 1:
            insert_user_hour_list(cid)
            all_task_min.pop(cid)
            task_ID.pop(cid)
    else:
        data = answer.split('\n')
        if len(data) == 3:
            tittle , description , required_min = data
            if required_min.isdigit():
                if not cid in all_task_min:
                    all_task_min[cid]=0
                required_min = int(required_min)
                all_task_min[cid] += required_min
                min_difference = min_have - all_task_min[cid]
                if min_difference >= 0:
                    insert_task_data(cid,tittle,description,required_min,task_ID[cid])
                    markup=InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton('NEXT TASK',callback_data='main_task'))
                    bot.send_message(cid,f'Task {task_ID[cid]} has been saved !\nYou have {min_difference} minute remaining.\nEnter your next task or finish it with sending STOP !',reply_markup=markup)
                    task_ID[cid] +=1
                else:
                    min_need = min_difference * -1
                    new_sleep_time=add_time(str(time_sleep),min_need)
                    markup=InlineKeyboardMarkup()
                    CTT=f'{tittle}_{description}_{int(required_min)-int(min_need)}_{task_ID[cid]}_{time_sleep}'
                    CST=f'{tittle}_{description}_{int(required_min)}_{task_ID[cid]}_{new_sleep_time}_{min_need}'
                    markup.add(InlineKeyboardButton('CHANGE SLEEP TIME',callback_data=f'change_time_sleep_{CST}'))
                    if int(required_min)-int(min_need) > 0 :
                        markup.add(InlineKeyboardButton('CHANGE TASK TIME',callback_data=f'change_task_time_{CTT}'))
                    caption=f"""
You are supposed to wake up at {time_wake} and go to sleep at {time_sleep} !
In total, you're supposed to have {min_have} minutes of time during your day!
But if we add the time for this task, you're supposed to sleep at {new_sleep_time} !
Do you want me to change your sleep time to {new_sleep_time}, or reduce the time needed for your task by {min_need} minutes to sleep at {time_sleep} ?
"""
                    bot.send_message(cid,caption,reply_markup=markup)
            else:
                hideboard=ReplyKeyboardRemove()
                bot.send_message(cid,'Enter number in the third line !',reply_markup=hideboard)
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('AGAIN',callback_data='main_task'))
                bot.send_message(cid,'Repeat again!!\nEnter your next task or finish it with sending STOP !',reply_markup=markup)
        else:
            hideboard=ReplyKeyboardRemove()
            bot.send_message(cid,'Enter your task as above !',reply_markup=hideboard)
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('AGAIN',callback_data='main_task'))
            bot.send_message(cid,'Repeat again!\nEnter your next task or finish it with sending STOP !',reply_markup=markup)

                




# [('task1', 'vxcovi', 'PASSED_TIME', 30, 1), ('task2', 'vxov', 'PASSED_TIME', 90, 2), ('newtask1', 'cvo', 'PASSED_TIME', 40, 3), ('newtask2', 'cvoix', 'PASSED_TIME', 80, 4)]#
@bot.message_handler(func= lambda message: user_steps.get(message.chat.id) == 'get_task_id_for_deleting')
def step_get_task_for_deleting_handle(message):
    cid=message.chat.id
    logging.info(f'user step {user_steps[cid]} for user {cid}')
    func_data = get_task_data(cid,'NOT_TIME')
    user_answer = message.text
    task_id_list= []
    for task in func_data:
        task_id_list.append(task[-1])
    if user_answer.isdigit():
        if int(user_answer) in task_id_list:
            task_obj = time_line_list[cid]['tasks'][int(user_answer)]
            schedule.cancel_job(task_obj)
            time_line_list[cid]['tasks'].pop(int(user_answer))
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('HOME',callback_data='home'))
            user_steps.pop(cid)
            edit_status_task(cid,int(user_answer),'PASSED_TIME')
            bot.send_message(cid,f'Task with ID : {user_answer} deleted!!',reply_markup=markup)
            delete_task_id.setdefault(cid, []).append(int(user_answer))
    else:
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('HOME',callback_data='home'))
        user_steps.pop(cid)
        bot.send_message(cid,f'Task with ID : {user_answer}',reply_markup=markup)





# (ID , CID , FIRST_NAME , LAST_NAME , USERNAME ,REGISTER_DATE , LAST_UPDATE)
# [(ID , CID , FIRST_NAME , LAST_NAME , USERNAME ,REGISTER_DATE , LAST_UPDATE),(ID , CID , FIRST_NAME , LAST_NAME , USERNAME ,REGISTER_DATE , LAST_UPDATE)]
@bot.message_handler(func= lambda message: user_steps.get(message.chat.id) == 'view_users_admin')
def step_view_users_info_admin_handle(message):
    cid=message.chat.id
    logging.info(f'user step {user_steps[cid]} for user {cid}')
    user_answer = message.text
    answer_list = user_answer.split('\n')
    if len(answer_list) == 2:
        start_id , end_id = answer_list
        start_id = int(start_id)
        end_id = int(end_id)
        if start_id == end_id :
            func_data = view_users_for_admin(cid,start_id,end_id)
            user_id = func_data[0]
            user_cid = func_data[1]
            user_first_name = func_data[2]
            user_last_name = func_data[3]
            user_username = func_data[4]
            user_register = str(func_data[5])
            user_register_last_update = str(func_data[6])
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('BAN USER',callback_data=f'ban_user_{user_cid}'))
            markup.add(InlineKeyboardButton('BACK',callback_data='view_users_for_admin'))
            message =f"ID : {user_id}\ncid : {user_cid}\nfirst name : {user_first_name}\nlast name : {user_last_name}\nuser name : {user_username}\nuser register : {user_register}\nuser register update : {user_register_last_update}"
            bot.send_message(cid,message,reply_markup=markup)
            user_steps.pop(cid)
        elif start_id < end_id:
            funcs_data = view_users_for_admin(cid,start_id,end_id)
            for func_data in funcs_data:
                user_id = func_data[0]
                user_cid = func_data[1]
                user_first_name = func_data[2]
                user_last_name = func_data[3]
                user_username = func_data[4]
                user_register = str(func_data[5])
                user_register_last_update = str(func_data[6])
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('BAN USER',callback_data=f'ban_user_{user_cid}'))
                message =f"ID : {user_id}\ncid : {user_cid}\nfirst name : {user_first_name}\nlast name : {user_last_name}\nuser name : {user_username}\nuser register : {user_register}\nuser register update : {user_register_last_update}"
                bot.send_message(cid,message,reply_markup=markup)
                time.sleep(1)
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('BACK',callback_data='view_users_for_admin'))
            bot.send_message(cid,'These were the users you selected.',reply_markup=markup)
            user_steps.pop(cid)
        else:#>
            funcs_data = view_users_for_admin(cid,start_id,end_id)
            for func_data in funcs_data:
                user_id = func_data[0]
                user_cid = func_data[1]
                user_first_name = func_data[2]
                user_last_name = func_data[3]
                user_username = func_data[4]
                user_register = str(func_data[5])
                user_register_last_update = str(func_data[6])
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('BAN USER',callback_data=f'ban_user_{user_cid}'))
                message =f"ID : {user_id}\ncid : {user_cid}\nfirst name : {user_first_name}\nlast name : {user_last_name}\nuser name : {user_username}\nuser register : {user_register}\nuser register update : {user_register_last_update}"
                bot.send_message(cid,message,reply_markup=markup)
                time.sleep(1)
            user_steps.pop(cid)
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('BACK',callback_data='view_users_for_admin'))
            bot.send_message(cid,'These were the users you selected.',reply_markup=markup)
    else:
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('BACK',callback_data='cancel_admin_tool'))
        bot.send_message(cid,'WRONG FORMAT\nEXAMPLE:\n\n0\n3',reply_markup=markup)
        user_steps.pop(cid)








@bot.message_handler(func=lambda message: (user_steps.get(message.chat.id, '').startswith('get_min_for_ban')))
def step_ban_user_with_cid_admin_handle(message):
    cid=message.chat.id
    logging.info(f'user step {user_steps[cid]} for user {cid}')
    user_answer = message.text
    if user_answer.isdigit():
        user_cid = user_steps[cid].split('_')[-1]
        today = datetime.now()
        time =today.strftime("%H:%M")
        target_time = add_time(time,int(user_answer))
        text = f'The {user_answer} minute ban is over. You are no longer banned!!'
        if user_cid != admin:
            ban_object = schedule.every().day.at(check_time_true_format(target_time)).do(job,cid=int(user_cid),message=text,markup='ban_user',task_id='ban_user')
            ban_user_cid[int(user_cid)]=ban_object
        bot.send_message(user_cid,f'You have been banned for {int(user_answer)+2} minutes, and you can use the bot again after the ban time at {add_time(target_time,2)} is over.')
        user_steps.pop(cid)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('BACK',callback_data='cancel_admin_tool'))
        bot.send_message(cid,f'user {user_cid} banned',reply_markup=markup)




@bot.message_handler(func= lambda message: user_steps.get(message.chat.id) == 'become_admin')
def step_become_admin_handle(message):
    cid=message.chat.id
    logging.info(f'user step {user_steps[cid]} for user {cid}')
    user_answer = message.text
    user_answer = int(user_answer)
    if str(user_answer).isdigit():
        func_data = give_user_id_list()
        if user_answer in func_data:
            user_data = get_user_date_with_id(user_answer)
            user_cid = user_data[0]
            user_first_name = user_data[1]
            user_last_name = user_data[2]
            user_username = user_data[3]
            if not user_cid in admins:
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('YES',callback_data=f'get_admin_{user_cid}'),InlineKeyboardButton('NO',callback_data='cancel_admin_tool'))
                text = f'user CID : {user_cid}\nfirst name : {user_first_name}\nlast name : {user_last_name}\nuser name : {user_username}'
                bot.send_message(cid,f'Are you sure you want to make the following user an admin?\n\n{text}',reply_markup=markup)
            else:
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('BACK',callback_data='cancel_admin_tool'))
                bot.send_message(cid,'user already is admin!!',reply_markup=markup)
            user_steps.pop(cid)
        else:
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('BACK',callback_data='cancel_admin_tool'))
            user_steps.pop(cid)
            bot.send_message(cid,'No user exists with the entered ID.',reply_markup=markup)
    else:
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('BACK',callback_data='cancel_admin_tool'))
        bot.send_message(cid,'send just id of user like:\n\n1',reply_markup=markup)
        user_steps.pop(cid)





@bot.message_handler(func= lambda message: user_steps.get(message.chat.id) == 'give_username_for_support')
def step_give_username_for_support_handle(message):
    cid=message.chat.id
    logging.info(f'user step {user_steps[cid]} for user {cid}')
    username = message.text
    global support_user_username
    support_user_username = username
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('BACK',callback_data='cancel_admin_tool'))
    user_steps.pop(cid)
    bot.send_message(cid,f'user with user name : @{username} become to support team!',reply_markup=markup)









# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    cid=message.chat.id
    if not cid in ban_user_cid:
        bot.reply_to(message, message.text)









def job(cid,message,markup,task_id):
    if markup=='NO':
        is_send_wakeup_message[cid]=True
        bot.send_message(cid,message)
        wakeup_obj = time_line_list[cid]['wakeup']
        schedule.cancel_job(wakeup_obj)
        time_line_list[cid].pop('wakeup')
        logging.info(f'send wake up message for user {cid}')
        print('job done!!')
    elif markup == 'yes_sleep':
        if task_id == 'sleep_wakeup':
            if cid in is_send_wakeup_message:
                logging.info(f'send sleep message for user {cid}')
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('YES',callback_data=f'successful_day'),InlineKeyboardButton('NO',callback_data=f'unsuccessful_day'))
                bot.send_message(cid,message,reply_markup=markup)
                sleep_obj = time_line_list[cid]['sleep']
                schedule.cancel_job(sleep_obj)
                time_line_list[cid].pop('sleep')
                is_send_wakeup_message.pop(cid)
                print('job done!!')
                # user_hour_list.pop(cid)
    elif markup == 'yes_task':
            if cid in is_send_wakeup_message:
                logging.info(f'send task message for user {cid}')
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('YES',callback_data=f'successful_work_{task_id}'),InlineKeyboardButton('NO',callback_data=f'unsuccessful_work_{task_id}'))
                bot.send_message(cid,message,reply_markup=markup)
                edit_status_task(cid,task_id,'PASSED_TIME')
                task_obj = time_line_list[cid]['tasks'][task_id]
                schedule.cancel_job(task_obj)
                time_line_list[cid]['tasks'].pop(task_id)
                print('job done!!')
    elif markup == 'ban_user':
        logging.info(f'send unban message for user {cid}')
        bot.send_message(cid,message)
        ban_obj = ban_user_cid[cid]
        schedule.cancel_job(ban_obj)
        ban_user_cid.pop(cid)
        print('job done!!')







def after_delete_schedule_list_add_every_user():
    users = after_delete_schedule_list()
    for user in users:
        insert_user_hour_list(user[0])








#[('1', 'df', 'NOT_YET', 200), ('2', 'dsfdsf', 'NOT_YET', 60)]
#user_hour_list = { cid : {wakeup_cid_wakeup  :  [time,message]   ,sleep_cid_sleep : [time,message] , task1 : [time,mesage]} }
def insert_user_hour_list(cid):
    logging.info(f'func insert_user_hour_list for user {cid}')
    wakeup_time,sleep_time , _ = get_wakeup_sleep_time(cid)
    wakeup_time_message = 'Good morning💫\nWake up and start your day!\nyour task starts now!!'
    sleep_time_message  = 'Good job💫\nYou finished your day!\nhope to had good day!!\nTomorrow will start again!\nBUT YOU CAN CANCEL IT!!\nDid you finish it successfully?'
    task_id='sleep_wakeup'
    user_hour_list[cid]={}
    user_hour_list[cid][f'wakeup_{cid}_wakeup'] = [str(wakeup_time) , wakeup_time_message , task_id]
    user_hour_list[cid][f'sleep_{cid}_sleep'] = [str(sleep_time) , sleep_time_message , task_id]
    func_data = get_task_data(cid,'NOT_TIME')
    start_time = wakeup_time
    for task in func_data:
        message =f'task  {task[0]}  finished!!\nDid you finish it successfully?'
        time = add_time(start_time,task[3])
        user_hour_list[cid][task[0]] = [str(time) , message , task[4]]
        start_time=time
    do_schedule(cid)






def do_schedule(cid):
    logging.info(f'func do_schedule for user {cid}')
    if cid in user_hour_list:
        time_line_list[cid]={}
        time_line_list[cid]['tasks']={}
        check_wakeup= f'wakeup_{cid}_wakeup'
        check_sleep= f'sleep_{cid}_sleep'
        for task in user_hour_list[cid]:
            time , message , task_id = user_hour_list[cid][task]
            if task == check_wakeup:
                time = check_time_true_format(time)
                wakeup = schedule.every().day.at(time).do(job,cid=cid,message=message, markup='NO',task_id=task_id)
                time_line_list[cid]['wakeup']=wakeup
            elif task == check_sleep:
                markup = 'yes_sleep'
                sleep = schedule.every().day.at(check_time_true_format(add_time(time,1))).do(job,cid=cid,message=message,markup=markup,task_id=task_id)
                time_line_list[cid]['sleep']=sleep
            else:
                markup = 'yes_task'
                task_obj = schedule.every().day.at(check_time_true_format(time)).do(job,cid=cid,message=message,markup=markup,task_id=task_id)
                time_line_list[cid]['tasks'][task_id]=task_obj
        # print('______________________________')
        # for i in time_line_list[cid]:
        #     print(time_line_list[cid][i])
        #     print('______________________________')







def worker():
    while True:
        schedule.run_pending()
        time.sleep(120)

t1 = threading.Thread(target=worker)
t1.start()









bot.infinity_polling()