from __future__ import annotations

from collections.abc import Callable
from datetime import date

import pytest

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.attractions.data_access.attraction import fetch_attraction_schedule_override_records
from api.attractions.data_access.attraction import fetch_attraction_schedule_records
from api.attractions.data_access.attraction_schedule_record import AttractionScheduleRecord
from api.attractions.logic.attraction import get_active_attraction_schedule_status
from api.defibrillators.coordinators.defibrillator_coordinator import DefibrillatorCoordinator
from api.drinking_fountains.coordinators.drinking_fountain_coordinator import DrinkingFountainCoordinator
from api.emergency_intercoms.coordinators.emergency_intercom_coordinator import EmergencyIntercomCoordinator
from api.event_sites.coordinators.event_site_coordinator import EventSiteCoordinator
from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator
from api.giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
from api.giftshops.data_access.gift_shop import fetch_gift_shop_schedule_override_records
from api.giftshops.data_access.gift_shop import fetch_gift_shop_schedule_records
from api.giftshops.data_access.gift_shop_schedule_record import GiftShopScheduleRecord
from api.giftshops.logic.gift_shop import get_active_gift_shop_schedule_status
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.guest_services.coordinators.guest_service_coordinator import GuestServiceCoordinator
from api.pavilions.coordinators.pavilion_coordinator import PavilionCoordinator
from api.picnic_sites.coordinators.picnic_site_coordinator import PicnicSiteCoordinator
from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from api.restaurants.data_access.restaurant import fetch_restaurant_schedule_override_records
from api.restaurants.data_access.restaurant import fetch_restaurant_schedule_records
from api.restaurants.data_access.restaurant_schedule_record import RestaurantScheduleRecord
from api.restaurants.logic.restaurant import get_active_restaurant_schedule_status
from api.restrooms.coordinators.restroom_coordinator import RestroomCoordinator
from api.shared.enums import ScheduleStatus
from api.types import Connection, Cursor
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from api.zoomobile.coordinators.zoomobile_coordinator import ZoomobileCoordinator
from conftest import DbControllers


AmenityScheduleRecord = (
   AttractionScheduleRecord
   | GiftShopScheduleRecord
   | RestaurantScheduleRecord
)


def apply_amenity_opening_schedule(
      db: DbControllers,
      setter_name: str,
      schedule: dict[ str, object ] ) -> bool:
   if setter_name == 'set_restaurant_opening_schedule':
      return RestaurantCoordinator.set_restaurant_opening_schedule( **schedule )

   if setter_name == 'set_gift_shop_opening_schedule':
      return GiftShopCoordinator.set_gift_shop_opening_schedule( **schedule )

   if setter_name == 'set_attraction_opening_schedule':
      return AttractionCoordinator.set_attraction_opening_schedule( **schedule )

   raise AssertionError( setter_name )


def get_amenity_schedule_status(
      db: DbControllers,
      method_name: str,
      item_name: str,
      target_date: date,
      weekday: int ) -> tuple[ ScheduleStatus, str | None ]:

   if method_name == 'get_active_restaurant_schedule_status':
      return get_active_restaurant_schedule_status(
         schedule_records=[
            schedule_record
            for schedule_record in fetch_restaurant_schedule_records( db.conn )
            if schedule_record.restaurant == item_name
         ],
         target_date=target_date,
         weekday=weekday )

   if method_name == 'get_active_gift_shop_schedule_status':
      return get_active_gift_shop_schedule_status(
         schedule_records=[
            schedule_record
            for schedule_record in fetch_gift_shop_schedule_records( db.conn )
            if schedule_record.gift_shop == item_name
         ],
         target_date=target_date,
         weekday=weekday )

   return get_active_attraction_schedule_status(
      schedule_records=[
         schedule_record
         for schedule_record in fetch_attraction_schedule_records( db.conn )
         if schedule_record.attraction == item_name
      ],
      attraction_name=item_name,
      target_date=target_date,
      weekday=weekday )


def test_region_and_static_location_queries( db: DbControllers ) -> None:
   regions = ExhibitCoordinator.get_regions()

   assert [
      region.to_dict()
      for region in regions
   ] == [
      { 'name': 'Africa', 'hasExhibits': True },
      { 'name': 'Americas', 'hasExhibits': True },
      { 'name': 'Australasia', 'hasExhibits': True },
      { 'name': 'Canadian Domain', 'hasExhibits': False },
      { 'name': 'Discovery Zone', 'hasExhibits': True },
      { 'name': 'Eurasia Wilds', 'hasExhibits': False },
      { 'name': 'Indo-Malaya', 'hasExhibits': True },
      { 'name': 'Tundra Trek', 'hasExhibits': False }
   ]

   assert ExhibitCoordinator.get_exhibits_in_region( 'Africa' ) == [
      'Africa Savanna',
      'African Rainforest Pavilion'
   ]
   assert ExhibitCoordinator.get_exhibits() == [
      'Africa Savanna',
      'African Rainforest Pavilion',
      'Americas Outdoor Mayan Temple Ruins',
      'Americas Pavilion',
      'Australasia Outdoor',
      'Australasia Pavilion',
      'Canadian Domain',
      'Eurasia Wilds',
      'Goat World',
      'Indo-Malaya Outdoor',
      'Indo-Malaya Pavilion',
      'Kids Zoo',
      'Malayan Woods Pavilion',
      'Tundra Trek'
   ]

   region_exhibits = ExhibitCoordinator.get_regions_with_exhibits()
   africa = next(
      region for region in region_exhibits
      if region.name == 'Africa'
   )
   assert africa.exhibits == [
      'Africa Savanna',
      'African Rainforest Pavilion'
   ]

   pavilions = {
      pavilion.name: pavilion
      for pavilion in PavilionCoordinator.get_pavilions()
   }
   restrooms = {
      restroom.title: restroom
      for restroom in RestroomCoordinator.get_restrooms( day=15, month='June', year=2026 )
   }
   drinking_fountains = DrinkingFountainCoordinator.get_drinking_fountains( day=15, month='June', year=2026 )

   assert pavilions[ 'African Rainforest Pavilion' ].region == 'Africa'
   assert 'Entrance Restroom' in restrooms
   assert 'Africa Restaurant Restroom' in restrooms
   assert len( drinking_fountains ) > 0
   assert all( 0 <= drinking_fountain.x_coord <= 100 for drinking_fountain in drinking_fountains )
   assert all( 0 <= drinking_fountain.y_coord <= 100 for drinking_fountain in drinking_fountains )
   assert all( drinking_fountain.is_closed is False for drinking_fountain in drinking_fountains )


