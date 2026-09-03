from __future__ import annotations

import pytest

from api.walk_graph.domain.viewing_spot_reference import ViewingSpotReference
from api.walk_graph.domain.viewing_spot_reference_mapper import ViewingSpotReferenceMapper

def Test_MapRecord_TestValidAnimal_ExpectViewingSpotReference() -> None:
   reference = ViewingSpotReferenceMapper.map_record( {
      'kind': 'animal',
      'key': [ 'Western Grey Kangaroo', 'Australasia Outdoor', 'Savanna Overlook' ],
   } )

   assert isinstance( reference, ViewingSpotReference )
   assert reference.species == 'Western Grey Kangaroo'
   assert reference.exhibit == 'Australasia Outdoor'
   assert reference.name == 'Savanna Overlook'

def Test_MapRecord_TestWrongKind_ExpectValueError() -> None:
   with pytest.raises( ValueError, match='animal master-route stop kind' ):
      ViewingSpotReferenceMapper.map_record( {
         'kind': 'attraction',
         'key': [ 'Western Grey Kangaroo', 'Australasia Outdoor', None ],
      } )

def Test_MapRecord_TestNonListKey_ExpectValueError() -> None:
   with pytest.raises( ValueError, match='list' ):
      ViewingSpotReferenceMapper.map_record( {
         'kind': 'animal',
         'key': 'Western Grey Kangaroo',
      } )

def Test_MapRecord_TestMissingSpeciesOrExhibit_ExpectValueError() -> None:
   with pytest.raises( ValueError, match='species and exhibit' ):
      ViewingSpotReferenceMapper.map_record( {
         'kind': 'animal',
         'key': [ '   ', 'Australasia Outdoor', None ],
      } )

   with pytest.raises( ValueError, match='species and exhibit' ):
      ViewingSpotReferenceMapper.map_record( {
         'kind': 'animal',
         'key': [ 'Western Grey Kangaroo', '   ', None ],
      } )
