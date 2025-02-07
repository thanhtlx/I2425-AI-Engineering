from main.models import UserModel


class Principal:
    def __init__(self, user: UserModel, roles: list[str] | None = None):
        self.user = user
        self.uid = user.id
        self.dob = user.dob
        self.email = user.email
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.job = user.job
        self.gender = user.gender
