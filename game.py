"""게임 전체의 진행을 맡는다. 메뉴, 출제, 점수를 관리한다."""

import random
from contextlib import contextmanager
from datetime import datetime

from console import read_number, read_optional_text, read_text
from default_quizzes import create_default_quizzes
from pet import Dotch
from quiz import Quiz
from storage import StateCorrupted

LINE = "=" * 40
THIN_LINE = "-" * 40
HINT_PENALTY = 5
MAX_HISTORY = 100


class QuizGame:
    """메뉴를 보여 주고 선택에 따라 기능을 실행한다."""

    def __init__(self, store):
        self.store = store
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.best_correct = 0
        self.best_total = 0
        self.history = []
        self.pet = Dotch()
        self.running = True

    def load(self):
        """저장된 데이터를 불러온다. 없거나 깨졌으면 기본 퀴즈로 시작한다."""
        try:
            data = self.store.load()
            if data is None:
                print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
                return
            self.apply_state(data)
        except (StateCorrupted, ValueError) as error:
            print(f"⚠️ state.json이 손상되어 기본 퀴즈로 복구합니다. ({error})")
            self.recover()
            return
        except OSError as error:
            print(f"⚠️ state.json을 읽지 못해 기본 퀴즈로 시작합니다. ({error})")
            return
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, {self.best_label()})")

    def apply_state(self, data):
        """읽어 온 데이터를 검사하고, 모두 올바를 때만 게임에 반영한다."""
        items = data.get("quizzes")
        if not isinstance(items, list):
            raise ValueError("quizzes는 목록이어야 합니다")
        quizzes = [Quiz.from_dict(item) for item in items]
        best_score = data.get("best_score")
        best_correct = data.get("best_correct", 0)
        best_total = data.get("best_total", 0)
        for value in (best_correct, best_total):
            if type(value) is not int or value < 0:
                raise ValueError("점수 기록은 0 이상의 정수여야 합니다")
        if best_score is not None and (type(best_score) is not int or not 0 <= best_score <= 100):
            raise ValueError("최고 점수는 0-100 사이의 정수여야 합니다")
        history = data.get("history", [])
        if not isinstance(history, list) or not all(self.is_record(item) for item in history):
            raise ValueError("history 형식이 올바르지 않습니다")
        pet = Dotch.from_dict(data["pet"]) if "pet" in data else Dotch()
        self.quizzes = quizzes
        self.best_score = best_score
        self.best_correct = best_correct
        self.best_total = best_total
        self.history = history
        self.pet = pet

    @staticmethod
    def is_record(item):
        """게임 기록 한 건의 형식이 올바른지 확인한다."""
        return (
            isinstance(item, dict)
            and isinstance(item.get("played_at"), str)
            and all(type(item.get(key)) is int for key in ("total", "correct", "hints", "score"))
        )

    def recover(self):
        """손상된 파일을 옮겨 두고 기본 데이터로 새로 저장한다."""
        try:
            self.store.set_aside()
        except OSError as error:
            print(f"⚠️ 손상된 파일을 옮기지 못했습니다. ({error})")
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.best_correct = 0
        self.best_total = 0
        self.history = []
        self.pet = Dotch()
        self.save()

    def refresh(self):
        """다른 접속자가 저장한 최신 상태를 읽어 온다. 읽지 못하면 지금 상태를 유지한다."""
        try:
            data = self.store.load()
            if data is not None:
                self.apply_state(data)
        except (StateCorrupted, ValueError, OSError):
            pass

    @contextmanager
    def shared_update(self):
        """잠근 채 최신 상태를 읽고, 블록 안에서 바꾼 뒤 저장한다."""
        with self.store.lock():
            self.refresh()
            yield
            self.save()

    def save(self):
        """현재 상태를 저장한다. 실패해도 게임은 계속한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
            "history": self.history,
            "pet": self.pet.to_dict(),
        }
        try:
            self.store.save(data)
        except OSError as error:
            print(f"⚠️ 저장하지 못했습니다. ({error})")

    @staticmethod
    def now():
        return datetime.now().astimezone()

    def best_label(self):
        return "최고점수 없음" if self.best_score is None else f"최고점수 {self.best_score}점"

    def show_menu(self):
        self.refresh()
        print(LINE)
        print("        🎯 도치의 파이썬 퀴즈 🎯")
        print(LINE)
        self.pet.show(self.now())
        print(LINE)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 퀴즈 삭제")
        print("6. 게임 기록")
        print("7. 종료")
        print(LINE)

    def handle_choice(self, choice):
        if choice == 1:
            self.play()
        elif choice == 2:
            self.add_quiz()
        elif choice == 3:
            self.list_quizzes()
        elif choice == 4:
            self.show_score()
        elif choice == 5:
            self.delete_quiz()
        elif choice == 6:
            self.show_history()
        elif choice == 7:
            with self.shared_update():
                pass
            print("👋 게임을 종료합니다.")
            self.running = False
        else:
            print("🚧 아직 준비 중인 기능입니다.")

    def play(self):
        """고른 수만큼 퀴즈를 무작위로 출제하고 결과를 보여 준다."""
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        total = read_number(f"몇 문제를 풀까요? (1-{len(self.quizzes)}): ", 1, len(self.quizzes))
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")
        correct = 0
        hints = 0
        for number, quiz in enumerate(random.sample(self.quizzes, total), start=1):
            print(THIN_LINE)
            is_correct, used_hint = self.ask(quiz, number)
            correct += is_correct
            hints += used_hint
        print(LINE)
        score = max(0, correct * 100 // total - hints * HINT_PENALTY)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점, 힌트 {hints}회)")
        with self.shared_update():
            self.record(score, correct, total, hints)
            self.pet.reward(correct, correct == total, self.now())
            is_best = self.update_best(score, correct, total)
        if correct:
            print(f"🍚 도치가 정답 {correct}개만큼 밥을 먹었습니다!")
        if is_best:
            print("🎉 새로운 최고 점수입니다!")
        print(LINE)

    def update_best(self, score, correct, total):
        """최고 점수를 넘었으면 갱신하고 True를 돌려준다."""
        if self.best_score is not None and score <= self.best_score:
            return False
        self.best_score = score
        self.best_correct = correct
        self.best_total = total
        return True

    def record(self, score, correct, total, hints):
        """게임 기록을 남긴다. 파일이 끝없이 커지지 않게 최근 기록만 둔다."""
        self.history.append(
            {
                "played_at": datetime.now().astimezone().isoformat(timespec="seconds"),
                "total": total,
                "correct": correct,
                "hints": hints,
                "score": score,
            }
        )
        del self.history[:-MAX_HISTORY]

    def ask(self, quiz, number):
        """한 문제를 출제하고 (맞혔는지, 힌트를 봤는지)를 돌려준다."""
        quiz.show(number)
        used_hint = False
        while True:
            answer = read_number(
                f"정답 입력 (h: 힌트, -{HINT_PENALTY}점): ", 1, quiz.CHOICE_COUNT, extras=("h",)
            )
            if answer != "h":
                break
            if quiz.hint is None:
                print("💡 이 문제에는 힌트가 없습니다.")
            else:
                print(f"💡 힌트: {quiz.hint}")
                used_hint = True
        if quiz.is_correct(answer):
            print("✅ 정답입니다!\n")
            return True, used_hint
        print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.\n")
        return False, used_hint

    def add_quiz(self):
        """사용자에게 문제, 선택지, 정답을 입력받아 퀴즈를 등록한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = read_text("문제를 입력하세요: ")
        choices = [read_text(f"선택지 {index}: ") for index in range(1, Quiz.CHOICE_COUNT + 1)]
        answer = read_number(f"정답 번호 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT)
        hint = read_optional_text("힌트 (없으면 Enter): ")
        with self.shared_update():
            self.quizzes.append(Quiz(question, choices, answer, hint))
        print("\n✅ 퀴즈가 추가되었습니다!\n")

    def list_quizzes(self):
        """등록된 퀴즈의 문제만 번호와 함께 보여 준다."""
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다.")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print(THIN_LINE)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print(THIN_LINE)

    def delete_quiz(self):
        """목록에서 번호를 골라 퀴즈를 지운다. 0을 고르면 취소한다."""
        if not self.quizzes:
            print("📭 삭제할 퀴즈가 없습니다.")
            return
        self.list_quizzes()
        number = read_number("삭제할 번호 (0: 취소): ", 0, len(self.quizzes))
        if number == 0:
            print("↩️ 삭제를 취소했습니다.")
            return
        target = self.quizzes[number - 1].to_dict()
        with self.shared_update():
            # 번호를 고르는 사이 목록이 바뀌었을 수 있어 내용으로 다시 찾는다.
            remaining = [quiz for quiz in self.quizzes if quiz.to_dict() != target]
            removed = len(remaining) < len(self.quizzes)
            self.quizzes = remaining
        if removed:
            print(f"🗑️ 삭제했습니다: {target['question']}")
        else:
            print("ℹ️ 다른 접속자가 이미 삭제한 퀴즈입니다.")

    def show_score(self):
        if self.best_score is None:
            print("📭 아직 퀴즈를 풀지 않았습니다.")
            return
        print(
            f"\n🏆 최고 점수: {self.best_score}점 "
            f"({self.best_total}문제 중 {self.best_correct}문제 정답)\n"
        )

    def show_history(self):
        """최근 게임 기록을 새로운 순서로 보여 준다."""
        if not self.history:
            print("📭 아직 게임 기록이 없습니다.")
            return
        print(f"\n📜 최근 게임 기록 ({len(self.history)}건)\n")
        print(THIN_LINE)
        for item in reversed(self.history[-10:]):
            print(
                f"{item['played_at'][:16].replace('T', ' ')}  "
                f"{item['total']}문제 중 {item['correct']}개 정답  "
                f"힌트 {item['hints']}회  {item['score']}점"
            )
        print(THIN_LINE)

    def run(self):
        """메뉴를 반복한다. Ctrl+C나 입력 종료가 와도 안전하게 끝낸다."""
        self.load()
        try:
            while self.running:
                self.show_menu()
                self.handle_choice(read_number("선택: ", 1, 7))
        except (KeyboardInterrupt, EOFError):
            print("\n👋 입력이 중단되어 저장 후 게임을 종료합니다.")
            try:
                with self.shared_update():
                    pass
            except KeyboardInterrupt:
                pass
