from ..animals.routes import ANIMAL_ROUTES
from ..attractions.routes import ATTRACTION_ROUTES
from ..defibrillators.routes import DEFIBRILLATOR_ROUTES
from ..drinking_fountains.routes import DRINKING_FOUNTAIN_ROUTES
from ..emergency_intercoms.routes import EMERGENCY_INTERCOM_ROUTES
from ..event_sites.routes import EVENT_SITE_ROUTES
from ..events.routes import EVENT_ROUTES
from ..exhibits.routes import EXHIBIT_ROUTES
from .get_registry import GET_ROUTES
from .get_registry import register_get_routes
from ..giftshops.routes import GIFT_SHOP_ROUTES
from ..guardians.routes import GUARDIANS_ROUTES
from ..guest_services.routes import GUEST_SERVICE_ROUTES
from ..itinerary.routes import ITINERARY_ROUTES
from ..pavilions.routes import PAVILION_ROUTES
from ..picnic_sites.routes import PICNIC_SITE_ROUTES
from .registry import POST_ROUTES
from .registry import register_post_routes
from ..restaurants.routes import RESTAURANT_ROUTES
from ..restrooms.routes import RESTROOM_ROUTES
from ..search.routes import SEARCH_ROUTES
from ..static.routes import STATIC_PAGE_ROUTES
from ..updates.routes import UPDATE_ROUTES
from ..wild_encounters.routes import WILD_ENCOUNTER_ROUTES
from ..zoo_hours.routes import ZOO_HOURS_ROUTES
from ..zoomobile.routes import ZOOMOBILE_ROUTES

register_get_routes( STATIC_PAGE_ROUTES )
register_post_routes( ANIMAL_ROUTES )
register_post_routes( ATTRACTION_ROUTES )
register_post_routes( DEFIBRILLATOR_ROUTES )
register_post_routes( DRINKING_FOUNTAIN_ROUTES )
register_post_routes( EMERGENCY_INTERCOM_ROUTES )
register_post_routes( EVENT_SITE_ROUTES )
register_post_routes( EVENT_ROUTES )
register_post_routes( EXHIBIT_ROUTES )
register_post_routes( GIFT_SHOP_ROUTES )
register_post_routes( ITINERARY_ROUTES )
register_post_routes( GUARDIANS_ROUTES )
register_post_routes( GUEST_SERVICE_ROUTES )
register_post_routes( PAVILION_ROUTES )
register_post_routes( PICNIC_SITE_ROUTES )
register_post_routes( RESTAURANT_ROUTES )
register_post_routes( RESTROOM_ROUTES )
register_post_routes( SEARCH_ROUTES )
register_post_routes( UPDATE_ROUTES )
register_post_routes( WILD_ENCOUNTER_ROUTES )
register_post_routes( ZOO_HOURS_ROUTES )
register_post_routes( ZOOMOBILE_ROUTES )

__all__ = [
   'GET_ROUTES',
   'POST_ROUTES',
   'register_get_routes',
   'register_post_routes',
]
