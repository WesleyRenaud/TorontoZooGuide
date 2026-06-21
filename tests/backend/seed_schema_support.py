from __future__ import annotations

from api.types import Cursor, Row


def column_names( cursor: Cursor, table: str ) -> set[ str ]:
   return {
      row[ 1 ]
      for row in cursor.execute( f'PRAGMA table_info( { table } );' ).fetchall()
   }


def column_info( cursor: Cursor, table: str, column: str ) -> Row:
   return next(
      row
      for row in cursor.execute( f'PRAGMA table_info( { table } );' ).fetchall()
      if row[ 1 ] == column
   )


def table_count( cursor: Cursor, table: str ) -> int:
   return cursor.execute( f'SELECT COUNT(*) FROM { table };' ).fetchone()[ 0 ]


PARTIAL_RUNTIME_TABLES = {
   'AnimalStatus': 'SPECIES TEXT, EXHIBIT TEXT',
   'AnimalVisibilitySchedule': 'SPECIES TEXT, EXHIBIT TEXT',
   'AnimalViewingAlert': 'SPECIES TEXT, EXHIBIT TEXT',
   'ExhibitStatus': 'EXHIBIT TEXT',
   'RestroomStatus': 'RESTROOM TEXT',
   'RestroomAlert': 'RESTROOM TEXT',
   'ZooUpdate': 'TITLE TEXT, START_DATE DATE',
   'RestaurantOpeningSchedule': 'RESTAURANT TEXT',
   'RestaurantScheduleOverride': 'RESTAURANT TEXT',
   'GiftShopOpeningSchedule': 'GIFT_SHOP TEXT',
   'GiftShopScheduleOverride': 'GIFT_SHOP TEXT',
   'AppSetting': 'ID INTEGER',
   'AttractionOpeningSchedule': 'ATTRACTION TEXT',
   'AttractionScheduleOverride': 'ATTRACTION TEXT',
   'ZoomobileRouteSchedule': 'ID INTEGER',
   'ZoomobileStationStatus': 'ZOOMOBILE_STATION TEXT',
   'GuardiansTalkSchedule': 'TALK_NAME TEXT, LOCATION TEXT',
   'GuardiansTalkCancellation': 'TALK_NAME TEXT, LOCATION TEXT',
   'WildEncounterSchedule': 'WILD_ENCOUNTER TEXT',
   'WildEncounterCancellation': 'WILD_ENCOUNTER TEXT',
   'ItineraryDate': 'ITINERARY_DATE DATE',
   'ItineraryAnimal': 'SPECIES TEXT',
   'ItineraryGuardiansTalk': 'TALK_NAME TEXT',
   'ItineraryWildEncounter': 'WILD_ENCOUNTER TEXT',
   'ItineraryEvent': 'EVENT_TYPE TEXT',
}

