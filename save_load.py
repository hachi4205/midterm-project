import pickle
import os
import state
from io_helper import get_input, say

def save_game():
    filename = get_input("저장할 파일명을 입력하세요 (예: save1): ")
    if not filename.endswith(".pkl"):
        filename += ".pkl"

    save_data = {
        "player": state.player,
        "environment": state.environment,
        "settings": state.settings,
        "input_history": state.input_history
    }
    with open(filename, "wb") as f:
        pickle.dump(save_data, f)
    say(f"게임이 {filename}에 저장되었습니다.")

def load_game():
    excluded = {"event.bin"}
    pkl_files = [f for f in os.listdir(".")
                 if (f.endswith(".pkl") or f.endswith(".bin"))
                 and f not in excluded]
    if len(pkl_files) > 0:
        say("현재 폴더의 저장 파일들:")
        for i, name in enumerate(pkl_files, start=1):
            say(f"{i}) {name}")
        say("또는 파일 경로를 직접 입력하세요 (상대경로/절대경로 모두 가능)")
    else:
        say("현재 폴더에 저장 파일이 없습니다.")
        say("파일 경로를 직접 입력하세요 (상대경로/절대경로 모두 가능)")

    choice = get_input("불러올 파일의 번호 또는 경로를 입력하세요: ")
    filename = None
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(pkl_files):
            filename = pkl_files[idx]
        else:
            say("잘못된 번호입니다.")
            return
    else:
        filename = choice

    if not os.path.exists(filename):
        say(f"파일을 찾을 수 없습니다: {filename}")
        return
    try:
        with open(filename, "rb") as f:
            save_data = pickle.load(f)
 
        state.player = save_data["player"]
        state.environment = save_data["environment"]
        state.settings = save_data["settings"]
        state.input_history = save_data["input_history"]
        say(f"{filename}에서 게임을 불러왔습니다.")
        say(f"현재 위치: {state.player.location}, HP: {state.player.HP}, 잔액: {state.player.balance}원")
    except Exception as e:
        say(f"불러오기 실패: {e}")