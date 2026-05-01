import state
from actions import show_status, show_quests, open_bag, interact, move
from save_load import save_game, load_game

action_map = {
    "상태": show_status,
    "임무": show_quests,
    "가방": open_bag,
    "상호작용": interact,
    "저장": save_game,
    "불러오기": load_game,
}

direction_set = {"동", "서", "남", "북"}

def main():
    print("송도 생활을 마치고 신촌에 처음 도착했다. 연대앞 버스정류장이다.")
    print("임무완료를 보고할 장소는 이윤재관 511호다.")
    print("배가 고프다.")

    while True:
        user_input = input("입력: ")
        state.input_history.append(user_input)

        if user_input == "종료":
            print("게임을 종료합니다.")
            break

        if user_input in action_map:
            action_map[user_input]()
        elif user_input in direction_set:
            move(user_input)
        else:
            print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()