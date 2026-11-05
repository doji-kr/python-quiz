"""나만의 퀴즈 게임 실행 파일."""

from pathlib import Path

from game import QuizGame
from storage import StateStore

STATE_PATH = Path(__file__).resolve().parent / "state.json"


def main():
    QuizGame(StateStore(STATE_PATH)).run()


if __name__ == "__main__":
    main()
