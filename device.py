"""함께 띄운 JD-8 기기에 라운드 결과를 알린다. 주소가 없으면 만들어지지 않는다."""

import json
import os
import urllib.request

TIMEOUT_SECONDS = 3


class Device:
    """도치를 기기가 키울 때, 터미널의 정답을 기기로 보낸다."""

    def __init__(self, url):
        self.url = url

    @classmethod
    def from_env(cls):
        url = os.environ.get("DOTCH_REWARD_URL", "").strip()
        return cls(url) if url else None

    def reward(self, correct, total):
        """기기가 준 결과를 돌려준다. 전하지 못하면 None이고, 게임은 계속된다."""
        request = urllib.request.Request(
            self.url,
            data=json.dumps({"correct": correct, "total": total}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
                return json.load(response)
        except (OSError, ValueError):
            return None
