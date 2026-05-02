import pickle
import os 

map_grid = [
    ["종합관", "본관", "경영관", "노천극장", "새천년관", "이윤재관"],
    ["백양관", "백양로5", "대강당", "음악관", "알렌관", "ABMRC"],
    ["중앙도서관", "독수리상", "학생회관", "루스채플", "재활병원", "치과대학"],
    ["체육관", "백양로3", "공터2", "광혜원", "어린이병원", "세브란스"],
    ["공학관", "백양로2", "백주년기념관", "안과병원", "제중관", ""],
    ["공학원", "백양로1", "공터1", "암병원", "의과대학", ""],
    ["연대앞 버스정류장", "정문", "스타벅스", "세브란스병원 버스정류장", "", ""]
]

shop_items = {
    "학생회관": {
        "두쫀쿠": {"price": 5000, "HP_gain": 10},
        "카페라떼": {"price": 3000, "HP_gain": 5}
    },
    "스타벅스": {
        "두쫀쿠": {"price": 4000, "HP_gain": 10},
        "카페라떼": {"price": 2000, "HP_gain": 5}
    },
    "ABMRC": {
        "두쫀쿠": {"price": 4000, "HP_gain": 10},
        "카페라떼": {"price": 2000, "HP_gain": 5}
    }
}

available_quests = {
    "교내 부조리 수사": {
        "description": "교내 어딘가에서 부조리가 일어나고있다. 이동하고 상호작용을 해서 부조리를 찾아서 보고하라.",
        "report_to": "이윤재관"
    },
    "교내 위생사건 수사": {
        "description": "학생들이 단체로 식중독에 걸렸다. 이동하고 상호작용을 해서 위생사건의 원인을 찾아서 보고하라.",
        "report_to": "이윤재관"
    }
}

intro_quest = {
    "name": "독수리상으로 가기",
    "description": "학교에서 어떤 일들이 일어나고있는지 소식들이 모이는 독수리상에서 알아보자."
}

quest_report_location = {
    "교내 부조리 수사": "본관",
    "교내 위생사건 수사": "세브란스"
}

quest_questions = {
    "본관": {
        "quest_name": "교내 부조리 수사",
        "question": "교내 어디에 부조리가 있나?"
    },
    "세브란스": {
        "quest_name": "교내 위생사건 수사",
        "question": "교내 어디에 식중독 원인이 있나?"
    }
}

buy_places = ["학생회관", "스타벅스", "ABMRC"]

sell_places_high = [
    "체육관", "공학관", "공학원", "재활병원", 
    "어린이병원", "종합관", "노천극장"
]

sell_places_normal = [
    "중앙도서관", "백양관", "대강당", "백주년기념관", 
    "안과병원", "암병원", "새천년관", "알렌관", "제중관", 
    "의과대학", "치과대학", "세브란스", "본관", "경영관"
]

sell_places = sell_places_high + sell_places_normal

sell_prices = {
    "high": {
        "두쫀쿠": 7000,
        "카페라떼": 4000
    },
    "normal": {
        "두쫀쿠": 6000,
        "카페라떼": 3000
    }
}

quest_places = ["정문", "독수리상", "본관", "세브란스", "이윤재관"]

def load_events(filepath="events.pkl"):
    if not os.path.exists(filepath):
        print(f"{filepath} 파일을 찾을 수 없습니다. create_events.py를 먼저 실행하세요.")
        return {}, {}
    
    try:
        with open(filepath, "rb") as f:
            data = pickle.load(f)
        events = data.get("events", {})
        answers = data.get("answers", {})
        return events, answers
    except Exception as e:
        print(f"events.pkl 로드 중 오류: {e}")
        return {}, {}

event_info, quest_answers = load_events()

hp_loss_by_difficulty = {
    "쉬움": 0.5,
    "보통": 1,
    "어려움": 2
}

valid_difficulties = ["쉬움", "보통", "어려움"]