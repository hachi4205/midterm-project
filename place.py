from io_helper import get_input

class Place:
    def __init__(self, name, buy_items=None, sell_prices=None, 
                 event_info=None, quest_role=None):
        self.name = name
        self.buy_items = buy_items       
        self.sell_prices = sell_prices     
        self.event_info = event_info       
        self.quest_role = quest_role
    
    def get_interactions(self):
        interactions = []
        if self.buy_items:
            interactions.append("구매")
        if self.sell_prices:
            interactions.append("판매")
        if self.quest_role:
            interactions.append("임무")
        return interactions
    
    def show_event(self):
        if self.event_info:
            print(self.event_info)
    
    def buy(self, player):
        if not self.buy_items:
            print("이곳에서는 구매할 수 없습니다.")
            return
        
        item_list = list(self.buy_items.keys())
        while True:
            print("구매 가능한 품목:")
            for i, item_name in enumerate(item_list, start=1):
                info = self.buy_items[item_name]
                print(f"{i}) {item_name}: {info['price']}원, HP +{info['HP_gain']}")
            print(f"{len(item_list) + 1}) 종료")
            
            choice = get_input("선택하세요: ")
            
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
            price = self.buy_items[item_name]["price"]
            if player.balance < price:
                print("잔액이 부족합니다.")
                continue
            player.balance -= price
            player.inventory.append(item_name)
            print(f"{item_name}을(를) 구매해서 가방에 넣었다. 계좌 잔액 = {player.balance}원")
    
    def sell(self, player):
        if not self.sell_prices:
            print("이곳에서는 판매할 수 없습니다.")
            return
        
        while True:
            counts = {}
            for item in player.inventory:
                counts[item] = counts.get(item, 0) + 1
            
            sellable = {name: qty for name, qty in counts.items() 
                       if name in self.sell_prices}
            
            if len(sellable) == 0:
                print("팔 것이 없어서 종료합니다.")
                return
            
            print("무엇을 판매하시겠습니까?")
            item_list = list(sellable.keys())
            for i, item_name in enumerate(item_list, start=1):
                print(f"{i}) {item_name} x{sellable[item_name]}")
            print(f"{len(item_list) + 1}) 종료")
            
            choice = get_input("선택하세요: ")
            
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
            price = self.sell_prices[item_name]
            player.inventory.remove(item_name)
            player.balance += price
            print(f"{item_name}를 판매해서 {price}원을 벌었다. 계좌 잔액 = {player.balance}원")
    
    def handle_quest(self, player):
        from data import quest_questions, quest_answers
        from quest import quests
        from io_helper import get_input
    
        intro_name = "독수리상으로 가기"
        main_quest_names = ["교내 부조리 수사", "교내 위생사건 수사"]
        
        if self.quest_role == "give_intro":
            if (intro_name not in player.quests 
                    and intro_name not in player.completed_quests):
                print(quests[intro_name].description)
                player.quests.append(intro_name)
                print("[임무목록]에 임무가 추가되었습니다.")
            else:
                print("이미 독수리상으로 가는 임무를 받았습니다.")
            return
        
        if self.quest_role == "give_quests":
            if intro_name in player.quests:
                player.quests.remove(intro_name)
                player.completed_quests.append(intro_name)
                print(f"다음의 임무가 해결되었다! [{quests[intro_name].description}]")
            
            for q_name in main_quest_names:
                if (q_name not in player.quests 
                        and q_name not in player.completed_quests):
                    player.quests.append(q_name)
                    print(quests[q_name])
            return
        
        if self.quest_role in ("report_bujori", "report_wisaeng"):
            info = quest_questions[self.name]
            quest_name = info["quest_name"]
            
            if quest_name not in player.quests:
                if quest_name in player.completed_quests:
                    print("이미 완료한 임무입니다.")
                else:
                    print("먼저 독수리상에서 임무를 받아오세요.")
                return
            
            print(info["question"])
            answer = get_input("입력: ")
            
            if answer == quest_answers[quest_name]:
                player.quests.remove(quest_name)
                player.completed_quests.append(quest_name)
                print(f"다음의 임무가 해결되었다! [{quest_name}]")
                print("수업들으러 이윤재관 가야지!")
            else:
                print("답이 틀렸습니다.")
            return
        
        if self.quest_role == "final":
            bujori_done = "교내 부조리 수사" in player.completed_quests
            wisaeng_done = "교내 위생사건 수사" in player.completed_quests
            bujori_in_progress = "교내 부조리 수사" in player.quests
            wisaeng_in_progress = "교내 위생사건 수사" in player.quests
            
            if (not bujori_done and not wisaeng_done 
                    and not bujori_in_progress and not wisaeng_in_progress):
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

def build_places():
    from data import (map_grid, shop_items, sell_places_high, 
                     sell_places_normal, sell_prices, quest_places, 
                     event_info)
    
    places = {}
    
    all_names = set()
    for row in map_grid:
        for name in row:
            if name: 
                all_names.add(name)
    
    for name in all_names:
        buy = shop_items.get(name)  
        
        sell = None
        if name in sell_places_high:
            sell = sell_prices["high"]
        elif name in sell_places_normal:
            sell = sell_prices["normal"]
        
        event = event_info.get(name)
        
        quest_role = None
        if name == "정문":
            quest_role = "give_intro"
        elif name == "독수리상":
            quest_role = "give_quests"
        elif name == "본관":
            quest_role = "report_bujori"
        elif name == "세브란스":
            quest_role = "report_wisaeng"
        elif name == "이윤재관":
            quest_role = "final"
        
        places[name] = Place(
            name=name,
            buy_items=buy,
            sell_prices=sell,
            event_info=event,
            quest_role=quest_role
        )
    
    return places

places = build_places()