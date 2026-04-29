player = {'status': '배고픔', 'location': '연대앞 버스정류장'}
environment = {'time': 11}

settings = {"difficulty": "보통"}

map_grid = [
    ["공학관", "백양로1", "백주년기념관"],
    ["공학원", "백양로1", "공터1"],
    ["연대앞 버스정류장", "정문", "세브란스병원 버스정류장"]
]

print(f"주인공 상태: {player['status']}")
print(f"현재 위치: {player['location']}")
print(f"현재 시각: {environment['time']}시")
print(f"난이도: {settings['difficulty']}")

row = 2
col = 0

while True:
    direction = input("이동방향을 입력하세요 (동/서/남/북): ")

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

    if new_row < 0 or new_row > 2 or new_col < 0 or new_col > 2:
        print("그 방향은 막혔어.")
        continue 
    
    if new_row < 0 or new_row > 2 or new_col < 0 or new_col > 2:
        print("그 방향은 막혔어.")
        continue 
    
    row = new_row
    col = new_col
    player["location"] = map_grid[row][col]
    
    print(f"현재 위치: {player['location']}")