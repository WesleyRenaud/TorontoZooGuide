from __future__ import annotations

from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_name_key_builder import ItineraryNameKeyBuilder
from api.shared.date_values import DateValues
from api.walk_graph.domain.master_route_stop_key_builder import MasterRouteStopKeyBuilder


def Test_NameKey_TestRecord_ExpectNormalizedName() -> None:
   attraction = 'Conservation Carousel'
   start_time = '11:00 AM'
   duration_minutes = 20
   record = ItineraryAttractionRecord(
      attraction=attraction,
      old_likelihood=None,
      new_likelihood=100,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ) )

   name_key = record.name_key()

   assert name_key == ItineraryNameKeyBuilder.build( record.attraction )


def Test_MasterRouteStopKey_TestRecord_ExpectAttractionStopKey() -> None:
   attraction = 'Conservation Carousel'
   start_time = '11:00 AM'
   duration_minutes = 20
   record = ItineraryAttractionRecord(
      attraction=attraction,
      old_likelihood=None,
      new_likelihood=100,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ) )

   stop_key = record.master_route_stop_key()

   assert stop_key == MasterRouteStopKeyBuilder.attraction( record.attraction )
