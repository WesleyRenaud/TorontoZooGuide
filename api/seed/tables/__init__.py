from . import animal
from . import animal_day_seasonal_viewability_multiplier
from . import animal_status
from . import animal_viewing_alert
from . import animal_visibility_schedule
from . import app_setting
from . import attraction
from . import attraction_animal
from . import attraction_day_seasonal_availability_multiplier
from . import attraction_hours_schedule
from . import attraction_opening_schedule
from . import attraction_schedule_override
from . import defibrillator
from . import drinking_fountain
from . import drinking_fountain_day_seasonal_availability_multiplier
from . import drinking_fountain_status
from . import emergency_intercom
from . import enclosure
from . import enclosure_viewing
from . import event_site
from . import exhibit
from . import exhibit_day_seasonal_availability_multiplier
from . import exhibit_status
from . import gift_shop
from . import gift_shop_day_seasonal_availability_multiplier
from . import gift_shop_opening_schedule
from . import gift_shop_schedule_override
from . import guardians_talk_animal
from . import guardians_talk_cancellation
from . import guardians_talk_occurrence
from . import guardians_talk_schedule
from . import guest_service
from . import itinerary_animal
from . import itinerary_attraction
from . import itinerary_date
from . import itinerary_event
from . import itinerary_event_default
from . import itinerary_exhibit
from . import itinerary_guardians_talk
from . import itinerary_status
from . import itinerary_status_suppression
from . import itinerary_transportation
from . import itinerary_transportation_leg
from . import itinerary_transportation_route_marker
from . import itinerary_walk_route_leg
from . import itinerary_walk_route_point
from . import itinerary_walk_route_stop
from . import itinerary_wild_encounter
from . import legacy_table_drops
from . import meet_the_guardians_talk
from . import pavilion
from . import picnic_site
from . import region
from . import restaurant
from . import restaurant_day_seasonal_availability_multiplier
from . import restaurant_opening_schedule
from . import restaurant_schedule_override
from . import restroom
from . import restroom_alert
from . import restroom_status
from . import transportation
from . import transportation_day_route
from . import transportation_leg
from . import transportation_route
from . import transportation_route_leg
from . import transportation_route_leg_marker
from . import transportation_route_schedule
from . import transportation_route_station
from . import transportation_station
from . import transportation_station_status
from . import wild_encounter
from . import wild_encounter_cancellation
from . import wild_encounter_meeting_spot
from . import wild_encounter_schedule
from . import zoo_event
from . import zoo_hours
from . import zoo_update


static_tables = [
   region,
   exhibit,
   exhibit_day_seasonal_availability_multiplier,
   animal,
   enclosure,
   enclosure_viewing,
   animal_day_seasonal_viewability_multiplier,
   pavilion,
   restaurant,
   restaurant_day_seasonal_availability_multiplier,
   restroom,
   gift_shop,
   gift_shop_day_seasonal_availability_multiplier,
   itinerary_event_default,
   itinerary_status,
   attraction,
   attraction_animal,
   attraction_day_seasonal_availability_multiplier,
   transportation,
   transportation_station,
   transportation_route,
   transportation_route_station,
   transportation_day_route,
   transportation_leg,
   transportation_route_leg,
   transportation_route_leg_marker,
   meet_the_guardians_talk,
   guardians_talk_animal,
   wild_encounter_meeting_spot,
   wild_encounter,
   drinking_fountain_day_seasonal_availability_multiplier,
   drinking_fountain,
   defibrillator,
   emergency_intercom,
   guest_service,
   picnic_site,
   event_site,
   zoo_hours,
]

runtime_tables = [
   legacy_table_drops,
   animal_status,
   animal_visibility_schedule,
   animal_viewing_alert,
   exhibit_status,
   restroom_status,
   restroom_alert,
   zoo_event,
   zoo_update,
   restaurant_opening_schedule,
   restaurant_schedule_override,
   gift_shop_opening_schedule,
   gift_shop_schedule_override,
   app_setting,
   attraction_opening_schedule,
   attraction_hours_schedule,
   attraction_schedule_override,
   transportation_route_schedule,
   transportation_station_status,
   guardians_talk_schedule,
   guardians_talk_cancellation,
   guardians_talk_occurrence,
   wild_encounter_schedule,
   wild_encounter_cancellation,
   drinking_fountain_status,
   itinerary_status_suppression,
   itinerary_date,
   itinerary_exhibit,
   itinerary_animal,
   itinerary_attraction,
   itinerary_transportation,
   itinerary_transportation_leg,
   itinerary_transportation_route_marker,
   itinerary_guardians_talk,
   itinerary_wild_encounter,
   itinerary_event,
   itinerary_walk_route_stop,
   itinerary_walk_route_point,
   itinerary_walk_route_leg,
]
