# 콘솔 게임을 ttyd로 브라우저에 연다. 접속마다 main.py가 하나씩 실행되고 state.json은 모두가 공유한다.
FROM python:3.13-slim-bookworm

ENV TTYD_VERSION=1.7.7
ENV TTYD_SHA256=8a217c968aba172e0dbf3f34447218dc015bc4d5e59bf51db2f2cd12b7be4f55
RUN python -c "import os, urllib.request as u; u.urlretrieve(f'https://github.com/tsl0922/ttyd/releases/download/{os.environ[\"TTYD_VERSION\"]}/ttyd.x86_64', '/usr/local/bin/ttyd')" \
 && echo "$TTYD_SHA256  /usr/local/bin/ttyd" | sha256sum -c - \
 && chmod +x /usr/local/bin/ttyd \
 && useradd --uid 1000 --create-home quiz \
 && install -d -o quiz -g quiz /data

COPY *.py /app/
WORKDIR /app
USER quiz

ENV LANG=C.UTF-8
ENV PYTHONUTF8=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV QUIZ_STATE_PATH=/data/state.json
EXPOSE 7681

# -W 입력 허용, -O 다른 사이트에서 오는 웹소켓 거부, -m 동시 접속 제한
CMD ["ttyd", "-W", "-O", "-p", "7681", "-m", "20", \
     "-t", "titleFixed=python-quiz", \
     "-t", "fontSize=18", \
     "-t", "theme={\"background\":\"#10140f\",\"foreground\":\"#b8f0a0\",\"cursor\":\"#b8f0a0\"}", \
     "python", "main.py"]
