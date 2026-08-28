from __future__ import annotations

from .attraction_route_stop import ATTRACTION_MASTER_ROUTE_STOP_KEY_LENGTH
from .attraction_route_stop import AttractionRouteStop
from ...shared.enums import ScheduleItemKind
from ...shared.value_conversion import ValueConversion


class AttractionRouteStopMapper():
   @classmethod
   def map_record( cls, payload: dict[ str, object ] ) -> AttractionRouteStop:
      kind = ScheduleItemKind.normalize(
         None if payload.get( 'kind' ) is None else str( payload.get( 'kind' ) ) )

      if kind != ScheduleItemKind.ATTRACTION:
         raise ValueError(
            f'Expected attraction master-route stop kind, found { repr( payload.get( "kind" ) ) }.' )

      if 'key' not in payload:
         raise ValueError( 'Master-route stops require a key.' )

      key = payload[ 'key' ]

      if not isinstance( key, list ):
         raise ValueError(
            f'Master-route stop key must be a list, found { type( key ).__name__ }.' )

      if len( key ) != ATTRACTION_MASTER_ROUTE_STOP_KEY_LENGTH:
         raise ValueError(
            f'Expected master-route stop key length { ATTRACTION_MASTER_ROUTE_STOP_KEY_LENGTH }, '
            f'found { len( key ) }.' )

      name = ValueConversion.as_trimmed_string(
         None if key[ 0 ] is None else str( key[ 0 ] ) )

      if not name:
         raise ValueError( 'Attraction master-route stop key requires a name.' )

      return AttractionRouteStop( name=name )
