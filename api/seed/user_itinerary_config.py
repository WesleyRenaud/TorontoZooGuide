from __future__ import annotations

from ..itinerary.data_access.itinerary_error_suppression import clear_itinerary_error_suppressions
from ..types import Cursor


def clear_user_itinerary_config( cursor: Cursor ) -> None:
   clear_itinerary_error_suppressions( cursor )
