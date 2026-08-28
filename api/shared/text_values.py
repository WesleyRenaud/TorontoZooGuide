from __future__ import annotations


class TextValues():
   @classmethod
   def normalize_for_matching(
         cls,
         value: str | None ) -> str:
      return ( value or '' ).strip().lower()
