from __future__ import annotations

from api.itinerary.wild_encounter_schedule_item_key import WildEncounterScheduleItemKey
from api.models import WildEncounter
from api.wild_encounters.itinerary.wild_encounter_itinerary_validator import WildEncounterItineraryValidator


def Test_ValidateForItinerary_TestAvailableAndUnavailable_ExpectSplitDiffs() -> None:
   day_schedule = [
      WildEncounter(
         name='Kangaroo',
         meeting_spot='Wild Encounter - Eurasia Meeting Spot',
         link='https://www.torontozoo.com/tickets/wekangaroo',
         start_time='1:00 PM',
         maximum_duration=45,
         is_available=True ),
      WildEncounter(
         name='African Rainforest',
         meeting_spot='Wild Encounter - Africa Meeting Spot',
         link='https://www.torontozoo.com/tickets/weafricarainforest',
         start_time='2:00 PM',
         maximum_duration=45,
         is_available=False,
         unavailable_message='Unavailable.' ),
   ]

   result = WildEncounterItineraryValidator.validate_for_itinerary(
      wild_encounters_to_include=[
         WildEncounterScheduleItemKey( name='African Rainforest', start_time='14:00' ),
         WildEncounterScheduleItemKey( name='Kangaroo', start_time='13:00' ),
      ],
      day_schedule=day_schedule )

   assert [
      ( d.name, d.is_deleted, d.start_time, d.end_time )
      for d in result
   ] == [
      ( 'African Rainforest', True, '2:00 PM', '2:45 PM' ),
      ( 'Kangaroo', False, '1:00 PM', '1:45 PM' ),
   ]
