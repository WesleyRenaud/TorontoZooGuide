from __future__ import annotations

from itinerary.support import guardians_talk_save_entries, wild_encounter_key
from wild_encounter_schedule_support import wire_schedule_row, wire_schedule_rows

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.enums import ItineraryErrorType
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers


def _set_lion_talk_and_grizzly_encounter_partial_overlap_schedules() -> None:
   GuardiansCoordinator.set_guardians_talk_schedule(
      talk='African Lion',
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '13:30', monday=True, tuesday=False, wednesday=False, thursday=False, friday=False, saturday=False, sunday=False ),
      message=None
   )
   WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='Grizzly Bear',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '13:00' ),
      message=None
   )


def test_set_itinerary_reports_partial_guardians_talk_encounter_overlap_without_trimming(
      db: DbControllers ) -> None:
   _set_lion_talk_and_grizzly_encounter_partial_overlap_schedules()

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[],
      guardians_talks=guardians_talk_save_entries( 'African Lion', start_time='13:30' ),
      wild_encounters=[ wild_encounter_key( 'Grizzly Bear', start_time='13:00' ) ],
   )

   assert not result.success
   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT
   assert len( result.reasons ) == 1
   assert result.reasons[ 0 ].to_dict()[ 'code' ] == 'wildEncounterTimeConflict'
   assert { item[ 'name' ] for item in result.reasons[ 0 ].to_dict()[ 'items' ] } == {
      'African Lion',
      'Grizzly Bear',
   }

   assert db.conn.execute(
      'SELECT COUNT(*) FROM ItineraryGuardiansTalk;'
   ).fetchone()[ 0 ] == 0
   assert db.conn.execute(
      'SELECT COUNT(*) FROM ItineraryWildEncounter;'
   ).fetchone()[ 0 ] == 0


def test_set_itinerary_saves_trimmed_guardians_talk_with_partial_encounter_overlap(
      db: DbControllers ) -> None:
   _set_lion_talk_and_grizzly_encounter_partial_overlap_schedules()

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[],
      guardians_talks=guardians_talk_save_entries( 'African Lion', start_time='13:30' ),
      wild_encounters=[ wild_encounter_key( 'Grizzly Bear', start_time='13:00' ) ],
      overriding_conflicting_guardians_talks=True,
      confirming_guardians_talk_without_animal=True,
   )

   assert result.success is True
   assert result.reasons == ()

   talk_schedule = db.conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryGuardiansTalk
            WHERE TALK_NAME = 'African Lion';
      """ ).fetchone()
   encounter_schedule = db.conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryWildEncounter
            WHERE WILD_ENCOUNTER = 'Grizzly Bear';
      """ ).fetchone()

   assert dict( talk_schedule ) == {
      'START_TIME': '1:45 PM',
      'END_TIME': '2:00 PM',
   }
   assert dict( encounter_schedule ) == {
      'START_TIME': '1:00 PM',
      'END_TIME': '1:45 PM',
   }
