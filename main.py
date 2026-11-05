"""나만의 퀴즈 게임 실행 파일."""

from console import read_number, read_text
from default_quizzes import create_default_quizzes
from quiz import Quiz

LINE = "=" * 40
THIN_LINE = "-" * 40


class QuizGame:
    """메뉴를 보여 주고 선택에 따라 기능을 실행한다."""

    def __init__(self):
        self.quizzes = create_default_quizzes()
        self.running = True

    def show_menu(self):
        print(LINE)
        print("        🎯 도치의 파이썬 퀴즈 🎯")
        print(LINE)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print(LINE)

    def handle_choice(self, choice):
        if choice == 1:
            self.play()
        elif choice == 2:
            self.add_quiz()
        elif choice == 5:
            print("👋 게임을 종료합니다.")
            self.running = False
        else:
            print("🚧 아직 준비 중인 기능입니다.")

    def play(self):
        """모든 퀴즈를 차례로 출제하고 결과를 보여 준다."""
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        total = len(self.quizzes)
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")
        correct = 0
        for number, quiz in enumerate(self.quizzes, start=1):
            print(THIN_LINE)
            if self.ask(quiz, number):
                correct += 1
        print(LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({correct * 100 // total}점)")
        print(LINE)

    def ask(self, quiz, number):
        """한 문제를 출제하고 맞혔는지 돌려준다."""
        quiz.show(number)
        answer = read_number("정답 입력: ", 1, quiz.CHOICE_COUNT)
        if quiz.is_correct(answer):
            print("✅ 정답입니다!\n")
            return True
        print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.\n")
        return False

    def add_quiz(self):
        """사용자에게 문제, 선택지, 정답을 입력받아 퀴즈를 등록한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = read_text("문제를 입력하세요: ")
        choices = [read_text(f"선택지 {index}: ") for index in range(1, Quiz.CHOICE_COUNT + 1)]
        answer = read_number(f"정답 번호 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT)
        self.quizzes.append(Quiz(question, choices, answer))
        print("\n✅ 퀴즈가 추가되었습니다!\n")

    def run(self):
        """메뉴를 반복한다. Ctrl+C나 입력 종료가 와도 안전하게 끝낸다."""
        try:
            while self.running:
                self.show_menu()
                self.handle_choice(read_number("선택: ", 1, 5))
        except (KeyboardInterrupt, EOFError):
            print("\n👋 입력이 중단되어 게임을 종료합니다.")


if __name__ == "__main__":
    QuizGame().run()
