from __future__ import annotations

from ..itinerary.data_access.itinerary_status import clear_itinerary_status_suppressions
from ..types import Cursor


def clear_user_itinerary_config( cursor: Cursor ) -> None:
   clear_itinerary_status_suppressions( cursor )

