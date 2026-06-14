from __future__ import annotations

from ...animals.search.animals_matching_query import species_exhibit_key_from_values
from ..data_access.itinerary_status import is_itinerary_error_suppressed
from ..data_access.saved_itinerary import SavedItinerary
from .itinerary_suppressed_warnings import append_suppressed_warning
from ..scheduling.items.parse_schedule_item_request import ParsedScheduleItemRequest
from ...shared.enums import ItineraryErrorType
from ...shared.enums import ScheduleItemKind
from ...types import Connection


def saved_itinerary_has_schedule_item(
      saved_itinerary: SavedItinerary,
      parsed: ParsedScheduleItemRequest ) -> bool:
   if parsed.kind == ScheduleItemKind.ANIMAL:
      key = species_exhibit_key_from_values( parsed.species, parsed.exhibit )
      return key in saved_itinerary.species_exhibit_pairs()

   if parsed.kind == ScheduleItemKind.ATTRACTION:
      return parsed.attraction_name in saved_itinerary.attraction_names()

   return True


def schedule_item_not_on_itinerary_warning_is_required(
      conn: Connection,
      saved_itinerary: SavedItinerary,
      parsed: ParsedScheduleItemRequest,
      *,
      confirming_schedule_item_not_on_itinerary: bool,
      suppressed_warnings: list[ ItineraryErrorType ] | None = None ) -> bool:
   if parsed.kind not in ( ScheduleItemKind.ANIMAL, ScheduleItemKind.ATTRACTION ):
      return False

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

   return not saved_itinerary_has_schedule_item( saved_itinerary, parsed )
