from typing import Dict
from uuid import UUID

from pynamodb.indexes import GlobalSecondaryIndex
from service.repository.pynamodb.pynamodb_repository_base import PynamoDBRepositoryBase

from .shipping import Shipping


class ShippingRepository(PynamoDBRepositoryBase[Shipping]):

    def get_by_order_id(
        self,
        order_id: UUID,
    ) -> Shipping:
        shipping_model = self.get_model_definition()
        results = shipping_model.order_id_index.query(str(order_id))
        for result in results:
            return self._to_domain(result)

        raise Exception(f'Shipping not found for order ID {order_id}')

    def get_table_name(self) -> str:
        return 'shipping'

    def _get_global_secondary_indexes(self) -> Dict[str, GlobalSecondaryIndex]:
        yield self._prepare_global_secondary_index('order_id_index', 'order_id')
