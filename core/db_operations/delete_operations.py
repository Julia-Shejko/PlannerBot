from models import User, Planner


def delete_plan_by_number_handler(chat_id, plan_id):
    user = User.get(User.chat_id == chat_id)
    del_plan = Planner.delete().where(Planner.user == user,
                                      Planner.id == plan_id)
    del_plan.execute()


def delete_completed_tasks_process_handler(chat_id):
    user = User.get(User.chat_id == chat_id)
    del_completed_plans = Planner.delete().where(Planner.user == user,
                                                 Planner.is_done == True)
    del_completed_plans.execute()
