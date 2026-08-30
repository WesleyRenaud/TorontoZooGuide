from __future__ import annotations

from datetime import date

from api.models.wild_encounter import WildEncounter
from api.wild_encounters.data_access.wild_encounter_schedule_record import WildEncounterScheduleRecord
from api.wild_encounters.scheduling.wild_encounter_day_schedule_builder import WildEncounterDayScheduleBuilder


STATION_COORD = 0.0
MONDAY_VISIT_DATE = date( 2026, 6, 15 )
TUESDAY_VISIT_DATE = date( 2026, 6, 16 )
ENCOUNTER_TIME = '2:00 PM'
MAXIMUM_DURATION = 45


def _schedule_record(
      *,
      monday: bool = True,
      tuesday: bool = False,
      is_cancelled: bool = False ) -> WildEncounterScheduleRecord:
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
      encounter_time=ENCOUNTER_TIME,
      is_cancelled=is_cancelled )


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


def Test_FilterAvailable_TestMixedAvailability_ExpectAvailableOnly() -> None:
   wild_encounters = [
      WildEncounter(
         name='Available Encounter',
         meeting_spot='Africa',
         link='',
         is_available=True ),
      WildEncounter(
         name='Unavailable Encounter',
         meeting_spot='Africa',
         link='',
         is_available=False ),
   ]

   available_encounters = WildEncounterDayScheduleBuilder.filter_available( wild_encounters )

   assert [ encounter.name for encounter in available_encounters ] == [ 'Available Encounter' ]
