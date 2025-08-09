"""Interactive wrapper for goal management."""

from imp.managers import goal_manager


def get_existing_goals():
    return goal_manager.read_goals()


def add_new_goal(user_input):
    new_goal = goal_manager.add_goal(user_input)
    print(f"[+] New goal added: {new_goal}")


if __name__ == "__main__":
    user_input = input("You: ")
    add_new_goal(user_input)
