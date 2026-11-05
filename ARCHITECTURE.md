# 아키텍처와 과제 요구사항 대응

과제의 요구사항이 코드 어디에 어떻게 반영되어 있는지 정리한 문서입니다. 코드 블록은 모두 실제 파일에서 그대로 옮겼고, 줄 번호는 금방 바뀌므로 파일과 메서드 이름으로 가리킵니다.

## 1. 구조 한눈에 보기

```
                 main.py  저장 경로를 정하고 객체를 조립한다
                    │
                    ▼
              ┌──────────┐
              │ QuizGame │  game.py: 메뉴, 출제, 점수, 기록, 저장 시점
              └────┬─────┘
    ┌─────────┬────┴────┬───────────┬──────────┐
    ▼         ▼         ▼           ▼          ▼
 console    Quiz      Dotch     StateStore   Device
 입력 검증   문제 1개   도치 규칙   파일 입출력   기기 전달(선택)
                                    │
                                    ▼
                               state.json
```

| 파일 | 내용 | 바깥 세계와의 접점 |
|---|---|---|
| `main.py` | 실행 시작점, 객체 조립 | 환경 변수 |
| `game.py` | `QuizGame`: 게임 진행 | 화면 출력 |
| `quiz.py` | `Quiz`: 문제 한 개 | 화면 출력(`show`) |
| `pet.py` | `Dotch`: 하트와 세대 계산 | 화면 출력(`show`) |
| `storage.py` | `StateStore`: 읽기, 쓰기, 잠금 | 파일 |
| `console.py` | 입력 공통 함수 | 키보드 |
| `device.py` | `Device`: 기기에 결과 전달 | 네트워크(선택) |
| `default_quizzes.py` | 기본 퀴즈 8개 | 없음 |

## 2. 요구사항 대응표

### 필수 구현

