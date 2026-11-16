from __future__ import annotations

from dataclasses import dataclass

from .closure_update import ClosureUpdate


@dataclass( frozen=True )
class ClosureUpdatePlan:
   added: list[ ClosureUpdate ]
   ended: list[ ClosureUpdate ]
   extended: list[ ClosureUpdate ]
   trimmed: list[ ClosureUpdate ]


   def count( self ) -> int:
      return (
         len( self.added )
         + len( self.ended )
         + len( self.extended )
         + len( self.trimmed )
      )
