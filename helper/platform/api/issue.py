class Issue:
    state = None
    app_version = None
    device = None
    error_record = None
    body = None

    def __init__(self, state, app_version, device):
        self.state = state
        self.app_version = app_version
        self.device = device

    def build_issue(self, title, description_body, app_version):
        body = {
            "title": title,
            # "title": "[Ignore][Automation][Heartbeat] - /livetv/check availability pageName",
            "description": "Data validation is failed with failures: " + description_body,
            "assignedTo": {
                "href": "https://api.testlio.com/user/v1/users/5727"
            },
            "isApproved": False,
            "severity": "low",
            "labels": ["bug", "automation"],
            "isClosed": False,
            "isDeleted": False,
            "buildVersion": app_version,
            "isStarred": False
        }

        self.body = body

        return self
