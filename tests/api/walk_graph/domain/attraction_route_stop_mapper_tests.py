from __future__ import annotations

import pytest

from api.walk_graph.domain.attraction_route_stop_mapper import AttractionRouteStopMapper

def Test_MapRecord_TestValidAttraction_ExpectRouteStop() -> None:
   stop = AttractionRouteStopMapper.map_record( {
      'kind': 'attraction',
      'key': [ 'Kangaroo Walk-Thru' ],
   } )

   assert stop.name == 'Kangaroo Walk-Thru'

def Test_MapRecord_TestWrongKind_ExpectValueError() -> None:
   with pytest.raises( ValueError, match='attraction master-route stop kind' ):
      AttractionRouteStopMapper.map_record( {
         'kind': 'animal',
         'key': [ 'Kangaroo Walk-Thru' ],
      } )

def Test_MapRecord_TestMissingKey_ExpectValueError() -> None:
   with pytest.raises( ValueError, match='key' ):
      AttractionRouteStopMapper.map_record( {
         'kind': 'attraction',
      } )

def Test_MapRecord_TestNonListKey_ExpectValueError() -> None:
   with pytest.raises( ValueError, match='list' ):
      AttractionRouteStopMapper.map_record( {
         'kind': 'attraction',
         'key': 'Kangaroo Walk-Thru',
      } )

def Test_MapRecord_TestEmptyName_ExpectValueError() -> None:
   with pytest.raises( ValueError, match='name' ):
      AttractionRouteStopMapper.map_record( {
         'kind': 'attraction',
         'key': [ '   ' ],
      } )
