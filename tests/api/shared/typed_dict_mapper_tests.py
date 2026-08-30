from __future__ import annotations

from dataclasses import dataclass

from api.shared.typed_dict_mapper import TypedDictMapper


@dataclass
class SampleSerializable():
   name: str


   def to_dict( self ) -> dict[ str, object ]:
      return { 'name': self.name }


def Test_ToDictWithType_TestSerializable_ExpectAddsFallbackType() -> None:
   result = TypedDictMapper.to_dict_with_type(
      SampleSerializable( name='Carousel' ),
      'attraction' )

   assert result == {
      'name': 'Carousel',
      'type': 'attraction',
   }


def Test_ToDictWithType_TestExistingType_ExpectRetainsExistingType() -> None:
   result = TypedDictMapper.to_dict_with_type(
      { 'name': 'Carousel', 'type': 'customType' },
      'attraction' )

   assert result[ 'type' ] == 'customType'


def Test_ToDictWithType_TestPlainDict_ExpectAddsFallbackType() -> None:
   result = TypedDictMapper.to_dict_with_type(
      { 'name': 'Carousel' },
      'attraction' )

   assert result == {
      'name': 'Carousel',
      'type': 'attraction',
   }
