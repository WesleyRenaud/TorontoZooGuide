from __future__ import annotations

from ...shared.text_values import TextValues


class ItineraryNameKeyBuilder():
   @classmethod
   def build( cls, value: str ) -> str:
      return TextValues.normalize_for_matching( value )
