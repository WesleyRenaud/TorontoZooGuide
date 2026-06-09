from ..animals.routes import ANIMAL_ROUTES
from ..exhibits.routes import EXHIBIT_ROUTES
from .registry import POST_ROUTES
from .registry import register_post_routes

register_post_routes( ANIMAL_ROUTES )
register_post_routes( EXHIBIT_ROUTES )

__all__ = [
   'POST_ROUTES',
   'register_post_routes',
]
