from __future__ import annotations

from collections.abc import Callable
from datetime import date

from support import guardians_talk_save_entries

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers

def test_get_itinerary_date_returns_empty_when_no_itinerary_saved(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.get_itinerary_date() is None


def test_get_itinerary_date_returns_saved_visit_date(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   assert ItineraryCoordinator.get_itinerary_date() == '2026-06-15'


def test_set_get_and_clear_itinerary(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   GuardiansCoordinator.set_guardians_talk_schedule(
      talk='African Lion',
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday_time='10:00',
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

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=[ { 'species': 'African Lion', 'exhibit': 'Africa Savanna' } ],
      attractions=[ 'Conservation Carousel' ],
      guardians_talks=guardians_talk_save_entries( 'African Lion' ),
      wild_encounters=[ 'African Rainforest' ],
   ).success

   talk_schedule = db.conn.execute(
      """   SELECT START_TIME, END_TIME, IS_DELETED
            FROM ItineraryGuardiansTalk
            WHERE TALK_NAME = 'African Lion';
      """ ).fetchone()
   encounter_schedule = db.conn.execute(
      """   SELECT START_TIME, END_TIME, IS_DELETED
            FROM ItineraryWildEncounter
            WHERE WILD_ENCOUNTER = 'African Rainforest';
      """ ).fetchone()

   assert dict( talk_schedule ) == {
      'START_TIME': '10:00',
      'END_TIME': '10:30',
      'IS_DELETED': 0
   }
   assert dict( encounter_schedule ) == {
      'START_TIME': '14:00',
      'END_TIME': '14:45',
      'IS_DELETED': 0
   }

   assert GuardiansCoordinator.cancel_guardians_talk_occurrence(
      talk='African Lion',
      location='Africa Savanna',
      date='2026-06-15',
      time='10:00'
   )
   assert WildEncounterCoordinator.cancel_wild_encounter_occurrence(
      wild_encounter_name='African Rainforest',
      date='2026-06-15',
      time='14:00'
   )

   itinerary = ItineraryCoordinator.get_itinerary()

   assert itinerary.date == '2026-06-15'
   assert itinerary.arrival_time == '09:30'
   assert itinerary.departure_time == '17:00'
   assert [ animal.species for animal in itinerary.animals ] == [ 'African Lion' ]
   assert [ attraction.name for attraction in itinerary.attractions ] == [ 'Conservation Carousel' ]
   assert [
      ( talk.name, talk.start_time, talk.end_time )
      for talk in itinerary.guardians_talks
   ] == [
      ( 'African Lion', '10:00', '10:30' )
   ]
   assert [
      ( encounter.name, encounter.start_time, encounter.end_time )
      for encounter in itinerary.wild_encounters
   ] == [
      ( 'African Rainforest', '14:00', '14:45' )
   ]
   itinerary_dict = itinerary.to_dict()
   assert itinerary_dict[ 'animals' ][ 0 ][ 'old_likelihood' ] is None
   assert itinerary_dict[ 'animals' ][ 0 ][ 'likelihood' ] > 0
   assert itinerary_dict[ 'attractions' ][ 0 ][ 'old_likelihood' ] is None
   assert itinerary_dict[ 'attractions' ][ 0 ][ 'likelihood' ] > 0

   assert ItineraryCoordinator.clear_itinerary()
   cleared = ItineraryCoordinator.get_itinerary()

   assert cleared.date == ''
   assert cleared.animals == []
   assert cleared.attractions == []
   assert cleared.guardians_talks == []
   assert cleared.wild_encounters == []

