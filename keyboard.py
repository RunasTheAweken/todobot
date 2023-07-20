from telebot import types

def generate_keyboard(tasks):
    keyboard = types.InlineKeyboardMarkup()
    for i, task in enumerate(tasks):
        status = '✅' if task['done'] else '❌'
        button_text = f"{i+1}. {task['task']} - {status}"
        button_callback = f"done_{i}"
        button = types.InlineKeyboardButton(text=button_text, callback_data=button_callback)
        keyboard.add(button)
    return keyboard

def generate_delete_keyboard(tasks):
    keyboard = types.InlineKeyboardMarkup()
    for i, task in enumerate(tasks):
        button_text = f"{i+1}. {task['task']}"
        button_callback = f"delete_{i}"
        button = types.InlineKeyboardButton(text=button_text, callback_data=button_callback)
        keyboard.add(button)
    return keyboard
