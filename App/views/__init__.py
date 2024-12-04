from .staff import staff_views
from .index import index_views
from .admin import admin_views
from .auth import auth_views
from .user import user_views

views = [staff_views, index_views, admin_views, auth_views, user_views]
# blueprints must be added to this list^^
