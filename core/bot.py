from os import getenv
from models import User, Planner
from threading import Thread
from datetime import datetime
import telebot
import schedule
import time

from db_operations.create_operations import *
from db_operations.read_operations import *
from db_operations.update_operations import *
from db_operations.delete_operations import *
from additional_operations import *


bot = telebot.TeleBot(getenv('TELEBOT_TOKEN', default=''))


@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id
    create_user_handler(chat_id=chat_id)
    bot.send_message(
        chat_id,
        f"Hello, {message.chat.first_name} {message.chat.last_name or ''}!\n{commands_set}"
    )


@bot.message_handler(commands=['today', 't'])
def get_today_planner_list(message):
    bot.send_message(
        message.chat.id,
        make_all_today_plans_list(chat_id=message.chat.id) or "‍💫 There are no tasks for today.",
        parse_mode='HTML'
    )


@bot.message_handler(regexp="\d+ done")
def make_done(message):
    chat_id = message.chat.id
    plan_id = message.text.split()[0]
    try:
        make_done_handler(chat_id=chat_id, plan_id=plan_id)
        bot.send_message(
            chat_id,
            f"✅ <b>{plan_id}</b> is done!",
            parse_mode='HTML'
        )
    except:
        bot.send_message(
            chat_id,
            f"⛔ You have no tasks with {plan_id} number"
        )


@bot.message_handler(regexp="\d+ delete")
def delete_plan_by_number(message):
    chat_id = message.chat.id
    plan_id = message.text.split()[0]
    try:
        delete_plan_by_number_handler(chat_id=chat_id, plan_id=plan_id)
        bot.send_message(
            chat_id,
            f"☑ <b>{plan_id}</b> task was deleted!",
            parse_mode='HTML'
        )
    except:
        bot.send_message(
            chat_id,
            f"⛔ You have no tasks with {plan_id} number"
        )


@bot.message_handler(commands=['delete', 'd'])
def delete_completed_plans(message):
    bot.send_message(message.chat.id,
                     text="Do you really want to delete all completed tasks?\nSelect:",
                     reply_markup=delete_completed_plans_markup())


@bot.message_handler(regexp="delete all completed tasks")
def delete_completed_tasks_process(message):
    chat_id = message.chat.id
    if message.text == "✅ yes, delete all completed tasks":
        delete_completed_tasks_process_handler(chat_id=chat_id)
        bot.send_message(
            chat_id,
            "Completed tasks were deleted!",
        )

    else:
        bot.send_message(
            chat_id,
            "Completed tasks weren't deleted!",
        )


@bot.message_handler(content_types=['text'])
def create_task(message):
    chat_id = message.chat.id
    message_text = message.text
    create_task_handler(chat_id, message_text)
    bot.send_message(
        chat_id,
        "📑 Your task was saved."
    )


def check_notify():
    for user in User.select():
        plans = Planner.select().where(Planner.user == user,
                                       Planner.date == datetime.today(),
                                       Planner.is_done == False)
        if plans:
            bot.send_message(
                user.chat_id,
                make_all_today_plans_list(user.chat_id),
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
