import state
from state import player
from data import (
    map_grid, shop_items, available_quests, intro_quest,
    buy_places, sell_places, quest_places, event_info,
    sell_places_high, sell_places_normal, sell_prices,
    quest_answers, quest_report_location, quest_questions,
    hp_loss_by_difficulty, valid_difficulties
)

def get_neighbors():
    neighbors = {}
    if state.row - 1 >= 0 and map_grid[state.row - 1][state.col] != "":
        neighbors["북"] = map_grid[state.row - 1][state.col]
    else:
        neighbors["북"] = "막힘"

    if state.row + 1 < len(map_grid) and map_grid[state.row + 1][state.col] != "":
        neighbors["남"] = map_grid[state.row + 1][state.col]
    else:
        neighbors["남"] = "막힘"

    if state.col + 1 < len(map_grid[0]) and map_grid[state.row][state.col + 1] != "":
        neighbors["동"] = map_grid[state.row][state.col + 1]
    else:
        neighbors["동"] = "막힘"

    if state.col - 1 >= 0 and map_grid[state.row][state.col - 1] != "":
        neighbors["서"] = map_grid[state.row][state.col - 1]
    else:
        neighbors["서"] = "막힘"
    return neighbors


def show_status():
    neighbors = get_neighbors()
    print(f"계좌의 잔액 = {player['balance']}원")
    print(f"HP = {player['HP']}")
    print(f"현재위치 = {player['location']}")
    print(f"동서남북 = {neighbors['동']}, {neighbors['서']}, {neighbors['남']}, {neighbors['북']}")

def get_available_interactions(location):
    interactions = []
    if location in buy_places:
        interactions.append("구매")
    if location in sell_places:
        interactions.append("판매")
    if location in quest_places:
        interactions.append("임무")
    return interactions

def move(direction):
    new_row, new_col = state.row, state.col

    if direction == "북":
        new_row = state.row - 1
    elif direction == "남":
        new_row = state.row + 1
    elif direction == "동":
        new_col = state.col + 1
    elif direction == "서":
        new_col = state.col - 1

    if (new_row < 0 or new_row >= len(map_grid)
            or new_col < 0 or new_col >= len(map_grid[0])
            or map_grid[new_row][new_col] == ""):
        print("그 방향은 막혔어.")
        return

    state.row, state.col = new_row, new_col
    player["location"] = map_grid[state.row][state.col]
    difficulty = state.settings["difficulty"]
    hp_loss = hp_loss_by_difficulty.get(difficulty, 1)
    player["HP"] -= hp_loss

    location = player["location"]
    move_msg = f"{location}에 도착했다."

    if location in event_info:
        move_msg += f" {event_info[location]}"

    interactions = get_available_interactions(location)
    if interactions:
        move_msg += f" [{', '.join(interactions)}]"

    print(move_msg)

def interact_shop():
    current_place = player["location"]
    if current_place not in shop_items:
        print("이곳에서는 구매할 수 없습니다.")
        return
    items = shop_items[current_place]
    item_list = list(items.keys())

    while True:
        print("구매 가능한 품목:")
        for i, name in enumerate(item_list, start=1):
            info = items[name]
            print(f"{i}) {name}: {info['price']}원, HP +{info['HP_gain']}")
        print(f"{len(item_list) + 1}) 종료")

        choice = input("선택하세요: ")

        if choice == str(len(item_list) + 1):
            print("구매를 종료합니다.")
            return
        if not choice.isdigit():
            print("숫자를 입력하세요.")
            continue
        idx = int(choice) - 1
        if idx < 0 or idx >= len(item_list):
            print("잘못된 선택입니다.")
            continue

        item_name = item_list[idx]
        price = items[item_name]["price"]
        if player["balance"] < price:
            print("잔액이 부족합니다.")
            continue
        player["balance"] -= price
        player["inventory"].append(item_name)
        print(f"{item_name}을(를) 구매해서 가방에 넣었다. 계좌 잔액 = {player['balance']}원")

def interact_sell():
    location = player["location"]
    
    if location in sell_places_high:
        prices = sell_prices["high"]
    elif location in sell_places_normal:
        prices = sell_prices["normal"]
    else:
        print("이곳에서는 판매할 수 없습니다.")
        return
    
    while True:
        counts = {}
        for item in player["inventory"]:
            counts[item] = counts.get(item, 0) + 1
        
        sellable = {name: qty for name, qty in counts.items() if name in prices}
        
        if len(sellable) == 0:
            print("팔 것이 없어서 종료합니다.")
            return
        
        print("무엇을 판매하시겠습니까?")
        item_list = list(sellable.keys())
        for i, name in enumerate(item_list, start=1):
            print(f"{i}) {name} x{sellable[name]}")
        print(f"{len(item_list) + 1}) 종료")
        
        choice = input("선택하세요: ")
        
        if choice == str(len(item_list) + 1):
            print("판매를 종료합니다.")
            return
        if not choice.isdigit():
            print("숫자를 입력하세요.")
            continue
        idx = int(choice) - 1
        if idx < 0 or idx >= len(item_list):
            print("잘못된 선택입니다.")
            continue
        
        item_name = item_list[idx]
        price = prices[item_name]
        player["inventory"].remove(item_name)
        player["balance"] += price
        print(f"{item_name}를 판매해서 {price}원을 벌었다. 계좌 잔액 = {player['balance']}원")

