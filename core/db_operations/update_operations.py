from models import User, Planner


def make_done_handler(chat_id, plan_id):
    user = User.get(User.chat_id == chat_id)
    plan = Planner.get(Planner.user == user, Planner.id == plan_id)
    plan.is_done = True
    plan.save()
