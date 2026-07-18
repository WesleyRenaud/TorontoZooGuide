from __future__ import annotations

from dataclasses import dataclass

from .master_route_stop_key import attraction_master_route_stop_key
from .master_route_stop_key import AttractionMasterRouteStopKey
from ...shared.enums import ScheduleItemKind
from ...shared.value_conversion import ValueConversion


ATTRACTION_MASTER_ROUTE_STOP_KEY_LENGTH = 1


@dataclass( frozen=True )
class AttractionRouteStop:
   name: str

   @property
   def kind( self ) -> ScheduleItemKind:
      return ScheduleItemKind.ATTRACTION


   def master_route_key( self ) -> AttractionMasterRouteStopKey:
      return attraction_master_route_stop_key( self.name )


def attraction_route_stop_from_json(
      payload: dict[ str, object ] ) -> AttractionRouteStop:
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