| 요구사항 | 반영 위치 | 어떻게 |
|---|---|---|
| Python 3.10 이상 | 전체 | 3.10에서 실행해 확인했습니다 |
| 표준 라이브러리만 사용 | 모든 `import` | `json`, `os`, `pathlib`, `random`, `datetime`, `contextlib`, `urllib`, `fcntl`, `readline`만 씁니다 |
| 클래스 2개 이상 | `quiz.py`, `game.py` | `Quiz`, `QuizGame` 외에 `StateStore`, `Dotch`, `Device` |
| 기능별 메서드 분리 | `QuizGame` | `play`, `ask`, `add_quiz`, `list_quizzes`, `show_score` 등 |
| 메뉴(풀기, 추가, 목록, 점수, 종료) | `QuizGame.show_menu`, `handle_choice`, `run` | [3.2](#32-메뉴와-기능-분리) |
| 기본 퀴즈 5개 이상 | `default_quizzes.py` | 파이썬과 Git 기초 8개 |
| 퀴즈 풀기와 정답 판정 | `QuizGame.play`, `ask`, `Quiz.is_correct` | [3.3](#33-퀴즈-풀기와-점수) |
| 퀴즈 추가 | `QuizGame.add_quiz` | [3.4](#34-퀴즈-추가) |
| 최고 점수 갱신 | `QuizGame.update_best`, `show_score` | [3.3](#33-퀴즈-풀기와-점수) |
| 프로젝트 루트의 `state.json` | `main.py`의 `STATE_PATH`, `QuizGame.save` | 경로는 [3.1](#31-시작과-저장-경로), 생성 과정은 [3.6](#36-statejson이-만들어지는-과정) |
| UTF-8 저장 | `StateStore.load`, `save` | `encoding="utf-8"`, `ensure_ascii=False` |
| 다시 실행해도 데이터 유지 | `QuizGame.load`, `save` | [3.7](#37-안전한-저장) |
| 파일이 없을 때 처리 | `QuizGame.load` | 안내 후 기본 퀴즈로 시작 ([3.8](#38-파일이-없거나-손상됐을-때)) |
| 파일이 손상됐을 때 처리 | `QuizGame.load`, `recover`, `apply_state` | 안내 후 옮겨 두고 기본값으로 복구 ([3.8](#38-파일이-없거나-손상됐을-때)) |
| 입력 공백 제거 | `console.py` | `input(prompt).strip()` |
| `abc`, 범위 밖, 빈 입력 재입력 | `read_number`, `read_text` | [3.5](#35-입력-검증) |
| Ctrl+C, EOF 안전 종료와 저장 | `QuizGame.run` | [3.9](#39-안전한-종료) |

### 보너스

| 요구사항 | 반영 위치 | 어떻게 |
|---|---|---|
| 랜덤 출제 | `QuizGame.play` | `random.sample` |
| 문제 수 선택 | `QuizGame.play` | `read_number`로 1부터 전체 개수까지 입력 |
| 힌트와 점수 차감 | `QuizGame.ask`, `play` | `h` 입력, 문제당 `HINT_PENALTY`점(5점) 차감 |
| 퀴즈 삭제 | `QuizGame.delete_quiz` | 번호 선택, 0은 취소 |
| 게임 기록 | `QuizGame.record`, `show_history` | 100건 보관, 최근 10건 표시 |

### Git과 문서

코드가 아니라 저장소 이력으로 확인하는 항목입니다.

| 요구사항 | 확인 방법 | 상태 |
|---|---|---|
| 의미 있는 커밋 10개 이상 | [`git_log.png`](docs/screenshots/git_log.png) | 캡처 시점에 30개 |
| 커밋 메시지 규칙 | [README의 커밋 규칙](README.md#커밋-규칙) | `Feat:`, `Fix:`, `Docs:`, `Refactor:`, `Chore:` |
| 브랜치와 병합 | [`git_log.png`](docs/screenshots/git_log.png) | `feature/play-quiz`, `feature/bonus`를 병합 |
| clone과 pull 실습 | [`clone_pull.png`](docs/screenshots/clone_pull.png), 커밋 `f3e5f39` | 화면은 별도 폴더에 clone한 뒤 원래 폴더의 변경을 복제본에서 pull한 기록이고, 복제본에서 고쳐 push한 뒤 원래 폴더에서 pull한 기록은 커밋 `f3e5f39`입니다 |
| README 필수 항목 | [README.md](README.md) | 개요, 주제와 이유, 실행 방법, 기능, 파일 구조, `state.json` 설명 |
| 실행 화면 | `docs/screenshots/` | `menu`, `play`, `add_quiz`, `score` |

## 3. 핵심 코드

### 3.1 시작과 저장 경로

`main.py`는 저장 경로를 정하고 객체를 조립하기만 합니다. 작업 폴더가 어디든 `__file__`을 기준으로 프로젝트 루트의 `state.json`을 찾습니다.

```python
STATE_PATH = Path(os.environ.get("QUIZ_STATE_PATH", Path(__file__).resolve().parent / "state.json"))


def main():
    QuizGame(StateStore(STATE_PATH), Device.from_env()).run()
```

### 3.2 메뉴와 기능 분리

메뉴를 보여 주는 일과 선택을 실행하는 일을 나누고, 기능은 각자의 메서드로 분리했습니다. `handle_choice`는 어떤 메서드를 부를지만 정합니다.

```python
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
```

### 3.3 퀴즈 풀기와 점수

한 라운드는 문제를 무작위로 뽑아 출제하고, 점수를 계산한 뒤, 잠금 안에서 기록과 최고 점수를 저장합니다. 정답 판정은 `Quiz`가 맡습니다.

```python
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
```

`is_correct`는 `True` 또는 `False`이고 파이썬에서는 각각 1과 0으로 더해지므로, `correct += is_correct`로 정답 수를 셉니다. 힌트 감점으로 점수가 음수가 되지 않도록 `max(0, ...)`을 씁니다.

```python
    def update_best(self, score, correct, total):
        """최고 점수를 넘었으면 갱신하고 True를 돌려준다."""
        if self.best_score is not None and score <= self.best_score:
            return False
        self.best_score = score
        self.best_correct = correct
        self.best_total = total
        return True
```

`None`은 아직 풀지 않은 상태입니다. 0점도 첫 기록으로 인정하려고 0이 아니라 `None`으로 구분합니다.

### 3.4 퀴즈 추가

입력을 모두 받은 뒤에 잠금을 잡습니다. 사용자가 입력하는 동안 다른 접속자의 저장을 막지 않기 위해서입니다.

```python
        question = read_text("문제를 입력하세요: ")
        choices = [read_text(f"선택지 {index}: ") for index in range(1, Quiz.CHOICE_COUNT + 1)]
        answer = read_number(f"정답 번호 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT)
        hint = read_optional_text("힌트 (없으면 Enter): ")
        with self.shared_update():
            self.quizzes.append(Quiz(question, choices, answer, hint))
```

### 3.5 입력 검증

모든 숫자 입력이 이 함수 하나를 거칩니다. 앞뒤 공백을 지우고, 숫자가 아니거나 빈 입력이면 `int()`의 `ValueError`로, 범위 밖이면 비교로 걸러 안내 후 다시 묻습니다. `extras`는 힌트의 `h`처럼 숫자가 아닌 입력을 허용할 때 씁니다.

```python
def read_number(prompt, low, high, extras=()):
    """low 이상 high 이하의 정수를 받을 때까지 묻는다. extras의 글자도 그대로 돌려준다."""
    guide = f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요."
    while True:
        text = input(prompt).strip()
        if text.lower() in extras:
            return text.lower()
        try:
            number = int(text)
        except ValueError:
            print(guide)
            continue
        if low <= number <= high:
            return number
        print(guide)
```

### 3.6 state.json이 만들어지는 과정

`state.json`은 저장소에 없고, 게임이 처음 저장할 때 만들어집니다. 실행 순서는 다음과 같습니다.

```
python3 main.py
  → StateStore.load   파일이 없으면 None을 돌려준다
  → QuizGame.load     안내를 출력하고, __init__에서 만든 기본 퀴즈로 시작한다 (아직 파일 없음)
  → 퀴즈 추가, 라운드 종료, 메뉴 7, Ctrl+C, EOF
  → shared_update → QuizGame.save → StateStore.save   이때 state.json이 생긴다
```

**1단계: 파일이 없는 것은 오류가 아닙니다.** `StateStore.load`가 `FileNotFoundError`를 잡아 `None`을 돌려주므로, 처음 실행도 정상 흐름으로 이어집니다.

```python
        try:
            with open(self.path, encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return None
```

**2단계: 처음에는 메모리의 기본값으로 시작합니다.** `QuizGame.__init__`이 파일과 상관없이 기본 퀴즈를 준비해 둡니다.

```python
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.best_correct = 0
        self.best_total = 0
        self.history = []
        self.pet = Dotch()
```

**3단계: 저장할 내용을 딕셔너리로 모읍니다.** `QuizGame.save`가 게임 상태를 JSON으로 바꿀 수 있는 형태로 만들어 `StateStore.save`에 넘깁니다. 이 키들이 `state.json`의 최상위 필드입니다. 실제로 파일을 쓰는 코드는 [3.7](#37-안전한-저장)에 있습니다.

```python
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
            "history": self.history,
            "pet": self.pet.to_dict(),
        }
```

**4단계: 변경이 없어도 종료할 때 저장합니다.** 블록 안이 `pass`뿐이어도 `shared_update`가 끝에서 `save`를 부르므로, 아무것도 하지 않고 메뉴 `7`로 끝내도 파일이 생깁니다.

```python
        elif choice == 7:
            with self.shared_update():
                pass
```

손상된 파일을 복구할 때도 `QuizGame.recover`가 `save`를 불러 기본값으로 새 파일을 만듭니다. 잠금을 쓸 수 있는 환경에서는 저장할 때 잠금 전용 파일 `state.json.lock`도 함께 생기며, 둘 다 `.gitignore`에 들어 있어 Git에는 올라가지 않습니다. 형식이 궁금하면 [`state.example.json`](state.example.json)을 보면 됩니다.

### 3.7 안전한 저장

파일에 바로 쓰다가 프로그램이 꺼지면 `state.json`이 반쯤 쓰인 채 남습니다. 그래서 임시 파일에 다 쓴 뒤 `os.replace`로 한 번에 바꿔치기합니다. `ensure_ascii=False`는 한글을 `\uXXXX`가 아닌 글자 그대로 저장합니다.

```python
    def save(self, data):
        """임시 파일에 쓴 뒤 바꿔치기해서 중간에 꺼져도 파일이 깨지지 않게 한다."""
        temp_path = self.path.with_name(f"{self.path.name}.{os.getpid()}.tmp")
        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        os.replace(temp_path, self.path)
```

변경은 모두 아래의 `shared_update`를 거칩니다. 잠근 채 최신 상태를 읽고, 바꾸고, 저장하므로 여러 접속자의 변경이 서로를 덮어쓰지 않습니다.

```python
    @contextmanager
    def shared_update(self):
        """잠근 채 최신 상태를 읽고, 블록 안에서 바꾼 뒤 저장한다."""
        with self.store.lock():
            self.refresh()
            yield
            self.save()
```

저장에 실패하면 `unsaved`를 켜서, 다음 `refresh`가 옛 파일을 읽어 방금 바꾼 내용을 지우지 않게 합니다.

```python
        if self.unsaved:  # 아직 저장하지 못한 변경을 옛 파일로 덮어쓰지 않는다.
            return
```

### 3.8 파일이 없거나 손상됐을 때

세 가지 경우를 나눕니다. 파일이 없으면 처음 실행이고, 내용을 해석할 수 없으면 손상이며, 읽을 수 없으면(권한 등) 원본을 건드리지 않습니다.

```python
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
```

JSON 문법이 맞아도 값이 틀리면 손상으로 봅니다. `Quiz.from_dict`가 문제, 선택지 개수, 정답 범위를 검사하고, `apply_state`는 전체 검사가 끝난 뒤에야 게임에 반영하므로 일부만 적용되는 일이 없습니다. 손상된 파일은 지우지 않고 `state.json.corrupt`로 옮깁니다.

```python
        if type(answer) is not int or not 1 <= answer <= cls.CHOICE_COUNT:
            raise ValueError(f"정답은 1-{cls.CHOICE_COUNT} 사이의 정수여야 합니다")
```

`isinstance(answer, int)`가 아니라 `type(...) is int`를 쓴 이유는 `True`가 `int`의 하위 타입이어서, `isinstance`로는 `"answer": true`가 통과하기 때문입니다.

### 3.9 안전한 종료

Ctrl+C는 `KeyboardInterrupt`, 입력 스트림 종료는 `EOFError`로 `input()`에서 올라옵니다. 메뉴 반복 전체를 감싸 어느 화면에서 끊겨도 저장 후 끝납니다.

```python
    def run(self):
        """메뉴를 반복한다. Ctrl+C나 입력 종료가 와도 안전하게 끝낸다."""
        self.load()
        try:
            while self.running:
                self.show_menu()
                self.handle_choice(read_number("선택: ", 1, 7))
        except (KeyboardInterrupt, EOFError):
            print("\n👋 입력이 중단되어 저장 후 게임을 종료합니다.")
```

라운드 도중에 끊으면 그 라운드는 기록되지 않습니다. 점수와 기록은 라운드가 끝나야 저장하기 때문입니다.

## 4. 과제 범위를 넘는 기능

아래는 과제 요구사항이 아니라 이 프로젝트에서 추가한 부분입니다. 없어도 필수 기능은 모두 동작합니다.

| 기능 | 파일 | 내용 |
|---|---|---|
| 도치 키우기 | `pet.py` | 정답으로 하트를 채웁니다. 백그라운드 작업 없이 저장 시각과의 차이로 계산합니다 |
| 잠금과 공유 | `storage.py`의 `lock`, `game.py`의 `shared_update`, `refresh` | 여러 접속자가 같은 `state.json`을 씁니다 |
| 웹 터미널 | `Dockerfile`, `compose.yaml` | ttyd로 브라우저에서 실행합니다 |
| 게임 스토어 항목 | `8bit/` | 8bit 라이브러리에 등록합니다 |
| 기기 연동 | `device.py` | `DOTCH_REWARD_URL`이 있을 때만 라운드 결과를 보냅니다 |

기기 연동은 `QuizGame`에 `device`를 넘기는 방식이라, 변수가 없으면 `Device.from_env()`가 `None`을 돌려주고 터미널만으로 동작합니다.

```python
    @classmethod
    def from_env(cls):
        url = os.environ.get("DOTCH_REWARD_URL", "").strip()
        return cls(url) if url else None
```

## 5. 알려진 한계

- 잠금은 `fcntl`을 쓰므로 Windows에서는 동작하지 않습니다. 한 사람이 플레이할 때는 문제가 없습니다.
- `state.json.corrupt`는 한 개만 남고, 다시 손상되면 덮어씁니다.
- 저장은 파일 전체를 다시 쓰는 방식입니다. 측정값과 대안은 [README의 JSON 설명](README.md#json을-고른-이유와-한계)에 있습니다.
- 웹 터미널에는 인증이 없어, 접속한 사람은 누구나 퀴즈를 추가하거나 지울 수 있습니다.
- 기기와 함께 쓸 때도 `Dotch`의 상태는 `state.json`에 계속 저장되지만 화면에는 보이지 않습니다.