def open_bag():
    if len(player["inventory"]) == 0:
        print("가방이 비어있습니다.")
        return
    print("가방 안의 물건들:")
    for i, item in enumerate(player["inventory"], start=1):
        print(f"{i}) {item}")

    sub_input = input("사용할 물건의 이름 또는 번호를 입력하세요 (또는 '종료'): ")
    if sub_input == "종료":
        return
    if sub_input.isdigit():
        idx = int(sub_input) - 1
        if 0 <= idx < len(player["inventory"]):
            use_item(player["inventory"][idx])
        else:
            print("잘못된 번호입니다.")
    else:
        use_item(sub_input)


def use_item(item_name):
    if item_name not in player["inventory"]:
        print(f"가방에 {item_name}이(가) 없습니다.")
        return
    for shop_name, items in shop_items.items():
        if item_name in items:
            HP_gain = items[item_name]["HP_gain"]
            player["HP"] += HP_gain
            player["inventory"].remove(item_name)
            print(f"{item_name}을(를) 먹었습니다. HP = {player['HP']}")
            return


def show_quests():
    if len(player["quests"]) == 0:
        print("현재 가지고있는 임무가 없습니다.")
        return
    print("[임무목록]")
    for q in player["quests"]:
        if q in available_quests:
            print(f"- {q}: {available_quests[q]['description']}")
        else:
            print(f"- {q}")

def handle_quest_interaction(location):
    if location == "정문":
        if intro_quest["name"] not in player["quests"] and intro_quest["name"] not in player["completed_quests"]:
            print(intro_quest["description"])
            player["quests"].append(intro_quest["name"])
            print("[임무목록]에 임무가 추가되었습니다.")
        else:
            print("이미 독수리상으로 가는 임무를 받았습니다.")
        return
    
    if location == "독수리상":
        if intro_quest["name"] in player["quests"]:
            player["quests"].remove(intro_quest["name"])
            player["completed_quests"].append(intro_quest["name"])
            print(f"다음의 임무가 해결되었다! [{intro_quest['description']}]")

        for q_name, q_info in available_quests.items():
            if q_name not in player["quests"] and q_name not in player["completed_quests"]:
                player["quests"].append(q_name)
                print(f"{q_name} - {q_info['description']}")
        return
    
    if location in quest_questions:
        info = quest_questions[location]
        quest_name = info["quest_name"]
        
        if quest_name not in player["quests"]:
            if quest_name in player["completed_quests"]:
                print("이미 완료한 임무입니다.")
            else:
                print("먼저 독수리상에서 임무를 받아오세요.")
            return
        
        print(info["question"])
        answer = input("입력: ")
        state.input_history.append(answer)
        
        if answer == quest_answers[quest_name]:
            player["quests"].remove(quest_name)
            player["completed_quests"].append(quest_name)
            print(f"다음의 임무가 해결되었다! [{quest_name}]")
            print("수업들으러 이윤재관 가야지!")
        else:
            print("답이 틀렸습니다.")
        return
    
    if location == "이윤재관":
        bujori_done = "교내 부조리 수사" in player["completed_quests"]
        wisaeng_done = "교내 위생사건 수사" in player["completed_quests"]
        bujori_in_progress = "교내 부조리 수사" in player["quests"]
        wisaeng_in_progress = "교내 위생사건 수사" in player["quests"]
        
        if not bujori_done and not wisaeng_done and \
           not bujori_in_progress and not wisaeng_in_progress:
            print("먼저 독수리상에서 임무를 받아오세요.")
            return
        
        if bujori_done and wisaeng_done:
            print("부조리와 식중독 수사를 완료했구나! 수업은 이걸로 끝입니다. 또 만나요~")
            return "GAME_OVER"
        
        if bujori_done:
            print("부조리 수사를 완료했구나! 식중독 원인도 찾아주세요~")
        elif wisaeng_done:
            print("식중독 수사를 완료했구나! 부조리도 찾아주세요~")
        else:
            print("아직 수사를 완료하지 못했네요. 본관과 세브란스에 가서 보고하세요.")
        return

def cmd_buy():
    location = player["location"]
    if location not in buy_places:
        print("이곳에서는 구매할 수 없습니다.")
        return
    interact_shop()

def cmd_sell():
    location = player["location"]
    if location not in sell_places:
        print("이곳에서는 판매할 수 없습니다.")
        return
    interact_sell()

def cmd_quest():
    location = player["location"]
    if location not in quest_places:
        print("이곳에서는 임무가 없습니다.")
        return
    result = handle_quest_interaction(location)
    if result == "GAME_OVER":
        return "GAME_OVER"
    return None

def cmd_difficulty():
    current = state.settings["difficulty"]
    print(f"현재 난이도: {current}")
    print("난이도를 변경하시겠습니까?")
    for i, d in enumerate(valid_difficulties, start=1):
        print(f"{i}) {d}")
    print(f"{len(valid_difficulties) + 1}) 변경하지 않음")
    
    choice = input("선택하세요: ")
    state.input_history.append(choice)
    
    if choice == str(len(valid_difficulties) + 1):
        print("난이도를 변경하지 않습니다.")
        return
    
    if not choice.isdigit():
        print("숫자를 입력하세요.")
        return
    idx = int(choice) - 1
    if idx < 0 or idx >= len(valid_difficulties):
        print("잘못된 선택입니다.")
        return
    
    new_difficulty = valid_difficulties[idx]
    state.settings["difficulty"] = new_difficulty
    print(f"난이도가 '{new_difficulty}'(으)로 변경되었습니다.")