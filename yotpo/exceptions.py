
class YotpoException(Exception):
    def __init__(self, response=dict()):
        status = response.json().get('status', dict())
        self.status_code = response.status_code
        self.error_type = status.get('error_type', 'No error type')
        self.message = status.get('message', 'No message')

    def __str__(self):
        return repr('{}:: {} || {}'.format(
            self.status_code,
            self.error_type,
            self.message,
        ))
