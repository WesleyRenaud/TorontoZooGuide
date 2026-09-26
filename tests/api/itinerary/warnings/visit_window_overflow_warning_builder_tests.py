from __future__ import annotations

from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.warnings.visit_window_overflow_warning_builder import VisitWindowOverflowWarningBuilder
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.shared.enums import ItineraryErrorType
from api.shared.enums.position import Position


ARRIVAL_TIME = '11:00 AM'
DEPARTURE_TIME = '1:00 PM'


def _validated_itinerary(
      talks: list[ GuardiansTalkDiff ] ) -> ValidatedItinerary:
   return ValidatedItinerary(
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      animals=[],
      attractions=[],
      guardians_talks=talks,
      wild_encounters=[],
      events=[] )


def Test_Build_TestOverflowTalk_ExpectWarningResult() -> None:
   talk = GuardiansTalkDiff(
      name='African Lion',
      is_deleted=False,
      start_time='10:00 AM',
      end_time='10:30 AM' )
   itinerary = ItineraryBuilder.empty()

   warning = VisitWindowOverflowWarningBuilder.build(
      ARRIVAL_TIME,
      DEPARTURE_TIME,
      _validated_itinerary( [ talk ] ),
      itinerary )

   assert warning is not None
   assert warning.status == ItineraryErrorType.SCHEDULED_ITEM_OUTSIDE_VISIT_HOURS
   assert warning.itinerary is itinerary
   assert warning.reasons[ Position.FIRST ].items[ Position.FIRST ].name == talk.name


def Test_Build_TestExactBounds_ExpectNone() -> None:
   talk = GuardiansTalkDiff(
      name='African Lion',
      is_deleted=False,
      start_time=ARRIVAL_TIME,
      end_time=DEPARTURE_TIME )

   warning = VisitWindowOverflowWarningBuilder.build(
      ARRIVAL_TIME,
      DEPARTURE_TIME,
      _validated_itinerary( [ talk ] ),
      ItineraryBuilder.empty() )

   assert warning is None
