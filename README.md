# 처음 셋팅하는 방법

처음 클론받고
docker-compose build
docker-compose up
터미널 하나 더열고
docker-compose run frontend npm install
노드모듈즈가 생긴다.
docker-compose run frontend npm run build
.next가 생긴다
좀 기다리다가 localhost:89로 접속해보면 뜸.
docker-compose run backend python manage.py makemigrations
docker exec -it 25cab1bff379 /bin/bash

Docker 이미지의 created 날짜가 2달 전으로 나오는 이유는 Docker 캐시 때문입니다. Docker는 효율성을 위해 이전에 빌드된 레이어를 재사용합니다.

# 모든 컨테이너 중지 및 삭제

docker-compose down --rmi all --volumes --remove-orphans

# 시스템 정리 (선택사항)

docker system prune -a -f

# 새로 빌드

docker-compose up --build

# API 설명
