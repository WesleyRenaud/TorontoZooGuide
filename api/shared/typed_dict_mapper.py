from __future__ import annotations

from .typed_dict import DictSerializable


class TypedDictMapper():
   @classmethod
   def to_dict_with_type(
         cls,
         obj: DictSerializable | dict[ str, object ],
         fallback_type: str ) -> dict[ str, object ]:
      if isinstance( obj, dict ):
         serialized = dict( obj )
      else:
         serialized = obj.to_dict()

      serialized[ 'type' ] = serialized.get( 'type', fallback_type )
      return serialized
