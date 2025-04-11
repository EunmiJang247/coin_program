처음 클론받고
docker-compose up
터미널 하나 더열고 
docker-compose run frontend npm install
노드모듈즈가 생긴다. 
docker-compose run frontend npm run build
.next가 생긴다
좀 기다리다가 localhost:85로 접속해보면 뜸. 
docker-compose run backend python manage.py makemigrations
docker exec -it 25cab1bff379 /bin/bash