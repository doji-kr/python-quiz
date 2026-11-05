"""state.json을 읽고 쓴다. 게임 규칙은 알지 못한다."""

import json
import os
from pathlib import Path


class StateCorrupted(Exception):
    """state.json을 해석할 수 없을 때 발생한다."""


class StateStore:
    def __init__(self, path):
        self.path = Path(path)

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
