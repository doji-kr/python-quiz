"""터미널 입력을 한곳에서 처리한다. 잘못된 입력은 안내 후 다시 묻는다."""

try:
    import readline  # noqa: F401  input()에서 한글을 지울 때 글자 폭을 바르게 맞춘다.
except ImportError:  # Windows에는 없다. 없어도 입력은 동작한다.
    pass


def read_text(prompt):
    """비어 있지 않은 문자열을 받을 때까지 반복해서 묻는다."""
    while True:
        # 터미널이 깨진 바이트를 넘겨도 저장에서 실패하지 않도록 정리한다.
        text = input(prompt).strip().encode("utf-8", "replace").decode("utf-8")
        if text:
            return text
        print("⚠️ 빈 입력입니다. 내용을 입력하세요.")


def read_optional_text(prompt):
    """비워 두어도 되는 문자열을 묻는다. 비어 있으면 None을 돌려준다."""
    text = input(prompt).strip().encode("utf-8", "replace").decode("utf-8")
    return text or None


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