def test_defibrillators_have_coordinates( db: DbControllers ) -> None:
   defibrillators = DefibrillatorCoordinator.get_defibrillators()

   assert len( defibrillators ) > 0
   assert all( 0 <= defibrillator.x_coord <= 100 for defibrillator in defibrillators )
   assert all( 0 <= defibrillator.y_coord <= 100 for defibrillator in defibrillators )


def test_emergency_intercoms_have_coordinates( db: DbControllers ) -> None:
   emergency_intercoms = EmergencyIntercomCoordinator.get_emergency_intercoms()

   assert len( emergency_intercoms ) > 0
   assert all( 0 <= emergency_intercom.x_coord <= 100 for emergency_intercom in emergency_intercoms )
   assert all( 0 <= emergency_intercom.y_coord <= 100 for emergency_intercom in emergency_intercoms )


def test_guest_services_have_types_and_coordinates( db: DbControllers, cursor: Cursor ) -> None:
   guest_services = GuestServiceCoordinator.get_guest_services()
   service_types = { service.service_type for service in guest_services }
   primary_key_columns = cursor.execute(
      """ SELECT
             NAME
          FROM PRAGMA_TABLE_INFO( 'GuestService' )
          WHERE PK > 0
          ORDER BY PK;
      """ ).fetchall()

   assert service_types == {
      'First Aid & Family Center',
      'Information',
      'Rentals & Accessibility',
      'Wheelchairs'
   }
   assert [ row[ 'name' ] for row in primary_key_columns ] == [
      'SERVICE_TYPE',
      'X_COORD',
      'Y_COORD'
   ]
   assert all( 0 <= service.x_coord <= 100 for service in guest_services )
   assert all( 0 <= service.y_coord <= 100 for service in guest_services )


def test_picnic_sites_have_coordinates( db: DbControllers ) -> None:
   picnic_sites = PicnicSiteCoordinator.get_picnic_sites()

   assert len( picnic_sites ) > 0
   assert all( 0 <= picnic_site.x_coord <= 100 for picnic_site in picnic_sites )
   assert all( 0 <= picnic_site.y_coord <= 100 for picnic_site in picnic_sites )


def test_event_sites_have_names_and_coordinates( db: DbControllers ) -> None:
   event_sites = EventSiteCoordinator.get_event_sites()
   event_site_names = { event_site.name for event_site in event_sites }

   assert event_site_names == {
      'Special Events Center',
      'Wildlife Marquee',
      'Conservation Clubhouse',
      'Learning & Engagement Auditorium',
      'Canopy Classroom',
      'Serengeti Bush Camp'
   }
   assert all( 0 <= event_site.x_coord <= 100 for event_site in event_sites )
   assert all( 0 <= event_site.y_coord <= 100 for event_site in event_sites )


def test_drinking_fountain_seasonal_fallback_controls_open_and_closed_results(
      db: DbControllers,
      cursor: Cursor ) -> None:
   summer_fountains = DrinkingFountainCoordinator.get_drinking_fountains( day=15, month='June', year=2026 )
   winter_fountains = DrinkingFountainCoordinator.get_drinking_fountains( day=15, month='January', year=2026 )
   transition_fountains = DrinkingFountainCoordinator.get_drinking_fountains( day=30, month='April', year=2026 )
   seasonal_rows = cursor.execute(
      """ SELECT
             MONTH,
             DAY,
             LIKELIHOOD
          FROM DrinkingFountainDaySeasonalAvailabilityMultiplier
          ORDER BY MONTH, DAY;
      """
   ).fetchall()
   seasonal_likelihoods = [ row[ 'LIKELIHOOD' ] for row in seasonal_rows ]
   likelihoods_by_date = {
      ( row[ 'MONTH' ], row[ 'DAY' ] ): row[ 'LIKELIHOOD' ]
      for row in seasonal_rows
   }
   spring_ramp = [
      likelihoods_by_date[ ( month, day ) ]
      for month, day in likelihoods_by_date
      if ( month, day ) >= ( 4, 16 ) and ( month, day ) <= ( 5, 15 )
   ]
   fall_ramp = [
      likelihoods_by_date[ ( month, day ) ]
      for month, day in likelihoods_by_date
      if ( month, day ) >= ( 11, 1 ) and ( month, day ) <= ( 11, 20 )
   ]

   assert len( summer_fountains ) > 0
   assert all( fountain.is_closed is False for fountain in summer_fountains )
   assert all( fountain.closed_message is None for fountain in summer_fountains )
   assert all( fountain.likelihood == 1.0 for fountain in summer_fountains )
   assert all( fountain.is_closed is True for fountain in winter_fountains )
   assert all( fountain.closed_message is None for fountain in winter_fountains )
   assert all( fountain.likelihood == 0.0 for fountain in winter_fountains )
   assert all( 0.0 < fountain.likelihood < 1.0 for fountain in transition_fountains )
   assert len( seasonal_rows ) == 366
   assert min( seasonal_likelihoods ) == 0.0
   assert max( seasonal_likelihoods ) == 1.0
   assert likelihoods_by_date[ ( 1, 15 ) ] == 0.0
   assert likelihoods_by_date[ ( 6, 15 ) ] == 1.0
   assert likelihoods_by_date[ ( 12, 15 ) ] == 0.0
   assert spring_ramp == sorted( spring_ramp )
   assert fall_ramp == sorted( fall_ramp, reverse=True )
   assert spring_ramp[ 0 ] == 0.0
   assert spring_ramp[ -1 ] == 1.0
   assert fall_ramp[ 0 ] == 1.0
   assert fall_ramp[ -1 ] == 0.0


