from datetime import datetime
from os import getenv
from models import User, Planner
from threading import Thread
import telebot
from telebot import types
import schedule
import time

bot = telebot.TeleBot(getenv('TELEBOT_TOKEN', default=''))

commands_set = f"List of available bot commands:\n" \
               f"/start - welcome message\n" \
               f"/today, /t - list of all tasks for today\n" \
               f"/delete, /d - deleting all completed tasks\n" \
               f"Create and save a task when you enter text in the message field\n" \
               f"task_id done - the task is marked as completed\n" \
               f"task_id delete - the task is deleted"


@bot.message_handler(commands=['start'])
def start_handler(message):
    if not User.select().where(User.chat_id == message.chat.id):
        User.create(
            chat_id=message.chat.id
        )
    bot.send_message(
        message.chat.id,
        f"Hello, {message.chat.first_name} {message.chat.last_name or ''}!\n{commands_set}"
    )


def create_all_today_plans_list(chat_id):
    user = User.get(User.chat_id == chat_id)
    plans = Planner.select().where(Planner.user == user,
                                   Planner.date == datetime.today())
    message_text = []

    for plan in plans:
        if plan.is_done:
            message_text.append(f"<s>{plan.id}. {plan.task}</s>\n")
        else:
            message_text.append(f"<b>{plan.id}. {plan.task}</b>\n")

    return "".join(message_text)


@bot.message_handler(commands=['today', 't'])
def get_today_planner_list(message):
    bot.send_message(
        message.chat.id,
        create_all_today_plans_list(message.chat.id) or "‍💫 There are no tasks for today.",
        parse_mode='HTML'
    )


@bot.message_handler(regexp="\d+ done")
def make_done(message):
    plan_id = message.text.split(" ")[0]
    try:
        user = User.get(User.chat_id == message.chat.id)
        plan = Planner.get(Planner.user == user, Planner.id == plan_id)
        plan.is_done = True
        plan.save()
        bot.send_message(
            message.chat.id,
            f"✅ <b>{plan.task}</b> is done!",
            parse_mode='HTML'
        )
    except:
        bot.send_message(
            message.chat.id,
            f"⛔ There is no task with {plan_id} number"
        )


@bot.message_handler(regexp="\d+ delete")
def delete_plan_by_number(message):
    plan_id = message.text.split(" ")[0]
    try:
        user = User.get(User.chat_id == message.chat.id)
        Planner.get(Planner.user == user, Planner.id == plan_id)
        Planner.delete_by_id(pk=plan_id)
        bot.send_message(
            message.chat.id,
            f"☑ <b>{plan_id}</b> task was deleted!",
            parse_mode='HTML'
        )
    except:
        bot.send_message(
            message.chat.id,
            f"⛔ There is no task with {plan_id} number"
        )


@bot.message_handler(commands=['delete', 'd'])
def delete_completed_plans(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    btn1 = types.KeyboardButton("✅ yes, delete all completed tasks")
    btn2 = types.KeyboardButton("❗ no, don't delete all completed tasks")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text="Do you really want to delete all completed tasks?\nSelect:", reply_markup=markup)


@bot.message_handler(regexp="delete all completed tasks")
def delete_completed_tasks_process(message):
    if message.text == "✅ yes, delete all completed tasks":
        user = User.get(User.chat_id == message.chat.id)
        del_completed_plans = Planner.delete().where(Planner.user == user,
                                                     Planner.is_done == True)
        del_completed_plans.execute()
        bot.send_message(
            message.chat.id,
            "Completed tasks were deleted!",
        )

    else:
        bot.send_message(
            message.chat.id,
            "Completed tasks weren't deleted!",
        )


@bot.message_handler(content_types=['text'])
def create_task_handler(message):
    user = User.get(User.chat_id == message.chat.id)
    Planner.create(
        user=user,
        task=message.text,
        date=datetime.today()
    )
    bot.send_message(
        message.chat.id,
        "📑 Your task was saved."
    )


def check_notify():
    for user in User.select():
        plans = Planner.select().where(Planner.user == user,
                                       Planner.date == datetime.today())
        if plans:
            bot.send_message(
                user.chat_id,
                create_all_today_plans_list(user.chat_id),
                parse_mode='HTML'
            )


def run_schedule():
    schedule.every(1).hours.do(check_notify)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    Thread(target=run_schedule).start()
    bot.infinity_polling()
