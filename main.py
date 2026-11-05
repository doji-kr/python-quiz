"""나만의 퀴즈 게임 실행 파일."""

import os
from pathlib import Path

from device import Device
from game import QuizGame
from storage import StateStore

# 기본은 프로젝트 루트의 state.json이다. 서버에서는 QUIZ_STATE_PATH로 데이터 볼륨을 가리킨다.
STATE_PATH = Path(os.environ.get("QUIZ_STATE_PATH", Path(__file__).resolve().parent / "state.json"))


def main():
    QuizGame(StateStore(STATE_PATH), Device.from_env()).run()


if __name__ == "__main__":
    main()
