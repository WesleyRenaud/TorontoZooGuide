from __future__ import annotations

from collections.abc import Callable

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ..data_access.itinerary import fetch_saved_itinerary
from ...guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ..results.itinerary_save_result import ItinerarySaveResult
from ..scheduling.items.schedule_item_key import ScheduleItemKey
from ..scheduling.items.schedule_itinerary_helpers import build_itinerary_context
from ..scheduling.items.schedule_itinerary_helpers import build_success_result
from ..scheduling.items.schedule_itinerary_helpers import persist_itinerary_walk_route
from ..scheduling.unscheduling.shift_guest_schedules_after_unschedule import apply_guest_schedule_shift_for_unschedule
from ...types import Connection
from ...types import Cursor
from ...wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


def commit_itinerary_item_schedule_change(
      conn: Connection,
      schedule_item_key: ScheduleItemKey | None,
      apply_change: Callable[ [ Cursor, ScheduleItemKey ], None ],
      ) -> ItinerarySaveResult:
   itinerary_context = build_itinerary_context(
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator )

   saved_itinerary = fetch_saved_itinerary( conn )
   cur = conn.cursor()

   try:
      if schedule_item_key is not None:
         apply_guest_schedule_shift_for_unschedule(
            conn,
            cur,
            saved_itinerary=saved_itinerary,
            schedule_item_key=schedule_item_key )
         apply_change( cur, schedule_item_key )

      conn.commit()

   finally:
      cur.close()

   persist_itinerary_walk_route( conn, **itinerary_context )

   return build_success_result( conn, **itinerary_context )
