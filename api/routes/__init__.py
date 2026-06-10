from ..animals.routes import ANIMAL_ROUTES
from ..exhibits.routes import EXHIBIT_ROUTES
from ..giftshops.routes import GIFT_SHOP_ROUTES
from ..pavilions.routes import PAVILION_ROUTES
from .registry import POST_ROUTES
from .registry import register_post_routes
from ..restaurants.routes import RESTAURANT_ROUTES
from ..restrooms.routes import RESTROOM_ROUTES

register_post_routes( ANIMAL_ROUTES )
register_post_routes( EXHIBIT_ROUTES )
register_post_routes( PAVILION_ROUTES )
register_post_routes( RESTAURANT_ROUTES )
register_post_routes( GIFT_SHOP_ROUTES )
register_post_routes( RESTROOM_ROUTES )

__all__ = [
   'POST_ROUTES',
   'register_post_routes',
]
