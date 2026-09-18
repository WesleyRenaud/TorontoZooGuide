from __future__ import annotations

from ..data_access.itinerary_animal_record import ItineraryAnimalRecord
from ..data_access.itinerary_provider import ItineraryProvider
from ..data_access.itinerary_transportation_animal_provider import ItineraryTransportationAnimalProvider
from .itinerary_transportation_animal_likelihood_resolver import ItineraryTransportationAnimalLikelihoodResolver
from ...models.animal_diff import AnimalDiff
from ...transportation.data_access.transportation_animal_provider import TransportationAnimalProvider
from ...transportation.data_access.transportation_animal_record import TransportationAnimalRecord
from ...types import Types


class ItineraryTransportationAnimalSyncer():
   @classmethod
   def apply( cls, conn: Types.Connection ) -> None:
      catalog_links = TransportationAnimalProvider.fetch_all( conn )
      present_leg_keys = {
         ( leg.transportation, leg.from_station, leg.to_station )
         for leg in ItineraryProvider.fetch_itinerary_transportation_leg_rows( conn )
      }
      wanted_links = [
         link
         for link in catalog_links
         if link.leg_key() in present_leg_keys
      ]
      existing_rows = ItineraryProvider.fetch_itinerary_animal_rows( conn )
      cur = conn.cursor()

      try:
         cls._upsert_wanted_links( cur, conn, wanted_links, existing_rows )
         cls._delete_stale_rows( cur, conn, wanted_links, catalog_links, existing_rows )
      finally:
         cur.close()


   @classmethod
   def promote_saved_animals(
         cls,
         conn: Types.Connection,
         animals: list[ AnimalDiff ] ) -> None:
      if not animals:
         return

      existing_by_spot = {
         row.viewing_spot_key(): row
         for row in ItineraryProvider.fetch_itinerary_animal_rows( conn )
      }
      cur = conn.cursor()

      try:
         for animal in animals:
            existing_row = existing_by_spot.get( animal.viewing_spot_key() )

            if existing_row is None or not existing_row.added_by_transportation:
               continue

            ItineraryTransportationAnimalProvider.delete_added_by_transportation(
               cur,
               existing_row )
      finally:
         cur.close()


   @classmethod
   def _upsert_wanted_links(
         cls,
         cur: Types.Cursor,
         conn: Types.Connection,
         wanted_links: list[ TransportationAnimalRecord ],
         existing_rows: list[ ItineraryAnimalRecord ] ) -> None:
      if not wanted_links:
         return

      existing_by_spot = {
         row.viewing_spot_key(): row
         for row in existing_rows
      }
      likelihood_lookup = ItineraryTransportationAnimalLikelihoodResolver.resolve(
         conn,
         wanted_links )

      for link in wanted_links:
         existing_row = existing_by_spot.get( link.viewing_spot_key() )
         new_likelihood = likelihood_lookup.for_link( link )

         if existing_row is None:
            ItineraryTransportationAnimalProvider.insert_added_by_transportation(
               cur,
               link,
               new_likelihood=new_likelihood )
            continue

         if existing_row.added_by_transportation:
            ItineraryTransportationAnimalProvider.update_added_by_transportation_likelihood(
               cur,
               link,
               new_likelihood=new_likelihood )


   @classmethod
   def _delete_stale_rows(
         cls,
         cur: Types.Cursor,
         conn: Types.Connection,
         wanted_links: list[ TransportationAnimalRecord ],
         catalog_links: list[ TransportationAnimalRecord ],
         existing_rows: list[ ItineraryAnimalRecord ] ) -> None:
      wanted_spots = {
         link.viewing_spot_key()
         for link in wanted_links
      }
      catalog_by_spot = {
         link.viewing_spot_key(): link
         for link in catalog_links
      }
      present_transportation_names = ItineraryProvider.fetch_itinerary_transportation_names( conn )

      for existing_row in existing_rows:
         if (
               not existing_row.added_by_transportation
               or existing_row.viewing_spot_key() in wanted_spots ):
            continue

         catalog_link = catalog_by_spot.get( existing_row.viewing_spot_key() )

         if (
               catalog_link is not None
               and catalog_link.transportation in present_transportation_names ):
            continue

         ItineraryTransportationAnimalProvider.delete_added_by_transportation(
            cur,
            existing_row )
