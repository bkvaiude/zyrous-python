from faker import Faker
from service.testing.mock_api_environment import MockApiEnvironment

from app.shipping_service.shipping import Shipping
from app.shipping_service.shipping import ShippingUpdate
from app.shipping_service.shipping_api import ShippingApi
from app.shipping_service.shipping_service import ShippingService
from app.shipping_service.shipping_repository import ShippingRepository

class TestShippingApi():

    def test_get_shipping_succeeds_when_shipping_exists(self, fake: Faker):

        # Arrange
        order_id = fake.uuid4()
        shipping_id = fake.uuid4()

        shipping = Shipping(
            id=shipping_id,
            order_id=order_id,
            updates=[ShippingUpdate(
                creation_timestamp=fake.date_time(),
                message=fake.sentence()
            )]
        )

        with MockApiEnvironment(ShippingApi, ShippingService, ShippingRepository) as env:

            env.repository._add_function('get_by_order_id')
            env.repository.mock_for('get_by_order_id').return_value = shipping

            # Act
            response = env.api.get_shipping(order_id)

            # Assert
            assert response.id == shipping.id
            assert response.order_id == shipping.order_id
            assert response.updates[0].creation_timestamp == shipping.updates[0].creation_timestamp
            assert response.updates[0].message == shipping.updates[0].message

            env.repository.mock_for('get_by_order_id').assert_called_once_with(order_id)

    def test_update_shipping_succeeds_when_shipping_exists(self, fake: Faker):

        # Arrange
        order_id = fake.uuid4()
        shipping_id = fake.uuid4()

        shipping = Shipping(
            id=shipping_id,
            order_id=order_id,
            updates=[ShippingUpdate(
                creation_timestamp=fake.date_time(),
                message=fake.sentence()
            )]
        )

        with MockApiEnvironment(ShippingApi, ShippingService, ShippingRepository) as env:
            
            env.service.mock_for('add_update').return_value = shipping

            # Act.
            test_message = fake.sentence()
            response = env.api.update_shipping(order_id, test_message)

            # Assert.
            assert response.id == shipping.id
            assert response.order_id == shipping.order_id
            assert response.updates[0].creation_timestamp == shipping.updates[0].creation_timestamp
            assert response.updates[0].message == shipping.updates[0].message

            env.service.mock_for('add_update').assert_called_once_with(order_id=order_id, message=test_message)

    def test_shipping_created_triggered_with_observation(self, fake: Faker):

        # Arrange
        order_id = fake.uuid4()
        shipping_id = fake.uuid4()

        shipping = Shipping(
            id=shipping_id,
            order_id=order_id,
            updates=[]
        )

        with MockApiEnvironment(ShippingApi) as env:
            
            with env.subscribe_gql(env.api.shipping_created()) as subscription:

                # Act
                env.observe_event('shipping_created', shipping)

                # Assert
                subscription.assert_triggered_exactly_once()
                message = subscription.get_first()
                assert message.id == shipping.id
                assert message.order_id == shipping.order_id
                assert message.updates == []
    
    def test_shipping_updated_triggered_with_observation_with_no_args(self, fake: Faker):

        # Arrange
        order_id = fake.uuid4()
        shipping_id = fake.uuid4()

        shipping = Shipping(
            id=shipping_id,
            order_id=order_id,
            updates=[ShippingUpdate(
                creation_timestamp=fake.date_time(),
                message=fake.sentence()
            )]
        )

        with MockApiEnvironment(ShippingApi) as env:
            
            with env.subscribe_gql(env.api.shipping_updated(order_id=None)) as subscription:

                # Act
                env.observe_event('shipping_updated', shipping)

                # Assert
                subscription.assert_triggered_exactly_once()
                message = subscription.get_first()
                assert message.id == shipping.id
                assert message.order_id == shipping.order_id
                assert message.updates[0].creation_timestamp == shipping.updates[0].creation_timestamp
                assert message.updates[0].message == shipping.updates[0].message
    
    def test_shipping_updated_triggered_with_observation_with_valid_order_id(self, fake: Faker):

        # Arrange
        order_id = fake.uuid4()
        shipping_id = fake.uuid4()

        shipping = Shipping(
            id=shipping_id,
            order_id=order_id,
            updates=[ShippingUpdate(
                creation_timestamp=fake.date_time(),
                message=fake.sentence()
            )]
        )

        with MockApiEnvironment(ShippingApi) as env:
            
            with env.subscribe_gql(env.api.shipping_updated(order_id=order_id)) as subscription:

                # Act
                env.observe_event('shipping_updated', shipping)

                # Assert
                subscription.assert_triggered_exactly_once()
                message = subscription.get_first()
                assert message.id == shipping.id
                assert message.order_id == shipping.order_id
                assert message.updates[0].creation_timestamp == shipping.updates[0].creation_timestamp
                assert message.updates[0].message == shipping.updates[0].message
    
    def test_shipping_updated_not_triggered_with_observation_with_invalid_order_id(self, fake: Faker):

        # Arrange
        order_id = fake.uuid4()
        shipping_id = fake.uuid4()

        shipping = Shipping(
            id=shipping_id,
            order_id=order_id,
            updates=[]
        )

        with MockApiEnvironment(ShippingApi) as env:
            
            with env.subscribe_gql(env.api.shipping_updated(order_id=fake.uuid4())) as subscription:

                # Act
                env.observe_event('shipping_updated', shipping)

                # Assert
                subscription.assert_not_triggered()