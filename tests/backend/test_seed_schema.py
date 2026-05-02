import sqlite3

from seed import data
from seed.schema import create_schema


def column_names( cursor, table ):
   return {
      row[ 1 ]
      for row in cursor.execute( f'PRAGMA table_info( { table } );' ).fetchall()
   }


def test_seed_data_exports_all_static_table_rows():
   assert data.regions
   assert data.exhibits
   assert data.exhibit_day_seasonal_availability_multipliers
   assert data.animals
   assert data.enclosures
   assert data.enclosure_viewings
   assert data.animal_day_seasonal_viewability_multipliers
   assert data.pavilions
   assert data.restaurants
   assert data.restaurant_day_seasonal_availability_multipliers
   assert data.restrooms
   assert data.gift_shops
   assert data.gift_shop_day_seasonal_availability_multipliers
   assert data.attractions
   assert data.attraction_day_seasonal_availability_multipliers
   assert data.zoomobile_stations
   assert data.zoomobile_day_routes
   assert data.guardians_talks
   assert data.wild_encounter_meeting_spots
   assert data.wild_encounters
   assert data.drinking_fountain_day_seasonal_availability_multipliers
   assert data.drinking_fountains
   assert data.defibrillators
   assert data.emergency_intercoms
   assert data.guest_services
   assert data.picnic_sites


