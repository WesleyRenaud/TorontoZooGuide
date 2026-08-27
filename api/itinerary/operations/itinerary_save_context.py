from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..conflicts.itinerary_unschedule_confirmations import ItineraryUnscheduleRequirements
from ..data_access.itinerary_save_input import ItinerarySaveInput
from ..data_access.saved_itinerary import SavedItinerary
from ..data_access.validated_itinerary import ValidatedItinerary
from ..domain.itinerary_adjustment import ItineraryAdjustment
from ...models import Itinerary
from ...shared.enums import ItineraryErrorType
from ...types import Connection
from ...types import DateKey


@dataclass( frozen=True )
class ItinerarySaveContext:
   conn: Connection
   save_input: ItinerarySaveInput
   validated_itinerary: ValidatedItinerary
   current_itinerary: Itinerary
   old_visit_date: DateKey | None
   saved_itinerary: SavedItinerary | None
   unschedule_requirements: ItineraryUnscheduleRequirements
   itinerary_controller_kwargs: dict[ str, Any ]
   adjustments: list[ ItineraryAdjustment ] = field( default_factory=list )
   suppressed_warnings: list[ ItineraryErrorType ] = field( default_factory=list )
