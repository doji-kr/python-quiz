"""퀴즈 한 문제를 표현한다."""


class Quiz:
    """문제, 선택지 4개, 정답 번호(1~4), 힌트(없어도 됨)를 가진 퀴즈."""

    CHOICE_COUNT = 4

    def __init__(self, question, choices, answer, hint=None):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

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

    def to_dict(self):
        data = {"question": self.question, "choices": self.choices, "answer": self.answer}
        if self.hint:
            data["hint"] = self.hint
        return data

    @classmethod
    def from_dict(cls, data):
        """state.json의 항목으로 퀴즈를 만든다. 형식이 틀리면 ValueError를 낸다."""
        try:
            question, choices, answer = data["question"], data["choices"], data["answer"]
        except (KeyError, TypeError) as error:
            raise ValueError(f"퀴즈 항목에 필요한 값이 없습니다: {error}") from error
        if not (isinstance(question, str) and question.strip()):
            raise ValueError("문제는 비어 있지 않은 문자열이어야 합니다")
        if not (
            isinstance(choices, list)
            and len(choices) == cls.CHOICE_COUNT
            and all(isinstance(choice, str) and choice.strip() for choice in choices)
        ):
            raise ValueError(f"선택지는 문자열 {cls.CHOICE_COUNT}개여야 합니다")
        if type(answer) is not int or not 1 <= answer <= cls.CHOICE_COUNT:
            raise ValueError(f"정답은 1-{cls.CHOICE_COUNT} 사이의 정수여야 합니다")
        hint = data.get("hint")
        if hint is not None and not isinstance(hint, str):
            raise ValueError("힌트는 문자열이어야 합니다")
        return cls(question, choices, answer, hint)
