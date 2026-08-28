from __future__ import annotations

from ..data_access.itinerary_provider import ItineraryProvider
from ...shared.calendar_dates import DateValues
from .transportation_day_loop_fetcher import TransportationDayLoopFetcher
from ...types import Types


class TransportationDefaultDurationResolver():
   @classmethod
   def resolve(
         cls,
         conn: Types.Connection,
         transportation: str ) -> int | None:
      visit_date = ItineraryProvider.fetch_itinerary_date( conn )
      parsed_visit_date = DateValues.parse_date_value( visit_date )

      if parsed_visit_date is None:
         return None

      day_loop = TransportationDayLoopFetcher.fetch(
         conn,
         transportation=transportation,
         target_date=parsed_visit_date )

      if day_loop is None:
         return None

      return day_loop.duration_seconds()
