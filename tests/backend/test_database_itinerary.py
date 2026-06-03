from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.animals.controllers.animal_controller import AnimalController
from api.animals.logic.itinerary_animals import build_itinerary_animals
from api.attractions.controllers.attraction_controller import AttractionController
from api.guardians.controllers.guardians_controller import GuardiansController
from api.guardians.logic.guardians_talk_itinerary_validation import validate_guardians_talks_for_itinerary
from api.itinerary.controllers.itinerary_controller import ItineraryController
from api.itinerary.data_access.itinerary_animal_input import ItineraryAnimalInput
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_animal_save_carryover import itinerary_animal_save_carryover
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_guardians_talk_input import ItineraryGuardiansTalkInput
from api.itinerary.logic.itinerary_validation import validate_itinerary_animals
from api.itinerary.logic.itinerary_validation import validate_itinerary_attractions
from api.models import GuardiansTalk
from api.models import WildEncounter
from api.shared.enums import ItineraryErrorType
from api.wild_encounters.controllers.wild_encounter_controller import WildEncounterController
from api.wild_encounters.logic.wild_encounter_itinerary_validation import validate_wild_encounters_for_itinerary
from api.zoo_hours.controllers.zoo_hours_controller import ZooHoursController
from conftest import DbControllers


def guardians_talk_save_entry(
      name: str,
      *,
      start_time: str | None = None,
      end_time: str | None = None,
) -> dict[ str, str | None ]:
   return {
      'name': name,
      'start_time': start_time,
      'end_time': end_time,
   }


def guardians_talk_save_entries( *names: str ) -> list[ dict[ str, str | None ] ]:
   return [
      guardians_talk_save_entry( name )
      for name in names
   ]


def test_get_itinerary_date_returns_empty_when_no_itinerary_saved(
      db: DbControllers ) -> None:
   assert ItineraryController.get_itinerary_date() is None


