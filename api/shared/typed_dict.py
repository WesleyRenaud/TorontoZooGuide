from __future__ import annotations


def to_dict_with_type(
      obj: object,
      fallback_type: str ) -> dict[ str, object ]:
   if hasattr( obj, 'to_dict' ):
      serialized = obj.to_dict()
   elif isinstance( obj, dict ):
      serialized = dict( obj )
   else:
      serialized = {}

   serialized[ 'type' ] = serialized.get( 'type', fallback_type )
   return serialized
