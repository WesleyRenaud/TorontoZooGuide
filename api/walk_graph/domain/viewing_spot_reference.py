from __future__ import annotations

from dataclasses import dataclass

from .master_route_stop_key import animal_master_route_stop_key
from .master_route_stop_key import AnimalMasterRouteStopKey
from ...shared.enums import ScheduleItemKind
from ...shared.value_conversion import ValueConversion
from .viewing_spot_name_key import ViewingSpotNameKey


ANIMAL_MASTER_ROUTE_STOP_KEY_LENGTH = 3


@dataclass( frozen=True )
class ViewingSpotReference:
   species: str
   exhibit: str
   name: str | None

   @property
   def kind( self ) -> ScheduleItemKind:
      return ScheduleItemKind.ANIMAL


   def key( self ) -> ViewingSpotNameKey:
      return ( self.species, self.exhibit, self.name )


   def master_route_key( self ) -> AnimalMasterRouteStopKey:
      return animal_master_route_stop_key(
         self.species,
         self.exhibit,
         self.name )


def viewing_spot_reference_from_json(
      payload: dict[ str, object ] ) -> ViewingSpotReference:
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
