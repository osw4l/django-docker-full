docker-compose exec backend python3 manage.py loaddata setup/themes/bt.json \
&& docker-compose exec backend python3 manage.py loaddata setup/themes/dj.json \
&& docker-compose exec backend python3 manage.py loaddata setup/themes/fd.json \
&& docker-compose exec backend python3 manage.py loaddata setup/themes/start.json \
&& docker-compose exec backend python3 manage.py loaddata setup/themes/usw.json