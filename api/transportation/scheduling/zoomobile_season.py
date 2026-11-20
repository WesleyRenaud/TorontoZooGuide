from __future__ import annotations

from ...shared.enums.transportation_name import TransportationName
from ...shared.enums.transportation_route_id import TransportationRouteId


class ZoomobileSeason():
   SUMMER_MONTHS = ( 5, 6, 7, 8, 9, 10 )
   WINTER_MONTHS = ( 11, 12, 1, 2, 3, 4 )


   @classmethod
   def route_for( cls, transportation: str, month: int ) -> str | None:
      if transportation != TransportationName.ZOOMOBILE:
         return None

      if month in cls.SUMMER_MONTHS:
         return TransportationRouteId.SUMMER.value

      if month in cls.WINTER_MONTHS:
         return TransportationRouteId.WINTER.value

      return None
