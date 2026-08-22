from __future__ import annotations

from ..data_access.transportation import fetch_transportation_records
from ..data_access.transportation_route import fetch_transportation_routes_by_name
from ..domain.transportation import build_transportations
from ..domain.transportation_route import group_transportation_routes
from ...models.transportation import Transportation
from ...request_connection import get_connection
from ..search.transportations_matching_query import build_transportations_matching_query
from ...shared.opening_schedule_visit_context import resolve_opening_schedule_visit_context
from ...types import MonthInput, VisitDay, VisitYear


class TransportationCoordinator():
   @classmethod
   def get_transportations(
         cls,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear ) -> list[ Transportation ]:
      context = resolve_opening_schedule_visit_context(
         day=day,
         month=month,
         year=year )

      return build_transportations(
         fetch_transportation_records(
            get_connection(),
            visit_date=context.target_date ),
         context=context )


   @classmethod
   def get_transportations_matching_query(
         cls,
         query: str,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear ) -> list[ Transportation ]:
      return build_transportations_matching_query(
         cls.get_transportations(
            day=day,
            month=month,
            year=year ),
         query )


   @classmethod
   def get_transportation_routes( cls ) -> list[ dict[ str, object ] ]:
      return group_transportation_routes(
         fetch_transportation_routes_by_name( get_connection() ) )
