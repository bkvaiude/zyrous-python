from datetime import datetime
from typing import List
from typing import Optional
from uuid import UUID
from uuid import uuid4

from service.service.domain_base import DomainBase


class ShippingUpdate(DomainBase):

    creation_timestamp: datetime

    message: str

    def __init__(
        self,
        creation_timestamp: Optional[datetime],
        message: str,
    ):
        self.creation_timestamp = datetime.now() if creation_timestamp is None else creation_timestamp
        self.message = message


class Shipping(DomainBase):

    id: UUID

    order_id: UUID

    updates: List[ShippingUpdate]

    def __init__(
        self,
        id: Optional[UUID],
        order_id: UUID,
        updates: List[ShippingUpdate],
    ):
        self.id = uuid4() if id is None else id
        self.order_id = order_id
        self.updates = updates

    def add_update(
        self,
        message: str,
    ) -> ShippingUpdate:
        update = ShippingUpdate(
            creation_timestamp=None,
            message=message,
        )
        self.updates.append(update)
        return update