EXPECTED_RUNTIME_COLUMNS = {
   'AnimalStatus': {
      'SPECIES',
      'EXHIBIT',
      'IS_OFF_DISPLAY',
      'VIEWING_SCOPE',
      'OFF_DISPLAY_MESSAGE',
      'OFF_DISPLAY_START',
      'OFF_DISPLAY_END',
   },
   'AnimalVisibilitySchedule': {
      'SPECIES',
      'EXHIBIT',
      'SCHEDULE_START_DATE',
      'SCHEDULE_END_DATE',
      'DAILY_START_TIME',
      'DAILY_END_TIME',
      'VIEWING_MESSAGE',
   },
   'AnimalViewingAlert': {
      'SPECIES',
      'EXHIBIT',
      'ALERT_MESSAGE',
      'ALERT_START_DATE',
      'ALERT_END_DATE',
   },
   'ExhibitStatus': {
      'EXHIBIT',
      'IS_CLOSED',
      'CLOSED_MESSAGE',
      'CLOSED_START',
      'CLOSED_END',
   },
   'RestroomStatus': {
      'RESTROOM',
      'IS_CLOSED',
      'CLOSED_MESSAGE',
      'CLOSED_START',
      'CLOSED_END',
   },
   'RestroomAlert': {
      'RESTROOM',
      'ALERT_MESSAGE',
      'ALERT_START_DATE',
      'ALERT_END_DATE',
   },
   'ZooUpdate': {
      'TITLE',
      'DESCRIPTION',
      'UPDATE_TYPE',
      'START_DATE',
      'END_DATE',
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
      'SCHEDULE_MESSAGE',
   },
   'RestaurantScheduleOverride': {
      'RESTAURANT',
      'OVERRIDE_START_DATE',
      'OVERRIDE_END_DATE',
      'IS_CLOSED',
      'OVERRIDE_MESSAGE',
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
      'SCHEDULE_MESSAGE',
   },
   'GiftShopScheduleOverride': {
      'GIFT_SHOP',
      'OVERRIDE_START_DATE',
      'OVERRIDE_END_DATE',
      'IS_CLOSED',
      'OVERRIDE_MESSAGE',
   },
   'AppSetting': {
      'ID',
      'SETTING_KEY',
      'SETTING_VALUE',
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
      'SCHEDULE_MESSAGE',
   },
   'AttractionScheduleOverride': {
      'ATTRACTION',
      'OVERRIDE_START_DATE',
      'OVERRIDE_END_DATE',
      'IS_CLOSED',
      'OVERRIDE_MESSAGE',
   },
   'ZoomobileRouteSchedule': {
      'ID',
      'SCHEDULE_START_DATE',
      'SCHEDULE_END_DATE',
      'ROUTE',
   },
   'ZoomobileStationStatus': {
      'ZOOMOBILE_STATION',
      'IS_CLOSED',
      'CLOSED_MESSAGE',
      'CLOSED_START',
      'CLOSED_END',
   },
   'GuardiansTalkSchedule': {
      'TALK_NAME',
      'LOCATION',
      'SCHEDULE_START_DATE',
      'SCHEDULE_END_DATE',
      'MONDAY_TIME',
      'TUESDAY_TIME',
      'WEDNESDAY_TIME',
      'THURSDAY_TIME',
      'FRIDAY_TIME',
      'SATURDAY_TIME',
      'SUNDAY_TIME',
      'SCHEDULE_MESSAGE',
   },
   'GuardiansTalkCancellation': {
      'TALK_NAME',
      'LOCATION',
      'CANCELLATION_DATE',
      'TALK_TIME',
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
      'SCHEDULE_MESSAGE',
   },
   'WildEncounterCancellation': {
      'WILD_ENCOUNTER',
      'CANCELLATION_DATE',
      'ENCOUNTER_TIME',
   },
   'ItineraryDate': {
      'ITINERARY_DATE',
      'ARRIVAL_TIME',
      'DEPARTURE_TIME',
   },
   'ItineraryAnimal': {
      'SPECIES',
      'EXHIBIT',
      'OLD_LIKELIHOOD',
      'NEW_LIKELIHOOD',
      'IS_ADDED',
      'START_TIME',
      'END_TIME',
   },
   'ItineraryAttraction': {
      'ATTRACTION',
      'OLD_LIKELIHOOD',
      'NEW_LIKELIHOOD',
      'START_TIME',
      'END_TIME',
   },
   'ItineraryGuardiansTalk': {
      'TALK_NAME',
      'START_TIME',
      'END_TIME',
      'IS_DELETED',
   },
   'ItineraryWildEncounter': {
      'WILD_ENCOUNTER',
      'START_TIME',
      'END_TIME',
      'IS_DELETED',
   },
   'ItineraryEvent': {
      'EVENT_TYPE',
      'START_TIME',
      'END_TIME',
   },
   'ItineraryWalkRouteStop': {
      'STOP_SEQUENCE',
      'SCHEDULE_ITEM_KIND',
      'ITEM_KEY',
      'WALK_NODE_ID',
      'START_TIME',
      'END_TIME',
   },
   'ItineraryWalkRoutePoint': {
      'POINT_SEQUENCE',
      'WALK_NODE_ID',
      'X',
      'Y',
      'X_PX',
      'Y_PX',
   },
   'ItineraryWalkRouteLeg': {
      'LEG_SEQUENCE',
      'FROM_ITEM_KEY',
      'TO_ITEM_KEY',
      'FROM_SCHEDULE_ITEM_KIND',
      'TO_SCHEDULE_ITEM_KIND',
      'FROM_POINT_SEQUENCE',
      'TO_POINT_SEQUENCE',
   },
}
