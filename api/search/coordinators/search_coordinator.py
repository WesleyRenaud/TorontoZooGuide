from __future__ import annotations

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ..enrich_transportation_attraction_route_durations import enrich_transportation_attraction_route_durations_for_visit
from ...giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
from ...guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ...models import Animal
from ...models import Attraction
from ...models import GiftShop
from ...models import GuardiansTalk
from ...models import Pavilion
from ...models import Restaurant
from ...models import Restroom
from ...models import TransportationStation
from ...models import WildEncounter
from ...pavilions.coordinators.pavilion_coordinator import PavilionCoordinator
from ...restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from ...restrooms.coordinators.restroom_coordinator import RestroomCoordinator
from ...shared.constants import ITINERARY_ANIMAL_MIN_LIKELIHOOD
from ...types import MonthInput, VisitDay, VisitYear
from ...wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from ...zoomobile.coordinators.zoomobile_coordinator import ZoomobileCoordinator


class SearchCoordinator():
   @classmethod
   def search(
         cls,
         *,
         query: str,
         include_animals: bool,
         include_pavilions: bool,
         include_restaurants: bool,
         include_restrooms: bool,
         include_gift_shops: bool,
         include_attractions: bool,
         include_zoomobile_stations: bool,
         include_guardians_talks: bool,
         include_wild_encounters: bool,
         month: MonthInput,
         day: VisitDay,
         year: VisitYear,
         temp: float | None,
         include_off_display_animals: bool,
         for_itinerary: bool,
         include_closed_restaurants: bool,
         include_closed_restrooms: bool,
         include_closed_attractions: bool,
         zoomobile_route: str | None ) -> dict[ str, list ]:

      animals: list[ Animal ] = []
      pavilions: list[ Pavilion ] = []
      restaurants: list[ Restaurant ] = []
      restrooms: list[ Restroom ] = []
      gift_shops: list[ GiftShop ] = []
      attractions: list[ Attraction ] = []
      zoomobile_stations: list[ TransportationStation ] = []
      wild_encounters: list[ WildEncounter ] = []
      guardians_talks: list[ GuardiansTalk ] = []

      if include_animals:
         animals = (
            AnimalCoordinator.get_animals_matching_query(
               query=query,
               day=day,
               month=month,
               year=year,
               temp=temp,
               include_off_display_animals=include_off_display_animals,
               for_itinerary=for_itinerary,
               threshold=(
                  ITINERARY_ANIMAL_MIN_LIKELIHOOD
                  if for_itinerary
                  else None ) ) or []
         )

      if include_pavilions:
         pavilions = (
            PavilionCoordinator.get_pavilions_matching_query( query=query ) or []
         )

      if include_restaurants:
         restaurants = (
            RestaurantCoordinator.get_restaurants_matching_query(
               query=query,
               day=day,
               month=month,
               year=year,
               include_closed_restaurants=include_closed_restaurants ) or []
         )

      if include_restrooms:
         restrooms = (
            RestroomCoordinator.get_restrooms_matching_query(
               query=query,
               day=day,
               month=month,
               year=year,
               include_closed_restrooms=include_closed_restrooms ) or []
         )

      if include_gift_shops:
         gift_shops = (
            GiftShopCoordinator.get_gift_shops_matching_query(
               query=query,
               day=day,
               month=month,
               year=year ) or []
         )

      if include_attractions:
         attractions = (
            AttractionCoordinator.get_attractions_matching_query(
               query=query,
               day=day,
               month=month,
               year=year,
               include_closed_attractions=include_closed_attractions ) or []
         )
         enrich_transportation_attraction_route_durations_for_visit(
            attractions,
            month=month,
            day=day,
            year=year,
         )

      if include_zoomobile_stations:
         zoomobile_stations = (
            ZoomobileCoordinator.get_zoomobile_stations_matching_query(
               query=query,
               route=zoomobile_route,
               day=day,
               month=month,
               year=year ) or []
         )

      if include_guardians_talks:
         guardians_talks = (
            GuardiansCoordinator.get_guardians_talks_matching_query(
               query=query,
               month=month,
               day=day,
               year=year ) or []
         )

      if include_wild_encounters:
         wild_encounters = (
            WildEncounterCoordinator.get_wild_encounters_matching_query(
               query=query,
               month=month,
               day=day,
               year=year ) or []
         )

      return {
         'animals': animals,
         'pavilions': pavilions,
         'restaurants': restaurants,
         'restrooms': restrooms,
         'gift_shops': gift_shops,
         'attractions': attractions,
         'zoomobile_stations': zoomobile_stations,
         'wild_encounters': wild_encounters,
         'guardians_talks': guardians_talks,
      }
