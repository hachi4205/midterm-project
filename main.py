import pickle
import os

player = {
    "status": "배고픔",
    "location": "연대앞 버스정류장",
    "HP": 10,
    "balance": 50000,
    "inventory": []
}

environment = {"time": 11}
settings = {"difficulty": "보통"}
input_history = []

map_grid = [
    ["", "", "", "", "새천년관", "이윤재관"],
    ["백양관", "백양로5", "대강당", "음악관", "알렌관", "ABMRC"],
    ["중앙도서관", "독수리상", "학생회관", "루스채플", "재활병원", "치과대학"],
    ["체육관", "백양로3", "공터2", "광혜원", "어린이병원", "세브란스병원"],
    ["공학관", "백양로2", "백주년기념관", "안과병원", "제중관", ""],
    ["공학원", "백양로1", "공터1", "암병원", "의과대학", ""],
    ["연대앞 버스정류장", "정문", "스타벅스", "세브란스병원 버스정류장", "", ""]
]

shop_items = {
    "학생회관": {
        "두쫀쿠": {"price": 5000, "HP_gain": 25},
        "카페라떼": {"price": 2500, "HP_gain": 25}
    }
}

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
        print(f"{item_name}을(를) 구매해서 가방에 넣었다. 계좌 잔액: {player['balance']}원")

def show_status():
    print(f"계좌의 잔액: {player['balance']}원")
    print(f"HP: {player['HP']}")

def show_inventory():
    if len(player["inventory"]) == 0:
        print("가방이 비어있습디다.")
        return 
    print("가방 안의 물건들: ") 
    for i, item in enumerate(player["inventory"], start=1):
        print(f"{i}) {item}")

def use_item(item_name):
    if item_name not in player["inventory"]:
        print(f"가방에 {item_name}이(가) 없습니다.")
        return

    for shop_name, items in shop_items.items():
        if item_name in items:
            HP_gain = items[item_name]["HP_gain"]
            player["HP"] += HP_gain
            player["inventory"].remove(item_name)
            print(f"{item_name}을(를) 먹었습니다. HP: {player['HP']}")
            return

def save_game():
    filename = input("저장할 파일명을 입력하세요 (예: save1): ")
    
    if not filename.endswith(".pkl"):
        filename += ".pkl"
    
    save_data = {
        "player": player,
        "environment": environment,
        "settings": settings,
        "row": row,
        "col": col,
        "input_history": input_history
    }
    
    with open(filename, "wb") as f:
        pickle.dump(save_data, f)
    
    print(f"게임이 {filename}에 저장되었습니다.")

def load_game():
    global player, environment, settings, row, col, input_history
    
    pkl_files = [f for f in os.listdir(".") if f.endswith(".pkl")]
    
    if len(pkl_files) > 0:
        print("현재 폴더의 저장 파일들:")
        for i, name in enumerate(pkl_files, start=1):
            print(f"{i}) {name}")
        print("또는 파일 경로를 직접 입력하세요 (상대경로/절대경로 모두 가능)")
    else:
        print("현재 폴더에 저장 파일이 없습니다.")
        print("파일 경로를 직접 입력하세요 (상대경로/절대경로 모두 가능)")
    
    choice = input("불러올 파일의 번호 또는 경로를 입력하세요: ")
    
    filename = None
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(pkl_files):
            filename = pkl_files[idx]
        else:
            print("잘못된 번호입니다.")
            return
    else:
        filename = choice
    
    if not os.path.exists(filename):
        print(f"파일을 찾을 수 없습니다: {filename}")
        return
    
    try:
        with open(filename, "rb") as f:
            save_data = pickle.load(f)
        
        player = save_data["player"]
        environment = save_data["environment"]
        settings = save_data["settings"]
        row = save_data["row"]
        col = save_data["col"]
        input_history = save_data["input_history"]
        
        print(f"{filename}에서 게임을 불러왔습니다.")
        print(f"현재 위치: {player['location']}, HP: {player['HP']}, 잔액: {player['balance']}원")
    except Exception as e:
        print(f"불러오기 실패: {e}")

row = 6
col = 0 

while True:
    user_input = input("입력: ")
    input_history.append(user_input)

    if user_input == "상태":
        show_status()
        continue
    elif user_input == "가방":
        show_inventory()
        if len(player["inventory"]) > 0:
            sub_input = input("사용할 물건의 이름 또는 번호를 입력하세요 (또는 '종료'): ")
            if sub_input == "종료":
                continue
            if sub_input.isdigit():
                idx = int(sub_input) - 1
                if 0 <= idx < len(player["inventory"]):
                    use_item(player["inventory"][idx])
                else:
                    print("잘못된 번호입니다.")
            else:
                use_item(sub_input)
        continue
    elif user_input == "구매":
            interact_shop()
            continue
    elif user_input == "저장":
        save_game()
        continue
    elif user_input == "불러오기":
        load_game()
        continue

    direction = user_input

    new_row = row
    new_col = col

    if direction == "북":
        new_row = row - 1
    elif direction == "남":
        new_row = row + 1
    elif direction == "동":
        new_col = col + 1
    elif direction == "서":
        new_col = col - 1
    else:
        print("잘못된 입력입니다. 동/서/남/북 중에서 선택하세요.")
        continue

    if new_row < 0 or new_row >= len(map_grid) or new_col < 0 or new_col >= len(map_grid[0]):
        print("그 방향은 막혔어.")
        continue

    if map_grid[new_row][new_col] == "":
        print("그 방향은 막혔어.")
        continue
    
    row = new_row
    col = new_col
    player["location"] = map_grid[row][col]
    player["HP"] -= 1

    print(f"현재 위치: {player['location']}")