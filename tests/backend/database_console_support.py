from __future__ import annotations

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
from api.models.animal import Animal
from api.models.attraction import Attraction
from api.models.gift_shop import GiftShop
from api.models.restaurant import Restaurant
from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from api.types import Types
from conftest import DbControllers

def get_animal( db: DbControllers, species: str, exhibit: str ) -> Animal:
   animals = AnimalCoordinator.get_animals_viewable_on_day(
      day=15,
      month='June',
      year=2026,
      temp=22,
      include_off_display_animals=True,
      exhibits_to_include=[ exhibit ] )

   return next(
      animal for animal in animals
      if animal.species == species and animal.exhibit == exhibit
   )

def get_animals_for_exhibit(
      species: str,
      exhibit: str,
      include_off_display_animals: bool = True ) -> list[ Animal ]:
   animals = AnimalCoordinator.get_animals_viewable_on_day(
      day=15,
      month='June',
      year=2026,
      temp=22,
      include_off_display_animals=include_off_display_animals,
      exhibits_to_include=[ exhibit ] )

   return [
      animal for animal in animals
      if animal.species == species and animal.exhibit == exhibit
   ]

def get_animal_status_scopes(
      cursor: Types.Cursor,
      species: str,
      exhibit: str ) -> list[ str ]:
   return [
      row[ 'VIEWING_SCOPE' ]
      for row in cursor.execute(
         """   SELECT VIEWING_SCOPE
               FROM AnimalStatus
               WHERE SPECIES = ?
                  AND EXHIBIT = ?
               ORDER BY VIEWING_SCOPE;
         """,
         (
            species,
            exhibit,
         ) ).fetchall()
   ]

def get_restaurant( db: DbControllers, name: str ) -> Restaurant:
   restaurants = RestaurantCoordinator.get_restaurants(
      day=15,
      month='June',
      year=2026,
      include_closed_restaurants=True )

   return next( restaurant for restaurant in restaurants if restaurant.name == name )

def get_gift_shop( db: DbControllers, name: str ) -> GiftShop:
   gift_shops = GiftShopCoordinator.get_gift_shops(
      day=15,
      month='June',
      year=2026,
      include_closed_gift_shops=True )

   return next( gift_shop for gift_shop in gift_shops if gift_shop.name == name )

def get_attraction( db: DbControllers, name: str ) -> Attraction:
   attractions = AttractionCoordinator.get_attractions(
      day=15,
      month='June',
      year=2026,
      include_closed_attractions=True )

   return next( attraction for attraction in attractions if attraction.name == name )
