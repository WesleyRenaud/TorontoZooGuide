from __future__ import annotations

from itinerary.support import wild_encounter_key

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.enums import ItineraryErrorType
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers


def test_set_itinerary_skips_wild_encounters_with_overlapping_times(
      db: DbControllers ) -> None:
   WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='African Rainforest',
      start_date='2026-06-01',
      end_date='2026-06-30',
      encounter_times=[ '14:00' ],
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      message=None
   )
   WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='Kangaroo',
      start_date='2026-06-01',
      end_date='2026-06-30',
      encounter_times=[ '14:30' ],
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      message=None
   )
   WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='Capybara',
      start_date='2026-06-01',
      end_date='2026-06-30',
      encounter_times=[ '16:00' ],
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      message=None
   )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[ 'Conservation Carousel' ],
      guardians_talks=[],
      wild_encounters=[
         wild_encounter_key(  'African Rainforest', start_time='14:00'  ),
         wild_encounter_key(  'Kangaroo', start_time='14:30'  ),
         wild_encounter_key(  'Capybara', start_time='16:00'  ),
      ],
   )

   assert not result.success
   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT
   assert [ issue.to_dict() for issue in result.reasons ] == [
      {
         'code': 'wildEncounterTimeConflict',
         'items': [
            {
               'name': 'African Rainforest',
               'start_time': '2:00 PM',
               'end_time': '2:45 PM',
               'item_type': 'wildEncounter',
               'meeting_spot': 'Wild Encounter - Africa Meeting Spot',
               'location': '',
               'link': 'https://www.torontozoo.com/tickets/weafricarainforest',
            },
            {
               'name': 'Kangaroo',
               'start_time': '2:30 PM',
               'end_time': '3:15 PM',
               'item_type': 'wildEncounter',
               'meeting_spot': 'Wild Encounter - Eurasia Meeting Spot',
               'location': '',
               'link': 'https://www.torontozoo.com/tickets/wekangaroo',
            },
         ],
      }
   ]

   assert db.conn.execute(
      'SELECT COUNT(*) FROM ItineraryWildEncounter;'
   ).fetchone()[ 0 ] == 0
   assert db.conn.execute(
      'SELECT COUNT(*) FROM ItineraryAttraction;'
   ).fetchone()[ 0 ] == 0
