from __future__ import annotations

from ..conflicts.visit_window_overflow_issue_finder import VisitWindowOverflowIssueFinder
from ..data_access.validated_itinerary import ValidatedItinerary
from ...models import Itinerary
from ..results.itinerary_save_result import ItinerarySaveResult
from ...shared.enums import ItineraryErrorType
from ...types import Types


class VisitWindowOverflowWarningBuilder():
   @classmethod
   def build(
         cls,
         arrival_time: Types.ScheduleTimeKey,
         departure_time: Types.ScheduleTimeKey,
         validated_itinerary: ValidatedItinerary,
         itinerary: Itinerary ) -> ItinerarySaveResult | None:
      overflow_issues = VisitWindowOverflowIssueFinder.find(
         arrival_time,
         departure_time,
         guardians_talks=validated_itinerary.guardians_talks,
         wild_encounters=validated_itinerary.wild_encounters,
         attractions=validated_itinerary.attractions )

      if not overflow_issues:
         return None

      return ItinerarySaveResult(
         status=ItineraryErrorType.SCHEDULED_ITEM_OUTSIDE_VISIT_HOURS,
         reasons=overflow_issues,
         itinerary=itinerary )
