import state

def get_input(prompt=""):
    user_input = input(prompt)
    state.input_history.append(user_input)
    return user_input