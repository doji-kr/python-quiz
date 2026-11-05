"""터미널 입력을 한곳에서 처리한다. 잘못된 입력은 안내 후 다시 묻는다."""


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
