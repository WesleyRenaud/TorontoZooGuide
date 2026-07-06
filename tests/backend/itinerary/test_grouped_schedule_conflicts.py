from __future__ import annotations

from itinerary.support import guardians_talk_save_entries, wild_encounter_keys
from wild_encounter_schedule_support import wire_schedule_row, wire_schedule_rows

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.enums import ItineraryErrorType
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers


def test_set_itinerary_groups_mutually_overlapping_activities_into_one_conflict(
      db: DbControllers ) -> None:
   GuardiansCoordinator.set_guardians_talk_schedule(
      talk='African Lion',
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday_time='13:00',
      tuesday_time=None,
      wednesday_time=None,
      thursday_time=None,
      friday_time=None,
      saturday_time=None,
      sunday_time=None,
      message=None
   )
   WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='African Rainforest',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '13:00' ),
      message=None
   )
   WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='Kangaroo',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '13:00' ),
      message=None
   )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[],
      guardians_talks=guardians_talk_save_entries( 'African Lion' ),
      wild_encounters=wild_encounter_keys(
         'African Rainforest',
         'Kangaroo',
         start_time='13:00' ),
   )

   assert not result.success
   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT
   assert len( result.reasons ) == 1

   issue = result.reasons[ 0 ].to_dict()

   assert issue[ 'code' ] == 'wildEncounterTimeConflict'
   assert { item[ 'name' ] for item in issue[ 'items' ] } == {
      'African Lion',
      'African Rainforest',
      'Kangaroo',
   }

   assert db.conn.execute(
      'SELECT COUNT(*) FROM ItineraryGuardiansTalk;'
   ).fetchone()[ 0 ] == 0
   assert db.conn.execute(
      'SELECT COUNT(*) FROM ItineraryWildEncounter;'
   ).fetchone()[ 0 ] == 0
