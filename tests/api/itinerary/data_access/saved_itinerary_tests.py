from __future__ import annotations

from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.shared.date_values import DateValues
from api.shared.enums.position import Position
from api.shared.enums.transportation_name import TransportationName


LION_TALK = 'African Lion'
RHINO_ENCOUNTER = 'White Rhinoceros'


def Test_TransportationNames_TestTransportationRows_ExpectNames() -> None:
   transportation = TransportationName.ZOOMOBILE
   transportation_rows = [
      ItineraryTransportationRecord(
         transportation=transportation,
         old_likelihood=None,
         new_likelihood=3,
         added_as_attraction=False ),
   ]
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      transportation_rows=transportation_rows )

   names = saved.transportation_names()

   assert names == [
      row.transportation for row in transportation_rows
   ]


def Test_GuardiansTalkNames_TestTalkRows_ExpectNames() -> None:
   start_time = '10:00 AM'
   duration_minutes = 30
   talk_rows = [
      ItineraryGuardiansTalkRecord(
         talk_name=LION_TALK,
         start_time=start_time,
         end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ),
         is_deleted=False ),
   ]
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      guardians_talk_rows=talk_rows )

   names = saved.guardians_talk_names()

   assert names == [ talk_rows[ Position.FIRST ].talk_name ]


def Test_WildEncounterNames_TestEncounterRows_ExpectNames() -> None:
   start_time = '1:00 PM'
   duration_minutes = 45
   encounter_rows = [
      ItineraryWildEncounterRecord(
         wild_encounter=RHINO_ENCOUNTER,
         start_time=start_time,
         end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ),
         is_deleted=False ),
   ]
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      wild_encounter_rows=encounter_rows )

   names = saved.wild_encounter_names()

   assert names == [ encounter_rows[ Position.FIRST ].wild_encounter ]
