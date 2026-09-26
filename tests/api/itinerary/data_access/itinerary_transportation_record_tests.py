from __future__ import annotations

from api.itinerary.data_access.itinerary_name_key_builder import ItineraryNameKeyBuilder
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.shared.date_values import DateValues
from api.shared.enums import ScheduleItemKind
from api.shared.enums.transportation_name import TransportationName
from api.walk_graph.domain.master_route_stop_key_builder import MasterRouteStopKeyBuilder


def Test_NameKey_TestRecord_ExpectNormalizedName() -> None:
   transportation = TransportationName.ZOOMOBILE
   start_time = '10:00 AM'
   duration_minutes = 75
   record = ItineraryTransportationRecord(
      transportation=transportation,
      old_likelihood=None,
      new_likelihood=100,
      added_as_attraction=True,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ),
      route='summer' )

   name_key = record.name_key()

   assert name_key == ItineraryNameKeyBuilder.build( record.transportation )


def Test_MasterRouteStopKey_TestRecord_ExpectAttractionStopKey() -> None:
   transportation = TransportationName.ZOOMOBILE
   start_time = '10:00 AM'
   duration_minutes = 75
   record = ItineraryTransportationRecord(
      transportation=transportation,
      old_likelihood=None,
      new_likelihood=100,
      added_as_attraction=True,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ),
      route='summer' )

   stop_key = record.master_route_stop_key()

   assert stop_key == MasterRouteStopKeyBuilder.attraction( record.transportation )


def Test_ScheduleItemKind_TestRecord_ExpectTransportation() -> None:
   transportation = TransportationName.ZOOMOBILE
   start_time = '10:00 AM'
   duration_minutes = 75
   record = ItineraryTransportationRecord(
      transportation=transportation,
      old_likelihood=None,
      new_likelihood=100,
      added_as_attraction=True,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ),
      route='summer' )

   kind = record.schedule_item_kind

   assert kind is ScheduleItemKind.TRANSPORTATION


def Test_Attraction_TestRecord_ExpectTransportationName() -> None:
   transportation = TransportationName.ZOOMOBILE
   start_time = '10:00 AM'
   duration_minutes = 75
   record = ItineraryTransportationRecord(
      transportation=transportation,
      old_likelihood=None,
      new_likelihood=100,
      added_as_attraction=True,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ),
      route='summer' )

   attraction = record.attraction

   assert attraction == record.transportation
