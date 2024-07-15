FROM python:3.11.6 
# Python 3.11.6을 포함한 공식 Python 이미지
ENV PYTHONDONTWRITEBYTECODE=1
# PYTHONDONTWRITEBYTECODE=1: Python이 .pyc 파일(바이트코드 파일)을 생성하지 않도록 합니다. 이를 통해 컨테이너 크기를 줄이고 파일 시스템 성능을 향상시킬 수 있습니다.
ENV PYTHONUNBUFFERED=1
#  Python 출력이 버퍼링되지 않도록 설정합니다. 즉, 출력이 실시간으로 터미널에 표시됩니다. 이는 로그를 즉시 볼 수 있게 하여 디버깅에 유용합니다.
# ENV: Docker 컨테이너에서 환경 변수를 설정하는 명령어

# RUN: Docker 컨테이너에서 명령어를 실행하는 데 사용됩니다.
RUN apt-get update -y && apt-get upgrade -y
# 패키지 목록을 업데이트 & 설치된 패키지를 최신 버전으로 업그레이드

WORKDIR /usr/src/app
# 작업 디렉토리 설정
COPY requirements.txt /usr/src/app/
# 호스트 머신의 requirements.txt 파일을 컨테이너의 /usr/src/app/ 디렉토리에 복사
RUN pip install --upgrade pip setuptools
# pip 및 setuptools를 최신 버전으로 업그레이드
RUN pip install -r requirements.txt
# requirements.txt 파일에 명시된 Python 패키지를 설치