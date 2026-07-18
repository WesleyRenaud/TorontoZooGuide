from __future__ import annotations

from .attraction_route_stop import attraction_route_stop_from_json
from .attraction_route_stop import AttractionRouteStop
from .master_route_stop_key import MasterRouteStopKey
from ...shared.enums import ScheduleItemKind
from .viewing_spot_reference import viewing_spot_reference_from_json
from .viewing_spot_reference import ViewingSpotReference


MasterRouteStop = ViewingSpotReference | AttractionRouteStop


def is_animal_route_stop( stop: MasterRouteStop ) -> bool:
   # TODO: Narrow or replace once attraction stops are handled everywhere animals are.
   return stop.kind == ScheduleItemKind.ANIMAL


def is_attraction_route_stop( stop: MasterRouteStop ) -> bool:
   return stop.kind == ScheduleItemKind.ATTRACTION


def master_route_stop_key( stop: MasterRouteStop ) -> MasterRouteStopKey:
   return stop.master_route_key()


def master_route_stop_from_json(
      payload: dict[ str, object ] ) -> MasterRouteStop:
   kind_value = payload.get( 'kind' )

   if kind_value is None:
      raise ValueError( 'Master-route stops require a kind.' )

   kind = ScheduleItemKind.normalize( str( kind_value ) )

   if kind == ScheduleItemKind.ATTRACTION:
      return attraction_route_stop_from_json( payload )

   if kind == ScheduleItemKind.ANIMAL:
      return viewing_spot_reference_from_json( payload )

   raise ValueError( f'Unknown master-route stop kind { repr( kind_value ) }.' )
