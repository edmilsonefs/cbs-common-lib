class Issue:
    state = None
    app_version = None
    device = None
    error_record = None
    body = None

    def __init__(self, state=None, app_version=None, device=None):
        self.state = state
        self.app_version = app_version
        self.device = device
