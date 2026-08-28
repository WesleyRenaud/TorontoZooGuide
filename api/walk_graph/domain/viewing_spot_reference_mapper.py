from __future__ import annotations

from ...shared.enums import ScheduleItemKind
from ...shared.value_conversion import ValueConversion
from .viewing_spot_reference import ANIMAL_MASTER_ROUTE_STOP_KEY_LENGTH
from .viewing_spot_reference import ViewingSpotReference


class ViewingSpotReferenceMapper():
   @classmethod
   def map_record( cls, payload: dict[ str, object ] ) -> ViewingSpotReference:
      kind = ScheduleItemKind.normalize(
         None if payload.get( 'kind' ) is None else str( payload.get( 'kind' ) ) )

      if kind != ScheduleItemKind.ANIMAL:
         raise ValueError(
            f'Expected animal master-route stop kind, found { repr( payload.get( "kind" ) ) }.' )

      if 'key' not in payload:
         raise ValueError( 'Master-route stops require a key.' )

      key = payload[ 'key' ]

      if not isinstance( key, list ):
         raise ValueError(
            f'Master-route stop key must be a list, found { type( key ).__name__ }.' )

      if len( key ) != ANIMAL_MASTER_ROUTE_STOP_KEY_LENGTH:
         raise ValueError(
            f'Expected master-route stop key length { ANIMAL_MASTER_ROUTE_STOP_KEY_LENGTH }, '
            f'found { len( key ) }.' )

      species = ValueConversion.as_trimmed_string(
         None if key[ 0 ] is None else str( key[ 0 ] ) )
      exhibit = ValueConversion.as_trimmed_string(
         None if key[ 1 ] is None else str( key[ 1 ] ) )

      if not species or not exhibit:
         raise ValueError(
            'Animal master-route stop key requires species and exhibit.' )

      return ViewingSpotReference(
         species=species,
         exhibit=exhibit,
         name=ValueConversion.as_nullable_string(
            None if key[ 2 ] is None else str( key[ 2 ] ) ) )
