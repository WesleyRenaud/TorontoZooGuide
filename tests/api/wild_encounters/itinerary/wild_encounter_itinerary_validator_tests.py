from __future__ import annotations

from api.itinerary.wild_encounter_schedule_item_key import WildEncounterScheduleItemKey
from api.models.wild_encounter import WildEncounter
from api.wild_encounters.itinerary.wild_encounter_itinerary_validator import WildEncounterItineraryValidator


DAY_SCHEDULE = [
   WildEncounter(
      name='Kangaroo',
      meeting_spot='Wild Encounter - Eurasia Meeting Spot',
      link='https://example.com/kangaroo',
      start_time='9:00 AM',
      end_time='9:45 AM' ),
   WildEncounter(
      name='African Rainforest',
      meeting_spot='Wild Encounter - Africa Meeting Spot',
      link='https://example.com/rainforest',
      start_time='2:00 PM',
      end_time='2:45 PM' ),
]


def Test_ValidateForItinerary_TestCaseInsensitiveNames_ExpectSortedMatches() -> None:
   result = WildEncounterItineraryValidator.validate_for_itinerary(
      [
         WildEncounterScheduleItemKey( name=' kangaroo ', start_time='09:00' ),
         WildEncounterScheduleItemKey( name='AFRICAN RAINFOREST', start_time='14:00' ),
      ],
      DAY_SCHEDULE )

   assert [
      ( diff.name, diff.is_deleted )
      for diff in result
   ] == [
      ( 'Kangaroo', False ),
      ( 'African Rainforest', False ),
   ]
