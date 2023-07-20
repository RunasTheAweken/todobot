import telebot
from telebot import types
import task_storage
import keyboard as kb

bot = telebot.TeleBot('6386726014:AAEl8HbtVBILgpetBaix6KPMysCnpLS88OU')

@bot.message_handler(commands=['start'])
def start(message):
    task_storage.load_tasks(message.chat.id)
    bot.send_message(message.chat.id, "Welcome to the Todo Bot! Here are the available commands:\n/add - Add a new task\n/list - Show all tasks\n/delete - Delete a task")

@bot.message_handler(commands=['add'])
def add(message):
    msg = bot.send_message(message.chat.id, "Please enter the task you want to add:")
    bot.register_next_step_handler(msg, process_add)

def process_add(message):
    task_storage.tasks.append({'task': message.text, 'done': False})
    task_storage.save_tasks(message.chat.id)
    bot.send_message(message.chat.id, "Task added successfully!")

@bot.callback_query_handler(func=lambda call: call.data.startswith('done_'))
def done(call):
    index = int(call.data.split('_')[1])
    task_storage.tasks[index]['done'] = not task_storage.tasks[index]['done']
    task_storage.save_tasks(call.message.chat.id)
    bot.answer_callback_query(call.id, "Task updated!")
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=kb.generate_keyboard(task_storage.tasks))

@bot.message_handler(commands=['list'])
def list_tasks(message):
    if not task_storage.tasks:
        bot.send_message(message.chat.id, "No tasks found.")
        return
    keyboard = kb.generate_keyboard(task_storage.tasks)
    bot.send_message(message.chat.id, "Here are your tasks:", reply_markup=keyboard)

@bot.message_handler(commands=['delete'])
def delete(message):
    if not task_storage.tasks:
        bot.send_message(message.chat.id, "No tasks found.")
        return
    keyboard = kb.generate_delete_keyboard(task_storage.tasks)
    bot.send_message(message.chat.id, "Select the task you want to delete:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_'))
def process_delete(call):
    index = int(call.data.split('_')[1])
    del task_storage.tasks[index]
    task_storage.save_tasks(call.message.chat.id)
    bot.answer_callback_query(call.id, "Task deleted!")
    if not task_storage.tasks:
        bot.edit_message_text("No tasks found.", call.message.chat.id, call.message.message_id)
        return
    keyboard = kb.generate_delete_keyboard(task_storage.tasks)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=keyboard)

bot.polling()