def test_drinking_fountain_status_controls_global_open_and_closed_results(
      db: DbControllers,
      cursor: Cursor ) -> None:
   default_message = 'The drinking fountains are closed for the season.'

   fountains = DrinkingFountainCoordinator.get_drinking_fountains( day=15, month='June', year=2026 )

   assert len( fountains ) > 0
   assert all( fountain.is_closed is False for fountain in fountains )
   assert all( fountain.closed_message is None for fountain in fountains )

   assert DrinkingFountainCoordinator.set_drinking_fountains_as_closed(
      start_date='2026-06-01',
      end_date='2026-06-30',
      message='Closed for testing.' )

   closed = DrinkingFountainCoordinator.get_drinking_fountains( day=15, month='June', year=2026 )
   outside_schedule = DrinkingFountainCoordinator.get_drinking_fountains( day=1, month='July', year=2026 )
   status_rows = cursor.execute(
      """ SELECT
             IS_CLOSED,
             START_DATE,
             END_DATE,
             CLOSED_MESSAGE
          FROM DrinkingFountainStatus;
      """
   ).fetchall()

   assert len( status_rows ) == 1
   assert dict( status_rows[ 0 ] ) == {
      'IS_CLOSED': 1,
      'START_DATE': '2026-06-01',
      'END_DATE': '2026-06-30',
      'CLOSED_MESSAGE': 'Closed for testing.'
   }
   assert all( fountain.is_closed is True for fountain in closed )
   assert all( fountain.closed_message == 'Closed for testing.' for fountain in closed )
   assert all( fountain.likelihood == 0.0 for fountain in closed )
   assert all( fountain.is_closed is False for fountain in outside_schedule )

   assert DrinkingFountainCoordinator.set_drinking_fountains_as_open(
      start_date='2026-06-15',
      end_date=None )

   reopened = DrinkingFountainCoordinator.get_drinking_fountains( day=15, month='June', year=2026 )

   assert all( fountain.is_closed is False for fountain in reopened )
   assert all( fountain.closed_message is None for fountain in reopened )
   assert all( fountain.likelihood == 1.0 for fountain in reopened )

   assert DrinkingFountainCoordinator.set_drinking_fountains_as_closed( message='' )

   default_closed = DrinkingFountainCoordinator.get_drinking_fountains( day=15, month='June', year=2026 )

   assert all( fountain.is_closed is True for fountain in default_closed )
   assert all( fountain.closed_message == default_message for fountain in default_closed )
   assert all( fountain.likelihood == 0.0 for fountain in default_closed )


def test_restaurant_schedule_controls_open_and_closed_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert RestaurantCoordinator.set_restaurant_opening_schedule(
      restaurant='Africa Restaurant',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday=False,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      holidays_only=False,
      message='Closed for testing.'
   )

   open_only = RestaurantCoordinator.get_restaurants( day=15, month='June', year=2026, include_closed_restaurants=False )
   with_closed = RestaurantCoordinator.get_restaurants( day=15, month='June', year=2026, include_closed_restaurants=True )

   assert all( restaurant.name != 'Africa Restaurant' for restaurant in open_only )
   restaurant = next( item for item in with_closed if item.name == 'Africa Restaurant' )
   assert restaurant.is_closed is True
   assert restaurant.closed_message == 'Closed for testing.'


def test_gift_shop_schedule_controls_open_and_closed_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert GiftShopCoordinator.set_gift_shop_opening_schedule(
      gift_shop='Zootique',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday=False,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      holidays_only=False,
      message='Closed for testing.'
   )

   open_only = GiftShopCoordinator.get_gift_shops( day=15, month='June', year=2026, include_closed_gift_shops=False )
   with_closed = GiftShopCoordinator.get_gift_shops( day=15, month='June', year=2026, include_closed_gift_shops=True )

   assert all( shop.name != 'Zootique' for shop in open_only )
   shop = next( item for item in with_closed if item.name == 'Zootique' )
   assert shop.is_closed is True
   assert shop.closed_message == 'Closed for testing.'


