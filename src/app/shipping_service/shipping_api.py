from typing import AsyncGenerator
from typing import Optional
from uuid import UUID

from service.api.api_base import ApiBase
from service.api.graphql_mutation_decorator import graphql_mutation
from service.api.graphql_query_decorator import graphql_query
from service.api.graphql_subscription_decorator import graphql_subscription
from service.validation.validation import equals_if_not_none_or_empty

from .shipping_model import ShippingModel
from .shipping_service import ShippingService


class ShippingApi(ApiBase[ShippingService]):

    @graphql_query()
    def get_shipping(
        self,
        order_id: UUID,
    ) -> ShippingModel:

        shipping = self.service.repository.get_by_order_id(order_id)
        return ShippingModel.from_domain(shipping)

    @graphql_mutation()
    def update_shipping(
        self,
        order_id: UUID,
        message: str,
    ) -> ShippingModel:

        shipping = self.service.add_update(order_id=order_id, message=message)
        return ShippingModel.from_domain(shipping)

    @graphql_subscription()
    async def shipping_created(self) -> AsyncGenerator[ShippingModel, None]:

        async for shipping in self.service.observe('shipping_created'):
            yield ShippingModel.from_domain(shipping)

    @graphql_subscription()
    async def shipping_updated(
        self,
        order_id: Optional[UUID],
    ) -> AsyncGenerator[ShippingModel, None]:

        async for shipping in self.service.observe('shipping_updated'):

            if equals_if_not_none_or_empty(shipping.order_id, order_id):
                yield ShippingModel.from_domain(shipping)
