from service.testing.mock_api_environment import MockApiEnvironment

from app.order_service.order_api import OrderApi
from app.order_service.order import Order

class TestOrderApi:

    def test_create_order_succeeds_with_valid_data(self, fake):

        # Arrange
        order_id = fake.uuid4()
        num_items = fake.random_int()
        status = fake.word()

        order = Order(
            order_id,
            num_items,
            status
        )

        with MockApiEnvironment(OrderApi) as env:

            env.service.mock_for('create_order').return_value = order

            # Act
            result = env.api.create_order(num_items=num_items)

            # Assert
            assert result.id == order.id
            assert result.num_items == order.num_items
            assert result.status == order.status

            env.service.mock_for('create_order').assert_called_once_with(num_items)

    def test_retrieve_order_succeeds_with_valid_data(self, fake):

        # Arrange
        order_id = fake.uuid4()
        num_items = fake.random_int()
        status = fake.word()

        order = Order(
            order_id,
            num_items,
            status
        )

        with MockApiEnvironment(OrderApi) as env:

            env.repository.retrieve_mock.return_value = order

            # Act
            result = env.api.retrieve_order(id=order_id)

            # Assert
            assert result.id == order.id
            assert result.num_items == order.num_items
            assert result.status == order.status
            
            env.repository.retrieve_mock.assert_called_once_with(order_id)

    def test_list_orders_succeeds_with_valid_data(self, fake):

        # Arrange
        orders = []

        for i in range(0,10):
            orders.append(Order(
                fake.uuid4(),
                fake.random_int(),
                fake.word()
            ))
            
        with MockApiEnvironment(OrderApi) as env:

            env.repository.get_all_mock.return_value = orders

            # Act
            result = env.api.list_orders()

            # Assert
            assert len(result) == 10

            for i in range(0,10):
                assert result[i].id == orders[i].id
                assert result[i].num_items == orders[i].num_items
                assert result[i].status == orders[i].status

            env.repository.get_all_mock.assert_called_once()

    def test_cancel_order_succeeds_with_valid_data(self, fake):

        # Arrange
        order_id = fake.uuid4()
        num_items = fake.random_int()
        status = fake.word()

        order = Order(
            order_id,
            num_items,
            status
        )

        with MockApiEnvironment(OrderApi) as env:
            
            env.service.mock_for('cancel_order').return_value = order

            # Act
            result = env.api.cancel_order(id=order_id)

            # Assert
            assert result.id == order.id
            assert result.num_items == order.num_items
            assert result.status == order.status
            
            env.service.mock_for('cancel_order').assert_called_once_with(order_id)

    def test_fulfil_order_succeeds_with_valid_data(self, fake):

        # Arrange
        order_id = fake.uuid4()
        num_items = fake.random_int()
        status = fake.word()

        order = Order(
            order_id,
            num_items,
            status
        )

        with MockApiEnvironment(OrderApi) as env:
            
            env.service.mock_for('fulfil_order').return_value = order

            # Act
            result = env.api.fulfil_order(id=order_id)

            # Assert
            assert result.id == order.id
            assert result.num_items == order.num_items
            assert result.status == order.status
            
            env.service.mock_for('fulfil_order').assert_called_once_with(order_id)

    def test_order_cancelled_event_triggered_by_notification(self, fake):

        # Arrange
        order_id = fake.uuid4()
        num_items = fake.random_int()
        status = fake.word()

        order = Order(
            order_id,
            num_items,
            status
        )

        with MockApiEnvironment(OrderApi) as env:

            with env.subscribe_gql(env.api.order_cancelled()) as subscription:
                
                # Act
                env.observe_event('order_cancelled', order)

                # Assert
                subscription.assert_triggered_exactly_once()
                result = subscription.get_first()

                assert result.id == order.id
                assert result.num_items == order.num_items
                assert result.status == order.status

    def test_order_created_event_triggered_by_notification(self, fake):

        # Arrange
        order_id = fake.uuid4()
        num_items = fake.random_int()
        status = fake.word()

        order = Order(
            order_id,
            num_items,
            status
        )

        with MockApiEnvironment(OrderApi) as env:

            with env.subscribe_gql(env.api.order_created()) as subscription:
                
                # Act
                env.observe_event('order_created', order)

                # Assert
                subscription.assert_triggered_exactly_once()
                result = subscription.get_first()

                assert result.id == order.id
                assert result.num_items == order.num_items
                assert result.status == order.status

    def test_order_fulfilled_event_triggered_by_notification(self, fake):

        # Arrange
        order_id = fake.uuid4()
        num_items = fake.random_int()
        status = fake.word()

        order = Order(
            order_id,
            num_items,
            status
        )

        with MockApiEnvironment(OrderApi) as env:

            with env.subscribe_gql(env.api.order_fulfilled()) as subscription:
                
                # Act
                env.observe_event('order_fulfilled', order)

                # Assert
                subscription.assert_triggered_exactly_once()
                result = subscription.get_first()

                assert result.id == order.id
                assert result.num_items == order.num_items
                assert result.status == order.status