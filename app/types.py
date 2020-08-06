import enum

class DeveloperVerificationStatus(enum.Enum):
    application_not_submitted = 0
    application_submitted = 1
    interview_offered = 2
    verified = 3
    rejected_at_application = 4
    rejected_at_interview = 5
    rejected_other = 6
