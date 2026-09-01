from __future__ import annotations

from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.shared.enums import ScheduleItemKind


ZOOMOBILE_RECORD = ItineraryTransportationRecord(
   transportation='Zoomobile',
   old_likelihood=None,
   new_likelihood=100,
   added_as_attraction=True,
   start_time='10:00 AM',
   end_time='11:15 AM',
   route='summer',
)


def Test_NameKey_TestRecord_ExpectNormalizedName() -> None:
   assert ZOOMOBILE_RECORD.name_key() == 'zoomobile'


def Test_MasterRouteStopKey_TestRecord_ExpectAttractionStopKey() -> None:
   assert ZOOMOBILE_RECORD.master_route_stop_key() == (
      ScheduleItemKind.ATTRACTION,
      'Zoomobile',
   )


def Test_ScheduleItemKind_TestRecord_ExpectTransportation() -> None:
   assert ZOOMOBILE_RECORD.schedule_item_kind is ScheduleItemKind.TRANSPORTATION


def Test_Attraction_TestRecord_ExpectTransportationName() -> None:
   assert ZOOMOBILE_RECORD.attraction == 'Zoomobile'
