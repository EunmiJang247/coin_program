docker-compose -f docker-compose-bill.yml up
docker-compose -f docker-compose-bill.yml run frontend npm install --force --legacy-peer-deps
docker-compose -f docker-compose-bill.yml run backend_ozo  python manage.py makemigrations cameraapp
docker-compose -f docker-compose-bill.yml run backend_ozo  python manage.py migrate

