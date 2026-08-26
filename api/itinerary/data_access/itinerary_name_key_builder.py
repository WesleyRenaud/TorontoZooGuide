from __future__ import annotations

from ...shared.name_matching_query import normalize_search_key


class ItineraryNameKeyBuilder():
   @classmethod
   def build( cls, value: str ) -> str:
      return normalize_search_key( value )
