from __future__ import annotations

from support import guardians_talk_save_entries

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
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
      encounter_time='14:00',
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
      encounter_time='14:30',
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
      encounter_time='16:00',
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
         'African Rainforest',
         'Kangaroo',
         'Capybara',
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
               'start_time': '14:00',
               'end_time': '14:45',
               'item_type': 'wildEncounter',
               'meeting_spot': 'Wild Encounter - Africa Meeting Spot',
               'location': '',
               'link': 'https://www.torontozoo.com/tickets/weafricarainforest',
            },
            {
               'name': 'Kangaroo',
               'start_time': '14:30',
               'end_time': '15:15',
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


def test_set_itinerary_reports_guardians_talk_and_wild_encounter_time_conflicts(
      db: DbControllers ) -> None:
   GuardiansCoordinator.set_guardians_talk_schedule(
      talk='African Lion',
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday_time='14:00',
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
      encounter_time='14:00',
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
      guardians_talks=guardians_talk_save_entries( 'African Lion' ),
      wild_encounters=[ 'African Rainforest' ],
   )

   assert not result.success
   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT
   assert [ issue.to_dict() for issue in result.reasons ] == [
      {
         'code': 'wildEncounterTimeConflict',
         'items': [
            {
               'name': 'African Lion',
               'start_time': '14:00',
               'end_time': '14:30',
               'item_type': 'guardiansTalk',
               'meeting_spot': '',
               'location': 'Africa Savanna',
               'link': '',
            },
            {
               'name': 'African Rainforest',
               'start_time': '14:00',
               'end_time': '14:45',
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


def test_set_itinerary_reports_partial_guardians_talk_encounter_overlap_without_trimming(
      db: DbControllers ) -> None:
   GuardiansCoordinator.set_guardians_talk_schedule(
      talk='African Lion',
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday_time='13:30',
      tuesday_time=None,
      wednesday_time=None,
      thursday_time=None,
      friday_time=None,
      saturday_time=None,
      sunday_time=None,
      message=None
   )
   WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='Grizzly Bear',
      start_date='2026-06-01',
      end_date='2026-06-30',
      encounter_time='13:00',
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
      attractions=[],
      guardians_talks=guardians_talk_save_entries( 'African Lion' ),
      wild_encounters=[ 'Grizzly Bear' ],
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
   GuardiansCoordinator.set_guardians_talk_schedule(
      talk='African Lion',
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday_time='13:30',
      tuesday_time=None,
      wednesday_time=None,
      thursday_time=None,
      friday_time=None,
      saturday_time=None,
      sunday_time=None,
      message=None
   )
   WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='Grizzly Bear',
      start_date='2026-06-01',
      end_date='2026-06-30',
      encounter_time='13:00',
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
      attractions=[],
      guardians_talks=guardians_talk_save_entries( 'African Lion' ),
      wild_encounters=[ 'Grizzly Bear' ],
      overriding_conflicting_guardians_talks=True,
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
      'START_TIME': '13:45',
      'END_TIME': '14:00',
   }
   assert dict( encounter_schedule ) == {
      'START_TIME': '13:00',
      'END_TIME': '13:45',
   }


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
      encounter_time='13:00',
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
      encounter_time='13:00',
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
      attractions=[],
      guardians_talks=guardians_talk_save_entries( 'African Lion' ),
      wild_encounters=[ 'African Rainforest', 'Kangaroo' ],
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

