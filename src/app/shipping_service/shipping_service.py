from uuid import UUID

from service.service.notifies_decorator import notifies
from service.service.observes_decorator import observes
from service.service.service_base import ServiceBase

from app.order_service.order import Order

from .shipping import Shipping


class ShippingService(ServiceBase[Shipping]):

    @observes('order_created')
    @notifies('shipping_created')
    def order_created(self, order: Order):
        shipping = Shipping(
            id=None,
            order_id=str(order.id),
            updates=[],
        )
        self.repository.create(shipping)
        return shipping

    @notifies('shipping_updated')
    def add_update(
        self,
        order_id: UUID,
        message: str,
    ) -> Shipping:
        shipping = self.repository.get_by_order_id(order_id)
        shipping.add_update(message)
        self.repository.update(shipping)
        return shipping
