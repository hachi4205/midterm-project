import state
from actions import (show_status, show_quests, open_bag, move,
                     cmd_buy, cmd_sell, cmd_quest, cmd_difficulty) 
from save_load import save_game, load_game

action_map = {
    "상태": show_status,
    "임무": cmd_quest,
    "난이도": cmd_difficulty,
    "임무목록": show_quests,      
    "가방": open_bag,
    "구매": cmd_buy,       
    "판매": cmd_sell,         
    "저장": save_game,
    "불러오기": load_game,
}

direction_set = {"동", "서", "남", "북"}

def main():
    print("송도 생활을 마치고 신촌에 처음 도착했다. 연대앞 버스정류장이다.")
    print("학교에 들어가기 위해 정문에서 상호작용을 한다.")
    print("학교에서 어떤 일이 벌어지고있을까?")
    print("배가 고프다.")

    while True:
        user_input = input("입력: ")
        state.input_history.append(user_input)

        if user_input == "종료":
            print("게임을 종료합니다.")
            break

        if user_input in action_map:
            result = action_map[user_input]()   
            if result == "GAME_OVER":         
                break
        elif user_input in direction_set:
            move(user_input)
        else:
            print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()