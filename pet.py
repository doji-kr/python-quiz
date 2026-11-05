"""퀴즈 정답으로 살아가는 도치. 시간은 접속할 때 한꺼번에 계산한다."""

from datetime import datetime


class Dotch:
    MAX_HEARTS = 4
    HUNGER_MINUTES = 60
    MOOD_MINUTES = 180
    LEAVE_MINUTES = 24 * 60

    def __init__(self, hunger=MAX_HEARTS, mood=MAX_HEARTS, generation=1, updated_at=None):
        self.hunger = hunger
        self.mood = mood
        self.generation = generation
        self.updated_at = updated_at or datetime.now().astimezone()

    def elapsed_minutes(self, now):
        return max(0, int((now - self.updated_at).total_seconds() // 60))

    def hearts(self, now):
        """지금 시각의 (밥, 기분) 하트 수를 돌려준다. 저장된 값은 바꾸지 않는다."""
        minutes = self.elapsed_minutes(now)
        return (
            max(0, self.hunger - minutes // self.HUNGER_MINUTES),
            max(0, self.mood - minutes // self.MOOD_MINUTES),
        )

    def has_left(self, now):
        """두 하트가 모두 빈 채로 하루가 지나면 도치는 떠난다."""
        empty_after = max(self.hunger * self.HUNGER_MINUTES, self.mood * self.MOOD_MINUTES)
        return self.elapsed_minutes(now) - empty_after >= self.LEAVE_MINUTES

    def reward(self, correct, is_perfect, now):
        """정답 수만큼 밥을, 모두 맞히면 기분을 채운다. 떠났으면 새 도치가 온다."""
        if self.has_left(now):
            self.generation += 1
            self.hunger, self.mood = 0, 0
        else:
            self.hunger, self.mood = self.hearts(now)
        self.hunger = min(self.MAX_HEARTS, self.hunger + correct)
        self.mood = min(self.MAX_HEARTS, self.mood + (1 if is_perfect else 0))
        self.updated_at = now

    def show(self, now):
        if self.has_left(now):
            print(f"  도치 {self.generation}세대가 떠났습니다. 정답을 맞히면 새 도치가 옵니다.")
            return
        hunger, mood = self.hearts(now)
        face = "^_^" if hunger + mood >= self.MAX_HEARTS else "-_-" if hunger + mood else "x_x"
        print(f"   ,/|\\|/|\\,    도치 {self.generation}세대")
        print(f"  ( {face} )|\\|/)   밥   {self.heart_bar(hunger)}")
        print(f"   `u-----u'     기분 {self.heart_bar(mood)}")

    def heart_bar(self, count):
        return "♥" * count + "♡" * (self.MAX_HEARTS - count)

    def to_dict(self):
        return {
            "hunger": self.hunger,
            "mood": self.mood,
            "generation": self.generation,
            "updated_at": self.updated_at.isoformat(timespec="seconds"),
        }

    @classmethod
    def from_dict(cls, data):
        """state.json의 항목으로 도치를 만든다. 형식이 틀리면 ValueError를 낸다."""
        if not isinstance(data, dict):
            raise ValueError("pet은 객체여야 합니다")
        hunger, mood = data.get("hunger"), data.get("mood")
        generation, updated_at = data.get("generation"), data.get("updated_at")
        for hearts in (hunger, mood):
            if type(hearts) is not int or not 0 <= hearts <= cls.MAX_HEARTS:
                raise ValueError(f"하트는 0-{cls.MAX_HEARTS} 사이의 정수여야 합니다")
        if type(generation) is not int or generation < 1:
            raise ValueError("세대는 1 이상의 정수여야 합니다")
        if not isinstance(updated_at, str):
            raise ValueError("updated_at은 문자열이어야 합니다")
        moment = datetime.fromisoformat(updated_at)
        if moment.tzinfo is None:
            raise ValueError("updated_at에는 시간대가 있어야 합니다")
        return cls(hunger, mood, generation, moment)
