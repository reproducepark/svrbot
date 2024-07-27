# 베이스 이미지 설정 (예: Python 3.8)
FROM python:3.10

WORKDIR /src

# 필요한 패키지 설치
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt