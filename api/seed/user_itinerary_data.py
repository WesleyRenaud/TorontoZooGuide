from __future__ import annotations

from ..itinerary.data_access.clear_itinerary import clear_itinerary_animals
from ..itinerary.data_access.clear_itinerary import clear_itinerary_attractions
from ..itinerary.data_access.clear_itinerary import clear_itinerary_date
from ..itinerary.data_access.clear_itinerary import clear_itinerary_guardians_talks
from ..itinerary.data_access.clear_itinerary import clear_itinerary_wild_encounters
from ..types import Cursor


def clear_user_itinerary_data( cursor: Cursor ) -> None:
   clear_itinerary_animals( cursor )
   clear_itinerary_attractions( cursor )
   clear_itinerary_guardians_talks( cursor )
   clear_itinerary_wild_encounters( cursor )
   clear_itinerary_date( cursor )
