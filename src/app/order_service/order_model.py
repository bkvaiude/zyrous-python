from __future__ import annotations

from uuid import UUID

from service.api.individual_model_base import IndividualModelBase

from .order import Order


class OrderModel(IndividualModelBase[Order]):
    """ The Model defines how we want to expose information to the user. Note
    that we inherit from IndividualModelBase here, because our API will be
    hosted discretely (not federated).
    """

    id: UUID
    num_items: int
    status: str

    def __init__(
        self,
        id: UUID,
        num_items: int,
        status: str,
    ):
        self.id = id
        self.num_items = num_items
        self.status = status

    @staticmethod
    def from_domain(obj: Order) -> OrderModel:
        return OrderModel(
            id=obj.id,
            num_items=obj.num_items,
            status=obj.status,
        )
