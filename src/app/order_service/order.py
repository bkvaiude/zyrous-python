from typing import Optional
from uuid import UUID
from uuid import uuid4

from service.service.domain_base import DomainBase


class Order(DomainBase):

    id: UUID
    num_items: int
    status: str

    def __init__(
        self,
        id: Optional[UUID],
        num_items: int,
        status: Optional[str],
    ):
        self.id = uuid4() if id is None else id
        self.num_items = num_items
        self.status = 'Created' if status is None else status

    def cancel(self):

        if self.status == 'Cancelled':
            raise Exception('Order is already cancelled; it cannot be cancelled again.')
        if self.status == 'Fulfilled':
            raise Exception('Order is already fulfilled; it cannot be cancelled.')

        self.status = 'Cancelled'

    def fulfil(self):

        if self.status == 'Fulfilled':
            raise Exception('Order is already fulfilled; it cannot be fulfilled again.')
        if self.status == 'Cancelled':
            raise Exception('Order is cancelled; it cannot be fulfilled.')

        self.status = 'Fulfilled'
