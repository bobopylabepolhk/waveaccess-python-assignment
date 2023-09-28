DEFAULT_404_MESSAGE = "entity not found!"

TASK_INVALID_ASIGNEE_ROLE = "status {} is not allowed with asignee role {}!"
TASK_INVALID_STATUS_CHAIN = "changing status from {} to {} is not allowed!"
TASK_INVALID_STATUS_IN_PROGRESS = "status IN_PROGRESS cannot be used with empty asignee"
TASK_STATUS_DOES_NOT_EXIST = "status {} does not exist!"
TASK_NOT_FOUND_BY_ID = "task with id == {} does not exist!"

TASK_LINK_NOT_FOUND_BY_ID = "task link with id == {} does not exist!"
TASK_LINK_WRONG_IDS = "task with id == {} cannnot be linked to task id == {}"

USER_NOT_FOUND_OR_WRONG_PASSWORD = (
    "user not found or entered the password is incorrect!"
)
USER_ALREADY_EXISTS = "user already exists!"
AUTHORIZATION_ERROR = (
    "access token not found in Authorization header or incorrect access token!"
)
WRONG_ROLE = "access not allowed with role {}. necessary role: {}"

NOT_FOUND_ASIGNEE_ID = "asigned user with id == {} not found!"

INVALID_SORT_PARAM = "sort param {} is invalid! available sort params: {}"
