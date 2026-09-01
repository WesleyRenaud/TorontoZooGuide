from __future__ import annotations

from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.shared.enums import ScheduleItemKind


CAROUSEL_RECORD = ItineraryAttractionRecord(
   attraction='Conservation Carousel',
   old_likelihood=None,
   new_likelihood=100,
   start_time='11:00 AM',
   end_time='11:20 AM',
)


def Test_NameKey_TestRecord_ExpectNormalizedName() -> None:
   assert CAROUSEL_RECORD.name_key() == 'conservation carousel'


def Test_MasterRouteStopKey_TestRecord_ExpectAttractionStopKey() -> None:
   assert CAROUSEL_RECORD.master_route_stop_key() == (
      ScheduleItemKind.ATTRACTION,
      'Conservation Carousel',
   )
