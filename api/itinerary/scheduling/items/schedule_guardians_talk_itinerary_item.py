from __future__ import annotations

from typing import Any

from ..core.scheduled_occurrence import schedule_guardians_talk_for_itinerary
from ...data_access.itinerary import fetch_saved_itinerary
from ...data_access.saved_itinerary import SavedItinerary
from ...data_access.schedule_itinerary_item import insert_itinerary_guardians_talk
from ....guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ....models.guardians_talk_diff import GuardiansTalkDiff
from ...results.itinerary_save_result import ItinerarySaveResult
from .schedule_itinerary_helpers import build_save_result
from .schedule_itinerary_helpers import build_success_result
from ....shared.enums import ItineraryErrorType
from ....types import Connection
from ..unscheduling.guardians_talk_unschedule_items import clear_saved_schedules_overlapping_guardians_talks
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
      saved_itinerary: SavedItinerary,
      talk_name: str,
      guardians_talk_diff: GuardiansTalkDiff,
      clear_overlapping_schedules: bool,
      itinerary_context: dict[ str, Any ] ) -> ItinerarySaveResult:
   cur = conn.cursor()

   try:
      if clear_overlapping_schedules:
         clear_saved_schedules_overlapping_guardians_talks(
            cur,
            saved_itinerary,
            [ guardians_talk_diff ] )

      scheduled = insert_itinerary_guardians_talk(
         cur,
         talk_name=talk_name,
         start_time=guardians_talk_diff.start_time,
         end_time=guardians_talk_diff.end_time,
      )

      if not scheduled:
         return build_save_result(
            conn,
            ItineraryErrorType.SAVE_FAILED,
            **itinerary_context )

      conn.commit()

   finally:
      cur.close()

   return build_success_result( conn, **itinerary_context )


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

   return _insert_scheduled_guardians_talk(
      conn,
      saved_itinerary=saved_itinerary,
      talk_name=talk_name,
      guardians_talk_diff=guardians_talk_diff,
      clear_overlapping_schedules=(
         has_overlap and confirming_guardians_talk_unschedule ),
      itinerary_context=itinerary_context )
