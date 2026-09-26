from __future__ import annotations

import pytest

from api.walk_graph.domain.viewing_spot_reference import ViewingSpotReference
from api.walk_graph.domain.viewing_spot_reference_mapper import ViewingSpotReferenceMapper


def Test_MapRecord_TestValidAnimal_ExpectViewingSpotReference() -> None:
   species = 'Western Grey Kangaroo'
   exhibit = 'Australasia Outdoor'
   name = 'Savanna Overlook'
   record = {
      'kind': 'animal',
      'key': [ species, exhibit, name ],
   }

   reference = ViewingSpotReferenceMapper.map_record( record )

   assert isinstance( reference, ViewingSpotReference )
   assert reference.species == species
   assert reference.exhibit == exhibit
   assert reference.name == name


def Test_MapRecord_TestWrongKind_ExpectValueError() -> None:
   record = {
      'kind': 'attraction',
      'key': [ 'Western Grey Kangaroo', 'Australasia Outdoor', None ],
   }

   with pytest.raises( ValueError, match='animal master-route stop kind' ):
      ViewingSpotReferenceMapper.map_record( record )


def Test_MapRecord_TestNonListKey_ExpectValueError() -> None:
   record = {
      'kind': 'animal',
      'key': 'Western Grey Kangaroo',
   }

   with pytest.raises( ValueError, match='list' ):
      ViewingSpotReferenceMapper.map_record( record )


def Test_MapRecord_TestMissingSpecies_ExpectValueError() -> None:
   record = {
      'kind': 'animal',
      'key': [ '   ', 'Australasia Outdoor', None ],
   }

   with pytest.raises( ValueError, match='species and exhibit' ):
      ViewingSpotReferenceMapper.map_record( record )


def Test_MapRecord_TestMissingExhibit_ExpectValueError() -> None:
   record = {
      'kind': 'animal',
      'key': [ 'Western Grey Kangaroo', '   ', None ],
   }

   with pytest.raises( ValueError, match='species and exhibit' ):
      ViewingSpotReferenceMapper.map_record( record )
