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
  python manage.py migrate

  echo "==> [Entrypoint] Заванаження даних..."
  INIT_FLAG="/usr/src/app/media/.data_initialized"
  if [ ! -f "$INIT_FLAG" ]; then
    echo "==> [Entrypoint] Перший запуск! Завантаження початкових даних (fixtures)..."
    python manage.py loaddata fixtures/data_backup.json

    if [ $? -eq 0 ]; then
      # Створюємо маркер, щоб при наступному запуску цей блок пропускався
      touch "$INIT_FLAG"
      echo "==> [Entrypoint] Дані успішно завантажені!"
    else
      echo "==> [Entrypoint] Помилка завантаження даних!"
    fi
  else
    echo "==> [Entrypoint] База даних вже була ініціалізована раніше, пропуск loaddata."
  fi

  echo "==> [Entrypoint] Збір статики..."
  python manage.py collectstatic --noinput
fi
exec "$@"