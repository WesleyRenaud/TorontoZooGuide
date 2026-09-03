from __future__ import annotations

import pytest

from api.animals.search.species_exhibit_key import SpeciesExhibitKey
from api.attractions.data_access.attraction_animal_provider import AttractionAnimalProvider
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.itinerary.warnings.attraction_without_animal_warning_builder import AttractionWithoutAnimalWarningBuilder
from api.models.animal_diff import AnimalDiff
from api.models.attraction_diff import AttractionDiff
from api.shared.enums import ItineraryErrorType


KANGAROO_WALK_THRU = 'Kangaroo Walk-Thru'
CAROUSEL = 'Conservation Carousel'
KANGAROO_LINK = {
   'species': 'Western Grey Kangaroo',
   'exhibit': 'Australasia Outdoor',
}

KANGAROO_SPECIES_EXHIBIT = SpeciesExhibitKey.from_values(
   'Western Grey Kangaroo',
   'Australasia Outdoor' )


def _validated_itinerary(
      *,
      animals: list[ AnimalDiff ] | None = None,
      attractions: list[ AttractionDiff ] | None = None ) -> ValidatedItinerary:
   return ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=animals or [],
      attractions=attractions or [],
      guardians_talks=[],
      wild_encounters=[],
      events=[] )


@pytest.fixture
def stub_attraction_animal_links( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AttractionAnimalProvider,
      'fetch_attraction_linked_animals',
      lambda conn, attraction_name: [ KANGAROO_LINK ]
      if attraction_name == KANGAROO_WALK_THRU
      else [] )


def Test_AttractionsWithoutMatchingAnimal_TestLinkedAndUnlinked_ExpectOnlyLinkedMissing(
      stub_attraction_animal_links: None ) -> None:
   missing = AttractionWithoutAnimalWarningBuilder.attractions_without_matching_animal(
      _validated_itinerary(
         attractions=[
            AttractionDiff(
               name=CAROUSEL,
               old_likelihood=None,
               new_likelihood=100 ),
            AttractionDiff(
               name=KANGAROO_WALK_THRU,
               old_likelihood=None,
               new_likelihood=100 ),
         ] ),
      None )

   assert [ attraction.name for attraction in missing ] == [ KANGAROO_WALK_THRU ]


def Test_AttractionsWithoutMatchingAnimal_TestWrongAnimal_ExpectLinkedAttractionMissing(
      stub_attraction_animal_links: None ) -> None:
   missing = AttractionWithoutAnimalWarningBuilder.attractions_without_matching_animal(
      _validated_itinerary(
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
         ] ),
      None )

   assert [ attraction.name for attraction in missing ] == [ KANGAROO_WALK_THRU ]


def Test_NewlyAddedWithoutMatchingAnimal_TestSavedAttraction_ExpectEmpty(
      stub_attraction_animal_links: None ) -> None:
   missing = AttractionWithoutAnimalWarningBuilder.newly_added_without_matching_animal(
      _validated_itinerary(
         attractions=[
            AttractionDiff(
               name=KANGAROO_WALK_THRU,
               old_likelihood=None,
               new_likelihood=100 ),
         ] ),
      None,
      saved_itinerary=SavedItinerary(
         date_value='2026-06-20',
         arrival_time='9:30 AM',
         departure_time='5:00 PM',
         attraction_rows=[
            ItineraryAttractionRecord(
               attraction=KANGAROO_WALK_THRU,
               old_likelihood=None,
               new_likelihood=100 ),
         ] ) )

   assert missing == []


def Test_IsRequired_TestConfirmingFlag_ExpectFalse(
      stub_attraction_animal_links: None ) -> None:
   assert AttractionWithoutAnimalWarningBuilder.is_required(
      _validated_itinerary(
         attractions=[
            AttractionDiff(
               name=KANGAROO_WALK_THRU,
               old_likelihood=None,
               new_likelihood=100 ),
         ] ),
      None,
      confirming_attraction_without_animal=True ) is False


def Test_BuildIssueFromAttractions_TestLinkedAttraction_ExpectWithoutAnimalIssue() -> None:
   issue = AttractionWithoutAnimalWarningBuilder.build_issue_from_attractions(
      [
         AttractionDiff(
            name=KANGAROO_WALK_THRU,
            old_likelihood=None,
            new_likelihood=100 ),
      ] )

   assert issue.code == ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL
   assert [ item.name for item in issue.items ] == [ KANGAROO_WALK_THRU ]


def Test_AttractionsWithoutMatchingAnimal_TestMatchingAnimal_ExpectEmpty(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AttractionAnimalProvider,
      'fetch_attraction_linked_animals',
      lambda conn, name: [ KANGAROO_SPECIES_EXHIBIT ] )

   missing = AttractionWithoutAnimalWarningBuilder.attractions_without_matching_animal(
      _validated_itinerary(
         animals=[
            AnimalDiff(
               species='Western Grey Kangaroo',
               exhibit='Australasia Outdoor',
               old_likelihood=None,
               new_likelihood=100 ),
         ],
         attractions=[
            AttractionDiff(
               name=KANGAROO_WALK_THRU,
               old_likelihood=None,
               new_likelihood=100 ),
         ] ),
      None )

   assert missing == []


def Test_NewlyAddedWithoutMatchingAnimal_TestNoSavedItinerary_ExpectMissing(
      stub_attraction_animal_links: None ) -> None:
   missing = AttractionWithoutAnimalWarningBuilder.newly_added_without_matching_animal(
      _validated_itinerary(
         attractions=[
            AttractionDiff(
               name=KANGAROO_WALK_THRU,
               old_likelihood=None,
               new_likelihood=100 ),
         ] ),
      None,
      saved_itinerary=None )

   assert [ item.name for item in missing ] == [ KANGAROO_WALK_THRU ]


def Test_IsRequired_TestMissingAnimalWithoutConfirmation_ExpectTrue(
      stub_attraction_animal_links: None ) -> None:
   assert AttractionWithoutAnimalWarningBuilder.is_required(
      _validated_itinerary(
         attractions=[
            AttractionDiff(
               name=KANGAROO_WALK_THRU,
               old_likelihood=None,
               new_likelihood=100 ),
         ] ),
      None,
      confirming_attraction_without_animal=False,
      saved_itinerary=None ) is True
