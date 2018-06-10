class Issue:
    state = None
    app_version = None
    device = None
    error_record = None

    body = {
        "title": "[Ignore][Automation][Heartbeat] - /livetv/check availability pageName",
        "description": "Data validation is failed with failures: " + error_record,
        "assignedTo": {
            "href": "https://api.testlio.com/user/v1/users/5727"
        },
        "isApproved": False,
        "severity": "low",
        "labels": ["bug", "automation"],
        "isClosed": False,
        "isDeleted": False,
        "buildVersion": "CBS-5.0.0-1650020",
        "isStarred": False
    }

    def __init__(self, state, app_version, device):
        self.state = state
        self.app_version = app_version
        self.device = device
