"""터미널 입력을 한곳에서 처리한다. 잘못된 입력은 안내 후 다시 묻는다."""


def read_text(prompt):
    """비어 있지 않은 문자열을 받을 때까지 반복해서 묻는다."""
    while True:
        # 터미널이 깨진 바이트를 넘겨도 저장에서 실패하지 않도록 정리한다.
        text = input(prompt).strip().encode("utf-8", "replace").decode("utf-8")
        if text:
            return text
        print("⚠️ 빈 입력입니다. 내용을 입력하세요.")


def read_number(prompt, low, high):
    """low 이상 high 이하의 정수를 받을 때까지 반복해서 묻는다."""
    guide = f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요."
    while True:
        text = input(prompt).strip()
        try:
            number = int(text)
        except ValueError:
            print(guide)
            continue
        if low <= number <= high:
            return number
        print(guide)
