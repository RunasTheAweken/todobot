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
