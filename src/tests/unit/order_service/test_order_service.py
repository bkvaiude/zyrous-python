import pytest

from service.testing.mock_service_environment import MockServiceEnvironment

from app.order_service.order_service import OrderService
from app.order_service.order import Order

class TestOrderService:
    
    def test_create_order_succeeds_with_valid_data(self, fake):

        # Arrange
        num_items = fake.random_int()

        with MockServiceEnvironment(OrderService) as env:
            
            # Act
            order = env.service.create_order(num_items)

            # Assert
            assert order.id is not None
            assert order.num_items == num_items
            assert order.status == 'Created'

            env.repository.create_mock.assert_called_once_with(order)

            env.notifications.assert_sent_exactly_once_on('order_created')
            assert env.notifications.get_first('order_created') == order

    def test_create_order_fails_with_invalid_data(self, fake):

        with MockServiceEnvironment(OrderService) as env:
            
            # Act
            with pytest.raises(ValueError):
                env.service.create_order(None)

            # Assert
            env.repository.create_mock.assert_not_called()
            env.notifications.assert_not_sent_on('order_created')

    def test_cancel_order_succeeds_with_valid_data(self, fake):

        # Arrange
        order_id = fake.uuid4()
        num_items = fake.word()

        order = Order(
            id=order_id,
            num_items=num_items,
            status=None
        )

        with MockServiceEnvironment(OrderService) as env:

            env.repository.retrieve_mock.return_value = order

            # Act
            result = env.service.cancel_order(order_id)

            # Assert
            assert result == order
            assert order.status == 'Cancelled'

            env.repository.retrieve_mock.assert_called_once_with(order_id)
            env.repository.update_mock.assert_called_once_with(order)

            env.notifications.assert_sent_exactly_once_on('order_cancelled')
            assert order == env.notifications.get_first('order_cancelled')

    def test_cancel_order_fails_with_missing_order(self, fake):

        # Arrange
        order_id = fake.uuid4()

        with MockServiceEnvironment(OrderService) as env:

            env.repository.retrieve_mock.return_value = None

            # Act
            with pytest.raises(ValueError):
                env.service.cancel_order(order_id)

            # Assert
            env.repository.update_mock.assert_not_called()
            env.notifications.assert_not_sent_on('order_cancelled')

    def test_fulfil_order_succeeds_with_valid_data(self, fake):

        # Arrange
        order_id = fake.uuid4()
        num_items = fake.word()

        order = Order(
            id=order_id,
            num_items=num_items,
            status=None
        )

        with MockServiceEnvironment(OrderService) as env:

            env.repository.retrieve_mock.return_value = order

            # Act
            result = env.service.fulfil_order(order_id)

            # Assert
            assert result == order
            assert result.status == 'Fulfilled'

            env.repository.retrieve_mock.assert_called_once_with(order_id)
            env.repository.update_mock.assert_called_once_with(order)

            env.notifications.assert_sent_exactly_once_on('order_fulfilled')
            assert result == env.notifications.get_first('order_fulfilled')

    def test_fulfil_order_fails_with_missing_order(self, fake):

        # Arrange
        order_id = fake.uuid4()

        with MockServiceEnvironment(OrderService) as env:

            env.repository.retrieve_mock.return_value = None

            # Act
            with pytest.raises(ValueError):
                env.service.fulfil_order(order_id)

            # Assert
            env.repository.update_mock.assert_not_called()
            env.notifications.assert_not_sent_on('order_fulfilled')