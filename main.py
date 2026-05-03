import state
from actions import (show_quests, open_bag,
                     cmd_buy, cmd_sell, cmd_quest, cmd_difficulty) 
from save_load import save_game, load_game
from io_helper import get_input, say, init_log_files, close_log_files

action_map = {
    "상태": state.player.print_status,
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
    init_log_files() 

    try:
        say("송도 생활을 마치고 신촌에 처음 도착했다. 연대앞 버스정류장이다.")
        say("현재 시각은 11시.")
        say("임무완료를 보고할 장소는 이윤재관 511호다.")
        say("배가 고프다.")

        while True:
            user_input = get_input("입력: ")

            if user_input == "종료":
                say("게임을 종료합니다.")
                break

            if user_input in action_map:
                result = action_map[user_input]()   
                if result == "GAME_OVER":         
                    break
            elif user_input in direction_set:
                state.player.move(user_input)
            else:
                say("잘못된 입력입니다.")
    finally:
        close_log_files()

if __name__ == "__main__":
    main()