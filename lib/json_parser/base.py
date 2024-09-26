class BaseModel:
    @classmethod
    def get(cls, id):
        """Получить экземпляр по его ID."""
        raise NotImplementedError

    @classmethod
    def save(cls, instance):
        """Сохранить экземпляр в хранилище."""
        raise NotImplementedError

    @classmethod
    def delete(cls, id):
        """Удалить экземпляр из хранилища."""
        raise NotImplementedError

    @classmethod
    def all(cls):
        """Получить все экземпляры."""
        raise NotImplementedError

    @classmethod
    def create(cls, **kwargs):
        """Создать и сохранить новый экземпляр."""
        raise NotImplementedError

    @classmethod
    def update(cls, id, **kwargs):
        """Обновить экземпляр."""
        raise NotImplementedError