def test_get_itinerary_date_returns_saved_visit_date(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert ItineraryController.get_itinerary_date() == '2026-06-15'


def test_set_get_and_clear_itinerary(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   GuardiansController.set_guardians_talk_schedule(
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
   WildEncounterController.set_wild_encounter_schedule(
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

   assert ItineraryController.set_itinerary(
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

   assert GuardiansController.cancel_guardians_talk_occurrence(
      talk='African Lion',
      location='Africa Savanna',
      date='2026-06-15',
      time='10:00'
   )
   assert WildEncounterController.cancel_wild_encounter_occurrence(
      wild_encounter_name='African Rainforest',
      date='2026-06-15',
      time='14:00'
   )

   itinerary = ItineraryController.get_itinerary()

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

   assert ItineraryController.clear_itinerary()
   cleared = ItineraryController.get_itinerary()

   assert cleared.date == ''
   assert cleared.animals == []
   assert cleared.attractions == []
   assert cleared.guardians_talks == []
   assert cleared.wild_encounters == []


def test_set_itinerary_arrival_and_departure_time_updates_only_requested_field(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert ItineraryController.set_arrival_time( '10:15 AM' ).success
   itinerary = ItineraryController.get_itinerary()

   assert itinerary.arrival_time == '10:15'
   assert itinerary.departure_time == '17:00'

   assert ItineraryController.set_arrival_time( None ).success
   itinerary = ItineraryController.get_itinerary()

   assert itinerary.arrival_time is None
   assert itinerary.departure_time == '17:00'

   assert ItineraryController.set_arrival_time( '10:15 AM' ).success
   assert ItineraryController.set_departure_time( None ).success
   itinerary = ItineraryController.get_itinerary()

   assert itinerary.arrival_time == '10:15'
   assert itinerary.departure_time is None


def test_set_itinerary_arrival_time_must_be_within_zoo_admission_hours(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert not ItineraryController.set_arrival_time( '09:00' ).success

   itinerary = ItineraryController.get_itinerary()
   assert itinerary.arrival_time == '09:30'

   assert ItineraryController.set_departure_time( '18:00' ).success
   assert ItineraryController.set_arrival_time(
      '17:00',
      confirming_short_visit=True ).success
   itinerary = ItineraryController.get_itinerary()
   assert itinerary.arrival_time == '17:00'
   assert itinerary.departure_time == '18:00'

   assert not ItineraryController.set_arrival_time( '17:15' ).success

   itinerary = ItineraryController.get_itinerary()
   assert itinerary.arrival_time == '17:00'


def test_set_itinerary_arrival_time_allows_early_admission_when_offered(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   itinerary = ItineraryController.get_itinerary()
   assert itinerary.arrival_time == '09:00'

   assert not ItineraryController.set_arrival_time( '08:45' ).success

   itinerary = ItineraryController.get_itinerary()
   assert itinerary.arrival_time == '09:00'


def test_set_itinerary_rejects_arrival_time_outside_zoo_admission_hours(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='17:15',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert not result.success

   itinerary = ItineraryController.get_itinerary()
   assert itinerary.arrival_time == '09:30'
   assert itinerary.departure_time == '17:00'


def test_set_itinerary_departure_time_must_be_within_zoo_operating_hours(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert not ItineraryController.set_departure_time( '09:00' ).success

   itinerary = ItineraryController.get_itinerary()
   assert itinerary.departure_time == '17:00'

   assert ItineraryController.set_departure_time( '18:00' ).success
   itinerary = ItineraryController.get_itinerary()
   assert itinerary.departure_time == '18:00'

   assert not ItineraryController.set_departure_time( '18:15' ).success

   itinerary = ItineraryController.get_itinerary()
   assert itinerary.departure_time == '18:00'


def test_set_itinerary_departure_time_requires_opening_not_early_admission(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='19:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert not ItineraryController.set_departure_time( '09:00' ).success

   itinerary = ItineraryController.get_itinerary()
   assert itinerary.departure_time == '19:00'

   assert ItineraryController.set_departure_time(
      '09:30',
      confirming_short_visit=True ).success
   itinerary = ItineraryController.get_itinerary()
   assert itinerary.departure_time == '09:30'


def test_set_itinerary_rejects_departure_time_outside_zoo_operating_hours(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='18:15',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert not result.success

   itinerary = ItineraryController.get_itinerary()
   assert itinerary.arrival_time == '09:30'
   assert itinerary.departure_time == '17:00'


def test_set_itinerary_departure_time_must_be_after_arrival_time(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert not ItineraryController.set_departure_time( '09:30' ).success

   itinerary = ItineraryController.get_itinerary()
   assert itinerary.departure_time == '17:00'

   assert not ItineraryController.set_arrival_time( '17:00' ).success

   itinerary = ItineraryController.get_itinerary()
   assert itinerary.arrival_time == '09:30'


def test_set_itinerary_arrival_time_rejects_visit_shorter_than_two_hours_without_confirmation(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryController.set_arrival_time( '16:30' )

   assert result.error_type == ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE

   itinerary = ItineraryController.get_itinerary()
   assert itinerary.arrival_time == '09:30'
   assert itinerary.departure_time == '17:00'


def test_set_itinerary_arrival_time_allows_short_visit_with_confirmation(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryController.set_arrival_time(
      '16:30',
      confirming_short_visit=True )

   assert result.success

   itinerary = ItineraryController.get_itinerary()
   assert itinerary.arrival_time == '16:30'
   assert itinerary.departure_time == '17:00'


def test_set_itinerary_departure_time_rejects_visit_shorter_than_two_hours_without_confirmation(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryController.set_departure_time( '10:00' )

   assert result.error_type == ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE

   itinerary = ItineraryController.get_itinerary()
   assert itinerary.departure_time == '17:00'


def test_set_itinerary_departure_time_allows_two_hour_visit_without_confirmation(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert ItineraryController.set_departure_time( '11:30' ).success
   itinerary = ItineraryController.get_itinerary()
   assert itinerary.departure_time == '11:30'


def test_set_itinerary_rejects_departure_time_that_does_not_follow_arrival(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='10:00',
      departure_time='10:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert not result.success

   itinerary = ItineraryController.get_itinerary()
   assert itinerary.arrival_time == '09:30'
   assert itinerary.departure_time == '17:00'


def test_set_itinerary_normalizes_display_format_schedule_times(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   WildEncounterController.set_wild_encounter_schedule(
      wild_encounter_name='Grizzly Bear',
      start_date='2026-06-01',
      end_date='2026-06-30',
      encounter_time='1:00 PM',
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      message=None
   )

   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[ 'Grizzly Bear' ],
   ).success

   encounter_schedule = db.conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryWildEncounter
            WHERE WILD_ENCOUNTER = 'Grizzly Bear';
      """ ).fetchone()

   assert dict( encounter_schedule ) == {
      'START_TIME': '13:00',
      'END_TIME': '13:45',
   }


def test_set_itinerary_expands_selected_exhibits_into_viewable_animals(
      db: DbControllers ) -> None:
   result = ItineraryController.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[ 'Africa Savanna' ],
   )

   assert result.success is True

   saved_animals = db.conn.execute(
      """   SELECT SPECIES, EXHIBIT
            FROM ItineraryAnimal
            WHERE EXHIBIT = 'Africa Savanna'
            ORDER BY SPECIES;
      """ ).fetchall()

   assert saved_animals
   assert {
      row[ 'EXHIBIT' ]
      for row in saved_animals
   } == { 'Africa Savanna' }


def test_set_itinerary_marks_exhibit_expanded_animals_as_added_on_update(
      db: DbControllers ) -> None:
   ItineraryController.set_itinerary(
      date='2026-06-15',
      animals=[
         { 'species': 'African Lion', 'exhibit': 'Africa Savanna' },
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[],
   )

   result = ItineraryController.set_itinerary(
      date='2026-06-15',
      animals=[
         { 'species': 'African Lion', 'exhibit': 'Africa Savanna' },
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[ 'Africa Savanna' ],
   )

   assert result.success is True

   added_rows = db.conn.execute(
      """   SELECT SPECIES, EXHIBIT, IS_ADDED
            FROM ItineraryAnimal
            WHERE IS_ADDED = 1
            ORDER BY SPECIES;
      """ ).fetchall()

   assert added_rows
   assert all( row[ 'IS_ADDED' ] == 1 for row in added_rows )
   assert {
      ( row[ 'SPECIES' ], row[ 'EXHIBIT' ] )
      for row in added_rows
   } != { ( 'African Lion', 'Africa Savanna' ) }

   added_in_response = [
      animal
      for animal in result.itinerary.animals
      if animal.is_added
   ]
   assert added_in_response
   assert all(
      animal.species != 'African Lion' or animal.exhibit != 'Africa Savanna'
      for animal in added_in_response )


def test_accept_itinerary_clears_added_animal_flags( db: DbControllers ) -> None:
   db.conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD,
               IS_ADDED
            )
            VALUES
               ( 'African Lion', 'Africa Savanna', 90, 90, 1 ),
               ( 'African Penguin', 'Africa Savanna', 80, 80, 0 );
      """ )
   db.conn.commit()

   assert ItineraryController.accept_itinerary()

   assert db.conn.execute(
      'SELECT COUNT(*) FROM ItineraryAnimal WHERE IS_ADDED = 1;'
   ).fetchone()[ 0 ] == 0

   assert db.conn.execute(
      'SELECT COUNT(*) FROM ItineraryAnimal WHERE OLD_LIKELIHOOD IS NOT NULL;'
   ).fetchone()[ 0 ] == 0


def test_set_itinerary_skips_wild_encounters_with_overlapping_times(
      db: DbControllers ) -> None:
   WildEncounterController.set_wild_encounter_schedule(
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
   WildEncounterController.set_wild_encounter_schedule(
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
   WildEncounterController.set_wild_encounter_schedule(
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

   result = ItineraryController.set_itinerary(
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
   assert result.error_type == ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT
   assert [ issue.to_dict() for issue in result.issues ] == [
      {
         'type': 'wildEncounterTimeConflict',
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
   GuardiansController.set_guardians_talk_schedule(
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
   WildEncounterController.set_wild_encounter_schedule(
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

   result = ItineraryController.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[ 'Conservation Carousel' ],
      guardians_talks=guardians_talk_save_entries( 'African Lion' ),
      wild_encounters=[ 'African Rainforest' ],
   )

   assert not result.success
   assert result.error_type == ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT
   assert [ issue.to_dict() for issue in result.issues ] == [
      {
         'type': 'wildEncounterTimeConflict',
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
   GuardiansController.set_guardians_talk_schedule(
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
   WildEncounterController.set_wild_encounter_schedule(
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

   result = ItineraryController.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[],
      guardians_talks=guardians_talk_save_entries( 'African Lion' ),
      wild_encounters=[ 'Grizzly Bear' ],
   )

   assert not result.success
   assert result.error_type == ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT
   assert len( result.issues ) == 1
   assert result.issues[ 0 ].to_dict()[ 'type' ] == 'wildEncounterTimeConflict'
   assert { item[ 'name' ] for item in result.issues[ 0 ].to_dict()[ 'items' ] } == {
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
   GuardiansController.set_guardians_talk_schedule(
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
   WildEncounterController.set_wild_encounter_schedule(
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

   result = ItineraryController.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[],
      guardians_talks=guardians_talk_save_entries( 'African Lion' ),
      wild_encounters=[ 'Grizzly Bear' ],
      overriding_conflicting_guardians_talks=True,
   )

   assert result.success is True
   assert result.issues == ()

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
   GuardiansController.set_guardians_talk_schedule(
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
   WildEncounterController.set_wild_encounter_schedule(
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
   WildEncounterController.set_wild_encounter_schedule(
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

   result = ItineraryController.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[],
      guardians_talks=guardians_talk_save_entries( 'African Lion' ),
      wild_encounters=[ 'African Rainforest', 'Kangaroo' ],
   )

   assert not result.success
   assert result.error_type == ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT
   assert len( result.issues ) == 1

   issue = result.issues[ 0 ].to_dict()

   assert issue[ 'type' ] == 'wildEncounterTimeConflict'
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


def test_get_zoo_hours_returns_seeded_operating_bounds( db: DbControllers ) -> None:
   assert ZooHoursController.get_zoo_hours( day=20, month='June', year=2026 ).to_dict() == {
      'date': '2026-06-20',
      'earlyAdmissionTime': '09:00',
      'openTime': '09:30',
      'lastAdmissionTime': '18:00',
      'closeTime': '19:00'
   }

   assert ZooHoursController.get_zoo_hours( day=22, month='June', year=2026 ).to_dict() == {
      'date': '2026-06-22',
      'earlyAdmissionTime': None,
      'openTime': '09:30',
      'lastAdmissionTime': '17:00',
      'closeTime': '18:00'
   }

   assert ZooHoursController.get_zoo_hours( day=25, month='December', year=2026 ).to_dict() == {
      'date': '2026-12-25',
      'earlyAdmissionTime': None,
      'openTime': '11:00',
      'lastAdmissionTime': '15:00',
      'closeTime': '16:00'
   }


def test_accept_itinerary_removes_zero_likelihood_and_deleted_items( db: DbControllers ) -> None:
   db.conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD
            )
            VALUES
               ( 'African Lion', 'Africa Savanna', 90, 60 ),
               ( 'African Penguin', 'Africa Savanna', 40, 80 );
      """ )
   db.conn.execute(
      """   INSERT INTO ItineraryAttraction (
               ATTRACTION,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD
            )
            VALUES
               ( 'Conservation Carousel', 100, 0 ),
               ( 'Greenhouse', 50, 75 );
      """ )
   db.conn.execute(
      """   INSERT INTO ItineraryGuardiansTalk (
               TALK_NAME,
               START_TIME,
               END_TIME,
               IS_DELETED
            )
            VALUES
               ( 'African Lion', '10:00', '10:30', 1 ),
               ( 'Amur Tiger', '11:00', '11:30', 0 );
      """ )
   db.conn.execute(
      """   INSERT INTO ItineraryWildEncounter (
               WILD_ENCOUNTER,
               START_TIME,
               END_TIME,
               IS_DELETED
            )
            VALUES
               ( 'African Rainforest', '14:00', '14:45', 1 ),
               ( 'Kangaroo', '13:00', '13:45', 0 );
      """ )
   db.conn.commit()

   assert ItineraryController.accept_itinerary()

   assert [
      row[ 'SPECIES' ]
      for row in db.conn.execute( 'SELECT SPECIES FROM ItineraryAnimal;' )
   ] == [ 'African Lion', 'African Penguin' ]
   assert [
      row[ 'ATTRACTION' ]
      for row in db.conn.execute( 'SELECT ATTRACTION FROM ItineraryAttraction;' )
   ] == [ 'Greenhouse' ]
   assert [
      row[ 'TALK_NAME' ]
      for row in db.conn.execute( 'SELECT TALK_NAME FROM ItineraryGuardiansTalk;' )
   ] == [ 'Amur Tiger' ]
   assert [
      row[ 'WILD_ENCOUNTER' ]
      for row in db.conn.execute( 'SELECT WILD_ENCOUNTER FROM ItineraryWildEncounter;' )
   ] == [ 'Kangaroo' ]


def test_accept_itinerary_removes_zero_likelihood_animals_without_override(
      db: DbControllers ) -> None:
   db.conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD
            )
            VALUES
               ( 'African Lion', 'Africa Savanna', 80, 0 ),
               ( 'African Penguin', 'Africa Savanna', 70, 0 );
      """ )
   db.conn.commit()

   assert ItineraryController.accept_itinerary()

   assert db.conn.execute( 'SELECT COUNT(*) FROM ItineraryAnimal;' ).fetchone()[ 0 ] == 0


def test_accept_itinerary_keeps_zero_likelihood_animals_when_overridden(
      db: DbControllers ) -> None:
   db.conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD
            )
            VALUES
               ( 'African Lion', 'Africa Savanna', 80, 0 ),
               ( 'African Penguin', 'Africa Savanna', 70, 0 );
      """ )
   db.conn.commit()

   assert ItineraryController.accept_itinerary(
      animals_to_keep=[
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
         },
      ] )

   rows = db.conn.execute(
      """   SELECT SPECIES, EXHIBIT, OLD_LIKELIHOOD
            FROM ItineraryAnimal
            ORDER BY SPECIES;
      """
   ).fetchall()

   assert len( rows ) == 1
   assert rows[ 0 ][ 'SPECIES' ] == 'African Lion'
   assert rows[ 0 ][ 'EXHIBIT' ] == 'Africa Savanna'
   assert rows[ 0 ][ 'OLD_LIKELIHOOD' ] is None


def test_accept_itinerary_removes_zero_likelihood_attractions_without_override(
      db: DbControllers ) -> None:
   db.conn.execute(
      """   INSERT INTO ItineraryAttraction (
               ATTRACTION,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD
            )
            VALUES
               ( 'Conservation Carousel', 100, 0 ),
               ( 'Greenhouse', 80, 0 );
      """ )
   db.conn.commit()

   assert ItineraryController.accept_itinerary()

   assert db.conn.execute(
      'SELECT COUNT(*) FROM ItineraryAttraction;'
   ).fetchone()[ 0 ] == 0


def test_accept_itinerary_keeps_zero_likelihood_attractions_when_overridden(
      db: DbControllers ) -> None:
   db.conn.execute(
      """   INSERT INTO ItineraryAttraction (
               ATTRACTION,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD
            )
            VALUES
               ( 'Conservation Carousel', 100, 0 ),
               ( 'Greenhouse', 80, 0 );
      """ )
   db.conn.commit()

   assert ItineraryController.accept_itinerary(
      attractions_to_keep=[ 'Conservation Carousel' ] )

   rows = db.conn.execute(
      """   SELECT ATTRACTION, OLD_LIKELIHOOD
            FROM ItineraryAttraction
            ORDER BY ATTRACTION;
      """
   ).fetchall()

   assert len( rows ) == 1
   assert rows[ 0 ][ 'ATTRACTION' ] == 'Conservation Carousel'
   assert rows[ 0 ][ 'OLD_LIKELIHOOD' ] is None


def test_validate_animals_removes_unavailable_entries(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   AnimalController.set_animal_as_off_display(
      species='African Lion',
      exhibit='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      message='Unavailable.'
   )

   result = validate_itinerary_animals(
      AnimalController,
      animals=[
         ItineraryAnimalInput(
            species='African Lion',
            exhibit='Africa Savanna' ),
         ItineraryAnimalInput(
            species='African Penguin',
            exhibit='Africa Savanna' ),
      ],
      new_visit_date=date( 2026, 6, 15 ),
      new_visit_date_temp=22,
      old_visit_date='2026-06-15' )

   assert len( result ) == 2

   assert [
      ( d.species, ( d.new_likelihood or 0 ) > 0 )
      for d in result
      if d.species == 'African Lion'
   ] == [ ( 'African Lion', False ) ]

   assert [
      ( d.species, ( d.new_likelihood or 0 ) > 0 )
      for d in result
      if d.species == 'African Penguin'
   ] == [ ( 'African Penguin', True ) ]


def test_get_itinerary_animals_dedupes_indoor_and_outdoor_viewing_per_row(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 5, 30 ) )

   animals = AnimalController.get_animals_for_saved_itinerary(
      day=30,
      month='May',
      year=2026,
      saved_animals=[
         ItineraryAnimalRecord(
            species='Masai Giraffe',
            exhibit='Africa Savanna',
            old_likelihood=100,
            new_likelihood=100,
         ),
      ],
   )

   giraffes = [
      animal
      for animal in animals
      if animal.species == 'Masai Giraffe'
   ]

   assert len( giraffes ) == 1
   assert giraffes[ 0 ].exhibit == 'Africa Savanna'
   assert giraffes[ 0 ].likelihood == 100
   assert giraffes[ 0 ].old_likelihood == 100


def test_validate_animals_uses_highest_likelihood_across_enclosures(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 5, 26 ) )

   result = validate_itinerary_animals(
      AnimalController,
      animals=[
         ItineraryAnimalInput(
            species='Masai Giraffe',
            exhibit='Africa Savanna' ),
      ],
      new_visit_date=date( 2026, 5, 30 ),
      old_visit_date='2026-05-26',
      saved_itinerary_animal_rows=[
         ItineraryAnimalRecord(
            species='Masai Giraffe',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
         ),
      ],
   )

   assert [ ( d.species, d.new_likelihood ) for d in result ] == [
      ( 'Masai Giraffe', 100 )
   ]


def test_itinerary_animal_save_carryover_matches_species_exhibit_case_insensitively() -> None:
   carryover = itinerary_animal_save_carryover(
      [
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time='14:30',
            end_time='14:45',
         ),
      ],
      ItineraryAnimalInput(
         species='African Lion',
         exhibit='Africa Savanna' ),
      old_visit_date='2026-06-15',
   )

   assert carryover.start_time == '14:30'
   assert carryover.end_time == '14:45'


def test_validate_attractions_removes_closed_entries(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   AttractionController.set_attraction_as_closed(
      attraction='Conservation Carousel',
      start_date='2026-06-01',
      end_date='2026-06-30',
      message='Unavailable.'
   )

   result = validate_itinerary_attractions(
      AttractionController,
      attractions=[ 'Conservation Carousel', 'Greenhouse' ],
      new_visit_date=date( 2026, 6, 15 ),
      old_visit_date='2026-06-15' )

   assert [
      ( d.name, d.new_likelihood )
      for d in result
      if d.name == 'Greenhouse'
   ] == [ ( 'Greenhouse', 100 ) ]

   assert [
      ( d.name, d.new_likelihood )
      for d in result
      if d.name == 'Conservation Carousel'
   ] == [ ( 'Conservation Carousel', 0 ) ]


def test_validate_attractions_removes_closure_override_entries(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   AttractionController.set_attraction_opening_schedule(
      attraction='Conservation Carousel',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      holidays_only=False,
      message='Open for June.'
   )
   AttractionController.set_attraction_closure_override(
      attraction='Conservation Carousel',
      start_date='2026-06-15',
      end_date='2026-06-15',
      message='Unavailable.'
   )

   result = validate_itinerary_attractions(
      AttractionController,
      attractions=[ 'Conservation Carousel' ],
      new_visit_date=date( 2026, 6, 15 ),
      old_visit_date='2026-06-15' )

   assert [
      ( d.name, d.new_likelihood )
      for d in result
   ] == [ ( 'Conservation Carousel', 0 ) ]


def test_validate_guardians_talks_splits_available_and_unavailable_entries() -> None:
   day_schedule = [
      GuardiansTalk(
         name='African Lion',
         location='Africa Savanna',
         x_coord=51.138,
         y_coord=41.279,
         start_time='10:00',
         maximum_duration=30,
         is_available=True ),
   ]

   result = validate_guardians_talks_for_itinerary(
      guardians_talks_to_include=[
         ItineraryGuardiansTalkInput( name='African Lion' ),
         ItineraryGuardiansTalkInput( name='Amur Tiger' ),
      ],
      day_schedule=day_schedule )

   assert [
      ( d.name, d.is_deleted, d.start_time, d.end_time )
      for d in result
   ] == [
      ( 'African Lion', False, '10:00', '10:30' ),
      ( 'Amur Tiger', True, None, None ),
   ]


def test_validate_wild_encounters_splits_available_and_unavailable_entries() -> None:
   day_schedule = [
      WildEncounter(
         name='Kangaroo',
         meeting_spot='Wild Encounter - Eurasia Meeting Spot',
         link='https://www.torontozoo.com/tickets/wekangaroo',
         start_time='13:00',
         maximum_duration=45,
         is_available=True ),
      WildEncounter(
         name='African Rainforest',
         meeting_spot='Wild Encounter - Africa Meeting Spot',
         link='https://www.torontozoo.com/tickets/weafricarainforest',
         start_time='14:00',
         maximum_duration=45,
         is_available=False,
         unavailable_message='Unavailable.' ),
   ]

   result = validate_wild_encounters_for_itinerary(
      wild_encounters_to_include=[ 'African Rainforest', 'Kangaroo' ],
      day_schedule=day_schedule )

   assert [
      ( d.name, d.is_deleted, d.start_time, d.end_time )
      for d in result
   ] == [
      ( 'African Rainforest', True, '14:00', '14:45' ),
      ( 'Kangaroo', False, '13:00', '13:45' ),
   ]


def test_itinerary_filter_helpers_sort_matching_animals( db: DbControllers ) -> None:
   animal_controller = AnimalController
   attraction_controller = AttractionController

   animals = animal_controller.get_animals_for_saved_itinerary(
      day=15,
      month='June',
      year=2026,
      saved_animals=[
         ItineraryAnimalRecord(
            species='African Penguin',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=None ),
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=None ),
      ] )
   attractions = attraction_controller.get_attractions_for_saved_itinerary(
      day=15,
      month='June',
      year=2026,
      saved_attractions=[
         ItineraryAttractionRecord(
            attraction='Greenhouse',
            old_likelihood=None,
            new_likelihood=None ),
         ItineraryAttractionRecord(
            attraction='Conservation Carousel',
            old_likelihood=None,
            new_likelihood=None ),
      ] )

   assert [ animal.species for animal in animals ] == sorted(
      [ animal.species for animal in animals ],
      key=str.lower
   )
   assert { animal.species for animal in animals } == { 'African Lion', 'African Penguin' }
   assert [ attraction.name for attraction in attractions ] == [ 'Conservation Carousel', 'Greenhouse' ]


def test_itinerary_filter_helpers_return_empty_without_filters( db: DbControllers ) -> None:
   assert build_itinerary_animals( [], [] ) == []
   assert AnimalController.get_animals_for_saved_itinerary(
      day=15,
      month='June',
      year=2026,
      saved_animals=[],
   ) == []
   assert AttractionController.get_attractions_for_saved_itinerary(
      day=15,
      month='June',
      year=2026,
      saved_attractions=[],
   ) == []
   assert GuardiansController.get_guardians_talk_details(
      guardians_talks_to_include=[]
   ) == []
   assert WildEncounterController.get_wild_encounter_details(
      wild_encounters_to_include=[]
   ) == []


def test_scheduled_itinerary_filter_helpers_filter_case_insensitively_and_sort(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert GuardiansController.set_guardians_talk_schedule(
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
   assert GuardiansController.set_guardians_talk_schedule(
      talk='Amur Tiger',
      location='Eurasia Wilds',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday_time='09:00',
      tuesday_time=None,
      wednesday_time=None,
      thursday_time=None,
      friday_time=None,
      saturday_time=None,
      sunday_time=None,
      message=None
   )
   assert WildEncounterController.set_wild_encounter_schedule(
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
   assert WildEncounterController.set_wild_encounter_schedule(
      wild_encounter_name='Kangaroo',
      start_date='2026-06-01',
      end_date='2026-06-30',
      encounter_time='09:00',
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      message=None
   )

   talk_result = validate_guardians_talks_for_itinerary(
      [
         ItineraryGuardiansTalkInput( name=' african lion ' ),
         ItineraryGuardiansTalkInput( name='AMUR TIGER' ),
      ],
      GuardiansController.get_guardians_talk_schedule(
         month='June',
         day=15,
         year=2026 )
   )
   encounter_result = validate_wild_encounters_for_itinerary(
      [ ' kangaroo ', 'AFRICAN RAINFOREST' ],
      WildEncounterController.get_wild_encounter_schedule(
         month='June',
         day=15,
         year=2026 )
   )

   assert [
      d.name for d in talk_result if not d.is_deleted
   ] == [
      'African Lion',
      'Amur Tiger',
   ]
   assert [
      ( d.name, d.is_deleted )
      for d in encounter_result
   ] == [
      ( 'Kangaroo', False ),
      ( 'African Rainforest', False ),
   ]
