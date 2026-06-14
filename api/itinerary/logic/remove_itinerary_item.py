from __future__ import annotations

from ..data_access.remove_itinerary_item import delete_itinerary_animal
from ..data_access.remove_itinerary_item import delete_itinerary_attraction
from ..data_access.remove_itinerary_item import delete_itinerary_event
from ..data_access.remove_itinerary_item import delete_itinerary_guardians_talk
from ..data_access.remove_itinerary_item import delete_itinerary_wild_encounter
from .itinerary_save_result import ItinerarySaveResult
from ...models import Itinerary
from ..scheduling.items.parse_schedule_item_request import parse_schedule_item_request
from ..scheduling.items.parse_schedule_item_request import ParsedScheduleItemRequest
from ...shared.enums import ItineraryErrorType
from ...shared.enums import ScheduleItemKind
from ...types import Connection
from ...types import Cursor


def _apply_remove(
      cur: Cursor,
      parsed: ParsedScheduleItemRequest ) -> None:
   if parsed.kind == ScheduleItemKind.ANIMAL:
      delete_itinerary_animal(
         cur,
         species=parsed.species,
         exhibit=parsed.exhibit )
      return

   if parsed.kind == ScheduleItemKind.ATTRACTION:
      delete_itinerary_attraction(
         cur,
         name=parsed.attraction_name )
      return

   if parsed.kind == ScheduleItemKind.GUARDIANS_TALK:
      delete_itinerary_guardians_talk(
         cur,
         talk_name=parsed.talk_name )
      return

   if parsed.kind == ScheduleItemKind.WILD_ENCOUNTER:
      delete_itinerary_wild_encounter(
         cur,
         wild_encounter=parsed.wild_encounter_name )
      return

   if parsed.kind == ScheduleItemKind.EVENT:
      delete_itinerary_event( cur, event_type=parsed.event_type )


def remove_itinerary_item(
      conn: Connection,
      item_type: str,
      key: str ) -> ItinerarySaveResult:
   parsed = parse_schedule_item_request( item_type, key )

   cur = conn.cursor()

   try:
      if parsed is not None:
         _apply_remove( cur, parsed )

      conn.commit()

   finally:
      cur.close()

   return ItinerarySaveResult(
      itinerary=Itinerary( date='' ),
      status=ItineraryErrorType.SUCCESS )
