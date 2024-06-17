"""The main module sets up the API and starts the server."""

from fastapi.middleware.cors import CORSMiddleware

from service.system.system_context import SystemContext

from .configuration import configure_app

# Create the FastAPI application. This configures
# all dependencies and routes.
app = configure_app()

# Set the application title.
app.title = 'Sample API'

# Configure CORS.
SystemContext.get_app().add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
