sed -i -e 's/DEBUG = True/DEBUG = False/g' movasat/settings.py

git pull origin master

docker network create nginx_network

docker rm movasat_movasat_1 --force
docker rm movasat_postgresql --force
docker rmi movasat_movasat --force


docker rmi nginx_nginx --force
docker rm nginx --force
docker volume rm movasat_static_volume

docker volume create movasat_files_volume
docker volume create movasat_static_volume
docker volume create movasat_postgresql
docker network create movasat_network

docker-compose up -d

sed -i -e 's/DEBUG = False/DEBUG = True/g' movasat/settings.py

python .\manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate

docker system prune -a -f
