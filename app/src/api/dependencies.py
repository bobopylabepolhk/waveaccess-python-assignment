from typing import Annotated
from fastapi import Depends
from core.constants import UserRoles
from core.security import has_access, has_access_by_role, get_current_user_id


has_access_dep = Depends(has_access)
def has_role_dep(role: UserRoles): 
	return Depends(has_access_by_role(role))
current_user_id_dep = Annotated[int, Depends(get_current_user_id)]
