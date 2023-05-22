from datetime import datetime
from os import getenv
from models import User, Planner
from threading import Thread
import telebot
import schedule
import time


bot = telebot.TeleBot(getenv('TELEBOT_TOKEN', default=''))


@bot.message_handler(commands=['start'])
def start_handler(message):
    if not User.select().where(User.chat_id == message.chat.id):
        User.create(
            chat_id=message.chat.id
        )
    bot.send_message(
        message.chat.id,
        f"Hello, {message.chat.first_name} {message.chat.last_name or ''}!"
    )


def create_all_plans_list(chat_id):
    user = User.get(User.chat_id == chat_id)
    plans = Planner.select().where(Planner.user == user,
                                   Planner.date == datetime.today(),
                                   Planner.is_done == False)
    message_text = []

    for plan in plans:
        if plan.is_done:
            message_text.append(f"<s>{plan.id}. {plan.task}</s>\n")
        else:
            message_text.append(f"<b>{plan.id}. {plan.task}</b>\n")

    return "".join(message_text)


@bot.message_handler(commands=['today', 't'])
def get_planner_list(message):
    bot.send_message(
        message.chat.id,
        create_all_plans_list(message.chat.id) or "‍💫 There are no tasks for today.",
        parse_mode='HTML'
    )


@bot.message_handler(regexp="\d+ done")
def make_done(message):
    plan_id = message.text.split(" ")[0]
    plan = Planner.get(Planner.id == plan_id)
    plan.is_done = True
    plan.save()

    bot.send_message(
        message.chat.id,
        f"✅ <b>{plan.task}</b> is done!",
        parse_mode='HTML'
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
                create_all_plans_list(user.chat_id),
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
