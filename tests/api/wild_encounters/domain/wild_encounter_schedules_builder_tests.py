from __future__ import annotations

from datetime import date

from api.wild_encounters.data_access.wild_encounter_schedule_listing_record import WildEncounterScheduleListingRecord
from api.wild_encounters.domain.wild_encounter_schedule import WildEncounterSchedule
from api.wild_encounters.domain.wild_encounter_schedules_builder import WildEncounterSchedulesBuilder


GIRAFFE = 'Giraffe'


def _record(
      name: str,
      start: str,
      end: str | None,
      *,
      monday: bool = False,
      sunday: bool = False ) -> WildEncounterScheduleListingRecord:
   return WildEncounterScheduleListingRecord(
      wild_encounter=name,
      schedule_start_date=start,
      schedule_end_date=end,
      encounter_time='11:00 AM',
      monday=monday,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=sunday,
   )


def _monday_schedule() -> WildEncounterSchedule:
   return WildEncounterSchedulesBuilder.build( [
      _record( GIRAFFE, '2026-11-01', '2026-11-05', monday=True ),
   ] )[ 0 ]


def Test_Build_TestListings_ExpectNameDatesAndWeekdays() -> None:
   schedules = WildEncounterSchedulesBuilder.build( [
      _record( GIRAFFE, '2026-11-01', '2026-11-05', monday=True ),
      _record( 'Kangaroo', '2026-11-02', None, sunday=True ),
   ] )

   assert schedules == [
      WildEncounterSchedule(
         name=GIRAFFE,
         start=date( 2026, 11, 1 ),
         end=date( 2026, 11, 5 ),
         encounter_time='11:00 AM',
         monday=True,
         tuesday=False,
         wednesday=False,
         thursday=False,
         friday=False,
         saturday=False,
         sunday=False,
      ),
      WildEncounterSchedule(
         name='Kangaroo',
         start=date( 2026, 11, 2 ),
         end=None,
         encounter_time='11:00 AM',
         monday=False,
         tuesday=False,
         wednesday=False,
         thursday=False,
         friday=False,
         saturday=False,
         sunday=True,
      ),
   ]


def Test_Covers_TestOpenEndedRange_ExpectStartThroughLaterDates() -> None:
   schedule = _monday_schedule()

   assert not schedule.covers( date( 2026, 10, 31 ) )
   assert schedule.covers( date( 2026, 11, 1 ) )
   assert schedule.covers( date( 2026, 11, 4 ) )
   assert not schedule.covers( date( 2026, 11, 5 ) )


def Test_WeekdayIndexes_TestMondayAndSunday_ExpectPythonWeekdays() -> None:
   schedule = WildEncounterSchedulesBuilder.build( [
      _record( GIRAFFE, '2026-11-01', None, monday=True, sunday=True ),
   ] )[ 0 ]

   assert schedule.weekday_indexes() == { 0, 6 }


def Test_Dates_TestMondayInsideRange_ExpectThatMonday() -> None:
   schedule = _monday_schedule()

   assert WildEncounterSchedule.dates(
      [ schedule ],
      GIRAFFE,
      date( 2026, 11, 1 ),
      date( 2026, 11, 5 ),
   ) == [ date( 2026, 11, 2 ) ]
