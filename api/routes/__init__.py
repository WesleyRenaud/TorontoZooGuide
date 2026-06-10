from ..animals.routes import ANIMAL_ROUTES
from ..exhibits.routes import EXHIBIT_ROUTES
from ..pavilions.routes import PAVILION_ROUTES
from .registry import POST_ROUTES
from .registry import register_post_routes
from ..restaurants.routes import RESTAURANT_ROUTES

register_post_routes( ANIMAL_ROUTES )
register_post_routes( EXHIBIT_ROUTES )
register_post_routes( PAVILION_ROUTES )
register_post_routes( RESTAURANT_ROUTES )

__all__ = [
   'POST_ROUTES',
   'register_post_routes',
]
