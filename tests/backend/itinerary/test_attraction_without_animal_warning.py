from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.animals.search.species_exhibit_key import SpeciesExhibitKey
from api.animals.search.species_exhibit_key_builder import SpeciesExhibitKeyBuilder
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.itinerary.warnings.attraction_without_animal_warning_builder import AttractionWithoutAnimalWarningBuilder
from api.models.animal_diff import AnimalDiff
from api.models.attraction_diff import AttractionDiff
from api.shared.enums import ItineraryErrorType
from conftest import DbControllers


KANGAROO_WALK_THRU = 'Kangaroo Walk-Thru'
CAROUSEL = 'Conservation Carousel'
KANGAROO = {
   'species': 'Western Grey Kangaroo',
   'exhibit': 'Australasia Outdoor',
}
AMUR_TIGER = {
   'species': 'Amur Tiger',
   'exhibit': 'Eurasia Wilds',
}


def test_attractions_without_matching_animal_skips_unlinked_attractions(
      db: DbControllers ) -> None:
   validated = ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=[],
      attractions=[
         AttractionDiff(
            name=CAROUSEL,
            old_likelihood=None,
            new_likelihood=100 ),
         AttractionDiff(
            name=KANGAROO_WALK_THRU,
            old_likelihood=None,
            new_likelihood=100 ),
      ],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
   )

   missing = AttractionWithoutAnimalWarningBuilder.attractions_without_matching_animal( validated, db.conn )

   assert [ attraction.name for attraction in missing ] == [ KANGAROO_WALK_THRU ]


def test_any_linked_in_species_exhibit_pairs() -> None:
   assert SpeciesExhibitKeyBuilder.any_linked_in(
      [
         SpeciesExhibitKey.from_values(
            'Western Grey Kangaroo',
            'Australasia Outdoor' ),
      ],
      [
         SpeciesExhibitKey.from_values(
            'Western Grey Kangaroo',
            'Australasia Outdoor' ),
      ] )
   assert not SpeciesExhibitKeyBuilder.any_linked_in(
      [
         SpeciesExhibitKey.from_values(
            'Western Grey Kangaroo',
            'Wrong Exhibit' ),
      ],
      [
         SpeciesExhibitKey.from_values(
            'Western Grey Kangaroo',
            'Australasia Outdoor' ),
      ] )


def test_build_attraction_without_animal_issue_from_attractions() -> None:
   issue = AttractionWithoutAnimalWarningBuilder.build_issue_from_attractions(
      [
         AttractionDiff(
            name=KANGAROO_WALK_THRU,
            old_likelihood=None,
            new_likelihood=100 ),
      ] )

   assert issue.code == ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL
   assert [ item.name for item in issue.items ] == [ KANGAROO_WALK_THRU ]


def test_set_itinerary_warns_when_attraction_has_no_matching_animal(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[ KANGAROO_WALK_THRU ],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert not result.success
   assert result.status == ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL
   assert result.reasons[ 0 ].code == ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL
   assert [ item.name for item in result.reasons[ 0 ].items ] == [
      KANGAROO_WALK_THRU,
   ]

   confirmed = ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[ KANGAROO_WALK_THRU ],
      guardians_talks=[],
      wild_encounters=[],
      confirming_attraction_without_animal=True,
   )

   assert confirmed.success
   assert [ attraction.name for attraction in confirmed.itinerary.attractions ] == [
      KANGAROO_WALK_THRU,
   ]


def test_set_itinerary_skips_without_animal_warning_for_already_saved_attraction(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   confirmed = ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[ KANGAROO_WALK_THRU ],
      guardians_talks=[],
      wild_encounters=[],
      confirming_attraction_without_animal=True,
   )

   assert confirmed.success

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[ KANGAROO_WALK_THRU ],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS


def test_set_itinerary_skips_without_animal_warning_when_kangaroo_is_selected(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ KANGAROO ],
      attractions=[ KANGAROO_WALK_THRU ],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS


def test_set_itinerary_warns_when_wrong_animal_is_selected_with_walk_thru(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ AMUR_TIGER ],
      attractions=[ KANGAROO_WALK_THRU ],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert not result.success
   assert result.status == ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL


def test_set_itinerary_does_not_warn_for_carousel_without_animal(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[ CAROUSEL ],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS


def test_attractions_without_matching_animal_detects_linked_attraction(
      db: DbControllers ) -> None:
   validated = ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=[
         AnimalDiff(
            species='Amur Tiger',
            exhibit='Eurasia Wilds',
            old_likelihood=None,
            new_likelihood=100 ),
      ],
      attractions=[
         AttractionDiff(
            name=KANGAROO_WALK_THRU,
            old_likelihood=None,
            new_likelihood=100 ),
      ],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
   )

   missing = AttractionWithoutAnimalWarningBuilder.attractions_without_matching_animal( validated, db.conn )

   assert [ attraction.name for attraction in missing ] == [ KANGAROO_WALK_THRU ]
