from __future__ import annotations


def itinerary_name_key( value: str ) -> str:
   return ( value or '' ).strip().lower()
