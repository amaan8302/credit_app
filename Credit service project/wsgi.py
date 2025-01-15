import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'django' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_service_project.settings')

# Create and expose the WSGI application callable for the server
application = get_wsgi_application()
