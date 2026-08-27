from __future__ import annotations

from typing import Any

from .fixed_time_item_long_wait_warning_builder import FixedTimeItemLongWaitWarningBuilder
from ...models import Itinerary
from ...models import WildEncounter
from ...models.wild_encounter_diff import WildEncounterDiff
from ..results.itinerary_result_reason import ItineraryResultReason
from ..scheduling.bulk.bulk_reschedule_long_wait_simulator import BulkRescheduleLongWaitSimulator
from ...shared.enums import ItinerarySaveIssueItemType
from ...types import Connection


class WildEncounterLongWaitWarningBuilder():
   @classmethod
   def isolated_from_itinerary(
         cls,
         itinerary: Itinerary ) -> list[ WildEncounter ]:
      return FixedTimeItemLongWaitWarningBuilder.isolated_from_itinerary(
         itinerary,
         ItinerarySaveIssueItemType.WILD_ENCOUNTER )


   @classmethod
   def reason_after_adding_with_simulated_bulk(
         cls,
         conn: Connection,
         new_encounter: WildEncounterDiff,
         *,
         itinerary_context: dict[ str, Any ],
         ) -> ItineraryResultReason | None:
      if not BulkRescheduleLongWaitSimulator.is_isolated_after_adding(
            conn,
            new_encounter,
            propose_on_itinerary=FixedTimeItemLongWaitWarningBuilder.propose_wild_encounter_on_itinerary,
            itinerary_context=itinerary_context ):
         return None

      return FixedTimeItemLongWaitWarningBuilder.build_wild_encounter_issue_from_encounters(
         [ new_encounter ] )
