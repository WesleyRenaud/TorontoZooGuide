from __future__ import annotations

from ...animals.logic.animals_matching_query import species_exhibit_key_from_values
from ..data_access.itinerary_error_suppression import is_itinerary_error_suppressed
from ..data_access.itinerary_error_suppression import suppress_itinerary_error
from ..data_access.saved_itinerary import SavedItinerary
from .parse_schedule_item_request import ParsedScheduleItemRequest
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
      confirming_schedule_item_not_on_itinerary: bool ) -> bool:
   if parsed.kind not in ( ScheduleItemKind.ANIMAL, ScheduleItemKind.ATTRACTION ):
      return False

   if confirming_schedule_item_not_on_itinerary:
      return False

   if is_itinerary_error_suppressed(
         conn,
         ItineraryErrorType.ITEM_NOT_ON_ITINERARY ):
      return False

   return not saved_itinerary_has_schedule_item( saved_itinerary, parsed )


def apply_schedule_item_not_on_itinerary_preferences(
      conn: Connection,
      *,
      suppress_schedule_item_not_on_itinerary_warning: bool ) -> None:
   if not suppress_schedule_item_not_on_itinerary_warning:
      return

   suppress_itinerary_error(
      conn,
      ItineraryErrorType.ITEM_NOT_ON_ITINERARY )
