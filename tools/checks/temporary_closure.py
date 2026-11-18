from __future__ import annotations

from datetime import date

from api.shared.enums.item_type import ItemType


class TemporaryClosure():
   place: str
   message: str
   kind: ItemType
   photo_path: str
   start: date | None
   end: date | None


   def __init__(
         self,
         place: str,
         message: str,
         kind: ItemType,
         photo_path: str,
         start: date | None = None,
         end: date | None = None ) -> None:
      self.place = place
      self.message = message
      self.kind = kind
      self.photo_path = photo_path
      self.start = start
      self.end = end
