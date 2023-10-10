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
	4. Легковоспроизводимая сборка
	5. Юнит-тесты

## Сборка для локальной разработки

Установить [task-cli](https://taskfile.dev/installation/).
Установить [poetry](https://python-poetry.org/docs/#installation).
Задать переменные окружения в **.env**. Можно скопировать из **.env.test**.

### Команды

```bash
  task start — запустить сервисы и выполнить миграции
  task test — создать тестовую базу и прогнать тесты 
  task up — docker compose up
  task down — docker compose up
  task upgrade-dev — выполнить миграции
  task upgrade-dev — выполнить на тестовой базе
```
