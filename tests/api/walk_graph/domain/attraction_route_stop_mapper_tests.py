from __future__ import annotations

import pytest

from api.walk_graph.domain.attraction_route_stop_mapper import AttractionRouteStopMapper


def Test_MapRecord_TestValidAttraction_ExpectRouteStop() -> None:
   name = 'Kangaroo Walk-Thru'
   record = {
      'kind': 'attraction',
      'key': [ name ],
   }

   stop = AttractionRouteStopMapper.map_record( record )

   assert stop.name == name


def Test_MapRecord_TestWrongKind_ExpectValueError() -> None:
   record = {
      'kind': 'animal',
      'key': [ 'Kangaroo Walk-Thru' ],
   }

   with pytest.raises( ValueError, match='attraction master-route stop kind' ):
      AttractionRouteStopMapper.map_record( record )


def Test_MapRecord_TestMissingKey_ExpectValueError() -> None:
   record = {
      'kind': 'attraction',
   }

   with pytest.raises( ValueError, match='key' ):
      AttractionRouteStopMapper.map_record( record )


def Test_MapRecord_TestNonListKey_ExpectValueError() -> None:
   record = {
      'kind': 'attraction',
      'key': 'Kangaroo Walk-Thru',
   }

   with pytest.raises( ValueError, match='list' ):
      AttractionRouteStopMapper.map_record( record )


def Test_MapRecord_TestEmptyName_ExpectValueError() -> None:
   record = {
      'kind': 'attraction',
      'key': [ '   ' ],
   }

   with pytest.raises( ValueError, match='name' ):
      AttractionRouteStopMapper.map_record( record )
