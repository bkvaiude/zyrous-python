from service.testing.mock_service_environment import MockServiceEnvironment

from app.shipping_service.shipping_service import ShippingService
from app.shipping_service.shipping_repository import ShippingRepository
from app.order_service.order import Order
from app.shipping_service.shipping import Shipping

class TestShippingService():

    def test_order_created_succeeds_when_triggered_with_observation(self, fake):

        # Arrange
        order_id = fake.uuid4()
        order = Order(
            id=order_id,
            num_items=fake.random_int(),
            status=fake.word()
        )

        with MockServiceEnvironment(ShippingService) as env:
            
            # Act
            env.observe_event('order_created', order)

            # Assert
            env.notifications.assert_sent_exactly_once_on('shipping_created')
            shipping = env.notifications.get_first('shipping_created')

            assert shipping.order_id == order_id
            assert shipping.id is not None
            assert shipping.updates == []

            env.repository.create_mock.assert_called_once_with(shipping)

    def test_add_update_succeeds_for_existing_shipping(self, fake):

        # Arrange
        order_id = fake.uuid4()
        shipping = Shipping(
            order_id=order_id,
            id=fake.uuid4(),
            updates=[]
        )

        test_message = fake.sentence()

        with MockServiceEnvironment(ShippingService, ShippingRepository) as env:
            
            env.repository.mock_for('get_by_order_id').return_value = shipping

            # Act
            result = env.service.add_update(order_id, test_message)

            # Assert
            assert result.order_id == order_id
            assert len(result.updates) == 1
            assert result.updates[0].message == test_message

            env.repository.mock_for('get_by_order_id').assert_called_once_with(order_id)
            env.repository.update_mock.assert_called_once_with(result)

            env.notifications.assert_sent_exactly_once_on('shipping_updated')
            assert env.notifications.get_first('shipping_updated') == shipping