from __future__ import annotations

import re
import unicodedata

from .paths import Paths


class AnimalDetailImage():
   @classmethod
   def normalize( cls, value: str ) -> str:
      text = unicodedata.normalize( 'NFD', value )
      text = ''.join(
         char
         for char in text
         if unicodedata.category( char ) != 'Mn'
      )
      text = text.replace( '&', ' and ' )
      text = text.lower()
      text = text.replace( "'", '' ).replace( '\u2019', '' )
      text = re.sub( r'[^a-z0-9\s-]', '', text )
      text = re.sub( r'\s+', '-', text )
      text = re.sub( r'-+', '-', text )
      return text.strip( '-' )


   @classmethod
   def source( cls, exhibit: str, species: str ) -> str:
      image = (
         Paths.DETAIL_IMAGES
         / 'animals'
         / cls.normalize( exhibit )
         / f'{ cls.normalize( species ) }.png'
      )
      return image.relative_to( Paths.ROOT ).as_posix()
