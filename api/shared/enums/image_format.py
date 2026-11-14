from __future__ import annotations

from enum import Enum
from pathlib import Path

from .shared_enum_values import SharedEnumValues


class ImageFormat( str, Enum ):
   # Enum bodies register a member per assigned name, so the shared JSON members
   # have to be written into the class namespace one name at a time.
   __members = SharedEnumValues.load_object_members( 'imageFormat.json' )
   locals().update( {
      member_name: member_definition[ 'kind' ]
      for member_name, member_definition in __members.items()
   } )


   @classmethod
   def matches_data_url( cls, image: str ) -> bool:
      header = image.partition( ',' )[ 0 ]

      return any(
         header.startswith( f'data:{ definition[ "mime" ] }' )
         for definition in cls.__members.values()
      )


   @classmethod
   def extensions( cls ) -> set[ str ]:
      return {
         extension
         for definition in cls.__members.values()
         for extension in definition[ 'extensions' ]
      }


   @classmethod
   def subtype_for( cls, filename: str ) -> str:
      suffix = Path( filename ).suffix.casefold()

      for definition in cls.__members.values():
         if suffix in definition[ 'extensions' ]:
            return str( definition[ 'kind' ] )

      return cls.JPEG.value
