from sqlmodel import Session


class ServiceMixin:
    def __init__(self, session: Session):
        self.session: Session = session