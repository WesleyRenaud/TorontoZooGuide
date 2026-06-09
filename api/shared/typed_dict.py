from __future__ import annotations

from typing import Protocol


class DictSerializable( Protocol ):
   def to_dict( self ) -> dict[ str, object ]:
      ...


def to_dict_with_type(
      obj: DictSerializable | dict[ str, object ],
      fallback_type: str ) -> dict[ str, object ]:
   if isinstance( obj, dict ):
      serialized = dict( obj )
   else:
      serialized = obj.to_dict()

   serialized[ 'type' ] = serialized.get( 'type', fallback_type )
   return serialized
