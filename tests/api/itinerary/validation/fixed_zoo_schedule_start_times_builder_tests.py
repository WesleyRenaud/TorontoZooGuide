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
from api.shared.calendar_dates import DateValues


VISIT_DATE = date( 2026, 6, 15 )
GREVYS_ZEBRA = "Grevy's Zebra"
AFRICAN_RAINFOREST = 'African Rainforest'
TALK_DURATION_MINUTES = 30
ENCOUNTER_DURATION_MINUTES = 45


def Test_FromSavedItinerary_TestActiveTalksAndEncounters_ExpectStartTimes() -> None:
   talk_start_time = '12:00 PM'
   encounter_start_time = '2:00 PM'
   active_talk = ItineraryGuardiansTalkRecord(
      talk_name=GREVYS_ZEBRA,
      start_time=talk_start_time,
      end_time=DateValues.add_minutes_to_time( talk_start_time, TALK_DURATION_MINUTES ),
      is_deleted=False )
   deleted_talk = ItineraryGuardiansTalkRecord(
      talk_name='Deleted Talk',
      start_time='1:00 PM',
      end_time=DateValues.add_minutes_to_time( '1:00 PM', TALK_DURATION_MINUTES ),
      is_deleted=True )
   encounter = ItineraryWildEncounterRecord(
      wild_encounter=AFRICAN_RAINFOREST,
      start_time=encounter_start_time,
      end_time=DateValues.add_minutes_to_time(
         encounter_start_time,
         ENCOUNTER_DURATION_MINUTES ),
      is_deleted=False )
   saved = SavedItinerary(
      date_value=VISIT_DATE.isoformat(),
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      guardians_talk_rows=[ active_talk, deleted_talk ],
      wild_encounter_rows=[ encounter ],
   )

   start_times = FixedZooScheduleStartTimesBuilder.from_saved_itinerary( saved )

   assert start_times == [ active_talk.start_time, encounter.start_time ]


def Test_FromSavedItinerary_TestNone_ExpectEmpty() -> None:
   saved = None

   start_times = FixedZooScheduleStartTimesBuilder.from_saved_itinerary( saved )

   assert start_times == []


def Test_FromSaveInput_TestTalksAndEncounters_ExpectStartTimes() -> None:
   talk = ItineraryGuardiansTalkInput( name=GREVYS_ZEBRA, start_time='12:00' )
   untimed_talk = ItineraryGuardiansTalkInput( name='No Time Talk', start_time=None )
   encounter = WildEncounterScheduleItemKey(
      name=AFRICAN_RAINFOREST,
      start_time='14:00' )
   save_input = ItinerarySaveInput(
      date=VISIT_DATE,
      arrival_time='09:30',
      departure_time='17:00',
      guardians_talks=[ talk, untimed_talk ],
      wild_encounters=[ encounter ],
   )

   start_times = FixedZooScheduleStartTimesBuilder.from_save_input( save_input )

   assert start_times == [ talk.start_time, encounter.start_time ]


def Test_Merge_TestMultipleGroups_ExpectConcatenated() -> None:
   morning = [ '10:00' ]
   afternoon = [ '12:00', '14:00' ]

   merged = FixedZooScheduleStartTimesBuilder.merge( morning, afternoon )

   assert merged == [ *morning, *afternoon ]


def Test_FromSaveInput_TestPreOpenWildEncounter_ExpectStartTime() -> None:
   encounter = WildEncounterScheduleItemKey(
      name=AFRICAN_RAINFOREST,
      start_time='08:45' )
   save_input = ItinerarySaveInput(
      date=VISIT_DATE,
      arrival_time=encounter.start_time,
      departure_time='17:00',
      wild_encounters=[ encounter ],
   )

   start_times = FixedZooScheduleStartTimesBuilder.from_save_input( save_input )

   assert start_times == [ encounter.start_time ]


def Test_FromSavedItinerary_TestUntimedEncounter_ExpectTalkOnly() -> None:
   talk_start_time = '12:00 PM'
   talk = ItineraryGuardiansTalkRecord(
      talk_name=GREVYS_ZEBRA,
      start_time=talk_start_time,
      end_time=DateValues.add_minutes_to_time( talk_start_time, TALK_DURATION_MINUTES ),
      is_deleted=False )
   untimed_encounter = ItineraryWildEncounterRecord(
      wild_encounter=AFRICAN_RAINFOREST,
      start_time=None,
      end_time=None,
      is_deleted=False )
   saved = SavedItinerary(
      date_value=VISIT_DATE.isoformat(),
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      guardians_talk_rows=[ talk ],
      wild_encounter_rows=[ untimed_encounter ],
   )

   start_times = FixedZooScheduleStartTimesBuilder.from_saved_itinerary( saved )

   assert start_times == [ talk.start_time ]


def Test_FromSaveInput_TestUntimedEncounter_ExpectTalkOnly() -> None:
   talk = ItineraryGuardiansTalkInput( name=GREVYS_ZEBRA, start_time='12:00' )
   save_input = ItinerarySaveInput(
      date=VISIT_DATE,
      arrival_time='09:30',
      departure_time='17:00',
      guardians_talks=[ talk ],
      wild_encounters=[ Mock( start_time=None ) ],  # type: ignore[ list-item ]
   )

   start_times = FixedZooScheduleStartTimesBuilder.from_save_input( save_input )

   assert start_times == [ talk.start_time ]
