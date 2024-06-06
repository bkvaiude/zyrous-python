from uuid import UUID

from service.service.notifies_decorator import notifies
from service.service.service_base import ServiceBase

from .order import Order


class OrderService(ServiceBase[Order]):
    """The Service is where all of our business logic should sit.
    """

    @notifies('order_created')
    def create_order(
        self,
        num_items: int,
    ) -> Order:
        
        # Validate inputs.
        if num_items is None:
            raise ValueError('num_items is required.')

        # Create a new domain object.
        order = Order(
            id=None,
            num_items=num_items,
            status=None,
        )

        # Use the Service's Repository to create the object.
        self.repository.create(order)

        # Whatever we return will be sent as an 'order_created' notification, because
        # of the decorator we added to the function.
        return order

    @notifies('order_cancelled')
    def cancel_order(
        self,
        id: UUID,
    ) -> Order:

        # Get the existing Order.
        order = self.repository.retrieve(id)

        if order is None:
            raise ValueError(f"Order with ID {id} cannot be found")

        # Cancel the Order. Note that the business logic for state transitions is held
        # in the Domain object, leading to a better separation of concerns.
        order.cancel()

        # Update the Order.
        self.repository.update(order)

        # Whatever we return will be sent as an 'order_cancelled' notification, because
        # of the decorator we added to the function.
        return order

    @notifies('order_fulfilled')
    def fulfil_order(
        self,
        id: UUID,
    ) -> Order:
        # Get the existing Order.
        order = self.repository.retrieve(id)

        if order is None:
            raise ValueError(f"Order with ID {id} cannot be found")

        # Fulfil the Order. Note that the business logic for state transitions is held
        # in the Domain object, leading to a better separation of concerns.
        order.fulfil()

        # Update the Order.
        self.repository.update(order)

        # Whatever we return will be sent as an 'order_fulfilled' notification, because
        # of the decorator we added to the function.
        return order
