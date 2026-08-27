from __future__ import annotations

from datetime import date

from .transportation_day_loop_fetcher import TransportationDayLoopFetcher
from ...types import Connection


class TransportationRouteDurationResolver():
   @classmethod
   def minutes(
         cls,
         conn: Connection,
         *,
         transportation: str,
         target_date: date,
         ) -> int | None:
      day_loop = TransportationDayLoopFetcher.fetch(
         conn,
         transportation=transportation,
         target_date=target_date,
         )

      if day_loop is None:
         return None

      return day_loop.duration_minutes()
