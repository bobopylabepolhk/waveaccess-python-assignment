import os

from dotenv import load_dotenv

load_dotenv()

def get_pg_conn_str(is_local: bool = False):
	return 'postgresql+asyncpg://{}:{}@{}:{}/{}'.format(
	os.environ.get('POSTGRES_USER'),
	os.environ.get('POSTGRES_PASSWORD'),
	'localhost' if is_local else os.environ.get('PGHOST'),
	os.environ.get('PGPORT'),
	os.environ.get('POSTGRES_DB'))
