from __future__ import annotations

from dataclasses import dataclass

from .itinerary_save_issue import ItinerarySaveIssue


@dataclass( frozen=True )
class ItinerarySaveResult:
   success: bool
   issues: tuple[ ItinerarySaveIssue, ... ] = ()


   def __bool__( self ) -> bool:
      return self.success
