import enum

class VerificationStatus(enum.Enum):
    not_submitted = 0
    pending = 1
    awaiting_response = 2
    accepted = 3
    rejected = 4

class DeveloperProjectStatus(enum.Enum):
    not_related = 0
    interested = 1
    assigned = 2
    deassigned = 3
    completed = 4

# Define constants
LEN_DISPLAY_NAME = 60
LEN_DESCRIPTION = 500
LEN_UUID=32
LEN_MIN_UUID=3  # User for user names and such
LEN_PRICE=10
LEN_URL=60
LEN_TAG = 20
LEN_INTERNAL_DB_COMMENT = 500
