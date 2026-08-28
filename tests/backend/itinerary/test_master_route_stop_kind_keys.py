from __future__ import annotations

from api.shared.enums import ScheduleItemKind
from api.walk_graph.domain.attraction_route_stop import AttractionRouteStop
from api.walk_graph.domain.master_route_stop_mapper import MasterRouteStopMapper
from api.walk_graph.domain.viewing_spot_reference import ViewingSpotReference


def test_master_route_stops_use_kind_prefixed_keys() -> None:
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


def test_master_route_stop_from_json_requires_kind() -> None:
   try:
      MasterRouteStopMapper.map_record( {
         'key': [ 'Western Grey Kangaroo', 'Australasia Outdoor', None ],
      } )
   except ValueError as error:
      assert 'kind' in str( error )
   else:
      raise AssertionError( 'Expected missing kind to raise ValueError' )


def test_master_route_stop_from_json_requires_key() -> None:
   try:
      MasterRouteStopMapper.map_record( {
         'kind': 'animal',
         'species': 'Western Grey Kangaroo',
         'exhibit': 'Australasia Outdoor',
         'name': None,
      } )
   except ValueError as error:
      assert 'key' in str( error )
   else:
      raise AssertionError( 'Expected missing key to raise ValueError' )


def test_master_route_stop_from_json_rejects_wrong_key_length() -> None:
   try:
      MasterRouteStopMapper.map_record( {
         'kind': 'animal',
         'key': [ 'Western Grey Kangaroo', 'Australasia Outdoor' ],
      } )
   except ValueError as error:
      assert 'length' in str( error )
   else:
      raise AssertionError( 'Expected wrong key length to raise ValueError' )

   try:
      MasterRouteStopMapper.map_record( {
         'kind': 'attraction',
         'key': [ 'Splash Island', 'extra' ],
      } )
   except ValueError as error:
      assert 'length' in str( error )
   else:
      raise AssertionError( 'Expected wrong key length to raise ValueError' )
