from __future__ import annotations

from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary

ZOOMOBILE = 'Zoomobile'
LION_TALK = 'African Lion'
RHINO_ENCOUNTER = 'White Rhinoceros'

def Test_TransportationNames_TestTransportationRows_ExpectNames() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      transportation_rows=[
         ItineraryTransportationRecord(
            transportation=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=False ),
      ] )

   assert saved.transportation_names() == [ ZOOMOBILE ]

def Test_GuardiansTalkNames_TestTalkRows_ExpectNames() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      guardians_talk_rows=[
         ItineraryGuardiansTalkRecord(
            talk_name=LION_TALK,
            start_time='10:00 AM',
            end_time='10:30 AM',
            is_deleted=False ),
      ] )

   assert saved.guardians_talk_names() == [ LION_TALK ]

def Test_WildEncounterNames_TestEncounterRows_ExpectNames() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      wild_encounter_rows=[
         ItineraryWildEncounterRecord(
            wild_encounter=RHINO_ENCOUNTER,
            start_time='1:00 PM',
            end_time='1:45 PM',
            is_deleted=False ),
      ] )

   assert saved.wild_encounter_names() == [ RHINO_ENCOUNTER ]
