from enum import Enum, IntEnum

""" TaskModels """


class TaskPriority(IntEnum):
    CRITICAL = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1


class TaskType(str, Enum):
    BUG = "bug"
    TASK = "task"


class TaskStatus(str, Enum):
    TODO = "To do"
    IN_PROGRESS = "In progress"
    CODE_REVIEW = "Code review"
    DEV_TEST = "Dev test"
    TESTING = "Testing"
    DONE = "Done"
    WONT_FIX = "Wontfix"


""" UserModels """


class UserRoles(IntEnum):
    TEAM_LEAD = 1
    DEV = 2
    MANAGER = 3
    QA = 4


""" PaginationModels """


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


DEFAULT_PER_PAGE = 5
DEFAULT_SORT_KEY = "created_at"
DEFAULT_SORT_ORDER = SortOrder.DESC
MAX_PER_PAGE = 15
