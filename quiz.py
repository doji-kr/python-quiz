"""퀴즈 한 문제를 표현한다."""


class Quiz:
    """문제, 선택지 4개, 정답 번호(1~4)를 가진 퀴즈."""

    CHOICE_COUNT = 4

    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def show(self, number):
        """문제와 선택지를 출력한다. number는 화면에 보일 문제 번호다."""
        print(f"[문제 {number}]")
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")
        print()

    def is_correct(self, answer):
        return answer == self.answer
