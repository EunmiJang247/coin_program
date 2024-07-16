1. docker-compose up

2. 프로젝트 생성: 
docker-compose run backend django-admin startproject myproject

3. 앱 생성:
docker-compose run backend 

docker-compose run frontend npm install 이거 한다음
docker-compose run frontend npm run build 이거를 수동으로. 
docker-compose run backend python manage.py makemigrations cameraapp
docker-compose run backend python manage.py startapp baseapp


처음 클론받고
docker-compose up
터미널 하나 더열고 
docker-compose run frontend npm install
노드모듈즈가 생긴다. 
docker-compose run frontend npm run build
.next가 생긴다
좀 기다리다가 localhost:85로 접속해보면 뜸. 