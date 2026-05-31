from __future__ import annotations

from ..data_access.unschedule_itinerary_item import clear_itinerary_animal_schedule
from ..data_access.unschedule_itinerary_item import clear_itinerary_attraction_schedule
from ..data_access.unschedule_itinerary_item import clear_itinerary_guardians_talk_schedule
from ..data_access.unschedule_itinerary_item import clear_itinerary_wild_encounter_schedule
from ..data_access.unschedule_itinerary_item import delete_itinerary_event_schedule
from .itinerary_save_result import ItinerarySaveResult
from ...models import Itinerary
from .parse_schedule_item_request import parse_schedule_item_request
from .parse_schedule_item_request import ParsedScheduleItemRequest
from ...shared.enums import ItineraryErrorType
from ...shared.enums import ScheduleItemKind
from ...types import Connection
from ...types import Cursor


def _apply_unschedule(
      cur: Cursor,
      parsed: ParsedScheduleItemRequest ) -> None:
   if parsed.kind == ScheduleItemKind.ANIMAL:
      clear_itinerary_animal_schedule(
         cur,
         species=parsed.species,
         exhibit=parsed.exhibit )
      return

   if parsed.kind == ScheduleItemKind.ATTRACTION:
      clear_itinerary_attraction_schedule(
         cur,
         name=parsed.attraction_name )
      return

   if parsed.kind == ScheduleItemKind.GUARDIANS_TALK:
      clear_itinerary_guardians_talk_schedule(
         cur,
         talk_name=parsed.talk_name )
      return

   if parsed.kind == ScheduleItemKind.WILD_ENCOUNTER:
      clear_itinerary_wild_encounter_schedule(
         cur,
         wild_encounter=parsed.wild_encounter_name )
      return

   if parsed.kind == ScheduleItemKind.EVENT:
      delete_itinerary_event_schedule( cur, event_type=parsed.event_type )


def unschedule_itinerary_item(
      conn: Connection,
      item_type: str,
      key: str ) -> ItinerarySaveResult:
   parsed = parse_schedule_item_request( item_type, key )

   cur = conn.cursor()

   try:
      if parsed is not None:
         _apply_unschedule( cur, parsed )

      conn.commit()

   finally:
      cur.close()

   return ItinerarySaveResult(
      itinerary=Itinerary( date='' ),
      error_type=ItineraryErrorType.SUCCESS )
