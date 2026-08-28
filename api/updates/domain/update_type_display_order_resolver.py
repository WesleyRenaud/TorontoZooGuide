from __future__ import annotations

from .update_type import UpdateType


class UpdateTypeDisplayOrderResolver():
   @classmethod
   def resolve(
         cls,
         update_type: str | None ) -> int:
      normalized = UpdateType.normalize( update_type )

      if normalized is None:
         return len( UpdateType )

      return normalized.order
