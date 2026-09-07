#!/bin/sh

if [ "$POSTGRES_DB" = "cosmetic_db" ]
then
    echo "Wait postgres..."

    while ! nc -z "db" $DATABASE_PORT; do
      sleep 0.5
    done

    echo "PostgreSQL is ready!"
fi

if [ "$1" = "python" ] || [ "$1" = "gunicorn" ]; then

  echo "==> [Entrypoint] Запуск міграцій..."
  python manage.py makemigrations
  python manage.py migrate

  echo "==> [Entrypoint] Заванаження даних..."
  python manage.py loaddata fixtures/data_backup.json

  echo "==> [Entrypoint] Збір статики..."
  python manage.py collectstatic --noinput --clear
fi
exec "$@"