def test_create_schema_migrates_partial_dynamic_tables():
   conn = sqlite3.connect( ':memory:' )
   cursor = conn.cursor()

   partial_tables = {
      'AnimalStatus': 'SPECIES TEXT, EXHIBIT TEXT',
      'AnimalVisibilitySchedule': 'SPECIES TEXT, EXHIBIT TEXT',
      'AnimalViewingAlert': 'SPECIES TEXT, EXHIBIT TEXT',
      'ExhibitStatus': 'EXHIBIT TEXT',
      'RestroomStatus': 'RESTROOM TEXT',
      'RestroomAlert': 'RESTROOM TEXT',
      'RestaurantOpeningSchedule': 'RESTAURANT TEXT',
      'GiftShopOpeningSchedule': 'GIFT_SHOP TEXT',
      'AppSetting': 'ID INTEGER',
      'AttractionOpeningSchedule': 'ATTRACTION TEXT',
      'ZoomobileRouteSchedule': 'ID INTEGER',
      'ZoomobileStationStatus': 'ZOOMOBILE_STATION TEXT',
      'GuardiansTalkSchedule': 'TALK_NAME TEXT, LOCATION TEXT',
      'GuardiansTalkCancellation': 'TALK_NAME TEXT, LOCATION TEXT',
      'WildEncounterSchedule': 'WILD_ENCOUNTER TEXT',
      'WildEncounterCancellation': 'WILD_ENCOUNTER TEXT',
      'Itinerary': 'ID INTEGER',
      'ItineraryAnimal': 'SPECIES TEXT'
   }

   for table, columns in partial_tables.items():
      cursor.execute( f'CREATE TABLE { table } ( { columns } );' )

   create_schema( cursor )

   expected_columns = {
      'AnimalStatus': {
         'SPECIES',
         'EXHIBIT',
         'IS_OFF_DISPLAY',
         'OFF_DISPLAY_MESSAGE',
         'OFF_DISPLAY_START',
         'OFF_DISPLAY_END'
      },
      'AnimalVisibilitySchedule': {
         'SPECIES',
         'EXHIBIT',
         'SCHEDULE_START_DATE',
         'SCHEDULE_END_DATE',
         'DAILY_START_TIME',
         'DAILY_END_TIME',
         'VIEWING_MESSAGE'
      },
      'AnimalViewingAlert': {
         'SPECIES',
         'EXHIBIT',
         'ALERT_MESSAGE',
         'ALERT_START_DATE',
         'ALERT_END_DATE'
      },
      'ExhibitStatus': {
         'EXHIBIT',
         'IS_CLOSED',
         'CLOSED_MESSAGE',
         'CLOSED_START',
         'CLOSED_END'
      },
      'RestroomStatus': {
         'RESTROOM',
         'IS_CLOSED',
         'CLOSED_MESSAGE',
         'CLOSED_START',
         'CLOSED_END'
      },
      'RestroomAlert': {
         'RESTROOM',
         'ALERT_MESSAGE',
         'ALERT_START_DATE',
         'ALERT_END_DATE'
      },
      'RestaurantOpeningSchedule': {
         'RESTAURANT',
         'SCHEDULE_START_DATE',
         'SCHEDULE_END_DATE',
         'MONDAY',
         'TUESDAY',
         'WEDNESDAY',
         'THURSDAY',
         'FRIDAY',
         'SATURDAY',
         'SUNDAY',
         'HOLIDAYS_ONLY',
         'SCHEDULE_MESSAGE'
      },
      'GiftShopOpeningSchedule': {
         'GIFT_SHOP',
         'SCHEDULE_START_DATE',
         'SCHEDULE_END_DATE',
         'MONDAY',
         'TUESDAY',
         'WEDNESDAY',
         'THURSDAY',
         'FRIDAY',
         'SATURDAY',
         'SUNDAY',
         'HOLIDAYS_ONLY',
         'SCHEDULE_MESSAGE'
      },
      'AppSetting': {
         'ID',
         'SETTING_KEY',
         'SETTING_VALUE'
      },
      'AttractionOpeningSchedule': {
         'ATTRACTION',
         'SCHEDULE_START_DATE',
         'SCHEDULE_END_DATE',
         'MONDAY',
         'TUESDAY',
         'WEDNESDAY',
         'THURSDAY',
         'FRIDAY',
         'SATURDAY',
         'SUNDAY',
         'HOLIDAYS_ONLY',
         'SCHEDULE_MESSAGE'
      },
      'ZoomobileRouteSchedule': {
         'ID',
         'SCHEDULE_START_DATE',
         'SCHEDULE_END_DATE',
         'ROUTE'
      },
      'ZoomobileStationStatus': {
         'ZOOMOBILE_STATION',
         'IS_CLOSED',
         'CLOSED_MESSAGE',
         'CLOSED_START',
         'CLOSED_END'
      },
      'GuardiansTalkSchedule': {
         'TALK_NAME',
         'LOCATION',
         'SCHEDULE_START_DATE',
         'SCHEDULE_END_DATE',
         'MONDAY',
         'TUESDAY',
         'WEDNESDAY',
         'THURSDAY',
         'FRIDAY',
         'SATURDAY',
         'SUNDAY',
         'TALK_TIME',
         'SCHEDULE_MESSAGE'
      },
      'GuardiansTalkCancellation': {
         'TALK_NAME',
         'LOCATION',
         'CANCELLATION_DATE',
         'TALK_TIME'
      },
      'WildEncounterSchedule': {
         'WILD_ENCOUNTER',
         'SCHEDULE_START_DATE',
         'SCHEDULE_END_DATE',
         'MONDAY',
         'TUESDAY',
         'WEDNESDAY',
         'THURSDAY',
         'FRIDAY',
         'SATURDAY',
         'SUNDAY',
         'ENCOUNTER_TIME',
         'SCHEDULE_MESSAGE'
      },
      'WildEncounterCancellation': {
         'WILD_ENCOUNTER',
         'CANCELLATION_DATE',
         'ENCOUNTER_TIME'
      },
      'Itinerary': {
         'ID',
         'IS_ACTIVE',
         'ITINERARY_DATE'
      },
      'ItineraryAnimal': {
         'SPECIES',
         'EXHIBIT'
      }
   }

   for table, expected in expected_columns.items():
      assert expected <= column_names( cursor, table )

   assert cursor.execute( 'SELECT COUNT(*) FROM Itinerary WHERE ID = 1;' ).fetchone()[ 0 ] == 1

   conn.close()
