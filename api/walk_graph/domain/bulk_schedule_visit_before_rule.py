from __future__ import annotations

from dataclasses import dataclass

from .viewing_spot_reference import ViewingSpotReference


@dataclass( frozen=True )
class BulkScheduleVisitBeforeRule:
   visit_first: ViewingSpotReference
   visit_before: tuple[ ViewingSpotReference, ... ]
