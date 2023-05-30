from datetime import datetime

from models import User, Planner


def create_user_handler(chat_id):
    if not User.select().where(User.chat_id == chat_id):
        User.create(
            chat_id=chat_id
        )


def create_task_handler(chat_id, message_text):
    user = User.get(User.chat_id == chat_id)
    Planner.create(
        user=user,
        task=message_text,
        date=datetime.today()
    )
