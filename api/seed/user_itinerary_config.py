from __future__ import annotations

from ..itinerary.data_access.itinerary_status_provider import ItineraryStatusProvider
from ..types import Cursor


def clear_user_itinerary_config( cursor: Cursor ) -> None:
   ItineraryStatusProvider.clear_itinerary_status_suppressions( cursor )

