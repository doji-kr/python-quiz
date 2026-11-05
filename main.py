"""나만의 퀴즈 게임 실행 파일."""

from console import read_number

LINE = "=" * 40


class QuizGame:
    """메뉴를 보여 주고 선택에 따라 기능을 실행한다."""

    def __init__(self):
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
        if choice == 5:
            print("👋 게임을 종료합니다.")
            self.running = False
        else:
            print("🚧 아직 준비 중인 기능입니다.")

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
