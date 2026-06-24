from __future__ import annotations

from typing import Any

from ..core.scheduled_occurrence import schedule_wild_encounter_for_itinerary
from ...data_access.itinerary import fetch_saved_itinerary
from ...data_access.saved_itinerary import SavedItinerary
from ...data_access.schedule_itinerary_item import insert_itinerary_wild_encounter
from ....models.wild_encounter_diff import WildEncounterDiff
from ..reschedule_itinerary_item_schedules import reschedule_itinerary_items_after_fixed_time_activity_add
from ...results.itinerary_save_result import ItinerarySaveResult
from .schedule_itinerary_helpers import build_save_result
from .schedule_itinerary_helpers import build_success_result
from .schedule_itinerary_helpers import persist_itinerary_walk_route
from ....shared.enums import ItineraryErrorType
from ....types import Connection
from ..unscheduling.wild_encounter_unschedule_items import saved_itinerary_has_overlap_with_wild_encounters
from ...warnings.wild_encounter_unschedule_warning import build_wild_encounter_unschedule_issue
from ....wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


def _saved_wild_encounter_exists(
      saved_itinerary: SavedItinerary,
      wild_encounter_name: str ) -> bool:
   return any(
      row.wild_encounter == wild_encounter_name and not row.is_deleted
      for row in saved_itinerary.wild_encounter_rows
   )


def _wild_encounter_diff_for_saved_itinerary_day(
      saved_itinerary: SavedItinerary,
      wild_encounter_name: str,
      wild_encounter_coordinator: type[ WildEncounterCoordinator ] ) -> WildEncounterDiff:
   encounter = wild_encounter_coordinator.get_wild_encounter_on_day_schedule(
      month=saved_itinerary.month(),
      day=saved_itinerary.day(),
      year=saved_itinerary.year(),
      encounter_name=wild_encounter_name )

   return schedule_wild_encounter_for_itinerary( wild_encounter_name, encounter )


def _insert_scheduled_wild_encounter(
      conn: Connection,
      *,
      wild_encounter_name: str,
      wild_encounter_diff: WildEncounterDiff,
      itinerary_context: dict[ str, Any ] ) -> ItinerarySaveResult | None:
   cur = conn.cursor()

   try:
      scheduled = insert_itinerary_wild_encounter(
         cur,
         wild_encounter_name=wild_encounter_name,
         start_time=wild_encounter_diff.start_time,
         end_time=wild_encounter_diff.end_time,
         is_deleted=wild_encounter_diff.is_deleted,
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


def schedule_wild_encounter_itinerary_item(
      conn: Connection,
      wild_encounter_name: str,
      *,
      itinerary_context: dict[ str, Any ],
      confirming_wild_encounter_unschedule: bool ) -> ItinerarySaveResult:
   saved_itinerary = fetch_saved_itinerary( conn )

   if saved_itinerary.is_empty():
      return build_save_result(
         conn,
         ItineraryErrorType.ITINERARY_DATE_NOT_SET,
         **itinerary_context )

   if _saved_wild_encounter_exists( saved_itinerary, wild_encounter_name ):
      return build_success_result( conn, **itinerary_context )

   wild_encounter_diff = _wild_encounter_diff_for_saved_itinerary_day(
      saved_itinerary,
      wild_encounter_name,
      itinerary_context[ 'wild_encounter_coordinator' ] )

   if wild_encounter_diff.is_deleted:
      return build_save_result(
         conn,
         ItineraryErrorType.SAVE_FAILED,
         **itinerary_context )

   has_overlap = saved_itinerary_has_overlap_with_wild_encounters(
      saved_itinerary,
      [ wild_encounter_diff ] )

   if has_overlap and not confirming_wild_encounter_unschedule:
      return build_save_result(
         conn,
         ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
         reasons=(
            build_wild_encounter_unschedule_issue( [ wild_encounter_diff ] ),
         ),
         **itinerary_context )

   insert_error = _insert_scheduled_wild_encounter(
      conn,
      wild_encounter_name=wild_encounter_name,
      wild_encounter_diff=wild_encounter_diff,
      itinerary_context=itinerary_context )

   if insert_error is not None:
      return insert_error

   if has_overlap and confirming_wild_encounter_unschedule:
      return reschedule_itinerary_items_after_fixed_time_activity_add(
         conn,
         saved_itinerary_before_clear=saved_itinerary,
         **itinerary_context )

   persist_itinerary_walk_route( conn, **itinerary_context )

   return build_success_result( conn, **itinerary_context )
