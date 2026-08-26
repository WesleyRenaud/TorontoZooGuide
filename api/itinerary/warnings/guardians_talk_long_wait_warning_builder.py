from __future__ import annotations

from typing import Any

from .fixed_time_item_long_wait_warning import build_guardians_talk_long_wait_issue_from_talks
from .fixed_time_item_long_wait_warning import isolated_fixed_time_items_from_itinerary
from .fixed_time_item_long_wait_warning import propose_guardians_talk_on_itinerary
from ...models import GuardiansTalk
from ...models import Itinerary
from ...models.guardians_talk_diff import GuardiansTalkDiff
from ..results.itinerary_result_reason import ItineraryResultReason
from ..scheduling.bulk.simulate_bulk_reschedule_for_long_wait import fixed_time_item_isolated_after_adding_with_simulated_bulk
from ...shared.enums import ItinerarySaveIssueItemType
from ...types import Connection


class GuardiansTalkLongWaitWarningBuilder():
   @classmethod
   def isolated_from_itinerary(
         cls,
         itinerary: Itinerary ) -> list[ GuardiansTalk ]:
      return isolated_fixed_time_items_from_itinerary(
         itinerary,
         ItinerarySaveIssueItemType.GUARDIANS_TALK )


   @classmethod
   def reason_after_adding_with_simulated_bulk(
         cls,
         conn: Connection,
         new_talk: GuardiansTalkDiff,
         *,
         itinerary_context: dict[ str, Any ],
         ) -> ItineraryResultReason | None:
      if not fixed_time_item_isolated_after_adding_with_simulated_bulk(
            conn,
            new_talk,
            propose_on_itinerary=propose_guardians_talk_on_itinerary,
            itinerary_context=itinerary_context ):
         return None

      return build_guardians_talk_long_wait_issue_from_talks( [ new_talk ] )
