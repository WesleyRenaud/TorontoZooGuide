from __future__ import annotations

from .update_type import UpdateType


class UpdateTypeValueNormalizer():
   @classmethod
   def normalize(
         cls,
         update_type: str ) -> str | None:
      normalized = UpdateType.normalize( update_type )

      if normalized is None:
         return None

      return normalized.value
