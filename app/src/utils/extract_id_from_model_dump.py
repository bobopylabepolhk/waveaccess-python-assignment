from typing import Any
from core.messages import INVALID_PAYLOAD


def extract_id_from_model_dump(dump: dict[str, Any]):
	id: int | None = dump.get('id')
	if id is None:
		raise ValueError(INVALID_PAYLOAD.format('id'))
	data: dict[str, Any] = { 
		key: value for key, value in dump.items() if key != 'id' 
	}

	return id, data