import state
from state import player
from data import map_grid, valid_difficulties, shop_items
from quest import quests
from io_helper import get_input, say
from place import places

def get_neighbors():
    neighbors = {}
    if state.player.row - 1 >= 0 and map_grid[state.player.row - 1][state.player.col] != "":
        neighbors["북"] = map_grid[state.player.row - 1][state.player.col]
    else:
        neighbors["북"] = "막힘"

    if state.player.row + 1 < len(map_grid) and map_grid[state.player.row + 1][state.player.col] != "":
        neighbors["남"] = map_grid[state.player.row + 1][state.player.col]
    else:
        neighbors["남"] = "막힘"

    if state.player.col + 1 < len(map_grid[0]) and map_grid[state.player.row][state.player.col + 1] != "":
        neighbors["동"] = map_grid[state.player.row][state.player.col + 1]
    else:
        neighbors["동"] = "막힘"

    if state.player.col - 1 >= 0 and map_grid[state.player.row][state.player.col - 1] != "":
        neighbors["서"] = map_grid[state.player.row][state.player.col - 1]
    else:
        neighbors["서"] = "막힘"
    return neighbors

def open_bag():
    if len(player.inventory) == 0:
        say("가방이 비어있습니다.")
        return
    say("가방 안의 물건들:")
    for i, item in enumerate(player.inventory, start=1):
        say(f"{i}) {item}")

    sub_input = get_input("사용할 물건의 이름 또는 번호를 입력하세요 (또는 '종료'): ")
    if sub_input == "종료":
        return
    if sub_input.isdigit():
        idx = int(sub_input) - 1
        if 0 <= idx < len(player.inventory):
            use_item(player.inventory[idx])
        else:
            say("잘못된 번호입니다.")
    else:
        use_item(sub_input)


def use_item(item_name):
    if item_name not in player.inventory:
        say(f"가방에 {item_name}이(가) 없습니다.")
        return
    for shop_name, items in shop_items.items():
        if item_name in items:
            HP_gain = items[item_name]["HP_gain"]
            player.HP += HP_gain
            player.inventory.remove(item_name)
            say(f"{item_name}을(를) 먹었습니다. HP = {player.HP}")
            return


def show_quests():
    if len(state.player.quests) == 0:
        say("현재 가지고있는 임무가 없습니다.")
        return
    say("[임무목록]")
    for q_name in state.player.quests:
        if q_name in quests:
            say(f"- {quests[q_name]}")   
        else:
            say(f"- {q_name}")

def cmd_buy():
    place = places[state.player.location]
    place.buy(state.player)

def cmd_sell():
    place = places[state.player.location]
    place.sell(state.player)

def cmd_quest():
    place = places[state.player.location]
    if not place.quest_role:
        say("이곳에서는 임무가 없습니다.")
        return
    return place.handle_quest(state.player)

def cmd_difficulty():
    current = state.settings["difficulty"]
    say(f"현재 난이도: {current}")
    say("난이도를 변경하시겠습니까?")
    for i, d in enumerate(valid_difficulties, start=1):
        say(f"{i}) {d}")
    say(f"{len(valid_difficulties) + 1}) 변경하지 않음")
    
    choice = get_input("선택하세요: ")
    
    if choice == str(len(valid_difficulties) + 1):
        say("난이도를 변경하지 않습니다.")
        return
    
    if not choice.isdigit():
        say("숫자를 입력하세요.")
        return
    idx = int(choice) - 1
    if idx < 0 or idx >= len(valid_difficulties):
        say("잘못된 선택입니다.")
        return
    
    new_difficulty = valid_difficulties[idx]
    state.settings["difficulty"] = new_difficulty
    say(f"난이도가 '{new_difficulty}'(으)로 변경되었습니다.")