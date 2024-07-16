1. docker-compose up

2. 프로젝트 생성: 
docker-compose run backend django-admin startproject myproject

3. 앱 생성:
docker-compose run backend 

docker-compose run frontend npm install 이거 한다음
docker-compose run frontend npm run build 이거를 수동으로. 
docker-compose run backend python manage.py makemigrations cameraapp
docker-compose run backend python manage.py startapp baseapp


