import telebot
from telebot import types
bot = telebot.TeleBot("dd")
Spisok = "Здесь будут задачи"
toollist = []
daylist = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]



class New_Task:
    def __init__ (self, text, time = "", day = ""):
        self.text = text
        self.time = time
        self.day = day


@bot.message_handler(commands = ["start"])
def send_Start (message):
    bot.send_message(message.chat.id, "Привет! Это бот список задач. Напиши 'Новая задача', для добавления новой задачи или 'список дел' для просмотра списка дел")
    markup = types.ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True, one_time_keyboard = True)
    new_task_btn = types.KeyboardButton("Новая задача")
    tasks_btn = types.KeyboardButton("Список дел")
    markup.add(new_task_btn, tasks_btn)
    bot.send_message(message.chat.id, "Кнопки", reply_markup = markup)

@bot.message_handler(content_types = ["text"])
def send_Answer(message):
    
    user_Text = message.text
    user_Text = user_Text.lower()
    if user_Text == "новая задача":
        
        bot.send_message(message.chat.id, "Введите название задачи")
        

    elif user_Text == "список дел":
        text_list = ""
        if len(toollist) == 0:
            text_list = "Ваш список пока что пуст"
        for i, task in enumerate(toollist):
            text_list += f"Ваши задачи на ближайшее время:\n задача {i + 1} {task.text}\n"
        bot.send_message(message.chat.id, text_list)
    else:
        new_Task_Name = message.text
        new_Task = New_Task(new_Task_Name)
        toollist.append(new_Task)
        bot.send_message(message.chat.id, f"Добавлена задача {new_Task.text}")
        keyboard = types.InlineKeyboardMarkup()
        for i in daylist:
            daybtn = types.InlineKeyboardButton(f"{i}", callback_data = i)
            keyboard.add(daybtn)
        bot.send_message(message.chat.id, "Выберите день недели", reply_markup = keyboard)

bot.polling(non_stop = True, interval = 0)
