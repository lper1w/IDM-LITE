from app.repositories.iris import IrisRepository, User


class IrisService:
    def __init__(self, repository: IrisRepository) -> None:
        self.repository = repository

    def get_user(self, id: int) -> User | None:
        return self.repository.get_user(id)

    def get_chats(self, id: int) -> list[dict]:
        return self.repository.get_chats(id)

    def create_user(self, user: User) -> User:
        return self.repository.create_user(user)

    def update_user(self, user: User) -> User:
        return self.repository.update_user(user)
