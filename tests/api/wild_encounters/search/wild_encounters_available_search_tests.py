from __future__ import annotations

from datetime import date

from api.models.wild_encounter import WildEncounter
from api.wild_encounters.data_access.wild_encounter_schedule_record import WildEncounterScheduleRecord
from api.wild_encounters.scheduling.wild_encounter_day_schedule_builder import WildEncounterDayScheduleBuilder
from api.wild_encounters.search.wild_encounters_matching_query_builder import WildEncountersMatchingQueryBuilder


ENCOUNTER_NAME = 'Mischevious Meerkats'
MONDAY_VISIT_DATE = date( 2026, 6, 15 )
SUNDAY_VISIT_DATE = date( 2026, 6, 21 )
STATION_COORD = 0.0
ENCOUNTER_TIME = '2:00 PM'


def _schedule_record( *, monday: bool, wednesday: bool, thursday: bool, saturday: bool ) -> WildEncounterScheduleRecord:
   return WildEncounterScheduleRecord(
      name=ENCOUNTER_NAME,
      meeting_spot='Africa Savanna',
      link=None,
      maximum_duration=45,
      x_coord=STATION_COORD,
      y_coord=STATION_COORD,
      region='Africa',
      schedule_start_date='2026-06-01',
      schedule_end_date='2026-06-30',
      monday=monday,
      tuesday=False,
      wednesday=wednesday,
      thursday=thursday,
      friday=False,
      saturday=saturday,
      sunday=False,
      encounter_time=ENCOUNTER_TIME,
      is_cancelled=False )


def _available_encounters_for( target_date: date ) -> list[ WildEncounter ]:
   return WildEncounterDayScheduleBuilder.filter_available(
      WildEncounterDayScheduleBuilder.build_for_target_date(
         [ _schedule_record(
            monday=True,
            wednesday=True,
            thursday=True,
            saturday=True ) ],
         target_date ) )


def Test_SearchAvailableEncounters_TestScheduledWeekday_ExpectMatchingEncounter() -> None:
   available_encounters = _available_encounters_for( MONDAY_VISIT_DATE )

   matches = WildEncountersMatchingQueryBuilder.build(
      available_encounters,
      ENCOUNTER_NAME )

   assert [ encounter.name for encounter in matches ] == [ ENCOUNTER_NAME ]


def Test_SearchAvailableEncounters_TestUnscheduledWeekday_ExpectNoMatches() -> None:
   available_encounters = _available_encounters_for( SUNDAY_VISIT_DATE )

   matches = WildEncountersMatchingQueryBuilder.build(
      available_encounters,
      ENCOUNTER_NAME )

   assert matches == []
   assert all( encounter.name != ENCOUNTER_NAME for encounter in available_encounters )
