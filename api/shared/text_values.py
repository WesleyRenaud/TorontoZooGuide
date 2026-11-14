from __future__ import annotations


class TextValues():
   @classmethod
   def normalize_for_matching(
         cls,
         value: str | None ) -> str:
      return ( value or '' ).strip().lower()


   @classmethod
   def spaced( cls, value: str ) -> str:
      return f' { value } '


   @classmethod
   def plural( cls, value: str ) -> str:
      return f'{ value }s'


   @classmethod
   def beside( cls, first: str, second: str ) -> str:
      return f'{ first } { second }'
