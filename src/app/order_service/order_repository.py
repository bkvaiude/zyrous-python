from service.repository.pynamodb.pynamodb_repository_base import PynamoDBRepositoryBase

from .order import Order


class OrderRepository(PynamoDBRepositoryBase[Order]):
    """Our Repository gives us access to DynamoDB, so we need to choose the right
    base class (PynamoDBRepositoryBase). Because we only need the base functions
    of Repositories (retrieve, create etc), we only need to define the name of the
    table that we want to use.
    """

    def get_table_name(self) -> str:
        return 'order'
