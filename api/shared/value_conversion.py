from __future__ import annotations

from typing import Any


class ValueConversion:
   @staticmethod
   def as_trimmed_string( value: Any ) -> str:
      if value is None:
         return ''

      return str( value ).strip()


   @staticmethod
   def as_nullable_string( value: Any ) -> str | None:
      normalized = ValueConversion.as_trimmed_string( value )

      return normalized or None


   @staticmethod
   def as_boolean( value: Any ) -> bool:
      if isinstance( value, bool ):
         return value

      if isinstance( value, int ):
         return value != 0

      return False
