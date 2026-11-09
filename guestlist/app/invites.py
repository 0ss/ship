from dataclasses import dataclass
from datetime import datetime, timedelta

INVITE_TTL = timedelta(days=14)


@dataclass
class Invite:
    name: str
    email: str
    phone: str
    created_at: datetime
    expires_at: datetime

    def is_expired(self, now=None):
        now = datetime.utcnow() if now is None else now
        return now >= self.expires_at


class InviteService:
    def __init__(self, notifier, clock=datetime.utcnow):
        self.notifier = notifier
        self.clock = clock
        self.invites = []

    def create(self, name, email, phone):
        created_at = self.clock()
        invite = Invite(name, email, phone, created_at, created_at + INVITE_TTL)
        self.invites.append(invite)
        return invite
