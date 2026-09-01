from __future__ import annotations

from api.itinerary.wild_encounter_schedule_item_key import WildEncounterScheduleItemKey
from api.models.wild_encounter import WildEncounter
from api.wild_encounters.itinerary.wild_encounter_itinerary_validator import WildEncounterItineraryValidator


KANGAROO_ENCOUNTER_TIME = '3:30 PM'

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


def Test_ValidateForItinerary_TestPreOpenEncounterTime_ExpectPreservedStartTime() -> None:
   result = WildEncounterItineraryValidator.validate_for_itinerary(
      [
         WildEncounterScheduleItemKey( name='African Rainforest', start_time='08:45' ),
      ],
      [
         WildEncounter(
            name='African Rainforest',
            meeting_spot='Wild Encounter - Africa Meeting Spot',
            link='https://example.com/rainforest',
            start_time='8:45 AM',
            maximum_duration=45 ),
      ] )

   assert len( result ) == 1
   assert result[ 0 ].start_time == '8:45 AM'
   assert result[ 0 ].end_time == '9:30 AM'


def Test_ValidateForItinerary_TestKangarooAt330PmThursday_ExpectPreservedSchedule() -> None:
   day_schedule = [
      WildEncounter(
         name='Kangaroo',
         meeting_spot='Wild Encounter - Eurasia Meeting Spot',
         link='https://example.test/kangaroo',
         start_time=KANGAROO_ENCOUNTER_TIME,
         maximum_duration=45,
         is_available=True ),
   ]

   result = WildEncounterItineraryValidator.validate_for_itinerary(
      [
         WildEncounterScheduleItemKey(
            name='Kangaroo',
            start_time=KANGAROO_ENCOUNTER_TIME ),
      ],
      day_schedule )

   assert len( result ) == 1
   assert result[ 0 ].name == 'Kangaroo'
   assert result[ 0 ].is_deleted is False
   assert result[ 0 ].start_time == KANGAROO_ENCOUNTER_TIME
   assert result[ 0 ].end_time == '4:15 PM'
