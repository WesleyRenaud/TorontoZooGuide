from ..animals.animal_routes import AnimalRoutes
from ..attractions.attraction_routes import AttractionRoutes
from ..defibrillators.defibrillator_routes import DefibrillatorRoutes
from ..drinking_fountains.drinking_fountain_routes import DrinkingFountainRoutes
from ..emergency_intercoms.emergency_intercom_routes import EmergencyIntercomRoutes
from ..event_sites.event_site_routes import EventSiteRoutes
from ..events.event_routes import EventRoutes
from ..exhibits.exhibit_routes import ExhibitRoutes
from .get_route_registry import GetRouteRegistry
from ..giftshops.gift_shop_routes import GiftShopRoutes
from ..guardians.guardians_routes import GuardiansRoutes
from ..guest_services.guest_service_routes import GuestServiceRoutes
from ..itinerary.itinerary_routes import ItineraryRoutes
from ..pavilions.pavilion_routes import PavilionRoutes
from ..picnic_sites.picnic_site_routes import PicnicSiteRoutes
from .post_route_registry import PostRouteRegistry
from ..restaurants.restaurant_routes import RestaurantRoutes
from ..restrooms.restroom_routes import RestroomRoutes
from ..search.search_routes import SearchRoutes
from ..static.static_page_routes import StaticPageRoutes
from ..transportation.transportation_routes import TransportationRoutes
from ..updates.update_routes import UpdateRoutes
from ..wild_encounters.wild_encounter_routes import WildEncounterRoutes
from ..zoo_hours.zoo_hours_routes import ZooHoursRoutes

GetRouteRegistry.register( StaticPageRoutes.PAGE_ROUTES )
PostRouteRegistry.register( AnimalRoutes.ROUTES )
PostRouteRegistry.register( AttractionRoutes.ROUTES )
PostRouteRegistry.register( DefibrillatorRoutes.ROUTES )
PostRouteRegistry.register( DrinkingFountainRoutes.ROUTES )
PostRouteRegistry.register( EmergencyIntercomRoutes.ROUTES )
PostRouteRegistry.register( EventSiteRoutes.ROUTES )
PostRouteRegistry.register( EventRoutes.ROUTES )
PostRouteRegistry.register( ExhibitRoutes.ROUTES )
PostRouteRegistry.register( GiftShopRoutes.ROUTES )
PostRouteRegistry.register( ItineraryRoutes.ROUTES )
PostRouteRegistry.register( GuardiansRoutes.ROUTES )
PostRouteRegistry.register( GuestServiceRoutes.ROUTES )
PostRouteRegistry.register( PavilionRoutes.ROUTES )
PostRouteRegistry.register( PicnicSiteRoutes.ROUTES )
PostRouteRegistry.register( RestaurantRoutes.ROUTES )
PostRouteRegistry.register( RestroomRoutes.ROUTES )
PostRouteRegistry.register( SearchRoutes.ROUTES )
PostRouteRegistry.register( TransportationRoutes.ROUTES )
PostRouteRegistry.register( UpdateRoutes.ROUTES )
PostRouteRegistry.register( WildEncounterRoutes.ROUTES )
PostRouteRegistry.register( ZooHoursRoutes.ROUTES )

__all__ = [
   'GetRouteRegistry',
   'PostRouteRegistry',
]
