from typing import AsyncGenerator
from typing import List
from uuid import UUID

# All APIs must inherit from ApiBase
from service.api.api_base import ApiBase
from service.api.graphql_mutation_decorator import graphql_mutation
# These decorators provide the ability to mark our functions as GraphQL
# queries, mutations, or subscriptions.
from service.api.graphql_query_decorator import graphql_query
from service.api.graphql_subscription_decorator import graphql_subscription

# This is our Model class, which we will use to represent data in the API.
from .order_model import OrderModel
# This is our Service class, which we will use to perform business logic.
from .order_service import OrderService


class OrderApi(ApiBase[OrderService]):
    """ This is an example API for Orders. Note that no permissions are added here,
    for the sake of simplicity. A real API would also use the permissions framework
    to ensure that only authorized users can access the API. See here for more:
    https://backstage.zyrous.com/docs/default/component/python-service/graphql-apis/permissions/
    """

    @graphql_mutation()
    def create_order(
        self,
        num_items: int,
    ) -> OrderModel:

        # Use the Service to create a new Order.
        order = self.service.create_order(num_items)

        # Return the new Order as a Model.
        return OrderModel.from_domain(order)

    @graphql_query()
    def retrieve_order(
        self,
        id: UUID,
    ) -> OrderModel:

        # Access the Service's Repository to directly retrieve an order. You could
        # also add a retrieval method to the Service, if you prefer.
        order = self.service.repository.retrieve(id)

        # Return the existing Order as a Model.
        return OrderModel.from_domain(order)

    @graphql_query()
    def list_orders(
        self,
    ) -> List[OrderModel]:

        # List all Order objects using the Service's Repository.
        all_orders = self.service.repository.get_all()

        # Map to the return type.
        return [OrderModel.from_domain(order) for order in all_orders]

    @graphql_mutation()
    def cancel_order(
        self,
        id: UUID,
    ) -> OrderModel:

        # We want state change logic to live in the Service. We don't want to
        # perform that logic in the API, or directly set the Order's status.
        order = self.service.cancel_order(id)
        return OrderModel.from_domain(order)

    @graphql_mutation()
    def fulfil_order(
        self,
        id: UUID,
    ) -> OrderModel:

        # We want state change logic to live in the Service. We don't want to
        # perform that logic in the API, or directly set the Order's status.
        order = self.service.fulfil_order(id)
        return OrderModel.from_domain(order)

