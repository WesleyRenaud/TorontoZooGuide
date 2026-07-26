from __future__ import annotations

from ...animals.search.animals_matching_query import species_exhibit_keys
from ...animals.search.species_exhibit_key import SpeciesExhibitKey
from ...attractions.data_access.attraction_animal import fetch_attraction_linked_animals
from ..data_access.itinerary_name_key import itinerary_name_key
from ..data_access.saved_itinerary import SavedItinerary
from ..data_access.validated_itinerary import ValidatedItinerary
from ...models.attraction_diff import AttractionDiff
from ..results.itinerary_result_reason import ItineraryResultReason
from ..results.itinerary_save_issue_item import ItinerarySaveIssueItem
from ...shared.enums import ItineraryErrorType
from ...shared.enums import ItinerarySaveIssueItemType
from ...types import Connection


def attraction_matches_species_exhibit_pairs(
      animal_species_exhibit_keys: list[ SpeciesExhibitKey ],
      *,
      linked_animals: list[ SpeciesExhibitKey ] ) -> bool:
   return any(
      linked_animal in animal_species_exhibit_keys
      for linked_animal in linked_animals
   )


def attractions_without_matching_animal(
      validated_itinerary: ValidatedItinerary,
      conn: Connection ) -> list[ AttractionDiff ]:
   animal_keys = species_exhibit_keys( validated_itinerary.animals )
   missing_attractions: list[ AttractionDiff ] = []

   for attraction in validated_itinerary.attractions:
      linked_animals = fetch_attraction_linked_animals( conn, attraction.name )

      if not linked_animals:
         continue

      if attraction_matches_species_exhibit_pairs(
            animal_keys,
            linked_animals=linked_animals ):
         continue

      missing_attractions.append( attraction )

   return missing_attractions


def newly_added_attractions_without_matching_animal(
      validated_itinerary: ValidatedItinerary,
      conn: Connection,
      *,
      saved_itinerary: SavedItinerary | None ) -> list[ AttractionDiff ]:
   missing_attractions = attractions_without_matching_animal(
      validated_itinerary,
      conn )

   if saved_itinerary is None:
      return missing_attractions

   saved_names = {
      row.name_key()
      for row in saved_itinerary.attraction_rows
   }

   return [
      attraction
      for attraction in missing_attractions
      if itinerary_name_key( attraction.name ) not in saved_names
   ]


def attraction_without_animal_warning_is_required(
      validated_itinerary: ValidatedItinerary,
      conn: Connection,
      *,
      confirming_attraction_without_animal: bool,
      saved_itinerary: SavedItinerary | None = None ) -> bool:
   if confirming_attraction_without_animal:
      return False

   return bool(
      newly_added_attractions_without_matching_animal(
         validated_itinerary,
         conn,
         saved_itinerary=saved_itinerary ) )


def build_attraction_without_animal_issue_from_attractions(
      attractions: list[ AttractionDiff ],
      ) -> ItineraryResultReason:
   issue_items = [
      ItinerarySaveIssueItem(
         name=attraction.name,
         start_time=attraction.start_time,
         end_time=attraction.end_time,
         item_type=ItinerarySaveIssueItemType.ATTRACTION,
      )
      for attraction in attractions
   ]

   return ItineraryResultReason(
      code=ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL,
      items=issue_items )
