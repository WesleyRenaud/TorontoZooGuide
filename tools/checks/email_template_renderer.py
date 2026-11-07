from __future__ import annotations

from .paths import Paths


class EmailTemplateRenderer():
   @classmethod
   def render( cls, name: str, **params: object ) -> str:
      template = ( Paths.EMAIL_TEMPLATES / f'{ name }.html' ).read_text().rstrip( '\n' )
      values = {
         key: str( value ).replace( '{', '{{' ).replace( '}', '}}' )
         for key, value in params.items()
      }
      return template.format( **values )
