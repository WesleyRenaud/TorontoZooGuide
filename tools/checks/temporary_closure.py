from __future__ import annotations

from api.shared.enums.item_type import ItemType


class TemporaryClosure():
   place: str
   message: str
   kind: ItemType
   photo_path: str


   def __init__(
         self,
         place: str,
         message: str,
         kind: ItemType,
         photo_path: str ) -> None:
      self.place = place
      self.message = message
      self.kind = kind
      self.photo_path = photo_path
