from __future__ import annotations

from typing import Any


class ValueConversion:
   @staticmethod
   def as_boolean( value: Any ) -> bool:
      if isinstance( value, bool ):
         return value

      if isinstance( value, int ):
         return value != 0

      return False
