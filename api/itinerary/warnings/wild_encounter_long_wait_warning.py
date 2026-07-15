from __future__ import annotations

from typing import Any

from .fixed_time_item_long_wait_warning import build_wild_encounter_long_wait_issue_from_encounters
from .fixed_time_item_long_wait_warning import isolated_fixed_time_items_from_itinerary
from .fixed_time_item_long_wait_warning import propose_wild_encounter_on_itinerary
from ...models import Itinerary
from ...models import WildEncounter
from ...models.wild_encounter_diff import WildEncounterDiff
from ..results.itinerary_result_reason import ItineraryResultReason
from ..scheduling.bulk.simulate_bulk_reschedule_for_long_wait import fixed_time_item_isolated_after_adding_with_simulated_bulk
from ...shared.enums import ItinerarySaveIssueItemType
from ...types import Connection


def isolated_wild_encounters_from_itinerary(
      itinerary: Itinerary ) -> list[ WildEncounter ]:
   return isolated_fixed_time_items_from_itinerary(
      itinerary,
      ItinerarySaveIssueItemType.WILD_ENCOUNTER )


def wild_encounter_long_wait_reason_after_adding_with_simulated_bulk(
      conn: Connection,
      new_encounter: WildEncounterDiff,
      *,
      itinerary_context: dict[ str, Any ],
      ) -> ItineraryResultReason | None:
   if not fixed_time_item_isolated_after_adding_with_simulated_bulk(
         conn,
         new_encounter,
         propose_on_itinerary=propose_wild_encounter_on_itinerary,
         itinerary_context=itinerary_context ):
      return None

   return build_wild_encounter_long_wait_issue_from_encounters(
      [ new_encounter ] )
