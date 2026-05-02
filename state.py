class Player:
    def __init__(self):
        self.status = "배고픔"
        self.location = "연대앞 버스정류장"
        self.HP = 10.0
        self.balance = 10000
        self.inventory = []
        self.quests = []
        self.completed_quests = []
        self.row = 6
        self.col = 0
    
    def print_status(self):
        from actions import get_neighbors
        from io_helper import say
        neighbors = get_neighbors()
        say(f"계좌의 잔액 = {self.balance}원")
        say(f"HP = {self.HP}")
        say(f"현재위치 = {self.location}")
        say(f"동서남북 = {neighbors['동']}, {neighbors['서']}, {neighbors['남']}, {neighbors['북']}")
    
    def move(self, direction):
        from data import map_grid, event_info, hp_loss_by_difficulty
        from place import places
        from io_helper import say
        
        new_row, new_col = self.row, self.col
        if direction == "북":
            new_row = self.row - 1
        elif direction == "남":
            new_row = self.row + 1
        elif direction == "동":
            new_col = self.col + 1
        elif direction == "서":
            new_col = self.col - 1
        
        if (new_row < 0 or new_row >= len(map_grid)
                or new_col < 0 or new_col >= len(map_grid[0])
                or map_grid[new_row][new_col] == ""):
            say("그 방향은 막혔어.")
            return
        
        self.row, self.col = new_row, new_col
        self.location = map_grid[self.row][self.col]
        
        difficulty = settings["difficulty"]
        hp_loss = hp_loss_by_difficulty.get(difficulty, 1)
        self.HP -= hp_loss

        place = places[self.location]

        move_msg = f"{self.location}에 도착했다."
        if place.event_info:
            move_msg += f" {place.event_info}"

        interactions = place.get_interactions()
        if interactions:
            move_msg += f" [{', '.join(interactions)}]"

        say(move_msg)

player = Player()

environment = {"time": 11}
settings = {"difficulty": "보통"}
input_history = []