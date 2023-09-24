# bugtracker-waveaccess-assignment

## Задача: реализовать упрощённую версию таск-треке
Используя [FastAPI](https://fastapi.tiangolo.com/) + Postgres + [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/) & [asyncpg](https://github.com/MagicStack/asyncpg)

	1. Регистрация и авторизация.
	2. Роли и разрешения для редактирования статусов и других пользователей.
	3. CRUDы для тасок:
		3.1. Фильтрация и сортировка;
		3.2. История изменений таски;
		3.3. Изменение статуса в зависимости от роли;
		3.4. История изменений;
		3.5. Списки блокирующих и блокируемых тасок;
	4. Легковоспроизводимая сборка (docker compose + alembic)
	5. Юнит-тесты


## Сборка для локальной разработки

Задать переменные окружения — переименовать **.env.example** в **.env**

### Запустить сервисы

```bash
  cd app
  docker compose up
```

установить poetry

```bash
  pip install poetry
  poetry install
  poetry shell
```

и запустить миграции

```bash
  alembic upgrade head
```