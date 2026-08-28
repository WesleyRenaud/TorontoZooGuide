from .tables.animal_day_seasonal_viewability_multiplier_seed_table import animal_day_seasonal_viewability_multipliers as _animal_day_seasonal_viewability_multipliers
from .tables.animal_seed_table import animals as _animals
from .tables.attraction_day_seasonal_availability_multiplier_seed_table import attraction_day_seasonal_availability_multipliers as _attraction_day_seasonal_availability_multipliers
from .tables.attraction_seed_table import attractions as _attractions
from .tables.defibrillator_seed_table import defibrillators as _defibrillators
from .tables.drinking_fountain_day_seasonal_availability_multiplier_seed_table import drinking_fountain_day_seasonal_availability_multipliers as _drinking_fountain_day_seasonal_availability_multipliers
from .tables.drinking_fountain_seed_table import drinking_fountains as _drinking_fountains
from .tables.emergency_intercom_seed_table import emergency_intercoms as _emergency_intercoms
from .tables.enclosure_seed_table import enclosures as _enclosures
from .tables.enclosure_viewing_seed_table import enclosure_viewings as _enclosure_viewings
from .tables.event_site_seed_table import event_sites as _event_sites
from .tables.exhibit_day_seasonal_availability_multiplier_seed_table import exhibit_day_seasonal_availability_multipliers as _exhibit_day_seasonal_availability_multipliers
from .tables.exhibit_seed_table import exhibits as _exhibits
from .tables.gift_shop_day_seasonal_availability_multiplier_seed_table import gift_shop_day_seasonal_availability_multipliers as _gift_shop_day_seasonal_availability_multipliers
from .tables.gift_shop_seed_table import gift_shops as _gift_shops
from .tables.guest_service_seed_table import guest_services as _guest_services
from .tables.itinerary_event_default_seed_table import itinerary_event_defaults as _itinerary_event_defaults
from .tables.itinerary_status_seed_table import itinerary_statuses as _itinerary_statuses
from .tables.meet_the_guardians_talk_seed_table import guardians_talks as _guardians_talks
from .tables.pavilion_seed_table import pavilions as _pavilions
from .tables.picnic_site_seed_table import picnic_sites as _picnic_sites
from .tables.region_seed_table import regions as _regions
from .tables.restaurant_day_seasonal_availability_multiplier_seed_table import restaurant_day_seasonal_availability_multipliers as _restaurant_day_seasonal_availability_multipliers
from .tables.restaurant_seed_table import restaurants as _restaurants
from .tables.restroom_seed_table import restrooms as _restrooms
from .tables.transportation_day_route_seed_table import transportation_day_routes as _transportation_day_routes
from .tables.transportation_leg_seed_table import transportation_legs as _transportation_legs
from .tables.transportation_route_leg_marker_seed_table import transportation_route_leg_markers as _transportation_route_leg_markers
from .tables.transportation_route_leg_seed_table import transportation_route_legs as _transportation_route_legs
from .tables.transportation_route_seed_table import transportation_routes as _transportation_routes
from .tables.transportation_route_station_seed_table import transportation_route_stations as _transportation_route_stations
from .tables.transportation_seed_table import transportations as _transportations
from .tables.transportation_station_seed_table import transportation_stations as _transportation_stations
from .tables.wild_encounter_meeting_spot_seed_table import wild_encounter_meeting_spots as _wild_encounter_meeting_spots
from .tables.wild_encounter_seed_table import wild_encounters as _wild_encounters
from .tables.zoo_hours_seed_table import zoo_hours as _zoo_hours


class Data():
   animals = _animals
   animal_day_seasonal_viewability_multipliers = _animal_day_seasonal_viewability_multipliers
   attractions = _attractions
   attraction_day_seasonal_availability_multipliers = _attraction_day_seasonal_availability_multipliers
   defibrillators = _defibrillators
   drinking_fountains = _drinking_fountains
   drinking_fountain_day_seasonal_availability_multipliers = (
      _drinking_fountain_day_seasonal_availability_multipliers )
   emergency_intercoms = _emergency_intercoms
   enclosures = _enclosures
   enclosure_viewings = _enclosure_viewings
   event_sites = _event_sites
   exhibits = _exhibits
   exhibit_day_seasonal_availability_multipliers = _exhibit_day_seasonal_availability_multipliers
   gift_shops = _gift_shops
   gift_shop_day_seasonal_availability_multipliers = _gift_shop_day_seasonal_availability_multipliers
   guest_services = _guest_services
   itinerary_event_defaults = _itinerary_event_defaults
   itinerary_statuses = _itinerary_statuses
   guardians_talks = _guardians_talks
   pavilions = _pavilions
   picnic_sites = _picnic_sites
   regions = _regions
   restaurants = _restaurants
   restaurant_day_seasonal_availability_multipliers = _restaurant_day_seasonal_availability_multipliers
   restrooms = _restrooms
   transportations = _transportations
   transportation_day_routes = _transportation_day_routes
   transportation_legs = _transportation_legs
   transportation_routes = _transportation_routes
   transportation_route_legs = _transportation_route_legs
   transportation_route_leg_markers = _transportation_route_leg_markers
   transportation_route_stations = _transportation_route_stations
   transportation_stations = _transportation_stations
   wild_encounters = _wild_encounters
   wild_encounter_meeting_spots = _wild_encounter_meeting_spots
   zoo_hours = _zoo_hours
