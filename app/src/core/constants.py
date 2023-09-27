from enum import Enum, IntEnum

""" enums for TaskModel """


class TaskPriority(IntEnum):
    CRITICAL = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1


class TaskStatus(str, Enum):
    TODO = "To do"
    IN_PROGRESS = "In progress"
    CODE_REVIEW = "Code review"
    DEV_TEST = "Dev test"
    TESTING = "Testing"
    DONE = "Done"
    WONT_FIX = "Wontfix"


""" enums for UserModel """


class UserRoles(IntEnum):
    TEAM_LEAD = 1
    DEV = 2
    MANAGER = 3
    QA = 4
