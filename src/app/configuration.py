from fastapi import FastAPI

from service.service.service_configurer import ServiceConfigurer
from service.system.system_configurer import SystemConfigurer

from .order_service.order_api import OrderApi
from .order_service.order_repository import OrderRepository
from .order_service.order_service import OrderService
from .shipping_service.shipping_api import ShippingApi
from .shipping_service.shipping_repository import ShippingRepository
from .shipping_service.shipping_service import ShippingService

# NOTE: This is only one way to do configuration. This is simple to understand
# but could be harder to test, and it will grow in complexity with the System.
# For production systems, consider using Dependency Injection.


def configure_app() -> FastAPI:
    # Order Service Configurer.
    order_api_configurer = ServiceConfigurer(
        service_type=OrderService,
        api_type=OrderApi,
        repository_type=OrderRepository,
    )

    # Shipping Service Configurer.
    shipping_api_configurer = ServiceConfigurer(
        service_type=ShippingService,
        api_type=ShippingApi,
        repository_type=ShippingRepository,
    )

    # System Configurer.
    system_configurer = SystemConfigurer(
        service_configurers=[
            order_api_configurer,
            shipping_api_configurer,
        ],
    )

    return system_configurer.configure()
