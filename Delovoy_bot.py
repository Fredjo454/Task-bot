import telebot
import json
from telebot import types
<<<<<<< HEAD
import datetime
import time as wait
import threading
bot = telebot.TeleBot("7947822600:AAGZvbWR11xPppVrV4UKzV41DNB-mEWz0N0")
=======
bot = telebot.TeleBot("dd")
>>>>>>> c70f1d7b9e5701b2d0da013e1b839d63b8c80a6c
Spisok = "Здесь будут задачи"
chatstoollist = {}
JSONNAME = "files.json"
daylist = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
timesttarts = 0
timeends = 23
btns = ["✅", "❌", "🗒", "🕑"]
bot.remove_webhook()

class New_Task:
    def __init__ (self, text, time = "", day = ""):
        self.id = wait.time()
        self.text = text
        self.time = time
        self.day = day
        self.message_id = 0



def get_data (day_Name):
    if not day_Name:
        return None
    weekday = wait.localtime().tm_wday
    
    daymapping = {"Понедельник": 0, "Вторник": 1, "Среда": 2, "Четверг": 3, "Пятница": 4, "Суббота": 5, "Воскресенье": 6}
    if day_Name in daymapping:
        targetday = daymapping[day_Name]
        daysDeadline = targetday - weekday
        if daysDeadline < 0:
            daysDeadline += 7
        
        return daysDeadline
    return None
def check ():
    while True:
        try:
            chatstoollist = jsonread()

            for chatid, toollist in chatstoollist.items() :
                for task in toollist:
                    if task.day:
                        due_date = get_data(task.day)
                        if due_date:
                            daysUntil = get_data(task.day)
                            if daysUntil == 1:
                                chatidday = int(chatid)
                                message = f"В {task.day} нужно сделать {task.text} "
                                if task.time:
                                    message += f"Время {task.time}"
                                    try:
                                        bot.send_message(chatidday, message)
                                    except Exception as e:
                                        print(e)
            wait.sleep(3600)
        except Exception as e:
            print(e) 
            wait.sleep(300)  

def startThread ():
    Thread = threading.Thread(target = check)
    Thread.daemon = True
    Thread.start()                         

def encode_task (task):
    return {"type":"Task", "id": task.id, "text": task.text, "time": task.time, "day": task.day, "message_id": task.message_id}

def decode_task (task):
    if task.get("type") == "Task":

        id = task.get("id")
        name = task.get("text")
        time = task.get("time")
        day = task.get("day")
        message_id = task.get("message_id")
        new_task = New_Task(name, time, day)
        new_task.id = id
        new_task.message_id = message_id
        return new_task
    else:
        return task

def jsonsave (chatstoollist):
    with open (JSONNAME, "w") as file:
        json.dump(chatstoollist, file, default = encode_task)

def jsonread ():
    with open (JSONNAME) as file:
        data = json.load(file, object_hook = decode_task)
        
        print(data)
        return data


def get_toollist (chatid):
    global chatstoollist
    chatstoollist = jsonread()
    toollist = chatstoollist.get(str(chatid))
    if toollist == None:
        toollist = []
    return toollist
def day_Select (call, idtask, dayindex):
    toollist = get_toollist(call.message.chat.id)
    for i, task in enumerate(toollist):
        if task.id == idtask:
            task.day = daylist[dayindex]
            chatstoollist[call.message.chat.id] = toollist
            jsonsave(chatstoollist)
            bot.edit_message_text(f"Заплонировано на {task.day}", call.message.chat.id, call.message.message_id)
            bot.answer_callback_query(call.id)


def hour_Select (call, idtask, time):
    toollist = get_toollist(call.message.chat.id)
    for i, task in enumerate(toollist):
        if task.id == idtask:
            task.time = time
            chatstoollist[call.message.chat.id] = toollist
            jsonsave(chatstoollist)
            bot.edit_message_text(f"Заплонировано на {task.time}", call.message.chat.id, call.message.message_id)
            bot.answer_callback_query(call.id)
    

