from datetime import date

import pytest


def test_region_and_static_location_queries( db ):
   regions = db.get_regions()

   assert regions == [
      { 'name': 'Africa', 'hasExhibits': True },
      { 'name': 'Americas', 'hasExhibits': True },
      { 'name': 'Australasia', 'hasExhibits': True },
      { 'name': 'Canadian Domain', 'hasExhibits': False },
      { 'name': 'Discovery Zone', 'hasExhibits': True },
      { 'name': 'Eurasia Wilds', 'hasExhibits': False },
      { 'name': 'Indo-Malaya', 'hasExhibits': True },
      { 'name': 'Tundra Trek', 'hasExhibits': False }
   ]

   assert db.get_exhibits_in_region( 'Africa' ) == [
      'Africa Savanna',
      'African Rainforest Pavilion'
   ]
   assert db.get_exhibits() == [
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

   pavilions = {
      pavilion.name: pavilion
      for pavilion in db.get_pavilions()
   }
   restrooms = {
      restroom.title: restroom
      for restroom in db.get_restrooms()
   }

   assert pavilions[ 'African Rainforest Pavilion' ].region == 'Africa'
   assert pavilions[ 'African Rainforest Pavilion' ].x_coord == 45.746
   assert restrooms[ 'Entrance Restroom' ].x_coord == 57.418
   assert restrooms[ 'Africa Restaurant Restroom' ].y_coord == 59.47


def test_restaurant_schedule_controls_open_and_closed_results( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )
   assert db.set_restaurant_opening_schedule(
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

   open_only = db.get_restaurants( month='June', day=15, include_closed_restaurants=False )
   with_closed = db.get_restaurants( month='June', day=15, include_closed_restaurants=True )

   assert all( restaurant.name != 'Africa Restaurant' for restaurant in open_only )
   restaurant = next( item for item in with_closed if item.name == 'Africa Restaurant' )
   assert restaurant.is_closed is True
   assert restaurant.closed_message == 'Closed for testing.'


def test_gift_shop_schedule_controls_open_and_closed_results( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )
   assert db.set_gift_shop_opening_schedule(
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

   open_only = db.get_gift_shops( month='June', day=15, include_closed_gift_shops=False )
   with_closed = db.get_gift_shops( month='June', day=15, include_closed_gift_shops=True )

   assert all( shop.name != 'Zootique' for shop in open_only )
   shop = next( item for item in with_closed if item.name == 'Zootique' )
   assert shop.is_closed is True
   assert shop.closed_message == 'Closed for testing.'


def test_restroom_status_controls_open_and_closed_results( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )
   assert db.set_restroom_as_closed(
      restroom='Entrance Restroom',
      start_date='2026-06-01',
      end_date='2026-06-30',
      message='Closed for testing.'
   )

   open_only = db.get_restrooms( month='June', day=15, include_closed_restrooms=False )
   with_closed = db.get_restrooms( month='June', day=15, include_closed_restrooms=True )

   assert all( restroom.title != 'Entrance Restroom' for restroom in open_only )
   restroom = next( item for item in with_closed if item.title == 'Entrance Restroom' )
   assert restroom.is_closed is True
   assert restroom.closed_message == 'Closed for testing.'

   assert db.set_restroom_as_open(
      restroom='Entrance Restroom',
      start_date='2026-06-15',
      end_date=None
   )

   reopened = db.get_restrooms( month='June', day=15, include_closed_restrooms=False )

   assert any( restroom.title == 'Entrance Restroom' for restroom in reopened )


def test_restroom_alert_controls_guest_message( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )
   assert db.set_restroom_alert(
      restroom='Entrance Restroom',
      alert_start_date='2026-06-01',
      alert_end_date='2026-06-30',
      message='Women\'s restroom is temporarily unavailable.'
   )

   restroom = next(
      item for item in db.get_restrooms( month='June', day=15 )
      if item.title == 'Entrance Restroom'
   )

   assert restroom.has_alert is True
   assert restroom.alert_message == 'Women\'s restroom is temporarily unavailable.'

   assert db.remove_restroom_alert( restroom='Entrance Restroom' )

   restroom = next(
      item for item in db.get_restrooms( month='June', day=15 )
      if item.title == 'Entrance Restroom'
   )

   assert restroom.has_alert is False
   assert restroom.alert_message is None


def test_setting_restroom_alert_twice_updates_existing_alert( db, cursor, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )
   assert db.set_restroom_alert(
      restroom='Entrance Restroom',
      alert_start_date='2026-06-01',
      alert_end_date='2026-06-30',
      message='Women\'s restroom is temporarily unavailable.'
   )
   assert db.set_restroom_alert(
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
      item for item in db.get_restrooms( month='June', day=15 )
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


def test_attraction_schedule_controls_open_and_closed_results( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )
   assert db.set_attraction_opening_schedule(
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

   open_only = db.get_attractions( month='June', day=15, include_closed_attractions=False )
   with_closed = db.get_attractions( month='June', day=15, include_closed_attractions=True )

   assert all( attraction.name != 'Conservation Carousel' for attraction in open_only )
   attraction = next( item for item in with_closed if item.name == 'Conservation Carousel' )
   assert attraction.is_closed is True
   assert attraction.closed_message == 'Closed for testing.'


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
      db,
      method_name,
      setter_name,
      item_kw,
      item_name,
      target_date,
      weekday_flag ):
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

   assert getattr( db, setter_name )( **schedule )

   assert getattr( db, method_name )( item_name, target_date, target_date.weekday() ) == ( 'open', None )


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
      db,
      method_name,
      setter_name,
      item_kw,
      item_name ):
   method = getattr( db, method_name )

   assert method( item_name, date( 2026, 5, 15 ), 4 ) == ( 'unknown', None )

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

   assert getattr( db, setter_name )( **schedule )

   assert method( item_name, date( 2026, 5, 15 ), 4 ) == ( 'unknown', None )
   assert method( item_name, date( 2026, 6, 15 ), 0 ) == ( 'closed', 'Closed for testing.' )

   schedule[ 'start_date' ] = '2026-01-01'
   schedule[ 'end_date' ] = '2026-12-31'
   schedule[ 'holidays_only' ] = True
   assert getattr( db, setter_name )( **schedule )

   assert method( item_name, date( 2026, 12, 25 ), 4 ) == ( 'open', None )


def test_zoomobile_route_selection_and_station_filtering( db, freeze_database_today ):
   freeze_database_today( date( 2026, 1, 15 ) )

   manual = db.get_zoomobile_route( route='winter', month='January', day=15 )
   invalid = db.get_zoomobile_route( route='bad-route', month='January', day=15 )

   assert manual[ 'route' ] == 'winter'
   assert invalid[ 'route' ] == 'summer'

   assert db.set_current_zoomobile_route( route='winter', start_date='2026-01-01', end_date='2026-01-31' )
   current = db.get_zoomobile_route( route='current', month='January', day=15 )

   assert current[ 'route' ] == 'winter'
   assert current[ 'route_source' ] == 'override'
   assert all( station.name != 'Africa Zoomobile Station' for station in current[ 'zoomobile_stations' ] )


def test_guardians_talk_schedule_and_cancellation( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )
   assert db.set_guardians_talk_schedule(
      talk='African Lion',
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      talk_time='10:00',
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      message=None
   )

   talks = db.get_guardians_talks( month='June', day=15 )
   assert any( talk.name == 'African Lion' and talk.time_of_day == '10:00' for talk in talks )

   assert db.cancel_guardians_talk_occurrence(
      talk='African Lion',
      location='Africa Savanna',
      date='2026-06-15',
      time='10:00'
   )
   talks_after_cancel = db.get_guardians_talks( month='June', day=15 )

   assert all( not ( talk.name == 'African Lion' and talk.time_of_day == '10:00' ) for talk in talks_after_cancel )

   assert db.get_guardians_talks( month='June', day=16 ) == []


def test_guardians_talk_occurrences_cover_all_weekdays_and_cancellations( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )
   assert db.set_guardians_talk_schedule(
      talk='African Lion',
      location='Africa Savanna',
      start_date='2026-06-15',
      end_date='2026-06-21',
      talk_time='10:00',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      message=None
   )
   assert db.cancel_guardians_talk_occurrence(
      talk='African Lion',
      location='Africa Savanna',
      date='2026-06-18',
      time='10:00'
   )

   occurrences = db.get_guardians_talk_occurrences(
      talk='African Lion',
      location='Africa Savanna',
      days_ahead=6
   )

   assert { occurrence[ 'date' ] for occurrence in occurrences } == {
      '2026-06-15',
      '2026-06-16',
      '2026-06-17',
      '2026-06-19',
      '2026-06-20',
      '2026-06-21'
   }
   assert db.get_guardians_talk_occurrences( talk='', location='Africa Savanna' ) == []
   assert db.get_guardians_talk_occurrences( talk='Bad Talk', location='Bad Location' ) == []


def test_wild_encounter_schedule_and_cancellation( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )
   assert db.set_wild_encounter_schedule(
      wild_encounter='African Rainforest',
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

   encounters = db.get_wild_encounters( month='June', day=15 )
   encounter = next( item for item in encounters if item.name == 'African Rainforest' and item.time_of_day == '14:00' )
   assert encounter.is_available is True

   assert db.cancel_wild_encounter_occurrence(
      wild_encounter='African Rainforest',
      date='2026-06-15',
      time='14:00'
   )
   encounters_after_cancel = db.get_wild_encounters( month='June', day=15 )
   cancelled = next( item for item in encounters_after_cancel if item.name == 'African Rainforest' and item.time_of_day == '14:00' )
   assert cancelled.is_available is False

   weekday_unavailable = next(
      item for item in db.get_wild_encounters( month='June', day=16 )
      if item.name == 'African Rainforest' and item.time_of_day == '14:00'
   )
   out_of_range = next(
      item for item in db.get_wild_encounters( month='July', day=1 )
      if item.name == 'African Rainforest' and item.time_of_day == '14:00'
   )
   assert weekday_unavailable.unavailable_message == 'African Rainforest is not offered on this day of the week.'
   assert out_of_range.unavailable_message == 'African Rainforest is not scheduled on July 1.'


def test_wild_encounter_occurrences_cover_all_weekdays_and_cancellations( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )
   assert db.set_wild_encounter_schedule(
      wild_encounter='African Rainforest',
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
   assert db.cancel_wild_encounter_occurrence(
      wild_encounter='African Rainforest',
      date='2026-06-18',
      time='14:00'
   )

   occurrences = db.get_wild_encounter_occurrences(
      wild_encounter='African Rainforest',
      days_ahead=6
   )

   assert { occurrence[ 'date' ] for occurrence in occurrences } == {
      '2026-06-15',
      '2026-06-16',
      '2026-06-17',
      '2026-06-19',
      '2026-06-20',
      '2026-06-21'
   }
   assert db.get_wild_encounter_occurrences( wild_encounter='' ) == []
   assert db.get_wild_encounter_occurrences( wild_encounter='Bad Encounter' ) == []


def test_search_helpers_filter_case_insensitively( db ):
   assert [
      restaurant.name
      for restaurant in db.get_restaurants_matching_query( 'AFRICA', 'June', 15, True )
   ] == [ 'Africa Restaurant' ]

   assert [
      shop.name
      for shop in db.get_gift_shops_matching_query( 'ZOOTIQUE', 'June', 15 )
   ] == [ 'Zootique' ]

   assert [
      attraction.name
      for attraction in db.get_attractions_matching_query( 'CAROUSEL', 'June', 15, True )
   ] == [ 'Conservation Carousel' ]

   assert [
      station.name
      for station in db.get_zoomobile_stations_matching_query(
         query='MAIN',
         route='summer',
         month='June',
         day=15 )
   ] == [
      'Main Zoomobile Station',
      'Canadian Domain Zoomobile Station'
   ]
