## Configuration

### Building project
- `docker compose build app`

### Running project
- remove `python manage.py runserver 0.0.0.0:8000` from `docker-compose.yml` without commiting
- `docker compose up -d`
- wait for containers to start
- `docker compose ps` confirm that all the containers are up
- `docker compose exec app bash` - connect to the `app` container
- `docker compose migrate` - run if needed
- `python manage.py runserver 0.0.0.0:8000`


### Useful commands
- `docker compose makemigrations`
- `docker compose migrate`
- `docker compose showmigrations`