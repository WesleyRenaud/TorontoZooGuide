from __future__ import annotations

from dataclasses import dataclass

from api.shared.typed_dict_mapper import TypedDictMapper


@dataclass
class SampleSerializable():
   name: str


   def to_dict( self ) -> dict[ str, object ]:
      return { 'name': self.name }


def Test_ToDictWithType_TestSerializable_ExpectAddsFallbackType() -> None:
   name = 'Carousel'
   fallback_type = 'attraction'
   sample = SampleSerializable( name=name )

   result = TypedDictMapper.to_dict_with_type( sample, fallback_type )

   assert result[ 'name' ] == sample.name
   assert result[ 'type' ] == fallback_type


def Test_ToDictWithType_TestExistingType_ExpectRetainsExistingType() -> None:
   existing_type = 'customType'
   fallback_type = 'attraction'
   payload = { 'name': 'Carousel', 'type': existing_type }

   result = TypedDictMapper.to_dict_with_type( payload, fallback_type )

   assert result[ 'type' ] == existing_type


def Test_ToDictWithType_TestPlainDict_ExpectAddsFallbackType() -> None:
   name = 'Carousel'
   fallback_type = 'attraction'
   payload = { 'name': name }

   result = TypedDictMapper.to_dict_with_type( payload, fallback_type )

   assert result[ 'name' ] == name
   assert result[ 'type' ] == fallback_type