@bot.callback_query_handler(func = lambda call: True)
def button_tap (call):
    print(f"Нажали кнопку {call.data}")
    data = json.loads(call.data)
    print(data)
    idtask = data["id"]
    actiontask = data["action"]
    print(f"{idtask}, {actiontask}")
    toollist = get_toollist(call.message.chat.id)
    if actiontask == btns[0]:
        for task in toollist:
            if task.id == idtask:
                toollist.remove(task)
                bot.edit_message_text("Задача выполнена", call.message.chat.id, call.message.message_id)
                chatstoollist[call.message.chat.id] = toollist
                jsonsave(chatstoollist)
                bot.answer_callback_query(call.id)
    elif actiontask == btns[1]:
        for task in toollist:
            if task.id == idtask:
                toollist.remove(task)
                bot.edit_message_text("Задача отменена", call.message.chat.id, call.message.message_id)
                chatstoollist[call.message.chat.id] = toollist
                jsonsave(chatstoollist)
                bot.answer_callback_query(call.id)


    elif actiontask == btns[2]:
        bot.edit_message_text(call.message.text, call.message.chat.id, call.message.message_id, reply_markup = day_keyboard(idtask))


                
    elif actiontask == "i":
        dayindex = data.get("dayindex")
        day_Select(call, idtask, dayindex)
    elif actiontask == btns[3]:
        bot.edit_message_text(call.message.text, call.message.chat.id, call.message.message_id, reply_markup = hour_keyboard(idtask))
    elif actiontask == "time":
        time = data.get("time")
        hour_Select(call, idtask, time)
    
    

@bot.message_handler(commands = ["start"])
def send_Start (message):
    bot.send_message(message.chat.id, "Привет! Это бот список задач. Напиши 'Новая задача', для добавления новой задачи или 'список дел' для просмотра списка дел")
    markup = types.ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True, one_time_keyboard = True)
    new_task_btn = types.KeyboardButton("Новая задача")
    tasks_btn = types.KeyboardButton("Список дел")
    markup.add(new_task_btn, tasks_btn)
    bot.send_message(message.chat.id, "Кнопки", reply_markup = markup)

def day_keyboard (idtask):
    keyboard = types.InlineKeyboardMarkup()
    keyboardbtns = []
    for i in daylist:
        data = {"id": idtask, "action": "i"}
        data["dayindex"] = daylist.index(i)
        jsonstring = json.dumps(data)
        daybtn = types.InlineKeyboardButton(f"{i}", callback_data = jsonstring)
        print(len(jsonstring))
        keyboardbtns.append(daybtn)
    keyboard.add(*keyboardbtns)
    return keyboard

def hour_keyboard (idtask):
    keyboard = types.InlineKeyboardMarkup()
    keyboardbtns = []
    for i in range (timesttarts, timeends):
        data = {"id": idtask, "action": "time"}
        timestr = f"{i}:00"
        data["time"] = timestr
        jsonstring = json.dumps(data)
        
        hourbtn = types.InlineKeyboardButton(timestr, callback_data = jsonstring)
        keyboardbtns.append(hourbtn)
    keyboard.add(*keyboardbtns)
    return keyboard

    


def task_keyboard (task_keyboard_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboardbtns = []
    for g in btns:
        data = {"id":task_keyboard_id, "action":g}
        print(data)
        jsonstring = json.dumps(data)
        print(jsonstring)
        taskbtn = types.InlineKeyboardButton(g, callback_data = jsonstring)
        keyboardbtns.append(taskbtn)
        print(jsonstring)
    keyboard.add(*keyboardbtns)
    return keyboard

@bot.message_handler(content_types = ["text"])
def send_Answer(message):
    
    user_Text = message.text
    user_Text = user_Text.lower()
    toollist = get_toollist(message.chat.id)
    if toollist == None:
        toollist = []
    if user_Text == "новая задача":
        
        bot.send_message(message.chat.id, "Введите название задачи")
        

    elif user_Text == "список дел":
        text_list = ""
        
        if len(toollist) == 0:
            text_list = "Ваш список пока что пуст"
            return
        for i, task in enumerate(toollist):
            bot.delete_message(message.chat.id, task.message_id)
            text_list = f"Ваши задачи на ближайшее время:\n задача {i + 1} {task.text} {task.day} в {task.time}\n"
            new_message = bot.send_message(message.chat.id, text_list, reply_markup = task_keyboard(task.id))
            task.message_id = new_message.id
            chatstoollist[message.chat.id] = toollist
            jsonsave(chatstoollist)
    else:
        new_Task_Name = message.text
        new_Task = New_Task(new_Task_Name)
        toollist.append(new_Task)
        new_message = bot.send_message(message.chat.id, f"Добавлена задача {new_Task.text}")
        new_Task.message_id = new_message.id
        print(new_message.id)
        chatstoollist[message.chat.id] = toollist
        jsonsave(chatstoollist)
        bot.send_message(message.chat.id, "Выберите день", reply_markup = day_keyboard(new_Task.id))
        bot.send_message(message.chat.id, "Выберите время", reply_markup = hour_keyboard(new_Task.id))
    print(message.chat.id)

<<<<<<< HEAD
startThread()
bot.polling(non_stop = True, interval = 0)
=======
bot.polling(non_stop = True, interval = 0)
>>>>>>> c70f1d7b9e5701b2d0da013e1b839d63b8c80a6c
