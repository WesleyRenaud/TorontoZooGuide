from __future__ import annotations

import pytest

from api.shared.enums import ScheduleItemKind
from api.walk_graph.domain.attraction_route_stop import AttractionRouteStop
from api.walk_graph.domain.master_route_stop_mapper import MasterRouteStopMapper
from api.walk_graph.domain.viewing_spot_reference import ViewingSpotReference


def Test_MapRecord_TestAnimalAndAttraction_ExpectKindPrefixedKeys() -> None:
   animal = MasterRouteStopMapper.map_record( {
      'kind': 'animal',
      'key': [ 'Western Grey Kangaroo', 'Australasia Outdoor', None ],
   } )
   attraction = MasterRouteStopMapper.map_record( {
      'kind': 'attraction',
      'key': [ 'Kangaroo Walk-Thru' ],
   } )

   assert isinstance( animal, ViewingSpotReference )
   assert animal.kind == ScheduleItemKind.ANIMAL
   assert animal.species == 'Western Grey Kangaroo'
   assert animal.exhibit == 'Australasia Outdoor'
   assert animal.name is None
   assert animal.master_route_key() == (
      ScheduleItemKind.ANIMAL,
      'Western Grey Kangaroo',
      'Australasia Outdoor',
      None,
   )

   assert isinstance( attraction, AttractionRouteStop )
   assert attraction.kind == ScheduleItemKind.ATTRACTION
   assert attraction.name == 'Kangaroo Walk-Thru'
   assert attraction.master_route_key() == (
      ScheduleItemKind.ATTRACTION,
      'Kangaroo Walk-Thru',
   )


def Test_MapRecord_TestMissingKind_ExpectValueError() -> None:
   with pytest.raises( ValueError, match='kind' ):
      MasterRouteStopMapper.map_record( {
         'key': [ 'Western Grey Kangaroo', 'Australasia Outdoor', None ],
      } )


def Test_MapRecord_TestMissingKey_ExpectValueError() -> None:
   with pytest.raises( ValueError, match='key' ):
      MasterRouteStopMapper.map_record( {
         'kind': 'animal',
         'species': 'Western Grey Kangaroo',
         'exhibit': 'Australasia Outdoor',
         'name': None,
      } )


def Test_MapRecord_TestWrongKeyLength_ExpectValueError() -> None:
   with pytest.raises( ValueError, match='length' ):
      MasterRouteStopMapper.map_record( {
         'kind': 'animal',
         'key': [ 'Western Grey Kangaroo', 'Australasia Outdoor' ],
      } )

   with pytest.raises( ValueError, match='length' ):
      MasterRouteStopMapper.map_record( {
         'kind': 'attraction',
         'key': [ 'Splash Island', 'extra' ],
      } )
