"""state.json을 읽고 쓴다. 게임 규칙은 알지 못한다."""

import json
import os
from contextlib import contextmanager
from pathlib import Path

try:
    import fcntl
except ImportError:  # Windows에는 fcntl이 없다. 혼자 플레이할 때는 잠금이 필요 없다.
    fcntl = None


class StateCorrupted(Exception):
    """state.json을 해석할 수 없을 때 발생한다."""


class StateStore:
    def __init__(self, path):
        self.path = Path(path)

    @contextmanager
    def lock(self):
        """여러 접속자가 동시에 저장해 서로의 변경을 덮어쓰지 않게 한다."""
        if fcntl is None:
            yield
            return
        try:
            lock_file = open(self.path.with_name(f"{self.path.name}.lock"), "w")
        except OSError:
            yield  # 잠금 파일을 못 만드는 위치라면 저장 쪽에서 안내한다.
            return
        with lock_file:
            fcntl.flock(lock_file, fcntl.LOCK_EX)
            yield

    def load(self):
        """저장된 데이터를 돌려준다. 파일이 없으면 None이다."""
        try:
            with open(self.path, encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return None
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise StateCorrupted(str(error)) from error
        if not isinstance(data, dict):
            raise StateCorrupted("최상위 값이 객체가 아닙니다")
        return data

    def save(self, data):
        """임시 파일에 쓴 뒤 바꿔치기해서 중간에 꺼져도 파일이 깨지지 않게 한다."""
        temp_path = self.path.with_name(f"{self.path.name}.{os.getpid()}.tmp")
        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        os.replace(temp_path, self.path)

    def set_aside(self):
        """손상된 파일을 지우지 않고 옆으로 옮겨 나중에 살펴볼 수 있게 한다."""
        os.replace(self.path, self.path.with_name(f"{self.path.name}.corrupt"))
