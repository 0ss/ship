class Notifier:
    """Real transports are wired in production. Tests use RecordingNotifier."""

    def send_email(self, to, subject, body):
        raise NotImplementedError

    def send_sms(self, phone, body):
        raise NotImplementedError


class RecordingNotifier(Notifier):
    def __init__(self):
        self.sent = []

    def send_email(self, to, subject, body):
        self.sent.append(("email", to, subject, body))

    def send_sms(self, phone, body):
        self.sent.append(("sms", phone, body))
