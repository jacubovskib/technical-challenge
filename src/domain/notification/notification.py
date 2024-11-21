class Notification:
    def __init__(self):
        self.errors = []

    def add_error(self, error: str):
        self.errors.append(error)

    def has_errors(self):
        return len(self.errors) > 0

    def get_errors(self):
        return self.errors
