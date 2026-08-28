from __future__ import annotations

from .attraction_route_stop_mapper import AttractionRouteStopMapper
from .master_route_stop import MasterRouteStop
from ...shared.enums import ScheduleItemKind
from .viewing_spot_reference_mapper import ViewingSpotReferenceMapper


class MasterRouteStopMapper():
   @classmethod
   def map_record( cls, payload: dict[ str, object ] ) -> MasterRouteStop.Stop:
      kind_value = payload.get( 'kind' )

      if kind_value is None:
         raise ValueError( 'Master-route stops require a kind.' )

      kind = ScheduleItemKind.normalize( str( kind_value ) )

      if kind == ScheduleItemKind.ATTRACTION:
         return AttractionRouteStopMapper.map_record( payload )

      if kind == ScheduleItemKind.ANIMAL:
         return ViewingSpotReferenceMapper.map_record( payload )

      raise ValueError( f'Unknown master-route stop kind { repr( kind_value ) }.' )
