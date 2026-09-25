from dataclasses import dataclass
from datetime import datetime


@dataclass
class Invite:
    name: str
    email: str
    phone: str
    created_at: datetime


class InviteService:
    def __init__(self, notifier, clock=datetime.utcnow):
        self.notifier = notifier
        self.clock = clock
        self.invites = []

    def create(self, name, email, phone):
        invite = Invite(name, email, phone, self.clock())
        self.invites.append(invite)
        return invite
