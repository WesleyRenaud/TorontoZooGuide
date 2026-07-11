from __future__ import annotations

from typing import Any

from ..core.scheduled_occurrence import schedule_guardians_talk_for_itinerary
from ...data_access.itinerary import fetch_saved_itinerary
from ...data_access.saved_itinerary import SavedItinerary
from ...data_access.schedule_itinerary_item import insert_itinerary_guardians_talk
from ..extend_departure_for_activity import ensure_departure_covers_end_time
from ....guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ....models.guardians_talk_diff import GuardiansTalkDiff
from ..reschedule_itinerary_item_schedules import reschedule_itinerary_items_after_fixed_time_activity_add
from ...results.itinerary_save_result import ItinerarySaveResult
from .schedule_itinerary_helpers import build_save_result
from .schedule_itinerary_helpers import build_success_result
from .schedule_itinerary_helpers import persist_itinerary_walk_route
from ....shared.enums import ItineraryErrorType
from ....types import Connection
from ..unscheduling.guardians_talk_unschedule_items import saved_itinerary_has_overlap_with_guardians_talks
from ...warnings.guardians_talk_unschedule_warning import build_guardians_talk_unschedule_issue


def _saved_guardians_talk_exists(
      saved_itinerary: SavedItinerary,
      talk_name: str ) -> bool:
   return any(
      row.talk_name == talk_name and not row.is_deleted
      for row in saved_itinerary.guardians_talk_rows
   )


def _guardians_talk_diff_for_saved_itinerary_day(
      saved_itinerary: SavedItinerary,
      talk_name: str,
      guardians_coordinator: type[ GuardiansCoordinator ] ) -> GuardiansTalkDiff:
   talk = guardians_coordinator.get_guardians_talk_on_day_schedule(
      month=saved_itinerary.month(),
      day=saved_itinerary.day(),
      year=saved_itinerary.year(),
      talk_name=talk_name )

   return schedule_guardians_talk_for_itinerary( talk_name, talk )


def _insert_scheduled_guardians_talk(
      conn: Connection,
      *,
      talk_name: str,
      guardians_talk_diff: GuardiansTalkDiff,
      itinerary_context: dict[ str, Any ] ) -> ItinerarySaveResult | None:
   cur = conn.cursor()

   try:
      scheduled = insert_itinerary_guardians_talk(
         cur,
         talk_name=talk_name,
         start_time=guardians_talk_diff.start_time,
         end_time=guardians_talk_diff.end_time,
         is_deleted=guardians_talk_diff.is_deleted,
      )

      if not scheduled:
         return build_save_result(
            conn,
            ItineraryErrorType.SAVE_FAILED,
            **itinerary_context )

      conn.commit()

   finally:
      cur.close()

   return None


def schedule_guardians_talk_itinerary_item(
      conn: Connection,
      talk_name: str,
      *,
      itinerary_context: dict[ str, Any ],
      confirming_guardians_talk_unschedule: bool ) -> ItinerarySaveResult:
   saved_itinerary = fetch_saved_itinerary( conn )

   if saved_itinerary.is_empty():
      return build_save_result(
         conn,
         ItineraryErrorType.ITINERARY_DATE_NOT_SET,
         **itinerary_context )

   if _saved_guardians_talk_exists( saved_itinerary, talk_name ):
      return build_success_result( conn, **itinerary_context )

   guardians_talk_diff = _guardians_talk_diff_for_saved_itinerary_day(
      saved_itinerary,
      talk_name,
      itinerary_context[ 'guardians_coordinator' ] )

   if guardians_talk_diff.is_deleted:
      return build_save_result(
         conn,
         ItineraryErrorType.ACTIVITY_NOT_ON_DAY_SCHEDULE,
         **itinerary_context )

   has_overlap = saved_itinerary_has_overlap_with_guardians_talks(
      saved_itinerary,
      [ guardians_talk_diff ] )

   if has_overlap and not confirming_guardians_talk_unschedule:
      return build_save_result(
         conn,
         ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
         reasons=(
            build_guardians_talk_unschedule_issue( [ guardians_talk_diff ] ),
         ),
         **itinerary_context )

   insert_error = _insert_scheduled_guardians_talk(
      conn,
      talk_name=talk_name,
      guardians_talk_diff=guardians_talk_diff,
      itinerary_context=itinerary_context )

   if insert_error is not None:
      return insert_error

   ensure_departure_covers_end_time(
      conn,
      end_time=guardians_talk_diff.end_time,
      current_departure_time=saved_itinerary.departure_time )

   if has_overlap and confirming_guardians_talk_unschedule:
      return reschedule_itinerary_items_after_fixed_time_activity_add(
         conn,
         saved_itinerary_before_clear=saved_itinerary,
         **itinerary_context )

   persist_itinerary_walk_route( conn, **itinerary_context )

   return build_success_result( conn, **itinerary_context )
