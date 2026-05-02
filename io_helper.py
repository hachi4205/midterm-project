import state

_input_file = None
_output_file = None
_input_counter = 0
_output_counter = 0

def init_log_files(input_path="player_input.txt", output_path="game_output.txt"):
    global _input_file, _output_file, _input_counter, _output_counter
    _input_file = open(input_path, "w", encoding="utf-8")
    _output_file = open(output_path, "w", encoding="utf-8")
    _input_counter = 0
    _output_counter = 0

def close_log_files():
    global _input_file, _output_file
    if _input_file:
        _input_file.close()
        _input_file = None
    if _output_file:
        _output_file.close()
        _output_file = None

def get_input(prompt=""):
    global _input_counter, _output_counter
    
    user_input = input(prompt)
    state.input_history.append(user_input)
    
    _input_counter += 1
    if _input_file:
        _input_file.write(f"[{_input_counter}] {user_input}\n")
        _input_file.flush()
    
    _output_counter += 1
    if _output_file:
        _output_file.write(f"[{_output_counter}] {prompt}{user_input}\n")
        _output_file.flush()
    
    return user_input

def say(*args, **kwargs):
    global _output_counter
    
    print(*args, **kwargs)
    
    sep = kwargs.get("sep", " ")
    end = kwargs.get("end", "\n")
    text = sep.join(str(a) for a in args)
    
    _output_counter += 1
    if _output_file:
        _output_file.write(f"[{_output_counter}] {text}{end}")
        _output_file.flush()