from __future__ import annotations

from typing import Any

from api.models.active_transportation_route import ActiveTransportationRoute
from api.models.transportation import Transportation
from api.models.transportation_station import TransportationStation


class StubTransportationCoordinator():
   instances: list[ StubTransportationCoordinator ] = []
   default_success: bool = True


   def __init__(
         self,
         *,
         transportations: list[ Transportation ],
         transportation_routes: list[ dict[ str, object ] ],
         transportation_route: ActiveTransportationRoute,
         transportation_station_names: list[ str ] ) -> None:
      self.transportations = transportations
      self.transportation_routes = transportation_routes
      self.transportation_route = transportation_route
      self.transportation_station_names = transportation_station_names
      self.calls: list[ tuple[ str, dict[ str, Any ] ] ] = []
      self.closed = False
      StubTransportationCoordinator.instances.append( self )


   def close( self ) -> None:
      self.closed = True


   def get_transportations(
         self,
         *,
         day: int,
         month: str,
         year: int ) -> list[ Transportation ]:
      self.calls.append(
         (
            'get_transportations',
            {
               'day': day,
               'month': month,
               'year': year,
            }
         )
      )
      return list( self.transportations )


   def get_transportation_routes( self ) -> list[ dict[ str, object ] ]:
      self.calls.append( ( 'get_transportation_routes', {} ) )
      return list( self.transportation_routes )


   def get_transportation_route(
         self,
         *,
         route: str,
         day: int,
         month: str,
         year: int,
         transportation_stations_to_include: list[ str ] | None = None,
         transportation: str ) -> ActiveTransportationRoute:
      self.calls.append(
         (
            'get_transportation_route',
            {
               'route': route,
               'day': day,
               'month': month,
               'year': year,
               'transportation_stations_to_include': transportation_stations_to_include,
               'transportation': transportation,
            }
         )
      )
      return self.transportation_route


   def get_transportation_station_names(
         self,
         *,
         transportation: str ) -> list[ str ]:
      self.calls.append(
         (
            'get_transportation_station_names',
            { 'transportation': transportation },
         )
      )
      return list( self.transportation_station_names )


   def set_transportation_station_as_closed( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_transportation_station_as_closed', kwargs ) )
      return StubTransportationCoordinator.default_success


   def set_transportation_station_as_open( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_transportation_station_as_open', kwargs ) )
      return StubTransportationCoordinator.default_success


   def set_current_transportation_route( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_current_transportation_route', kwargs ) )
      return StubTransportationCoordinator.default_success
