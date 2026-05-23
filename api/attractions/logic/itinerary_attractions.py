from __future__ import annotations

from datetime import date

from ...models import Attraction
from ...itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ...itinerary.data_access.itinerary_name_key import itinerary_name_key


def build_itinerary_attractions(
      attractions: list[ Attraction ],
      saved_attractions: list[ ItineraryAttractionRecord ] ) -> list[ Attraction ]:
   attractions_filter = {
      saved_attraction.name_key()
      for saved_attraction in saved_attractions
   }

   attractions = [
      attraction for attraction in attractions
      if itinerary_name_key( attraction.name ) in attractions_filter
   ]

   saved_attraction_by_name = {
      saved_attraction.name_key(): saved_attraction
      for saved_attraction in saved_attractions
   }

   for attraction in attractions:
      saved_attraction = saved_attraction_by_name.get(
         itinerary_name_key( attraction.name ) )

      if saved_attraction == None:
         continue

      attraction.old_likelihood = saved_attraction.old_likelihood

   attractions.sort( key=lambda attraction: ( attraction.name or '' ).lower() )

   return attractions
