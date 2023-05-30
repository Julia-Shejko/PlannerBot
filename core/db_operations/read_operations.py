from datetime import datetime

from models import User, Planner


def make_all_today_plans_list(chat_id):
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