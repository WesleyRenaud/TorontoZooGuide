from __future__ import annotations

from api.models.wild_encounter import WildEncounter
from api.wild_encounters.scheduling.wild_encounter_day_schedule_finder import WildEncounterDayScheduleFinder


ENCOUNTER_TIME = '3:30 PM'


def _encounter(
      *,
      name: str = 'Kangaroo',
      start_time: str = ENCOUNTER_TIME,
      is_available: bool = True,
      unavailable_message: str | None = None ) -> WildEncounter:
   return WildEncounter(
      name=name,
      meeting_spot='Wild Encounter - Eurasia Meeting Spot',
      link='https://example.test',
      start_time=start_time,
      end_time='4:15 PM',
      is_available=is_available,
      unavailable_message=unavailable_message )


def Test_FindOnDaySchedule_TestMatchingEncounter_ExpectEncounter() -> None:
   day_schedule = [ _encounter() ]

   match = WildEncounterDayScheduleFinder.find_on_day_schedule(
      day_schedule,
      'kangaroo',
      start_time=ENCOUNTER_TIME )

   assert match is not None
   assert match.name == 'Kangaroo'
   assert match.start_time == ENCOUNTER_TIME


def Test_FindOnDaySchedule_TestBlankEncounterName_ExpectNone() -> None:
   day_schedule = [ _encounter() ]

   match = WildEncounterDayScheduleFinder.find_on_day_schedule(
      day_schedule,
      '',
      start_time=ENCOUNTER_TIME )

   assert match is None


def Test_FindOnDaySchedule_TestUnavailableEncounter_ExpectUnavailableMatch() -> None:
   day_schedule = [
      _encounter(
         is_available=False,
         unavailable_message='Kangaroo is not scheduled on July 9.' ),
   ]

   match = WildEncounterDayScheduleFinder.find_on_day_schedule(
      day_schedule,
      'Kangaroo',
      start_time=ENCOUNTER_TIME )

   assert match is not None
   assert match.is_available is False
   assert match.unavailable_message == 'Kangaroo is not scheduled on July 9.'


def Test_FindOnDaySchedule_TestInvalidStartTime_ExpectNone() -> None:
   assert WildEncounterDayScheduleFinder.find_on_day_schedule(
      [ _encounter() ],
      'Kangaroo',
      start_time=None,
   ) is None


def Test_FindOnDaySchedule_TestNoMatchingStartTime_ExpectNone() -> None:
   assert WildEncounterDayScheduleFinder.find_on_day_schedule(
      [ _encounter( start_time='3:30 PM' ) ],
      'Kangaroo',
      start_time='2:00 PM',
   ) is None
