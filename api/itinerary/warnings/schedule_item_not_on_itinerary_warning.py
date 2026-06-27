from __future__ import annotations

from ..animal_item_key import AnimalScheduleItemKey
from ...animals.search.animals_matching_query import species_exhibit_key_from_values
from ..data_access.itinerary_status import is_itinerary_error_suppressed
from ..data_access.saved_itinerary import SavedItinerary
from .itinerary_suppressed_warnings import append_suppressed_warning
from ..scheduling.items.schedule_item_key import ListedScheduleItemKey
from ...shared.enums import ItineraryErrorType
from ...types import Connection


def saved_itinerary_has_schedule_item(
      saved_itinerary: SavedItinerary,
      schedule_item_key: ListedScheduleItemKey ) -> bool:
   if isinstance( schedule_item_key, AnimalScheduleItemKey ):
      key = species_exhibit_key_from_values(
         schedule_item_key.species,
         schedule_item_key.exhibit )
      return key in saved_itinerary.species_exhibit_pairs()

   return schedule_item_key.name in saved_itinerary.attraction_names()


def schedule_item_not_on_itinerary_warning_is_required(
      conn: Connection,
      saved_itinerary: SavedItinerary,
      schedule_item_key: ListedScheduleItemKey,
      *,
      confirming_schedule_item_not_on_itinerary: bool,
      suppressed_warnings: list[ ItineraryErrorType ] | None = None ) -> bool:
   if confirming_schedule_item_not_on_itinerary:
      return False

   if is_itinerary_error_suppressed(
         conn,
         ItineraryErrorType.ITEM_NOT_ON_ITINERARY ):
      if suppressed_warnings is not None:
         append_suppressed_warning(
            suppressed_warnings,
            ItineraryErrorType.ITEM_NOT_ON_ITINERARY )

      return False

   return not saved_itinerary_has_schedule_item(
      saved_itinerary,
      schedule_item_key )
