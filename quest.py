class Quest:
    def __init__(self, name, description, report_to=None):
        self.name = name
        self.description = description
        self.report_to = report_to
    
    def __str__(self):
        return f"{self.name} - {self.description}"

def build_quests():
    quests = {
        "독수리상으로 가기": Quest(
            name="독수리상으로 가기",
            description="학교에서 어떤 일들이 일어나고있는지 소식들이 모이는 독수리상에서 알아보자.",
            report_to=None
        ),
        "교내 부조리 수사": Quest(
            name="교내 부조리 수사",
            description="교내 어딘가에서 부조리가 일어나고있다. 이동하고 상호작용을 해서 부조리를 찾아서 보고하라.",
            report_to="본관"
        ),
        "교내 위생사건 수사": Quest(
            name="교내 위생사건 수사",
            description="학생들이 단체로 식중독에 걸렸다. 이동하고 상호작용을 해서 위생사건의 원인을 찾아서 보고하라.",
            report_to="세브란스"
        ),
    }
    return quests

quests = build_quests()