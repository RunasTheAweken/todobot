import telebot
from telebot import types

bot = telebot.TeleBot('6386726014:AAEl8HbtVBILgpetBaix6KPMysCnpLS88OU')

tasks = []

def get_user_file(chat_id):
    return f"{chat_id}.txt"

def save_tasks(chat_id):
    with open(get_user_file(chat_id), 'w') as f:
        for task in tasks:
            f.write(f"{task['task']},{task['done']}\n")

def load_tasks(chat_id):
    try:
        with open(get_user_file(chat_id), 'r') as f:
            lines = f.readlines()
            for line in lines:
                task, done = line.strip().split(',')
                tasks.append({'task': task, 'done': done == 'True'})
    except FileNotFoundError:
        pass

def generate_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    for i, task in enumerate(tasks):
        status = '✅' if task['done'] else '❌'
        button_text = f"{i+1}. {task['task']} - {status}"
        button_callback = f"done_{i}"
        button = types.InlineKeyboardButton(text=button_text, callback_data=button_callback)
        keyboard.add(button)
    return keyboard

def generate_delete_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    for i, task in enumerate(tasks):
        button_text = f"{i+1}. {task['task']}"
        button_callback = f"delete_{i}"
        button = types.InlineKeyboardButton(text=button_text, callback_data=button_callback)
        keyboard.add(button)
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    load_tasks(message.chat.id)
    bot.send_message(message.chat.id, "Welcome to the Todo Bot! Here are the available commands:\n/add - Add a new task\n/list - Show all tasks\n/delete - Delete a task")

@bot.message_handler(commands=['add'])
def add(message):
    msg = bot.send_message(message.chat.id, "Please enter the task you want to add:")
    bot.register_next_step_handler(msg, process_add)

def process_add(message):
    tasks.append({'task': message.text, 'done': False})
    save_tasks(message.chat.id)
    bot.send_message(message.chat.id, "Task added successfully!")

@bot.callback_query_handler(func=lambda call: call.data.startswith('done_'))
def done(call):
    index = int(call.data.split('_')[1])
    tasks[index]['done'] = not tasks[index]['done']
    save_tasks(call.message.chat.id)
    bot.answer_callback_query(call.id, "Task updated!")
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=generate_keyboard())

@bot.message_handler(commands=['list'])
def list_tasks(message):
    if not tasks:
        bot.send_message(message.chat.id, "No tasks found.")
        return
    keyboard = generate_keyboard()
    bot.send_message(message.chat.id, "Here are your tasks:", reply_markup=keyboard)

@bot.message_handler(commands=['delete'])
def delete(message):
    if not tasks:
        bot.send_message(message.chat.id, "No tasks found.")
        return
    keyboard = generate_delete_keyboard()
    bot.send_message(message.chat.id, "Select the task you want to delete:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_'))
def process_delete(call):
    index = int(call.data.split('_')[1])
    del tasks[index]
    save_tasks(call.message.chat.id)
    bot.answer_callback_query(call.id, "Task deleted!")
    if not tasks:
        bot.edit_message_text("No tasks found.", call.message.chat.id, call.message.message_id)
        return
    keyboard = generate_delete_keyboard()
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=keyboard)

bot.polling()
