from telebot import types

commands_set = f"List of available bot commands:\n" \
               f"/start - welcome message\n" \
               f"/today, /t - list of all tasks for today\n" \
               f"/delete, /d - deleting all completed tasks\n" \
               f"Create and save a task when you enter text in the message field\n" \
               f"task_id done - the task is marked as completed\n" \
               f"task_id delete - the task is deleted"


def delete_completed_plans_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton("✅ yes, delete all completed tasks")
    btn2 = types.KeyboardButton("❗ no, don't delete all completed tasks")
    markup.add(btn1, btn2)
    return markup
