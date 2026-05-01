import state
from state import player
from data import map_grid, shop_items, available_quests, intro_quest


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
    player["HP"] -= 1
    print(f"{player['location']}으로 이동했다.")


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


def interact():
    location = player["location"]

    if location == "정문":
        if intro_quest["name"] not in player["quests"]:
            print(intro_quest["description"])
            player["quests"].append(intro_quest["name"])
            print("[임무목록]에 임무가 추가되었습니다.")
        else:
            print("이미 독수리상으로 가는 임무를 받았습니다.")
        return

    if location == "독수리상":
        if intro_quest["name"] in player["quests"]:
            player["quests"].remove(intro_quest["name"])
            print(f"다음의 임무가 해결되었다! [{intro_quest['description']}]")
        for q_name, q_info in available_quests.items():
            if q_name not in player["quests"]:
                player["quests"].append(q_name)
                print(f"{q_name} - {q_info['description']}")
        return

    if location == "학생회관":
        interact_shop()
        return

    if location == "이윤재관":
        remaining = [q for q in player["quests"] if q in available_quests]
        if intro_quest["name"] in player["quests"]:
            print("먼저 독수리상에 가서 임무를 받아오세요.")
            return
        if len(remaining) == 0:
            print("모든 임무를 완료했습니다! 또 만나요~")
        else:
            print(f"아직 해결하지 못한 임무가 있습니다: {remaining}")
        return

    print("이곳에서는 특별한 상호작용이 없습니다.")