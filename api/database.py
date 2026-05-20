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
      if not title or not start_date:
         return False

      if not end_date:
         end_date = datetime.now().date().isoformat()

      try:
         parsed_end_date = zoo.ZooUtil.parse_date_value( end_date )
      except ValueError:
         return False

      cur = self.conn.cursor()
      cur.execute(
         """   UPDATE ZooUpdate
               SET END_DATE = ?
               WHERE TITLE = ?
                  AND START_DATE = ?;
         """,
         (
            parsed_end_date.isoformat(),
            title,
            start_date
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def edit_update( self, title, start_date, description=None, update_type=None, end_date=None ):
      if not title or not start_date:
         return False

      parsed_end_date = None
      should_update_end_date = end_date is not None
      normalized_update_type = None

      if update_type:
         normalized_update_type = self.normalize_update_type( update_type )

         if normalized_update_type == None:
            return False

      if should_update_end_date and end_date:
         try:
            parsed_end_date = zoo.ZooUtil.parse_date_value( end_date )
         except ValueError:
            return False

      cur = self.conn.cursor()
      data = cur.execute(
         """   SELECT
                  START_DATE,
                  END_DATE
               FROM ZooUpdate
               WHERE TITLE = ?
                  AND START_DATE = ?;
         """,
         (
            title,
            start_date
         ) )
      current_update = data.fetchone()

      if current_update == None:
         cur.close()
         return False

      current_start_date = zoo.ZooUtil.parse_date_value( current_update[ 'START_DATE' ] )

      if should_update_end_date and parsed_end_date == None:
         next_end_date = None
      else:
         next_end_date = parsed_end_date.isoformat() if parsed_end_date != None else current_update[ 'END_DATE' ]

      if parsed_end_date != None and parsed_end_date < current_start_date:
         cur.close()
         return False

      update_fields = []
      update_values = []

      if description != None and str( description ).strip():
         update_fields.append( 'DESCRIPTION = ?' )
         update_values.append( str( description ).strip() )

      if normalized_update_type != None:
         update_fields.append( 'UPDATE_TYPE = ?' )
         update_values.append( normalized_update_type )

      if should_update_end_date:
         update_fields.append( 'END_DATE = ?' )
         update_values.append( next_end_date )

      if not update_fields:
         cur.close()
         return False

      update_values.extend( [ title, start_date ] )

      cur.execute(
         f"""  UPDATE ZooUpdate
               SET { ', '.join( update_fields ) }
               WHERE TITLE = ?
                  AND START_DATE = ?;
         """,
         tuple( update_values ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_restaurant_as_closed( self, restaurant, start_date, end_date, message ):
      if not restaurant:
         return False

      if not message:
         message = f'The { restaurant } is temporarily closed.'

      return self.set_restaurant_opening_schedule(
         restaurant=restaurant,
         start_date=start_date,
         end_date=end_date,
         monday=False,
         tuesday=False,
         wednesday=False,
         thursday=False,
         friday=False,
         saturday=False,
         sunday=False,
         holidays_only=False,
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
      if not restaurant:
         return False

      if not start_date:
         start_date = datetime.now().date().isoformat()

      if not end_date:
         end_date = None

      if not message:
         message = f'The { restaurant } is not scheduled to be open today.'

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO RestaurantOpeningSchedule (
                  RESTAURANT,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY,
                  HOLIDAYS_ONLY,
                  SCHEDULE_MESSAGE
               )
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(RESTAURANT) DO UPDATE SET
                  SCHEDULE_START_DATE = excluded.SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE = excluded.SCHEDULE_END_DATE,
                  MONDAY = excluded.MONDAY,
                  TUESDAY = excluded.TUESDAY,
                  WEDNESDAY = excluded.WEDNESDAY,
                  THURSDAY = excluded.THURSDAY,
                  FRIDAY = excluded.FRIDAY,
                  SATURDAY = excluded.SATURDAY,
                  SUNDAY = excluded.SUNDAY,
                  HOLIDAYS_ONLY = excluded.HOLIDAYS_ONLY,
                  SCHEDULE_MESSAGE = excluded.SCHEDULE_MESSAGE;
         """,
         (
            restaurant,
            start_date,
            end_date,
            int( bool( monday ) ),
            int( bool( tuesday ) ),
            int( bool( wednesday ) ),
            int( bool( thursday ) ),
            int( bool( friday ) ),
            int( bool( saturday ) ),
            int( bool( sunday ) ),
            int( bool( holidays_only ) ),
            message
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_gift_shop_as_closed( self, gift_shop, start_date, end_date, message ):
      if not gift_shop:
         return False

      if not message:
         message = f'The { gift_shop } is temporarily closed.'

      return self.set_gift_shop_opening_schedule(
         gift_shop=gift_shop,
         start_date=start_date,
         end_date=end_date,
         monday=False,
         tuesday=False,
         wednesday=False,
         thursday=False,
         friday=False,
         saturday=False,
         sunday=False,
         holidays_only=False,
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
      if not gift_shop:
         return False

      if not start_date:
         start_date = datetime.now().date().isoformat()

      if not end_date:
         end_date = None

      if not message:
         message = f'The { gift_shop } is not scheduled to be open today.'

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO GiftShopOpeningSchedule (
                  GIFT_SHOP,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY,
                  HOLIDAYS_ONLY,
                  SCHEDULE_MESSAGE
               )
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(GIFT_SHOP) DO UPDATE SET
                  SCHEDULE_START_DATE = excluded.SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE = excluded.SCHEDULE_END_DATE,
                  MONDAY = excluded.MONDAY,
                  TUESDAY = excluded.TUESDAY,
                  WEDNESDAY = excluded.WEDNESDAY,
                  THURSDAY = excluded.THURSDAY,
                  FRIDAY = excluded.FRIDAY,
                  SATURDAY = excluded.SATURDAY,
                  SUNDAY = excluded.SUNDAY,
                  HOLIDAYS_ONLY = excluded.HOLIDAYS_ONLY,
                  SCHEDULE_MESSAGE = excluded.SCHEDULE_MESSAGE;
         """,
         (
            gift_shop,
            start_date,
            end_date,
            int( bool( monday ) ),
            int( bool( tuesday ) ),
            int( bool( wednesday ) ),
            int( bool( thursday ) ),
            int( bool( friday ) ),
            int( bool( saturday ) ),
            int( bool( sunday ) ),
            int( bool( holidays_only ) ),
            message
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_attraction_as_closed( self, attraction, start_date, end_date, message ):
      if not attraction:
         return False

      if not message:
         message = f'The { attraction } is temporarily closed.'

      return self.set_attraction_opening_schedule(
         attraction=attraction,
         start_date=start_date,
         end_date=end_date,
         monday=False,
         tuesday=False,
         wednesday=False,
         thursday=False,
         friday=False,
         saturday=False,
         sunday=False,
         holidays_only=False,
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
      if not attraction:
         return False

      if not start_date:
         start_date = datetime.now().date().isoformat()

      if not end_date:
         end_date = None

      if not message:
         message = f'The { attraction } is not scheduled to be open today.'

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO AttractionOpeningSchedule (
                  ATTRACTION,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY,
                  HOLIDAYS_ONLY,
                  SCHEDULE_MESSAGE
               )
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(ATTRACTION) DO UPDATE SET
                  SCHEDULE_START_DATE = excluded.SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE = excluded.SCHEDULE_END_DATE,
                  MONDAY = excluded.MONDAY,
                  TUESDAY = excluded.TUESDAY,
                  WEDNESDAY = excluded.WEDNESDAY,
                  THURSDAY = excluded.THURSDAY,
                  FRIDAY = excluded.FRIDAY,
                  SATURDAY = excluded.SATURDAY,
                  SUNDAY = excluded.SUNDAY,
                  HOLIDAYS_ONLY = excluded.HOLIDAYS_ONLY,
                  SCHEDULE_MESSAGE = excluded.SCHEDULE_MESSAGE;
         """,
         (
            attraction,
            start_date,
            end_date,
            int( bool( monday ) ),
            int( bool( tuesday ) ),
            int( bool( wednesday ) ),
            int( bool( thursday ) ),
            int( bool( friday ) ),
            int( bool( saturday ) ),
            int( bool( sunday ) ),
            int( bool( holidays_only ) ),
            message
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_zoomobile_station_as_closed( self, zoomobile_station, start_date, end_date, message ):
      if not zoomobile_station:
         return False

      if not start_date:
         start_date = datetime.now().date().isoformat()

      if not end_date:
         end_date = None

      if not message:
         message = f'The { zoomobile_station } is temporarily closed.'

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO ZoomobileStationStatus (
                  ZOOMOBILE_STATION,
                  IS_CLOSED,
                  CLOSED_MESSAGE,
                  CLOSED_START,
                  CLOSED_END
               )
               VALUES (?, 1, ?, ?, ?)
               ON CONFLICT(ZOOMOBILE_STATION) DO UPDATE SET
                  IS_CLOSED = 1,
                  CLOSED_MESSAGE = excluded.CLOSED_MESSAGE,
                  CLOSED_START = excluded.CLOSED_START,
                  CLOSED_END = excluded.CLOSED_END;
         """, ( zoomobile_station, message, start_date, end_date ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_zoomobile_station_as_open( self, zoomobile_station ):
      if not zoomobile_station:
         return False

      cur = self.conn.cursor()

      cur.execute(
         """   DELETE FROM ZoomobileStationStatus
               WHERE ZOOMOBILE_STATION = ?;
         """, ( zoomobile_station, ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_current_zoomobile_route( self, route, start_date, end_date ):
      if route not in ( 'summer', 'winter' ):
         return False

      try:
         normalized_start_date = (
            zoo.ZooUtil.parse_date_value( value=start_date ).isoformat()
            if start_date
            else datetime.now().date().isoformat()
         )
      except ValueError:
         return False

      normalized_end_date = None

      if end_date:
         try:
            normalized_end_date = zoo.ZooUtil.parse_date_value( value=end_date ).isoformat()
         except ValueError:
            return False

         if normalized_end_date < normalized_start_date:
            return False

      cur = self.conn.cursor()

      cur.execute(
         """   DELETE FROM ZoomobileRouteSchedule;
         """ )

      cur.execute(
         """   INSERT INTO ZoomobileRouteSchedule (
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  ROUTE
               )
               VALUES ( ?, ?, ? )
         """, ( normalized_start_date, normalized_end_date, route ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


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
      if not talk or not location:
         return False

      if not start_date:
         start_date = datetime.now().date().isoformat()

      if not end_date:
         end_date = None

      if not message:
         message = f'The { talk } at { location } is not scheduled today.'

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO GuardiansTalkSchedule (
                  TALK_NAME,
                  LOCATION,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  TALK_TIME,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY,
                  SCHEDULE_MESSAGE
               )
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(TALK_NAME, LOCATION) DO UPDATE SET
                  SCHEDULE_START_DATE = excluded.SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE = excluded.SCHEDULE_END_DATE,
                  TALK_TIME = excluded.TALK_TIME,
                  MONDAY = excluded.MONDAY,
                  TUESDAY = excluded.TUESDAY,
                  WEDNESDAY = excluded.WEDNESDAY,
                  THURSDAY = excluded.THURSDAY,
                  FRIDAY = excluded.FRIDAY,
                  SATURDAY = excluded.SATURDAY,
                  SUNDAY = excluded.SUNDAY,
                  SCHEDULE_MESSAGE = excluded.SCHEDULE_MESSAGE;
         """,
         (
            talk,
            location,
            start_date,
            end_date,
            talk_time,
            int( bool( monday ) ),
            int( bool( tuesday ) ),
            int( bool( wednesday ) ),
            int( bool( thursday ) ),
            int( bool( friday ) ),
            int( bool( saturday ) ),
            int( bool( sunday ) ),
            message
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def end_guardians_talk_schedule( self, talk, location, schedule_end_date ):
      if not talk or not location:
         return False

      if not schedule_end_date:
         schedule_end_date = datetime.now().date().isoformat()

      cur = self.conn.cursor()

      cur.execute(
         """   UPDATE GuardiansTalkSchedule
               SET SCHEDULE_END_DATE = ?
               WHERE TALK_NAME = ?
               AND LOCATION = ?;
         """,
         (
            schedule_end_date,
            talk,
            location
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def cancel_guardians_talk_occurrence( self, talk, location, date, time ):
      if not talk or not location or not date or not time:
         return False

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO GuardiansTalkCancellation (
                  TALK_NAME,
                  LOCATION,
                  CANCELLATION_DATE,
                  TALK_TIME
               )
               VALUES (?, ?, ?, ?)
               ON CONFLICT(TALK_NAME, LOCATION, CANCELLATION_DATE, TALK_TIME)
               DO NOTHING;
         """,
         (
            talk,
            location,
            date,
            time
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


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
      if not wild_encounter:
         return False

      if not start_date:
         start_date = datetime.now().date().isoformat()

      if not end_date:
         end_date = None

      if not message:
         message = f'The { wild_encounter } is not scheduled today.'

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO WildEncounterSchedule (
                  WILD_ENCOUNTER,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  ENCOUNTER_TIME,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY,
                  SCHEDULE_MESSAGE
               )
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(WILD_ENCOUNTER) DO UPDATE SET
                  SCHEDULE_START_DATE = excluded.SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE = excluded.SCHEDULE_END_DATE,
                  ENCOUNTER_TIME = excluded.ENCOUNTER_TIME,
                  MONDAY = excluded.MONDAY,
                  TUESDAY = excluded.TUESDAY,
                  WEDNESDAY = excluded.WEDNESDAY,
                  THURSDAY = excluded.THURSDAY,
                  FRIDAY = excluded.FRIDAY,
                  SATURDAY = excluded.SATURDAY,
                  SUNDAY = excluded.SUNDAY,
                  SCHEDULE_MESSAGE = excluded.SCHEDULE_MESSAGE;
         """,
         (
            wild_encounter,
            start_date,
            end_date,
            encounter_time,
            int( bool( monday ) ),
            int( bool( tuesday ) ),
            int( bool( wednesday ) ),
            int( bool( thursday ) ),
            int( bool( friday ) ),
            int( bool( saturday ) ),
            int( bool( sunday ) ),
            message
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def end_wild_encounter_schedule( self, wild_encounter, schedule_end_date ):
      if not wild_encounter:
         return False

      if not schedule_end_date:
         schedule_end_date = datetime.now().date().isoformat()

      cur = self.conn.cursor()

      cur.execute(
         """   UPDATE WildEncounterSchedule
               SET SCHEDULE_END_DATE = ?
               WHERE WILD_ENCOUNTER = ?;
         """,
         (
            schedule_end_date,
            wild_encounter
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def cancel_wild_encounter_occurrence( self, wild_encounter, date, time ):
      if not wild_encounter or not date or not time:
         return False

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO WildEncounterCancellation (
                  WILD_ENCOUNTER,
                  CANCELLATION_DATE,
                  ENCOUNTER_TIME
               )
               VALUES (?, ?, ?)
               ON CONFLICT(WILD_ENCOUNTER, CANCELLATION_DATE, ENCOUNTER_TIME)
               DO NOTHING;
         """,
         (
            wild_encounter,
            date,
            time
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_drinking_fountains_as_closed( self, start_date=None, end_date=None, message=None ):
      if not message:
         message = 'The drinking fountains are closed for the season.'

      cur = self.conn.cursor()

      cur.execute(
         """ DELETE FROM DrinkingFountainStatus;
         """ )

      cur.execute(
         """   INSERT INTO DrinkingFountainStatus (
                  IS_CLOSED,
                  START_DATE,
                  END_DATE,
                  CLOSED_MESSAGE
               )
               VALUES (1, ?, ?, ?);
         """, (
            start_date,
            end_date,
            message
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_drinking_fountains_as_open( self, start_date=None, end_date=None ):
      cur = self.conn.cursor()

      cur.execute(
         """ DELETE FROM DrinkingFountainStatus;
         """ )

      cur.execute(
         """   INSERT INTO DrinkingFountainStatus (
                  IS_CLOSED,
                  START_DATE,
                  END_DATE,
                  CLOSED_MESSAGE
               )
               VALUES (0, ?, ?, NULL);
         """, (
            start_date,
            end_date
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0
