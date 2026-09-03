from __future__ import annotations

from datetime import date
from unittest.mock import Mock

from api.itinerary.data_access.itinerary_guardians_talk_input import ItineraryGuardiansTalkInput
from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.itinerary.data_access.itinerary_save_input import ItinerarySaveInput
from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.validation.fixed_zoo_schedule_start_times_builder import FixedZooScheduleStartTimesBuilder
from api.itinerary.wild_encounter_schedule_item_key import WildEncounterScheduleItemKey


def Test_FromSavedItinerary_TestActiveTalksAndEncounters_ExpectStartTimes() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      guardians_talk_rows=[
         ItineraryGuardiansTalkRecord(
            talk_name="Grevy's Zebra",
            start_time='12:00 PM',
            end_time='12:30 PM',
            is_deleted=False ),
         ItineraryGuardiansTalkRecord(
            talk_name='Deleted Talk',
            start_time='1:00 PM',
            end_time='1:30 PM',
            is_deleted=True ),
      ],
      wild_encounter_rows=[
         ItineraryWildEncounterRecord(
            wild_encounter='African Rainforest',
            start_time='2:00 PM',
            end_time='2:45 PM',
            is_deleted=False ),
      ],
   )

   assert FixedZooScheduleStartTimesBuilder.from_saved_itinerary( saved ) == [
      '12:00 PM',
      '2:00 PM',
   ]


def Test_FromSavedItinerary_TestNone_ExpectEmpty() -> None:
   assert FixedZooScheduleStartTimesBuilder.from_saved_itinerary( None ) == []


def Test_FromSaveInput_TestTalksAndEncounters_ExpectStartTimes() -> None:
   save_input = ItinerarySaveInput(
      date=date( 2026, 6, 15 ),
      arrival_time='09:30',
      departure_time='17:00',
      guardians_talks=[
         ItineraryGuardiansTalkInput( name="Grevy's Zebra", start_time='12:00' ),
         ItineraryGuardiansTalkInput( name='No Time Talk', start_time=None ),
      ],
      wild_encounters=[
         WildEncounterScheduleItemKey( name='African Rainforest', start_time='14:00' ),
      ],
   )

   assert FixedZooScheduleStartTimesBuilder.from_save_input( save_input ) == [
      '12:00',
      '2:00 PM',
   ]


def Test_Merge_TestMultipleGroups_ExpectConcatenated() -> None:
   assert FixedZooScheduleStartTimesBuilder.merge(
      [ '10:00' ],
      [ '12:00', '14:00' ],
   ) == [ '10:00', '12:00', '14:00' ]


def Test_FromSaveInput_TestPreOpenWildEncounter_ExpectStartTime() -> None:
   save_input = ItinerarySaveInput(
      date=date( 2026, 6, 15 ),
      arrival_time='08:45',
      departure_time='17:00',
      wild_encounters=[
         WildEncounterScheduleItemKey( name='African Rainforest', start_time='08:45' ),
      ],
   )

   assert FixedZooScheduleStartTimesBuilder.from_save_input( save_input ) == [ '8:45 AM' ]


def Test_FromSavedItinerary_TestUntimedEncounter_ExpectTalkOnly() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      guardians_talk_rows=[
         ItineraryGuardiansTalkRecord(
            talk_name="Grevy's Zebra",
            start_time='12:00 PM',
            end_time='12:30 PM',
            is_deleted=False ),
      ],
      wild_encounter_rows=[
         ItineraryWildEncounterRecord(
            wild_encounter='African Rainforest',
            start_time=None,
            end_time=None,
            is_deleted=False ),
      ],
   )

   assert FixedZooScheduleStartTimesBuilder.from_saved_itinerary( saved ) == [ '12:00 PM' ]


def Test_FromSaveInput_TestUntimedEncounter_ExpectTalkOnly() -> None:
   save_input = ItinerarySaveInput(
      date=date( 2026, 6, 15 ),
      arrival_time='09:30',
      departure_time='17:00',
      guardians_talks=[
         ItineraryGuardiansTalkInput( name="Grevy's Zebra", start_time='12:00' ),
      ],
      wild_encounters=[ Mock( start_time=None ) ],  # type: ignore[ list-item ]
   )

   assert FixedZooScheduleStartTimesBuilder.from_save_input( save_input ) == [ '12:00' ]