def test_restroom_status_controls_open_and_closed_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert RestroomCoordinator.set_restroom_as_closed(
      restroom='Entrance Restroom',
      start_date='2026-06-01',
      end_date='2026-06-30',
      message='Closed for testing.'
   )

   open_only = RestroomCoordinator.get_restrooms( day=15, month='June', year=2026, include_closed_restrooms=False )
   with_closed = RestroomCoordinator.get_restrooms( day=15, month='June', year=2026, include_closed_restrooms=True )

   assert all( restroom.title != 'Entrance Restroom' for restroom in open_only )
   restroom = next( item for item in with_closed if item.title == 'Entrance Restroom' )
   assert restroom.is_closed is True
   assert restroom.closed_message == 'Closed for testing.'

   assert RestroomCoordinator.set_restroom_as_open(
      restroom='Entrance Restroom',
      start_date='2026-06-15',
      end_date=None
   )

   reopened = RestroomCoordinator.get_restrooms( day=15, month='June', year=2026, include_closed_restrooms=False )

   assert any( restroom.title == 'Entrance Restroom' for restroom in reopened )


def test_restroom_alert_controls_guest_message(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert RestroomCoordinator.set_restroom_alert(
      restroom='Entrance Restroom',
      alert_start_date='2026-06-01',
      alert_end_date='2026-06-30',
      message='Women\'s restroom is temporarily unavailable.'
   )

   restroom = next(
      item for item in RestroomCoordinator.get_restrooms( day=15, month='June', year=2026 )
      if item.title == 'Entrance Restroom'
   )

   assert restroom.has_alert is True
   assert restroom.alert_message == 'Women\'s restroom is temporarily unavailable.'

   assert RestroomCoordinator.remove_restroom_alert( restroom='Entrance Restroom' )

   restroom = next(
      item for item in RestroomCoordinator.get_restrooms( day=15, month='June', year=2026 )
      if item.title == 'Entrance Restroom'
   )

   assert restroom.has_alert is False
   assert restroom.alert_message is None


def test_setting_restroom_alert_twice_updates_existing_alert(
      db: DbControllers,
      cursor: Cursor,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert RestroomCoordinator.set_restroom_alert(
      restroom='Entrance Restroom',
      alert_start_date='2026-06-01',
      alert_end_date='2026-06-30',
      message='Women\'s restroom is temporarily unavailable.'
   )
   assert RestroomCoordinator.set_restroom_alert(
      restroom='Entrance Restroom',
      alert_start_date='2026-06-15',
      alert_end_date='2026-07-15',
      message='Family restroom is temporarily unavailable.'
   )

   alert_rows = cursor.execute(
      """ SELECT
             ALERT_MESSAGE,
             ALERT_START_DATE,
             ALERT_END_DATE
          FROM RestroomAlert
          WHERE RESTROOM = ?;
      """,
      ( 'Entrance Restroom', )
   ).fetchall()
   restroom = next(
      item for item in RestroomCoordinator.get_restrooms( day=15, month='June', year=2026 )
      if item.title == 'Entrance Restroom'
   )

   assert len( alert_rows ) == 1
   assert dict( alert_rows[ 0 ] ) == {
      'ALERT_MESSAGE': 'Family restroom is temporarily unavailable.',
      'ALERT_START_DATE': '2026-06-15',
      'ALERT_END_DATE': '2026-07-15'
   }
   assert restroom.has_alert is True
   assert restroom.alert_message == 'Family restroom is temporarily unavailable.'


def test_attraction_schedule_controls_open_and_closed_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert AttractionCoordinator.set_attraction_opening_schedule(
      attraction='Conservation Carousel',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday=False,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      holidays_only=False,
      message='Closed for testing.'
   )

   open_only = AttractionCoordinator.get_attractions( day=15, month='June', year=2026, include_closed_attractions=False )
   with_closed = AttractionCoordinator.get_attractions( day=15, month='June', year=2026, include_closed_attractions=True )

   assert all( attraction.name != 'Conservation Carousel' for attraction in open_only )
   attraction = next( item for item in with_closed if item.name == 'Conservation Carousel' )
   assert attraction.is_closed is True
   assert attraction.closed_message == 'Closed for testing.'


def test_attraction_opening_schedule_rejects_overlapping_date_ranges( db: DbControllers ) -> None:
   assert AttractionCoordinator.set_attraction_opening_schedule(
      attraction='Conservation Carousel',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      holidays_only=False,
      message='June schedule.'
   )

   assert AttractionCoordinator.set_attraction_opening_schedule(
      attraction='Conservation Carousel',
      start_date='2026-06-15',
      end_date='2026-07-15',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      holidays_only=False,
      message='Overlapping schedule.'
   ) is False

   assert AttractionCoordinator.set_attraction_opening_schedule(
      attraction='Conservation Carousel',
      start_date='2026-07-01',
      end_date='2026-07-31',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      holidays_only=False,
      message='July schedule.'
   )


@pytest.mark.parametrize(
   'setter, item_kw, item_name',
   [
      (
         RestaurantCoordinator.set_restaurant_opening_schedule,
         'restaurant',
         'Africa Restaurant'
      ),
      (
         GiftShopCoordinator.set_gift_shop_opening_schedule,
         'gift_shop',
         'Zootique'
      )
   ]
)
def test_restaurant_and_gift_shop_opening_schedules_reject_overlapping_date_ranges(
      db: DbControllers,
      setter: Callable[ ..., bool ],
      item_kw: str,
      item_name: str ) -> None:
   june_schedule = {
      item_kw: item_name,
      'start_date': '2026-06-01',
      'end_date': '2026-06-30',
      'monday': True,
      'tuesday': True,
      'wednesday': True,
      'thursday': True,
      'friday': True,
      'saturday': True,
      'sunday': True,
      'holidays_only': False,
      'message': 'June schedule.'
   }
   overlapping_schedule = {
      **june_schedule,
      'start_date': '2026-06-15',
      'end_date': '2026-07-15',
      'message': 'Overlapping schedule.'
   }
   july_schedule = {
      **june_schedule,
      'start_date': '2026-07-01',
      'end_date': '2026-07-31',
      'message': 'July schedule.'
   }

   assert setter( **june_schedule )
   assert setter( **overlapping_schedule ) is False
   assert setter( **july_schedule )


@pytest.mark.parametrize(
   'controller, item_kw, item_name, records_fetcher, record_name_attr',
   [
      (
         RestaurantCoordinator,
         'restaurant',
         'Africa Restaurant',
         fetch_restaurant_schedule_records,
         'restaurant'
      ),
      (
         GiftShopCoordinator,
         'gift_shop',
         'Zootique',
         fetch_gift_shop_schedule_records,
         'gift_shop'
      ),
      (
         AttractionCoordinator,
         'attraction',
         'Conservation Carousel',
         fetch_attraction_schedule_records,
         'attraction'
      )
   ]
)
def test_opening_schedule_can_replace_overlapping_schedules(
      db: DbControllers,
      controller: type,
      item_kw: str,
      item_name: str,
      records_fetcher: Callable[ [ Connection ], list[ AmenityScheduleRecord ] ],
      record_name_attr: str ) -> None:
   base_schedule = {
      item_kw: item_name,
      'start_date': '2026-06-01',
      'end_date': '2026-06-30',
      'monday': True,
      'tuesday': True,
      'wednesday': True,
      'thursday': True,
      'friday': True,
      'saturday': True,
      'sunday': True,
      'holidays_only': False,
      'message': 'June schedule.'
   }
   replacement_schedule = {
      **base_schedule,
      'start_date': '2026-06-15',
      'end_date': '2026-07-15',
      'message': 'Replacement schedule.'
   }

   set_method = getattr( controller, f'set_{ item_kw }_opening_schedule' )
   replace_method = getattr(
      controller,
      f'replace_{ item_kw }_opening_schedule_overlaps' )

   assert set_method( **base_schedule )
   assert replace_method(
      **replacement_schedule )

   schedule_records = [
      schedule_record
      for schedule_record in records_fetcher( db.conn )
      if getattr( schedule_record, record_name_attr ) == item_name
   ]

   assert [
      (
         record.schedule_start_date,
         record.schedule_end_date,
         record.schedule_message
      )
      for record in schedule_records
   ] == [
      (
         '2026-06-15',
         '2026-07-15',
         'Replacement schedule.'
      )
   ]


@pytest.mark.parametrize(
   'controller, item_kw, item_name, records_fetcher, record_name_attr',
   [
      (
         RestaurantCoordinator,
         'restaurant',
         'Africa Restaurant',
         fetch_restaurant_schedule_records,
         'restaurant'
      ),
      (
         GiftShopCoordinator,
         'gift_shop',
         'Zootique',
         fetch_gift_shop_schedule_records,
         'gift_shop'
      ),
      (
         AttractionCoordinator,
         'attraction',
         'Conservation Carousel',
         fetch_attraction_schedule_records,
         'attraction'
      )
   ]
)
def test_opening_schedule_can_trim_existing_schedule_around_new_schedule(
      db: DbControllers,
      controller: type,
      item_kw: str,
      item_name: str,
      records_fetcher: Callable[ [ Connection ], list[ AmenityScheduleRecord ] ],
      record_name_attr: str ) -> None:
   base_schedule = {
      item_kw: item_name,
      'start_date': '2026-06-01',
      'end_date': '2026-07-31',
      'monday': True,
      'tuesday': True,
      'wednesday': True,
      'thursday': True,
      'friday': True,
      'saturday': True,
      'sunday': True,
      'holidays_only': False,
      'message': 'Summer schedule.'
   }
   inserted_schedule = {
      **base_schedule,
      'start_date': '2026-06-15',
      'end_date': '2026-06-20',
      'message': 'Special schedule.'
   }

   set_method = getattr( controller, f'set_{ item_kw }_opening_schedule' )
   trim_method = getattr(
      controller,
      f'trim_{ item_kw }_opening_schedule_overlaps' )

   assert set_method( **base_schedule )
   assert trim_method(
      **inserted_schedule )

   schedule_records = sorted(
      [
         schedule_record
         for schedule_record in records_fetcher( db.conn )
         if getattr( schedule_record, record_name_attr ) == item_name
      ],
      key=lambda record: record.schedule_start_date )

   assert [
      (
         record.schedule_start_date,
         record.schedule_end_date,
         record.schedule_message
      )
      for record in schedule_records
   ] == [
      (
         '2026-06-01',
         '2026-06-14',
         'Summer schedule.'
      ),
      (
         '2026-06-15',
         '2026-06-20',
         'Special schedule.'
      ),
      (
         '2026-06-21',
         '2026-07-31',
         'Summer schedule.'
      )
   ]


def test_attraction_closure_override_takes_precedence_over_opening_schedule( db: DbControllers ) -> None:
   assert AttractionCoordinator.set_attraction_opening_schedule(
      attraction='Conservation Carousel',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      holidays_only=False,
      message='Open for June.'
   )

   assert AttractionCoordinator.set_attraction_closure_override(
      attraction='Conservation Carousel',
      start_date='2026-06-20',
      end_date='2026-06-21',
      message='Closed this weekend.'
   )

   override_records = fetch_attraction_schedule_override_records( db.conn )
   assert [
      (
         record.attraction,
         record.override_start_date,
         record.override_end_date,
         record.is_closed,
         record.override_message
      )
      for record in override_records
      if record.attraction == 'Conservation Carousel'
   ] == [
      (
         'Conservation Carousel',
         '2026-06-20',
         '2026-06-21',
         1,
         'Closed this weekend.'
      )
   ]

   closed_attraction = next(
      attraction for attraction in AttractionCoordinator.get_attractions(
         day=20,
         month='June',
         year=2026,
         include_closed_attractions=True )
      if attraction.name == 'Conservation Carousel'
   )
   open_attraction = next(
      attraction for attraction in AttractionCoordinator.get_attractions(
         day=22,
         month='June',
         year=2026,
         include_closed_attractions=True )
      if attraction.name == 'Conservation Carousel'
   )

   assert closed_attraction.is_closed is True
   assert closed_attraction.closed_message == 'Closed this weekend.'
   assert open_attraction.is_closed is False


def test_restaurant_closure_override_takes_precedence_over_opening_schedule( db: DbControllers ) -> None:
   assert RestaurantCoordinator.set_restaurant_opening_schedule(
      restaurant='Africa Restaurant',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      holidays_only=False,
      message='Open for June.'
   )

   assert RestaurantCoordinator.set_restaurant_closure_override(
      restaurant='Africa Restaurant',
      start_date='2026-06-20',
      end_date='2026-06-21',
      message='Closed this weekend.'
   )

   override_records = fetch_restaurant_schedule_override_records( db.conn )
   assert [
      (
         record.restaurant,
         record.override_start_date,
         record.override_end_date,
         record.is_closed,
         record.override_message
      )
      for record in override_records
      if record.restaurant == 'Africa Restaurant'
   ] == [
      (
         'Africa Restaurant',
         '2026-06-20',
         '2026-06-21',
         1,
         'Closed this weekend.'
      )
   ]

   closed_restaurant = next(
      restaurant for restaurant in RestaurantCoordinator.get_restaurants(
         day=20,
         month='June',
         year=2026,
         include_closed_restaurants=True )
      if restaurant.name == 'Africa Restaurant'
   )
   open_restaurant = next(
      restaurant for restaurant in RestaurantCoordinator.get_restaurants(
         day=22,
         month='June',
         year=2026,
         include_closed_restaurants=True )
      if restaurant.name == 'Africa Restaurant'
   )

   assert closed_restaurant.is_closed is True
   assert closed_restaurant.closed_message == 'Closed this weekend.'
   assert open_restaurant.is_closed is False


def test_gift_shop_closure_override_takes_precedence_over_opening_schedule( db: DbControllers ) -> None:
   assert GiftShopCoordinator.set_gift_shop_opening_schedule(
      gift_shop='Zootique',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      holidays_only=False,
      message='Open for June.'
   )

   assert GiftShopCoordinator.set_gift_shop_closure_override(
      gift_shop='Zootique',
      start_date='2026-06-20',
      end_date='2026-06-21',
      message='Closed this weekend.'
   )

   override_records = fetch_gift_shop_schedule_override_records( db.conn )
   assert [
      (
         record.gift_shop,
         record.override_start_date,
         record.override_end_date,
         record.is_closed,
         record.override_message
      )
      for record in override_records
      if record.gift_shop == 'Zootique'
   ] == [
      (
         'Zootique',
         '2026-06-20',
         '2026-06-21',
         1,
         'Closed this weekend.'
      )
   ]

   closed_gift_shop = next(
      gift_shop for gift_shop in GiftShopCoordinator.get_gift_shops(
         day=20,
         month='June',
         year=2026,
         include_closed_gift_shops=True )
      if gift_shop.name == 'Zootique'
   )
   open_gift_shop = next(
      gift_shop for gift_shop in GiftShopCoordinator.get_gift_shops(
         day=22,
         month='June',
         year=2026,
         include_closed_gift_shops=True )
      if gift_shop.name == 'Zootique'
   )

   assert closed_gift_shop.is_closed is True
   assert closed_gift_shop.closed_message == 'Closed this weekend.'
   assert open_gift_shop.is_closed is False


@pytest.mark.parametrize(
   'method_name, setter_name, item_kw, item_name',
   [
      (
         'get_active_restaurant_schedule_status',
         'set_restaurant_opening_schedule',
         'restaurant',
         'Africa Restaurant'
      ),
      (
         'get_active_gift_shop_schedule_status',
         'set_gift_shop_opening_schedule',
         'gift_shop',
         'Zootique'
      ),
      (
         'get_active_attraction_schedule_status',
         'set_attraction_opening_schedule',
         'attraction',
         'Conservation Carousel'
      )
   ]
)
@pytest.mark.parametrize(
   'target_date, weekday_flag',
   [
      ( date( 2026, 6, 15 ), 'monday' ),
      ( date( 2026, 6, 16 ), 'tuesday' ),
      ( date( 2026, 6, 17 ), 'wednesday' ),
      ( date( 2026, 6, 18 ), 'thursday' ),
      ( date( 2026, 6, 19 ), 'friday' ),
      ( date( 2026, 6, 20 ), 'saturday' ),
      ( date( 2026, 6, 21 ), 'sunday' )
   ]
)
def test_amenity_schedule_status_opens_on_each_weekday(
      db: DbControllers,
      method_name: str,
      setter_name: str,
      item_kw: str,
      item_name: str,
      target_date: date,
      weekday_flag: str ) -> None:
   schedule = {
      item_kw: item_name,
      'start_date': '2026-06-01',
      'end_date': '2026-06-30',
      'monday': False,
      'tuesday': False,
      'wednesday': False,
      'thursday': False,
      'friday': False,
      'saturday': False,
      'sunday': False,
      'holidays_only': False,
      'message': 'Closed for testing.'
   }
   schedule[ weekday_flag ] = True

   assert apply_amenity_opening_schedule( db, setter_name, schedule )

   assert get_amenity_schedule_status(
      db,
      method_name,
      item_name,
      target_date,
      target_date.weekday() ) == ( 'open', None )


@pytest.mark.parametrize(
   'method_name, setter_name, item_kw, item_name',
   [
      (
         'get_active_restaurant_schedule_status',
         'set_restaurant_opening_schedule',
         'restaurant',
         'Africa Restaurant'
      ),
      (
         'get_active_gift_shop_schedule_status',
         'set_gift_shop_opening_schedule',
         'gift_shop',
         'Zootique'
      ),
      (
         'get_active_attraction_schedule_status',
         'set_attraction_opening_schedule',
         'attraction',
         'Conservation Carousel'
      )
   ]
)
def test_amenity_schedule_status_handles_unknown_inactive_closed_and_holiday(
      db: DbControllers,
      method_name: str,
      setter_name: str,
      item_kw: str,
      item_name: str ) -> None:
   assert get_amenity_schedule_status(
      db,
      method_name,
      item_name,
      date( 2026, 5, 15 ),
      4 ) == ( 'unknown', None )

   schedule = {
      item_kw: item_name,
      'start_date': '2026-06-01',
      'end_date': '2026-06-30',
      'monday': False,
      'tuesday': False,
      'wednesday': False,
      'thursday': False,
      'friday': False,
      'saturday': False,
      'sunday': False,
      'holidays_only': False,
      'message': 'Closed for testing.'
   }

   assert apply_amenity_opening_schedule( db, setter_name, schedule )

   assert get_amenity_schedule_status(
      db,
      method_name,
      item_name,
      date( 2026, 5, 15 ),
      4 ) == ( 'unknown', None )
   assert get_amenity_schedule_status(
      db,
      method_name,
      item_name,
      date( 2026, 6, 15 ),
      0 ) == ( 'closed', 'Closed for testing.' )

   schedule[ 'end_date' ] = '2026-12-31'
   schedule[ 'holidays_only' ] = True
   assert apply_amenity_opening_schedule( db, setter_name, schedule )

   assert get_amenity_schedule_status(
      db,
      method_name,
      item_name,
      date( 2026, 12, 25 ),
      4 ) == ( 'open', None )


def test_zoomobile_route_selection_and_station_filtering(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 1, 15 ) )

   manual = ZoomobileCoordinator.get_zoomobile_route( route='winter', day=15, month='January', year=2026 )
   invalid = ZoomobileCoordinator.get_zoomobile_route( route='bad-route', day=15, month='January', year=2026 )

   assert manual.route == 'winter'
   assert invalid.route == 'summer'

   assert ZoomobileCoordinator.set_current_zoomobile_route( route='winter', start_date='2026-01-01', end_date='2026-01-31' )
   current = ZoomobileCoordinator.get_zoomobile_route( route='current', day=15, month='January', year=2026 )

   assert current.route == 'winter'
   assert current.route_source == 'override'
   assert all( station.name != 'Africa Zoomobile Station' for station in current.zoomobile_stations )


def test_guardians_talk_schedule_and_cancellation(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk='African Lion',
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday_time='10:00',
      tuesday_time=None,
      wednesday_time=None,
      thursday_time=None,
      friday_time=None,
      saturday_time=None,
      sunday_time=None,
      message=None
   )

   talks = GuardiansCoordinator.get_guardians_talk_schedule( month='June', day=15, year=2026 )
   assert any( talk.name == 'African Lion' and talk.start_time == '10:00' for talk in talks )
   talk = next(
      talk for talk in talks
      if talk.name == 'African Lion' and talk.start_time == '10:00'
   )
   assert talk.maximum_duration == 30
   assert talk.end_time == '10:30'

   assert GuardiansCoordinator.cancel_guardians_talk_occurrence(
      talk='African Lion',
      location='Africa Savanna',
      date='2026-06-15',
      time='10:00'
   )
   talks_after_cancel = GuardiansCoordinator.get_guardians_talk_schedule( month='June', day=15, year=2026 )

   assert all( not ( talk.name == 'African Lion' and talk.start_time == '10:00' ) for talk in talks_after_cancel )

   assert GuardiansCoordinator.get_guardians_talk_schedule( month='June', day=16, year=2026 ) == []


def test_guardians_talk_schedule_supports_different_weekday_times(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk='African Lion',
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday_time=None,
      tuesday_time=None,
      wednesday_time='13:00',
      thursday_time='14:00',
      friday_time=None,
      saturday_time=None,
      sunday_time=None,
      message=None
   )

   wednesday_talks = GuardiansCoordinator.get_guardians_talk_schedule(
      month='June',
      day=17,
      year=2026 )
   thursday_talks = GuardiansCoordinator.get_guardians_talk_schedule(
      month='June',
      day=18,
      year=2026 )

   assert any(
      talk.name == 'African Lion' and talk.start_time == '13:00'
      for talk in wednesday_talks
   )
   assert any(
      talk.name == 'African Lion' and talk.start_time == '14:00'
      for talk in thursday_talks
   )


def test_guardians_talk_occurrences_cover_all_weekdays_and_cancellations(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk='African Lion',
      location='Africa Savanna',
      start_date='2026-06-15',
      end_date='2026-06-21',
      monday_time='10:00',
      tuesday_time='10:00',
      wednesday_time='10:00',
      thursday_time='10:00',
      friday_time='10:00',
      saturday_time='10:00',
      sunday_time='10:00',
      message=None
   )
   assert GuardiansCoordinator.cancel_guardians_talk_occurrence(
      talk='African Lion',
      location='Africa Savanna',
      date='2026-06-18',
      time='10:00'
   )

   occurrences = GuardiansCoordinator.get_guardians_talk_occurrences(
      talk='African Lion',
      location='Africa Savanna',
      days_ahead=6
   )

   assert { occurrence.date for occurrence in occurrences } == {
      '2026-06-15',
      '2026-06-16',
      '2026-06-17',
      '2026-06-19',
      '2026-06-20',
      '2026-06-21'
   }
   assert GuardiansCoordinator.get_guardians_talk_occurrences( talk='', location='Africa Savanna' ) == []
   assert GuardiansCoordinator.get_guardians_talk_occurrences( talk='Bad Talk', location='Bad Location' ) == []


def test_wild_encounter_schedule_and_cancellation(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='African Rainforest',
      start_date='2026-06-01',
      end_date='2026-06-30',
      encounter_time='14:00',
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      message=None
   )

   encounters = WildEncounterCoordinator.get_wild_encounter_schedule( month='June', day=15, year=2026 )
   encounter = next( item for item in encounters if item.name == 'African Rainforest' and item.start_time == '14:00' )
   assert encounter.is_available is True
   assert encounter.maximum_duration == 45
   assert encounter.end_time == '14:45'

   assert WildEncounterCoordinator.cancel_wild_encounter_occurrence(
      wild_encounter_name='African Rainforest',
      date='2026-06-15',
      time='14:00'
   )
   encounters_after_cancel = WildEncounterCoordinator.get_wild_encounter_schedule( month='June', day=15, year=2026 )
   cancelled = next( item for item in encounters_after_cancel if item.name == 'African Rainforest' and item.start_time == '14:00' )
   assert cancelled.is_available is False

   weekday_unavailable = next(
      item for item in WildEncounterCoordinator.get_wild_encounter_schedule( month='June', day=16, year=2026 )
      if item.name == 'African Rainforest' and item.start_time == '14:00'
   )
   out_of_range = next(
      item for item in WildEncounterCoordinator.get_wild_encounter_schedule( month='July', day=1, year=2026 )
      if item.name == 'African Rainforest' and item.start_time == '14:00'
   )
   assert weekday_unavailable.unavailable_message == 'African Rainforest is not offered on this day of the week.'
   assert out_of_range.unavailable_message == 'African Rainforest is not scheduled on July 1.'


def test_wild_encounter_search_only_returns_available_schedule_days(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='Mischevious Meerkats',
      start_date='2026-06-01',
      end_date='2026-06-30',
      encounter_time='14:00',
      monday=True,
      tuesday=False,
      wednesday=True,
      thursday=True,
      friday=False,
      saturday=True,
      sunday=False,
      message=None
   )

   monday_results = WildEncounterCoordinator.get_wild_encounters_matching_query(
      query='Mischevious Meerkats',
      month='June',
      day=15,
      year=2026 )
   sunday_results = WildEncounterCoordinator.get_wild_encounters_matching_query(
      query='Mischevious Meerkats',
      month='June',
      day=21,
      year=2026 )
   sunday_available = WildEncounterCoordinator.get_available_wild_encounters(
      month='June',
      day=21,
      year=2026 )

   assert [ item.name for item in monday_results ] == [ 'Mischevious Meerkats' ]
   assert sunday_results == []
   assert all( item.name != 'Mischevious Meerkats' for item in sunday_available )


def test_wild_encounter_occurrences_cover_all_weekdays_and_cancellations(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='African Rainforest',
      start_date='2026-06-15',
      end_date='2026-06-21',
      encounter_time='14:00',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      message=None
   )
   assert WildEncounterCoordinator.cancel_wild_encounter_occurrence(
      wild_encounter_name='African Rainforest',
      date='2026-06-18',
      time='14:00'
   )

   occurrences = WildEncounterCoordinator.get_wild_encounter_occurrences(
      wild_encounter_name='African Rainforest',
      days_ahead=6
   )

   assert { occurrence.date for occurrence in occurrences } == {
      '2026-06-15',
      '2026-06-16',
      '2026-06-17',
      '2026-06-19',
      '2026-06-20',
      '2026-06-21'
   }
   assert WildEncounterCoordinator.get_wild_encounter_occurrences( wild_encounter_name='' ) == []
   assert WildEncounterCoordinator.get_wild_encounter_occurrences( wild_encounter_name='Bad Encounter' ) == []


def test_search_helpers_filter_case_insensitively( db: DbControllers ) -> None:
   assert [
      restaurant.name
      for restaurant in RestaurantCoordinator.get_restaurants_matching_query( 'AFRICA', 15, 'June', 2026, True )
   ] == [ 'Africa Restaurant' ]

   assert [
      shop.name
      for shop in GiftShopCoordinator.get_gift_shops_matching_query( 'ZOOTIQUE', 15, 'June', 2026 )
   ] == [ 'Zootique' ]

   assert [
      attraction.name
      for attraction in AttractionCoordinator.get_attractions_matching_query( 'CAROUSEL', 15, 'June', 2026, True )
   ] == [ 'Conservation Carousel' ]

   assert [
      station.name
      for station in ZoomobileCoordinator.get_zoomobile_stations_matching_query(
         query='MAIN',
         route='summer',
         day=15,
         month='June',
         year=2026 )
   ] == [
      'Main Zoomobile Station',
      'Canadian Domain Zoomobile Station'
   ]
