from .repositories.iris import IrisRepository
from .services.iris import IrisService

iris_repository = IrisRepository()

iris_service = IrisService(iris_repository)


def get_iris_service() -> IrisService:
    return iris_service
