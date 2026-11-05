"""state.json이 없을 때 쓰는 기본 퀴즈. 주제는 파이썬과 Git 기초다."""

from quiz import Quiz


def create_default_quizzes():
    return [
        Quiz(
            "변수에 값을 넣지 않고 print(x)를 실행하면 나는 오류는?",
            ["TypeError", "NameError", "ValueError", "IndexError"],
            2,
            "이름을 찾지 못했다는 뜻의 오류입니다.",
        ),
        Quiz(
            "[10, 20, 30][1]의 값은?",
            ["10", "20", "30", "오류가 난다"],
            2,
            "인덱스는 0부터 셉니다.",
        ),
        Quiz(
            "키와 값을 짝지어 저장하는 자료형은?",
            ["list", "str", "dict", "bool"],
            3,
            "사전을 떠올려 보세요.",
        ),
        Quiz(
            "반복 횟수를 미리 알 수 없을 때 더 자연스러운 반복문은?",
            ["for", "while", "if", "def"],
            2,
            "조건이 참인 동안 계속 도는 반복문입니다.",
        ),
        Quiz(
            "클래스의 메서드에서 객체 자신을 가리키는 첫 번째 매개변수의 관례적인 이름은?",
            ["this", "me", "self", "cls_obj"],
            3,
            "영어로 '자기 자신'입니다.",
        ),
        Quiz(
            "파일을 다룬 뒤 자동으로 닫아 주는 문법은?",
            ["with open(...) as f:", "try open(...):", "for open(...):", "def open(...):"],
            1,
            "컨텍스트 매니저라고 부르는 문법입니다.",
        ),
        Quiz(
            "원격 저장소의 변경 사항을 가져와 현재 브랜치에 합치는 Git 명령은?",
            ["git push", "git commit", "git clone", "git pull"],
            4,
            "fetch와 merge를 합친 명령입니다.",
        ),
        Quiz(
            "feature 브랜치의 작업을 main에 합치는 올바른 순서는?",
            [
                "git merge main → git checkout feature",
                "git checkout main → git merge feature",
                "git push feature → git pull main",
                "git commit main → git add feature",
            ],
            2,
            "합칠 곳으로 먼저 이동합니다.",
        ),
    ]
