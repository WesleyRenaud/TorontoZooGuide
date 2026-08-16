from __future__ import annotations

from ..data_access.transportation_route_record import TransportationRouteRecord


def group_transportation_routes(
      route_records: list[ TransportationRouteRecord ],
) -> list[ dict[ str, object ] ]:
   transportations_by_name: dict[ str, list[ str ] ] = {}

   for route_record in route_records:
      if route_record.transportation not in transportations_by_name:
         transportations_by_name[ route_record.transportation ] = []

      transportations_by_name[ route_record.transportation ].append(
         route_record.route )

   return [
      {
         'name': transportation_name,
         'routes': routes,
      }
      for transportation_name, routes in transportations_by_name.items()
   ]
