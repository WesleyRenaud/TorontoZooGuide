from __future__ import annotations

from ..scheduling.transportation_current_route_schedule import TransportationCurrentRouteSchedule
from ...types import Types


class TransportationRouteScheduleMapper():
   @classmethod
   def map_record(
         cls,
         row: Types.Row ) -> TransportationCurrentRouteSchedule:
      return TransportationCurrentRouteSchedule(
         route=row[ 'ROUTE' ],
         start_date=row[ 'SCHEDULE_START_DATE' ],
         end_date=row[ 'SCHEDULE_END_DATE' ],
      )


   @classmethod
   def map_records(
         cls,
         rows: list[ Types.Row ] ) -> list[ TransportationCurrentRouteSchedule ]:
      return [ cls.map_record( row ) for row in rows ]
