import pytest
from faker import Faker

from app.order_service.order import Order

class TestOrder():

    def test_init_succeeds_with_minimal_data(self, fake):
        # Arrange
        num_items = fake.random_int()

        # Act
        order = Order(None, num_items, None)

        # Assert
        assert order.id is not None
        assert order.num_items == num_items
        assert order.status == 'Created'

    def test_init_succeeds_with_all_data(self, fake):
        # Arrange
        id = fake.uuid4()
        num_items = fake.word()
        status = fake.word()

        # Act
        order = Order(id, num_items, status)

        # Assert
        assert order.id == id
        assert order.num_items == num_items
        assert order.status == status

    def test_cancel_succeeds_with_created_order(self, fake):
        # Arrange
        order = Order(
            fake.uuid4(),
            fake.random_int(),
            'Created'
        )

        # Act
        order.cancel()

        # Assert.
        assert order.status == 'Cancelled'

    def test_cancel_fails_with_cancelled_order(self, fake):
        # Arrange
        order = Order(
            fake.uuid4(),
            fake.random_int(),
            'Cancelled'
        )

        # Act
        with pytest.raises(Exception):
            order.cancel()

    def test_cancel_fails_with_fulfilled_order(self, fake):
        # Arrange
        order = Order(
            fake.uuid4(),
            fake.random_int(),
            'Fulfilled'
        )

        # Act
        with pytest.raises(Exception):
            order.cancel()

    def test_fulfil_succeeds_with_created_order(self, fake):
        # Arrange
        order = Order(
            fake.uuid4(),
            fake.random_int(),
            'Created'
        )

        # Act
        order.fulfil()

        # Assert.
        assert order.status == 'Fulfilled'

    def test_fulfil_fails_with_cancelled_order(self, fake):
        # Arrange
        order = Order(
            fake.uuid4(),
            fake.random_int(),
            'Cancelled'
        )

        # Act
        with pytest.raises(Exception):
            order.fulfil()

    def test_fulfil_fails_with_fulfilled_order(self, fake):
        # Arrange
        order = Order(
            fake.uuid4(),
            fake.random_int(),
            'Fulfilled'
        )

        # Act
        with pytest.raises(Exception):
            order.fulfil()