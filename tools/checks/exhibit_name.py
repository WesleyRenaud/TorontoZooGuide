from __future__ import annotations

from .website_page import WebsitePage


class ExhibitName():
   KEY_REPLACEMENTS = {
      'african': 'africa',
   }


   @classmethod
   def key( cls, value: str ) -> str:
      normalized = WebsitePage.normalize_name( value )

      for source, replacement in cls.KEY_REPLACEMENTS.items():
         normalized = normalized.replace( source, replacement )

      return normalized


   @classmethod
   def matching( cls, location: str, exhibits: list[ str ] ) -> list[ str ]:
      website_key = cls.key( location )
      exact = [
         name
         for name in exhibits
         if cls.key( name ) == website_key
      ]

      if exact:
         return exact

      return [
         name
         for name in exhibits
         if cls.key( name ).startswith( f'{ website_key } ' )
      ]
