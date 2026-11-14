from __future__ import annotations


class RestroomNotice():
   restroom: str
   message: str
   closure: bool


   def __init__( self, restroom: str, message: str, closure: bool ) -> None:
      self.restroom = restroom
      self.message = message
      self.closure = closure
