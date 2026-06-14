from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.animals.logic.itinerary_animals import build_itinerary_animals
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.guardians.itinerary.guardians_talk_itinerary_validation import validate_guardians_talks_for_itinerary
from api.itinerary.data_access.itinerary_animal_input import ItineraryAnimalInput
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_animal_save_carryover import itinerary_animal_save_carryover
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_guardians_talk_input import ItineraryGuardiansTalkInput
from api.itinerary.validation.itinerary_validation import validate_itinerary_animals
from api.itinerary.validation.itinerary_validation import validate_itinerary_attractions
from api.models import GuardiansTalk
from api.models import WildEncounter
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from api.wild_encounters.itinerary.wild_encounter_itinerary_validation import validate_wild_encounters_for_itinerary
from conftest import DbControllers

def test_validate_animals_removes_unavailable_entries(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   AnimalCoordinator.set_animal_as_off_display(
      species='African Lion',
      exhibit='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      message='Unavailable.'
   )

   result = validate_itinerary_animals(
      AnimalCoordinator,
      animals=[
         ItineraryAnimalInput(
            species='African Lion',
            exhibit='Africa Savanna' ),
         ItineraryAnimalInput(
            species='African Penguin',
            exhibit='Africa Savanna' ),
      ],
      new_visit_date=date( 2026, 6, 15 ),
      arrival_time='09:30',
      departure_time='17:00',
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


def test_get_itinerary_animals_keeps_indoor_and_outdoor_viewing_for_map_markers(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 5, 30 ) )

   animals = AnimalCoordinator.get_animals_for_saved_itinerary(
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

   assert sorted( [
      ( giraffe.exhibit, giraffe.enclosure_type, giraffe.x_coord, giraffe.y_coord )
      for giraffe in giraffes
   ] ) == [
      ( 'Africa Savanna', 'Indoor', 42.35, 71.366 ),
      ( 'Africa Savanna', 'Outdoor', 39.885, 70.927 ),
   ]
   assert all( giraffe.likelihood == 100 for giraffe in giraffes )
   assert all( giraffe.old_likelihood == 100 for giraffe in giraffes )


def test_validate_animals_uses_highest_likelihood_across_enclosures(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 5, 26 ) )

   result = validate_itinerary_animals(
      AnimalCoordinator,
      animals=[
         ItineraryAnimalInput(
            species='Masai Giraffe',
            exhibit='Africa Savanna' ),
      ],
      new_visit_date=date( 2026, 5, 30 ),
      arrival_time='09:30',
      departure_time='17:00',
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
   AttractionCoordinator.set_attraction_as_closed(
      attraction='Conservation Carousel',
      start_date='2026-06-01',
      end_date='2026-06-30',
      message='Unavailable.'
   )

   result = validate_itinerary_attractions(
      AttractionCoordinator,
      attractions=[ 'Conservation Carousel', 'Greenhouse' ],
      new_visit_date=date( 2026, 6, 15 ),
      arrival_time='09:30',
      departure_time='17:00',
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
   AttractionCoordinator.set_attraction_opening_schedule(
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
   AttractionCoordinator.set_attraction_closure_override(
      attraction='Conservation Carousel',
      start_date='2026-06-15',
      end_date='2026-06-15',
      message='Unavailable.'
   )

   result = validate_itinerary_attractions(
      AttractionCoordinator,
      attractions=[ 'Conservation Carousel' ],
      new_visit_date=date( 2026, 6, 15 ),
      arrival_time='09:30',
      departure_time='17:00',
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
   animal_controller = AnimalCoordinator
   attraction_coordinator = AttractionCoordinator

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
   attractions = attraction_coordinator.get_attractions_for_saved_itinerary(
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


def test_itinerary_animals_keep_same_species_in_multiple_exhibits_for_map_markers(
      db: DbControllers ) -> None:
   animals = AnimalCoordinator.get_animals_for_saved_itinerary(
      day=15,
      month='June',
      year=2026,
      saved_animals=[
         ItineraryAnimalRecord(
            species='Cheetah',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=None ),
         ItineraryAnimalRecord(
            species='Cheetah',
            exhibit='Indo-Malaya Outdoor',
            old_likelihood=None,
            new_likelihood=None ),
      ] )

   assert [
      ( animal.species, animal.exhibit )
      for animal in animals
      if animal.species == 'Cheetah'
   ] == [
      ( 'Cheetah', 'Africa Savanna' ),
      ( 'Cheetah', 'Indo-Malaya Outdoor' ),
   ]


def test_itinerary_filter_helpers_return_empty_without_filters( db: DbControllers ) -> None:
   assert build_itinerary_animals( [], [] ) == []
   assert AnimalCoordinator.get_animals_for_saved_itinerary(
      day=15,
      month='June',
      year=2026,
      saved_animals=[],
   ) == []
   assert AttractionCoordinator.get_attractions_for_saved_itinerary(
      day=15,
      month='June',
      year=2026,
      saved_attractions=[],
   ) == []
   assert GuardiansCoordinator.get_guardians_talk_details(
      guardians_talks_to_include=[]
   ) == []
   assert WildEncounterCoordinator.get_wild_encounter_details(
      wild_encounters_to_include=[]
   ) == []


def test_scheduled_itinerary_filter_helpers_filter_case_insensitively_and_sort(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert GuardiansCoordinator.set_guardians_talk_schedule(
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
   assert GuardiansCoordinator.set_guardians_talk_schedule(
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
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
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
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
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
      GuardiansCoordinator.get_guardians_talk_schedule(
         month='June',
         day=15,
         year=2026 )
   )
   encounter_result = validate_wild_encounters_for_itinerary(
      [ ' kangaroo ', 'AFRICAN RAINFOREST' ],
      WildEncounterCoordinator.get_wild_encounter_schedule(
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
