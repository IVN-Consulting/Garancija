## Configuration

### Building project - 
Needed to install new python packages
- `docker compose build app`

### Running project
- remove `python manage.py runserver 0.0.0.0:8000` from `docker-compose.yml` without commiting
- `docker compose up -d`
- wait for containers to start
- `docker compose ps` confirm that all the containers are up
- `docker compose exec app bash` - connect to the `app` container
- `docker compose migrate` - run if needed
- `python manage.py runserver python manage.py shell_p0.0.0.0:8000`

### docker commands
- `docker compose ps`
- `docker compose exec app bash`
- `docker compose logs -f app`
- `docker compose logs -f --tail=100 app`

### django commands
- `python manage.py runserver 0.0.0.0:8000`
- `python manage.py shell_plus`
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py showmigrations`