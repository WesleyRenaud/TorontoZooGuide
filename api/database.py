import sqlite3
from datetime import date, datetime, timedelta

from . import zoo


################################################################################

class Database():
   def __init__( self, db_path='animals.db' ):
      self.conn = sqlite3.connect( db_path )
      self.conn.row_factory = sqlite3.Row


   def close( self ):
      if self.conn is None:
         return

      self.conn.close()
      self.conn = None


   def get_animals_viewable_on_day(
         self,
         day,
         month,
         year,
         temp=None,
         include_off_display_animals=False,
         threshold=0,
         exhibits_to_include=None ):
      from .animals.controllers.animal_controller import AnimalController

      return AnimalController( self.conn ).get_animals_viewable_on_day(
         day=day,
         month=month,
         year=year,
         temp=temp,
         include_off_display_animals=include_off_display_animals,
         threshold=threshold,
         exhibits_to_include=exhibits_to_include )


   def get_exhibits_in_region( self, region ):
      from .exhibits.controllers.exhibit_controller import ExhibitController

      return ExhibitController( self.conn ).get_exhibits_in_region(
         region=region )


   def get_regions( self ):
      from .exhibits.controllers.exhibit_controller import ExhibitController

      return ExhibitController( self.conn ).get_regions()


   def get_names_of_animals_in_exhibit( self, exhibit ):
      from .exhibits.controllers.exhibit_controller import ExhibitController

      return ExhibitController( self.conn ).get_names_of_animals_in_exhibit(
         exhibit=exhibit )


   def get_animal_information( self, species ):
      from .animals.controllers.animal_controller import AnimalController

      return AnimalController( self.conn ).get_animal_information(
         species=species )


   def get_pavilions( self ):
      from .pavilions.controllers.pavilion_controller import PavilionController

      return PavilionController( self.conn ).get_pavilions()


   def get_restaurants( self, day, month, year, include_closed_restaurants, restaurants_to_include=[] ):
      from .restaurants.controllers.restaurant_controller import RestaurantController

      return RestaurantController( self.conn ).get_restaurants(
         day=day,
         month=month,
         year=year,
         include_closed_restaurants=include_closed_restaurants,
         restaurants_to_include=restaurants_to_include )


   def get_restrooms( self, day, month, year, include_closed_restrooms=False ):
      from .restrooms.controllers.restroom_controller import RestroomController

      return RestroomController( self.conn ).get_restrooms(
         day=day,
         month=month,
         year=year,
         include_closed_restrooms=include_closed_restrooms )


   def get_gift_shops( self, day, month, year, include_closed_gift_shops, gift_shops_to_include=[] ):
      from .giftshops.controllers.gift_shop_controller import GiftShopController

      return GiftShopController( self.conn ).get_gift_shops(
         day=day,
         month=month,
         year=year,
         include_closed_gift_shops=include_closed_gift_shops,
         gift_shops_to_include=gift_shops_to_include )


   def get_attractions( self, day, month, year, include_closed_attractions=False ):
      from .attractions.controllers.attraction_controller import AttractionController

      return AttractionController( self.conn ).get_attractions(
         day=day,
         month=month,
         year=year,
         include_closed_attractions=include_closed_attractions )


   def get_zoomobile_stations( self, route, day, month, year, zoomobile_stations_to_include=None ):
      from .zoomobile.controllers.zoomobile_controller import ZoomobileController

      return ZoomobileController( self.conn ).get_zoomobile_stations(
         route=route,
         day=day,
         month=month,
         year=year,
         zoomobile_stations_to_include=zoomobile_stations_to_include )


   def get_zoomobile_route( self, route, day, month, year, zoomobile_stations_to_include=None ):
      from .zoomobile.controllers.zoomobile_controller import ZoomobileController

      return ZoomobileController( self.conn ).get_zoomobile_route(
         route=route,
         day=day,
         month=month,
         year=year,
         zoomobile_stations_to_include=zoomobile_stations_to_include )


   def get_active_zoomobile_route( self, target_date ):
      from .zoomobile.controllers.zoomobile_controller import ZoomobileController

      return ZoomobileController( self.conn ).get_active_zoomobile_route(
         target_date=target_date )


   def get_zoomobile_day_route( self, month, day ):
      from .zoomobile.controllers.zoomobile_controller import ZoomobileController

      return ZoomobileController( self.conn ).get_zoomobile_day_route(
         month=month,
         day=day )


   def get_guardians_talk_details( self, guardians_talks_to_include=None ):
      from .guardians.controllers.guardians_controller import GuardiansController

      return GuardiansController( self.conn ).get_guardians_talk_details(
         guardians_talks_to_include=guardians_talks_to_include )


   def get_guardians_talk_schedule( self, month, day, year ):
      from .guardians.controllers.guardians_controller import GuardiansController

      return GuardiansController( self.conn ).get_guardians_talk_schedule(
         month,
         day,
         year )


   def get_guardians_talk_on_day_schedule(
         self,
         month,
         day,
         talk_name,
         year,
         day_schedule=None ):
      from .guardians.controllers.guardians_controller import GuardiansController

      return GuardiansController( self.conn ).get_guardians_talk_on_day_schedule(
         month=month,
         day=day,
         talk_name=talk_name,
         year=year,
         day_schedule=day_schedule )


   def get_wild_encounter_details( self, wild_encounters_to_include=None ):
      from .wild_encounters.controllers.wild_encounter_controller import WildEncounterController

      return WildEncounterController( self.conn ).get_wild_encounter_details(
         wild_encounters_to_include=wild_encounters_to_include )


   def get_wild_encounter_schedule( self, month, day, year ):
      from .wild_encounters.controllers.wild_encounter_controller import WildEncounterController

      return WildEncounterController( self.conn ).get_wild_encounter_schedule(
         month=month,
         day=day,
         year=year )


   def get_wild_encounter_on_day_schedule(
         self,
         month,
         day,
         encounter_name,
         year,
         day_schedule=None ):
      from .wild_encounters.controllers.wild_encounter_controller import WildEncounterController

      return WildEncounterController( self.conn ).get_wild_encounter_on_day_schedule(
         month=month,
         day=day,
         encounter_name=encounter_name,
         year=year,
         day_schedule=day_schedule )


   def get_available_wild_encounters( self, month, day, year ):
      from .wild_encounters.controllers.wild_encounter_controller import WildEncounterController

      return WildEncounterController( self.conn ).get_available_wild_encounters(
         month=month,
         day=day,
         year=year )


   def get_drinking_fountains( self, day, month, year ):
      from .drinking_fountains.controllers.drinking_fountain_controller import DrinkingFountainController

      return DrinkingFountainController( self.conn ).get_drinking_fountains(
         month=month,
         day=day,
         year=year )


   def get_defibrillators( self ):
      from .defibrillators.controllers.defibrillator_controller import DefibrillatorController

      return DefibrillatorController( self.conn ).get_defibrillators()


   def get_emergency_intercoms( self ):
      from .emergency_intercoms.controllers.emergency_intercom_controller import EmergencyIntercomController

      return EmergencyIntercomController( self.conn ).get_emergency_intercoms()


   def get_guest_services( self ):
      from .guest_services.controllers.guest_service_controller import GuestServiceController

      return GuestServiceController( self.conn ).get_guest_services()


   def get_picnic_sites( self ):
      from .picnic_sites.controllers.picnic_site_controller import PicnicSiteController

      return PicnicSiteController( self.conn ).get_picnic_sites()


   def get_event_sites( self ):
      from .event_sites.controllers.event_site_controller import EventSiteController

      return EventSiteController( self.conn ).get_event_sites()


   def get_updates_for_visit_date( self, month=None, day=None, year=None ):
      from .updates.controllers.update_controller import UpdateController

      return UpdateController( self.conn ).get_updates_for_visit_date(
         month=month,
         day=day,
         year=year )


   def get_unexpired_updates( self ):
      from .updates.controllers.update_controller import UpdateController

      return UpdateController( self.conn ).get_unexpired_updates()


   def get_closed_exhibits( self, month, day, year=None ):
      from .exhibits.controllers.exhibit_controller import ExhibitController

      return ExhibitController( self.conn ).get_closed_exhibits_for_visit_date(
         month=month,
         day=day,
         year=year )


   def get_animals_matching_query(
         self,
         query,
         day,
         month,
         year,
         temp=None,
         include_off_display_animals=False ):
      from .animals.controllers.animal_controller import AnimalController

      return AnimalController( self.conn ).get_animals_matching_query(
         query=query,
         day=day,
         month=month,
         year=year,
         temp=temp,
         include_off_display_animals=include_off_display_animals )


   def get_pavilions_matching_query( self, query ):
      from .pavilions.controllers.pavilion_controller import PavilionController

      return PavilionController( self.conn ).get_pavilions_matching_query(
         query=query )


   def get_restaurants_matching_query( self, query, day, month, year, include_closed_restaurants ):
      from .restaurants.controllers.restaurant_controller import RestaurantController

      return RestaurantController( self.conn ).get_restaurants_matching_query(
         query=query,
         day=day,
         month=month,
         year=year,
         include_closed_restaurants=include_closed_restaurants )


   def get_restrooms_matching_query( self, query, day, month, year, include_closed_restrooms ):
      from .restrooms.controllers.restroom_controller import RestroomController

      return RestroomController( self.conn ).get_restrooms_matching_query(
         query=query,
         day=day,
         month=month,
         year=year,
         include_closed_restrooms=include_closed_restrooms )


   def get_gift_shops_matching_query( self, query, day, month, year ):
      from .giftshops.controllers.gift_shop_controller import GiftShopController

      return GiftShopController( self.conn ).get_gift_shops_matching_query(
         query=query,
         day=day,
         month=month,
         year=year )


   def get_attractions_matching_query( self, query, day, month, year, include_closed_attractions ):
      from .attractions.controllers.attraction_controller import AttractionController

      return AttractionController( self.conn ).get_attractions_matching_query(
         query=query,
         day=day,
         month=month,
         year=year,
         include_closed_attractions=include_closed_attractions )


   def get_zoomobile_stations_matching_query( self, query, route, day, month, year ):
      from .zoomobile.controllers.zoomobile_controller import ZoomobileController

      return ZoomobileController( self.conn ).get_zoomobile_stations_matching_query(
         query=query,
         route=route,
         day=day,
         month=month,
         year=year )


   def get_guardians_talks_matching_query( self, query, month, day, year ):
      from .guardians.controllers.guardians_controller import GuardiansController

      return GuardiansController( self.conn ).get_guardians_talks_matching_query(
         query=query,
         month=month,
         day=day,
         year=year )


   def get_wild_encounters_matching_query( self, query, month, day, year ):
      from .wild_encounters.controllers.wild_encounter_controller import WildEncounterController

      return WildEncounterController( self.conn ).get_wild_encounters_matching_query(
         query=query,
         month=month,
         day=day,
         year=year )


   def get_animal_species_names( self ):
      from .animals.controllers.animal_controller import AnimalController

      return AnimalController( self.conn ).get_animal_species_names()


   def get_itinerary( self ):
      from .itinerary.controllers.itinerary_controller import ItineraryController

      return ItineraryController( self.conn ).get_itinerary()


   def get_zoo_hours( self, day, month, year ):
      from .zoo_hours.controllers.zoo_hours_controller import ZooHoursController

      return ZooHoursController( self.conn ).get_zoo_hours(
         day=day,
         month=month,
         year=year )


   def set_itinerary(
         self,
         date,
         animals,
         attractions,
         guardians_talks,
         wild_encounters ):
      from .itinerary.controllers.itinerary_controller import ItineraryController

      return ItineraryController( self.conn ).set_itinerary(
         date=date,
         animals=animals,
         attractions=attractions,
         guardians_talks=guardians_talks,
         wild_encounters=wild_encounters )


   def clear_itinerary( self ):
      from .itinerary.controllers.itinerary_controller import ItineraryController

      return ItineraryController( self.conn ).clear_itinerary()


   def accept_itinerary( self ):
      from .itinerary.controllers.itinerary_controller import ItineraryController

      return ItineraryController( self.conn ).accept_itinerary()


   def get_regions_with_exhibits( self ):
      from .exhibits.controllers.exhibit_controller import ExhibitController

      return ExhibitController( self.conn ).get_regions_with_exhibits()


   def get_exhibits( self ):
      from .exhibits.controllers.exhibit_controller import ExhibitController

      return ExhibitController( self.conn ).get_exhibits()


   def get_restaurant_names( self ):
      from .restaurants.controllers.restaurant_controller import RestaurantController

      return RestaurantController( self.conn ).get_restaurant_names()


   def get_restroom_names( self ):
      from .restrooms.controllers.restroom_controller import RestroomController

      return RestroomController( self.conn ).get_restroom_names()


   def get_gift_shop_names( self ):
      from .giftshops.controllers.gift_shop_controller import GiftShopController

      return GiftShopController( self.conn ).get_gift_shop_names()


   def get_attraction_names( self ):
      from .attractions.controllers.attraction_controller import AttractionController

      return AttractionController( self.conn ).get_attraction_names()


   def get_zoomobile_station_names( self ):
      from .zoomobile.controllers.zoomobile_controller import ZoomobileController

      return ZoomobileController( self.conn ).get_zoomobile_station_names()


   def get_guardians_talk_locations( self ):
      from .guardians.controllers.guardians_controller import GuardiansController

      return GuardiansController( self.conn ).get_guardians_talk_locations()


   def get_guardians_talk_names( self ):
      from .guardians.controllers.guardians_controller import GuardiansController

      return GuardiansController( self.conn ).get_guardians_talk_names()


   def get_guardians_talk_names_at_location( self, location ):
      from .guardians.controllers.guardians_controller import GuardiansController

      return GuardiansController( self.conn ).get_guardians_talk_names_at_location(
         location=location )


   def get_guardians_talk_occurrences( self, talk, location, days_ahead=60 ):
      from .guardians.controllers.guardians_controller import GuardiansController

      return GuardiansController( self.conn ).get_guardians_talk_occurrences(
         talk=talk,
         location=location,
         days_ahead=days_ahead )


   def get_wild_encounter_names( self ):
      from .wild_encounters.controllers.wild_encounter_controller import WildEncounterController

      return WildEncounterController( self.conn ).get_wild_encounter_names()


   def get_wild_encounter_occurrences( self, wild_encounter, days_ahead=60 ):
      from .wild_encounters.controllers.wild_encounter_controller import WildEncounterController

      return WildEncounterController( self.conn ).get_wild_encounter_occurrences(
         wild_encounter=wild_encounter,
         days_ahead=days_ahead )


   def set_animal_as_off_display( self, species, exhibit, start_date, end_date, message ):
      from .animals.controllers.animal_controller import AnimalController

      return AnimalController( self.conn ).set_animal_as_off_display(
         species=species,
         exhibit=exhibit,
         start_date=start_date,
         end_date=end_date,
         message=message )


   def set_animal_as_on_display( self, species, exhibit ):
      from .animals.controllers.animal_controller import AnimalController

      return AnimalController( self.conn ).set_animal_as_on_display(
         species=species,
         exhibit=exhibit )


   def set_animal_limited_viewing_schedule( self, species, exhibit, start_date, end_date, daily_start_time,
                                            daily_end_time, message ):
      from .animals.controllers.animal_controller import AnimalController

      return AnimalController( self.conn ).set_animal_limited_viewing_schedule(
         species=species,
         exhibit=exhibit,
         start_date=start_date,
         end_date=end_date,
         daily_start_time=daily_start_time,
         daily_end_time=daily_end_time,
         message=message )


   def remove_animal_visibility_schedule( self, species, exhibit ):
      from .animals.controllers.animal_controller import AnimalController

      return AnimalController( self.conn ).remove_animal_visibility_schedule(
         species=species,
         exhibit=exhibit )


   def set_animal_viewing_alert( self, species, exhibit, alert_start_date, alert_end_date, message ):
      from .animals.controllers.animal_controller import AnimalController

      return AnimalController( self.conn ).set_animal_viewing_alert(
         species=species,
         exhibit=exhibit,
         alert_start_date=alert_start_date,
         alert_end_date=alert_end_date,
         message=message )


   def remove_animal_viewing_alert( self, species, exhibit ):
      from .animals.controllers.animal_controller import AnimalController

      return AnimalController( self.conn ).remove_animal_viewing_alert(
         species=species,
         exhibit=exhibit )


   def set_exhibit_as_closed( self, exhibit, start_date, end_date, message ):
      from .exhibits.controllers.exhibit_controller import ExhibitController

      return ExhibitController( self.conn ).set_exhibit_as_closed(
         exhibit=exhibit,
         start_date=start_date,
         end_date=end_date,
         message=message )


   def set_exhibit_as_open( self, exhibit, start_date, end_date ):
      from .exhibits.controllers.exhibit_controller import ExhibitController

      return ExhibitController( self.conn ).set_exhibit_as_open(
         exhibit=exhibit,
         start_date=start_date,
         end_date=end_date )


   def set_restroom_as_closed( self, restroom, start_date, end_date, message ):
      from .restrooms.controllers.restroom_controller import RestroomController

      return RestroomController( self.conn ).set_restroom_as_closed(
         restroom=restroom,
         start_date=start_date,
         end_date=end_date,
         message=message )


   def set_restroom_as_open( self, restroom, start_date, end_date ):
      from .restrooms.controllers.restroom_controller import RestroomController

      return RestroomController( self.conn ).set_restroom_as_open(
         restroom=restroom,
         start_date=start_date,
         end_date=end_date )


   def set_restroom_alert( self, restroom, alert_start_date, alert_end_date, message ):
      from .restrooms.controllers.restroom_controller import RestroomController

      return RestroomController( self.conn ).set_restroom_alert(
         restroom=restroom,
         alert_start_date=alert_start_date,
         alert_end_date=alert_end_date,
         message=message )


   def remove_restroom_alert( self, restroom ):
      from .restrooms.controllers.restroom_controller import RestroomController

      return RestroomController( self.conn ).remove_restroom_alert(
         restroom=restroom )


   def normalize_update_type( self, update_type ):
      from .updates.logic.update_type import normalize_update_type

      return normalize_update_type( update_type )


   def create_update( self, title, description, update_type, start_date, end_date ):
      from .updates.controllers.update_controller import UpdateController

      return UpdateController( self.conn ).create_update(
         title=title,
         description=description,
         update_type=update_type,
         start_date=start_date,
         end_date=end_date )


   def end_update( self, title, start_date, end_date ):
      from .updates.controllers.update_controller import UpdateController

      return UpdateController( self.conn ).end_update(
         title=title,
         start_date=start_date,
         end_date=end_date )


   def edit_update(
         self,
         title,
         start_date,
         description,
         update_type,
         end_date ):
      from .updates.controllers.update_controller import UpdateController

      return UpdateController( self.conn ).edit_update(
         title=title,
         start_date=start_date,
         description=description,
         update_type=update_type,
         end_date=end_date )


   def set_restaurant_as_closed( self, restaurant, start_date, end_date, message ):
      from .restaurants.controllers.restaurant_controller import RestaurantController

      return RestaurantController( self.conn ).set_restaurant_as_closed(
         restaurant=restaurant,
         start_date=start_date,
         end_date=end_date,
         message=message )


   def set_restaurant_opening_schedule(
         self,
         restaurant,
         start_date,
         end_date,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         holidays_only,
         message ):
      from .restaurants.controllers.restaurant_controller import RestaurantController

      return RestaurantController( self.conn ).set_restaurant_opening_schedule(
         restaurant=restaurant,
         start_date=start_date,
         end_date=end_date,
         monday=monday,
         tuesday=tuesday,
         wednesday=wednesday,
         thursday=thursday,
         friday=friday,
         saturday=saturday,
         sunday=sunday,
         holidays_only=holidays_only,
         message=message )


   def set_gift_shop_as_closed( self, gift_shop, start_date, end_date, message ):
      from .giftshops.controllers.gift_shop_controller import GiftShopController

      return GiftShopController( self.conn ).set_gift_shop_as_closed(
         gift_shop=gift_shop,
         start_date=start_date,
         end_date=end_date,
         message=message )


   def set_gift_shop_opening_schedule(
         self,
         gift_shop,
         start_date,
         end_date,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         holidays_only,
         message ):
      from .giftshops.controllers.gift_shop_controller import GiftShopController

      return GiftShopController( self.conn ).set_gift_shop_opening_schedule(
         gift_shop=gift_shop,
         start_date=start_date,
         end_date=end_date,
         monday=monday,
         tuesday=tuesday,
         wednesday=wednesday,
         thursday=thursday,
         friday=friday,
         saturday=saturday,
         sunday=sunday,
         holidays_only=holidays_only,
         message=message )


   def set_attraction_as_closed( self, attraction, start_date, end_date, message ):
      from .attractions.controllers.attraction_controller import AttractionController

      return AttractionController( self.conn ).set_attraction_as_closed(
         attraction=attraction,
         start_date=start_date,
         end_date=end_date,
         message=message )


   def set_attraction_opening_schedule(
         self,
         attraction,
         start_date,
         end_date,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         holidays_only,
         message ):
      from .attractions.controllers.attraction_controller import AttractionController

      return AttractionController( self.conn ).set_attraction_opening_schedule(
         attraction=attraction,
         start_date=start_date,
         end_date=end_date,
         monday=monday,
         tuesday=tuesday,
         wednesday=wednesday,
         thursday=thursday,
         friday=friday,
         saturday=saturday,
         sunday=sunday,
         holidays_only=holidays_only,
         message=message )


   def set_zoomobile_station_as_closed( self, zoomobile_station, start_date, end_date, message ):
      from .zoomobile.controllers.zoomobile_controller import ZoomobileController

      return ZoomobileController( self.conn ).set_zoomobile_station_as_closed(
         zoomobile_station=zoomobile_station,
         start_date=start_date,
         end_date=end_date,
         message=message )


   def set_zoomobile_station_as_open( self, zoomobile_station ):
      from .zoomobile.controllers.zoomobile_controller import ZoomobileController

      return ZoomobileController( self.conn ).set_zoomobile_station_as_open(
         zoomobile_station=zoomobile_station )


   def set_current_zoomobile_route( self, route, start_date, end_date ):
      from .zoomobile.controllers.zoomobile_controller import ZoomobileController

      return ZoomobileController( self.conn ).set_current_zoomobile_route(
         route=route,
         start_date=start_date,
         end_date=end_date )


   def set_guardians_talk_schedule(
         self,
         talk,
         location,
         start_date,
         end_date,
         talk_time,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         message ):
      from .guardians.controllers.guardians_controller import GuardiansController

      return GuardiansController( self.conn ).set_guardians_talk_schedule(
         talk=talk,
         location=location,
         start_date=start_date,
         end_date=end_date,
         talk_time=talk_time,
         monday=monday,
         tuesday=tuesday,
         wednesday=wednesday,
         thursday=thursday,
         friday=friday,
         saturday=saturday,
         sunday=sunday,
         message=message )


   def end_guardians_talk_schedule( self, talk, location, schedule_end_date ):
      from .guardians.controllers.guardians_controller import GuardiansController

      return GuardiansController( self.conn ).end_guardians_talk_schedule(
         talk=talk,
         location=location,
         schedule_end_date=schedule_end_date )


   def cancel_guardians_talk_occurrence( self, talk, location, date, time ):
      from .guardians.controllers.guardians_controller import GuardiansController

      return GuardiansController( self.conn ).cancel_guardians_talk_occurrence(
         talk=talk,
         location=location,
         date=date,
         time=time )


   def set_wild_encounter_schedule(
         self,
         wild_encounter,
         start_date,
         end_date,
         encounter_time,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         message ):
      from .wild_encounters.controllers.wild_encounter_controller import WildEncounterController

      return WildEncounterController( self.conn ).set_wild_encounter_schedule(
         wild_encounter=wild_encounter,
         start_date=start_date,
         end_date=end_date,
         encounter_time=encounter_time,
         monday=monday,
         tuesday=tuesday,
         wednesday=wednesday,
         thursday=thursday,
         friday=friday,
         saturday=saturday,
         sunday=sunday,
         message=message )


   def end_wild_encounter_schedule( self, wild_encounter, schedule_end_date ):
      from .wild_encounters.controllers.wild_encounter_controller import WildEncounterController

      return WildEncounterController( self.conn ).end_wild_encounter_schedule(
         wild_encounter=wild_encounter,
         schedule_end_date=schedule_end_date )


   def cancel_wild_encounter_occurrence( self, wild_encounter, date, time ):
      from .wild_encounters.controllers.wild_encounter_controller import WildEncounterController

      return WildEncounterController( self.conn ).cancel_wild_encounter_occurrence(
         wild_encounter=wild_encounter,
         date=date,
         time=time )


   def set_drinking_fountains_as_closed( self, start_date=None, end_date=None, message=None ):
      from .drinking_fountains.controllers.drinking_fountain_controller import DrinkingFountainController

      return DrinkingFountainController( self.conn ).set_drinking_fountains_as_closed(
         start_date=start_date,
         end_date=end_date,
         message=message )


   def set_drinking_fountains_as_open( self, start_date=None, end_date=None ):
      from .drinking_fountains.controllers.drinking_fountain_controller import DrinkingFountainController

      return DrinkingFountainController( self.conn ).set_drinking_fountains_as_open(
         start_date=start_date,
         end_date=end_date )
