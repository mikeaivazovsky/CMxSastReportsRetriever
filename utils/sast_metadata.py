from enum import Enum

# put here all the columns you want to delete during report optimization
optimizable_columns = ['Custom', 'Comment']

class Projects(Enum):
    # sample projects and id definition
    Project1 = 1
    Project2 = 2
    Project3 = 3

class reportStatus(Enum):
    Deleted = 0
    InProcess = 1
    Created = 2
    Failed = 3

