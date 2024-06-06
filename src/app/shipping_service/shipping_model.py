from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID

from service.api.individual_model_base import IndividualModelBase

from .shipping import Shipping
from .shipping import ShippingUpdate


class ShippingUpdateModel(IndividualModelBase[ShippingUpdate]):

    creation_timestamp: datetime
    message: str

    def __init__(
        self,
        creation_timestamp: datetime,
        message: str,
    ):
        self.creation_timestamp = creation_timestamp
        self.message = message

    @staticmethod
    def from_domain(obj: ShippingUpdate) -> ShippingUpdateModel:
        return ShippingUpdateModel(
            creation_timestamp=obj.creation_timestamp,
            message=obj.message,
        )


class ShippingModel(IndividualModelBase[Shipping]):

    id: UUID

    order_id: UUID

    updates: List[ShippingUpdateModel]

    def __init__(
        self,
        id: UUID,
        order_id: UUID,
        updates: List[ShippingUpdateModel],
    ):
        self.id = id
        self.order_id = order_id
        self.updates = updates

    @staticmethod
    def from_domain(obj: Shipping) -> ShippingModel:
        return ShippingModel(
            id=obj.id,
            order_id=obj.order_id,
            updates=[ShippingUpdateModel.from_domain(u) for u in obj.updates],
        )
