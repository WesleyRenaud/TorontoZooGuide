from __future__ import annotations

from datetime import date

from api.models.wild_encounter import WildEncounter
from api.wild_encounters.data_access.wild_encounter_schedule_record import WildEncounterScheduleRecord
from api.wild_encounters.scheduling.wild_encounter_day_schedule_builder import WildEncounterDayScheduleBuilder


STATION_COORD = 0.0
MONDAY_VISIT_DATE = date( 2026, 6, 15 )
TUESDAY_VISIT_DATE = date( 2026, 6, 16 )
OUTSIDE_SCHEDULE_VISIT_DATE = date( 2026, 7, 9 )
ENCOUNTER_TIME = '2:00 PM'
KANGAROO_ENCOUNTER_TIME = '3:30 PM'
MAXIMUM_DURATION = 45


def _schedule_record(
      *,
      monday: bool = True,
      tuesday: bool = False,
      is_cancelled: bool = False,
      encounter_time: str = ENCOUNTER_TIME ) -> WildEncounterScheduleRecord:
   return WildEncounterScheduleRecord(
      name='Giraffe Feeding',
      meeting_spot='Africa Savanna',
      link='https://example.com',
      maximum_duration=MAXIMUM_DURATION,
      x_coord=STATION_COORD,
      y_coord=STATION_COORD,
      region='Africa',
      schedule_start_date='2026-06-01',
      schedule_end_date='2026-09-30',
      monday=monday,
      tuesday=tuesday,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      encounter_time=encounter_time,
      is_cancelled=is_cancelled )


def _kangaroo_schedule_record() -> WildEncounterScheduleRecord:
   return WildEncounterScheduleRecord(
      name='Kangaroo',
      meeting_spot='Wild Encounter - Eurasia Meeting Spot',
      link='https://example.test',
      maximum_duration=MAXIMUM_DURATION,
      x_coord=STATION_COORD,
      y_coord=STATION_COORD,
      region='Eurasia Wilds',
      schedule_start_date='2026-06-28',
      schedule_end_date='2026-07-05',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      encounter_time=KANGAROO_ENCOUNTER_TIME,
      is_cancelled=False )


def _active_kangaroo_schedule_record() -> WildEncounterScheduleRecord:
   return WildEncounterScheduleRecord(
      name='Kangaroo',
      meeting_spot='Wild Encounter - Eurasia Meeting Spot',
      link='https://example.test',
      maximum_duration=MAXIMUM_DURATION,
      x_coord=STATION_COORD,
      y_coord=STATION_COORD,
      region='Eurasia Wilds',
      schedule_start_date='2026-07-06',
      schedule_end_date=None,
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      encounter_time=KANGAROO_ENCOUNTER_TIME,
      is_cancelled=False )


def _wild_encounter(
      *,
      name: str,
      is_available: bool ) -> WildEncounter:
   return WildEncounter(
      name=name,
      meeting_spot='Africa',
      link='',
      is_available=is_available )


def Test_BuildForTargetDate_TestMultipleTimesOnSameDay_ExpectAvailableEncounters() -> None:
   encounters = WildEncounterDayScheduleBuilder.build_for_target_date(
      [
         _schedule_record(),
         _schedule_record( encounter_time='3:30 PM' ),
      ],
      MONDAY_VISIT_DATE )

   available_times = sorted(
      encounter.start_time
      for encounter in encounters
      if encounter.is_available )

   assert available_times == [ '2:00 PM', '3:30 PM' ]


def Test_BuildForTargetDate_TestMatchingWeekday_ExpectAvailableEncounter() -> None:
   encounters = WildEncounterDayScheduleBuilder.build_for_target_date(
      [ _schedule_record() ],
      MONDAY_VISIT_DATE )

   assert len( encounters ) == 1
   assert encounters[ 0 ].name == 'Giraffe Feeding'
   assert encounters[ 0 ].is_available is True
   assert encounters[ 0 ].unavailable_message is None
   assert encounters[ 0 ].end_time == '2:45 PM'


def Test_BuildForTargetDate_TestWrongWeekday_ExpectUnavailableEncounter() -> None:
   encounters = WildEncounterDayScheduleBuilder.build_for_target_date(
      [ _schedule_record() ],
      TUESDAY_VISIT_DATE )

   assert encounters[ 0 ].is_available is False
   assert encounters[ 0 ].name in encounters[ 0 ].unavailable_message


def Test_BuildForTargetDate_TestCancelledEncounter_ExpectUnavailableEncounter() -> None:
   encounters = WildEncounterDayScheduleBuilder.build_for_target_date(
      [ _schedule_record( is_cancelled=True ) ],
      MONDAY_VISIT_DATE )

   assert encounters[ 0 ].is_available is False
   assert 'Giraffe Feeding' in encounters[ 0 ].unavailable_message


def Test_BuildForTargetDate_TestVisitDateOutsideScheduleRange_ExpectUnavailableEncounter() -> None:
   encounters = WildEncounterDayScheduleBuilder.build_for_target_date(
      [ _kangaroo_schedule_record() ],
      OUTSIDE_SCHEDULE_VISIT_DATE )

   assert len( encounters ) == 1
   assert encounters[ 0 ].is_available is False
   assert encounters[ 0 ].unavailable_message is not None


def Test_BuildForTargetDate_TestActiveKangarooThursday_ExpectAvailableEncounter() -> None:
   encounters = WildEncounterDayScheduleBuilder.build_for_target_date(
      [ _active_kangaroo_schedule_record() ],
      OUTSIDE_SCHEDULE_VISIT_DATE )

   assert len( encounters ) == 1
   assert encounters[ 0 ].name == 'Kangaroo'
   assert encounters[ 0 ].is_available is True
   assert encounters[ 0 ].start_time == KANGAROO_ENCOUNTER_TIME
   assert encounters[ 0 ].end_time == '4:15 PM'


def Test_FilterAvailable_TestMixedAvailability_ExpectAvailableOnly() -> None:
   wild_encounters = [
      _wild_encounter( name='Available Encounter', is_available=True ),
      _wild_encounter( name='Unavailable Encounter', is_available=False ),
   ]

   available_encounters = WildEncounterDayScheduleBuilder.filter_available( wild_encounters )

   assert [ encounter.name for encounter in available_encounters ] == [ 'Available Encounter' ]
