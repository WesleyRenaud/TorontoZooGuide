from __future__ import annotations

from ...animals.search.species_exhibit_key_builder import SpeciesExhibitKeyBuilder
from ...attractions.data_access.attraction_animal_provider import AttractionAnimalProvider
from ..data_access.itinerary_name_key_builder import ItineraryNameKeyBuilder
from ..data_access.saved_itinerary import SavedItinerary
from ..data_access.validated_itinerary import ValidatedItinerary
from ...models.attraction_diff import AttractionDiff
from ..results.itinerary_result_reason import ItineraryResultReason
from ..results.itinerary_save_issue_item import ItinerarySaveIssueItem
from ...shared.enums import ItineraryErrorType
from ...shared.enums import ItinerarySaveIssueItemType
from ...types import Types


class AttractionWithoutAnimalWarningBuilder():
   @classmethod
   def attractions_without_matching_animal(
         cls,
         validated_itinerary: ValidatedItinerary,
         conn: Types.Connection ) -> list[ AttractionDiff ]:
      animal_keys = SpeciesExhibitKeyBuilder.from_animals( validated_itinerary.animals )
      missing_attractions: list[ AttractionDiff ] = []

      for attraction in validated_itinerary.attractions:
         linked_animals = AttractionAnimalProvider.fetch_attraction_linked_animals(
            conn,
            attraction.name )

         if not linked_animals:
            continue

         if SpeciesExhibitKeyBuilder.any_linked_in(
               animal_keys,
               linked_animals=linked_animals ):
            continue

         missing_attractions.append( attraction )

      return missing_attractions


   @classmethod
   def newly_added_without_matching_animal(
         cls,
         validated_itinerary: ValidatedItinerary,
         conn: Types.Connection,
         *,
         saved_itinerary: SavedItinerary | None ) -> list[ AttractionDiff ]:
      missing_attractions = cls.attractions_without_matching_animal(
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
         if ItineraryNameKeyBuilder.build( attraction.name ) not in saved_names
      ]


   @classmethod
   def is_required(
         cls,
         validated_itinerary: ValidatedItinerary,
         conn: Types.Connection,
         *,
         confirming_attraction_without_animal: bool,
         saved_itinerary: SavedItinerary | None = None ) -> bool:
      if confirming_attraction_without_animal:
         return False

      return bool(
         cls.newly_added_without_matching_animal(
            validated_itinerary,
            conn,
            saved_itinerary=saved_itinerary ) )


   @classmethod
   def build_issue_from_attractions(
         cls,
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
