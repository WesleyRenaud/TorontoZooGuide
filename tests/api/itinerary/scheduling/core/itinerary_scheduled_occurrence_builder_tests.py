from __future__ import annotations

from api.itinerary.scheduling.core.scheduled_occurrence_builder import ScheduledOccurrenceBuilder
from api.models.wild_encounter import WildEncounter


KANGAROO_ENCOUNTER_TIME = '3:30 PM'
MAXIMUM_DURATION = 45


def _kangaroo_encounter( *, is_available: bool = True ) -> WildEncounter:
   return WildEncounter(
      name='Kangaroo',
      meeting_spot='Wild Encounter - Eurasia Meeting Spot',
      link='https://example.test/kangaroo',
      start_time=KANGAROO_ENCOUNTER_TIME,
      maximum_duration=MAXIMUM_DURATION,
      is_available=is_available )


def Test_WildEncounter_TestAvailableKangaroo_ExpectScheduledDiff() -> None:
   diff = ScheduledOccurrenceBuilder.wild_encounter(
      'Kangaroo',
      _kangaroo_encounter() )

   assert diff.name == 'Kangaroo'
   assert diff.is_deleted is False
   assert diff.start_time == KANGAROO_ENCOUNTER_TIME
   assert diff.end_time == '4:15 PM'
   assert diff.meeting_spot == 'Wild Encounter - Eurasia Meeting Spot'


def Test_WildEncounter_TestUnavailableEncounter_ExpectDeletedDiff() -> None:
   diff = ScheduledOccurrenceBuilder.wild_encounter(
      'Kangaroo',
      _kangaroo_encounter( is_available=False ) )

   assert diff.is_deleted is True
   assert diff.start_time == KANGAROO_ENCOUNTER_TIME
   assert diff.end_time == '4:15 PM'
