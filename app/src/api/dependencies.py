from fastapi import Depends

from core.constants import UserRoles
from core.security import has_access, has_access_by_role

has_access_dep = Depends(has_access)


def has_role_dep(role: UserRoles):
    return Depends(has_access_by_role(role))
