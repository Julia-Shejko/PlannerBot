from datetime import datetime
from os import getenv
from models import User, Planner
import telebot


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
                                   Planner.date == datetime.today())
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


if __name__ == "__main__":
    bot.infinity_polling()
