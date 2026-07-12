from __future__ import annotations

from itinerary.support import CAROUSEL, GUARDIANS_TALK, guardians_talk_save_entries, set_guardians_talk_and_wild_encounter_schedules_at_1400, WILD_ENCOUNTER, wild_encounter_key

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.enums import ItineraryErrorType
from conftest import DbControllers


def test_set_itinerary_reports_guardians_talk_and_wild_encounter_time_conflicts(
      db: DbControllers ) -> None:
   set_guardians_talk_and_wild_encounter_schedules_at_1400()

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[ CAROUSEL ],
      guardians_talks=guardians_talk_save_entries( GUARDIANS_TALK, start_time='14:00' ),
      wild_encounters=[ wild_encounter_key( WILD_ENCOUNTER ) ],
   )

   assert not result.success
   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT
   assert [ issue.to_dict() for issue in result.reasons ] == [
      {
         'code': 'wildEncounterTimeConflict',
         'items': [
            {
               'name': 'African Lion',
               'start_time': '2:00 PM',
               'end_time': '2:30 PM',
               'item_type': 'guardiansTalk',
               'meeting_spot': '',
               'location': 'Africa Savanna',
               'link': '',
            },
            {
               'name': 'African Rainforest',
               'start_time': '2:00 PM',
               'end_time': '2:45 PM',
               'item_type': 'wildEncounter',
               'meeting_spot': 'Wild Encounter - Africa Meeting Spot',
               'location': '',
               'link': 'https://www.torontozoo.com/tickets/weafricarainforest',
            },
         ],
      }
   ]

   assert db.conn.execute(
      'SELECT COUNT(*) FROM ItineraryGuardiansTalk;'
   ).fetchone()[ 0 ] == 0
   assert db.conn.execute(
      'SELECT COUNT(*) FROM ItineraryWildEncounter;'
   ).fetchone()[ 0 ] == 0
   assert db.conn.execute(
      'SELECT COUNT(*) FROM ItineraryAttraction;'
   ).fetchone()[ 0 ] == 0
