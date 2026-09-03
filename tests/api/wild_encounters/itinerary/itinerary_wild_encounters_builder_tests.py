from __future__ import annotations

from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.models.wild_encounter import WildEncounter
from api.wild_encounters.itinerary.itinerary_wild_encounters_builder import ItineraryWildEncountersBuilder

BEAVER = 'Canadian Beaver Encounter'
OTTER = 'Otter Encounter'
SAVED_START = '11:00 AM'
SAVED_END = '11:30 AM'

def _wild_encounter(
      name: str,
      *,
      start_time: str | None = None,
      end_time: str | None = None,
      is_deleted: bool = False ) -> WildEncounter:
   return WildEncounter(
      name=name,
      meeting_spot='Meeting Spot',
      link='https://example.com',
      start_time=start_time,
      end_time=end_time,
      is_deleted=is_deleted )

def _saved_wild_encounter(
      *,
      wild_encounter: str,
      start_time: str | None = None,
      end_time: str | None = None,
      is_deleted: bool = False ) -> ItineraryWildEncounterRecord:
   return ItineraryWildEncounterRecord(
      wild_encounter=wild_encounter,
      start_time=start_time,
      end_time=end_time,
      is_deleted=is_deleted )

def Test_Build_TestMatchingSaved_ExpectTimesAndDeletedCopied() -> None:
   encounters = [ _wild_encounter( BEAVER ) ]
   saved = [
      _saved_wild_encounter(
         wild_encounter=BEAVER,
         start_time=SAVED_START,
         end_time=SAVED_END,
         is_deleted=True ),
   ]

   result = ItineraryWildEncountersBuilder.build( encounters, saved )

   assert result[ 0 ].start_time == SAVED_START
   assert result[ 0 ].end_time == SAVED_END
   assert result[ 0 ].is_deleted is True

def Test_Build_TestNoMatch_ExpectUnchanged() -> None:
   encounters = [
      _wild_encounter(
         OTTER,
         start_time='10:00 AM',
         end_time='10:20 AM',
         is_deleted=False ),
   ]
   saved = [
      _saved_wild_encounter(
         wild_encounter=BEAVER,
         start_time=SAVED_START,
         end_time=SAVED_END,
         is_deleted=True ),
   ]

   result = ItineraryWildEncountersBuilder.build( encounters, saved )

   assert result[ 0 ].name == OTTER
   assert result[ 0 ].start_time == '10:00 AM'
   assert result[ 0 ].end_time == '10:20 AM'
   assert result[ 0 ].is_deleted is False

def Test_Build_TestSortsByNameAndStartTime_ExpectOrdered() -> None:
   encounters = [
      _wild_encounter( OTTER, start_time='2:00 PM' ),
      _wild_encounter( BEAVER, start_time='1:00 PM' ),
      _wild_encounter( BEAVER, start_time='11:00 AM' ),
   ]

   result = ItineraryWildEncountersBuilder.build( encounters, [] )

   assert [ ( encounter.name, encounter.start_time ) for encounter in result ] == [
      ( BEAVER, '11:00 AM' ),
      ( BEAVER, '1:00 PM' ),
      ( OTTER, '2:00 PM' ),
   ]
