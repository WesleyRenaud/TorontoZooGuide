from __future__ import annotations

from collections.abc import Callable
from io import BytesIO
import json
from typing import Any

import pytest

from api.itinerary.logic.itinerary_save_result import ItinerarySaveResult
from api.itinerary.logic.itinerary_time_set_result import ItineraryTimeSetResult
from api.itinerary.logic.suppress_itinerary_warning import SuppressItineraryWarningResult
from api.models import Animal
from api.models import Attraction
from api.models import Defibrillator
from api.models import DrinkingFountain
from api.models import EmergencyIntercom
from api.models import EventSite
from api.models import GiftShop
from api.models import GuardiansTalk
from api.models import GuestService
from api.models import Itinerary
from api.models import Pavilion
from api.models import PicnicSite
from api.models import Region
from api.models import RegionWithExhibits
from api.models import Restaurant
from api.models import Restroom
from api.models import ScheduledOccurrence
from api.models import Update
from api.models import WildEncounter
from api.models import ZooHours
from api.models import ZoomobileStation
from api.models.zoomobile_route import ZoomobileRoute
import api.server as server
from api.shared.enums import AnimalViewingScope
from api.types import Connection


ANIMAL_NAME = 'African Lion'
ANIMAL_EXHIBIT = 'Africa Savanna'
ATTRACTION_NAME = 'Conservation Carousel'
REMOVED_ATTRACTION_NAME = 'TundraAir Ride'
PAVILION_NAME = 'African Rainforest Pavilion'
RESTAURANT_NAME = 'Africa Restaurant'
RESTROOM_NAME = 'Entrance Restroom'
GIFT_SHOP_NAME = 'Zootique'
ZOOMOBILE_STATION_NAME = 'Main Zoomobile Station'
GUARDIANS_TALK_NAME = 'African Lion'
GUARDIANS_TALK_LOCATION = 'Africa Savanna'
WILD_ENCOUNTER_NAME = 'African Rainforest'
WILD_ENCOUNTER_MEETING_SPOT = 'Wild Encounter - Africa Meeting Spot'
WILD_ENCOUNTER_LINK = 'https://www.torontozoo.com/tickets/weafricarainforest'
DRINKING_FOUNTAIN_X_COORD = 18.191
DRINKING_FOUNTAIN_Y_COORD = 12.561
UPDATE_TITLE = 'New baby giraffe'


def make_handler( path: str = '/', body: dict[ str, Any ] | None = None ) -> server.MyHandler:
   encoded = json.dumps( body or {} ).encode( 'utf-8' )
   handler = server.MyHandler.__new__( server.MyHandler )
   handler.path = path
   handler.headers = { 'Content-Length': str( len( encoded ) ) }
   handler.rfile = BytesIO( encoded )
   handler.wfile = BytesIO()
   handler.statuses = []
   handler.sent_headers = []
   handler.errors = []
   handler.conn = None
   handler.send_response = lambda code: handler.statuses.append( code )
   handler.send_header = lambda name, value: handler.sent_headers.append( ( name, value ) )
   handler.end_headers = lambda: None
   handler.send_error = lambda code, message=None: handler.errors.append( ( code, message ) )
   return handler


def response_json( handler: server.MyHandler ) -> dict[ str, Any ]:
   handler.wfile.seek( 0 )
   return json.loads( handler.wfile.read().decode( 'utf-8' ) )


class StubControllerNamespace:
   def __init__( self, root: StubZooControllers ) -> None:
      self._root = root


   def __getattr__( self, name: str ) -> Any:
      return getattr( self._root, name )


class StubZooControllers:
   instances: list[ StubZooControllers ] = []
   default_success: bool = True
   controller_attributes: tuple[ str, ... ] = (
      'animals',
      'exhibits',
      'pavilions',
      'restaurants',
      'restrooms',
      'giftshops',
      'attractions',
      'zoomobile',
      'guardians',
      'wild_encounters',
      'drinking_fountains',
      'defibrillators',
      'emergency_intercoms',
      'guest_services',
      'picnic_sites',
      'event_sites',
      'updates',
      'itinerary',
      'zoo_hours',
   )

   def __init__( self, conn: Connection | None = None ) -> None:
      self.conn: Connection | None = conn
      self.calls: list[ tuple[ str, dict[ str, Any ] ] ] = []
      self.closed = False
      StubZooControllers.instances.append( self )

      for attribute in self.controller_attributes:
         setattr( self, attribute, StubControllerNamespace( self ) )


   def close( self ) -> None:
      self.closed = True
      self.conn = None


   def get_animals_viewable_on_day( self, **kwargs: Any ) -> list[ Animal ]:
      self.calls.append( ( 'get_animals_viewable_on_day', kwargs ) )
      return [ Animal( species=ANIMAL_NAME, exhibit=ANIMAL_EXHIBIT, likelihood=100 ) ]


   def get_exhibits_in_region( self, region: str ) -> list[ str ]:
      self.calls.append( ( 'get_exhibits_in_region', { 'region': region } ) )
      return [ ANIMAL_EXHIBIT ]


   def get_regions( self ) -> list[ Region ]:
      self.calls.append( ( 'get_regions', {} ) )
      return [ Region( name='Africa', has_exhibits=True ) ]


   def get_names_of_animals_in_exhibit( self, exhibit: str ) -> list[ str ]:
      self.calls.append( ( 'get_names_of_animals_in_exhibit', { 'exhibit': exhibit } ) )
      return [ ANIMAL_NAME ]


   def get_animal_viewing_scopes(
         self,
         species: str,
         exhibit: str ) -> list[ AnimalViewingScope ]:
      self.calls.append(
         (
            'get_animal_viewing_scopes',
            {
               'species': species,
               'exhibit': exhibit
            }
         )
      )
      return [ AnimalViewingScope.INDOOR, AnimalViewingScope.OUTDOOR ]


   def get_animal_information( self, species: str ) -> Animal:
      self.calls.append( ( 'get_animal_information', { 'species': species } ) )
      return Animal( species=species, exhibit=ANIMAL_EXHIBIT )


   def get_pavilions( self ) -> list[ Pavilion ]:
      self.calls.append( ( 'get_pavilions', {} ) )
      return [ Pavilion( name=PAVILION_NAME, region='Africa' ) ]


   def get_restaurants( self, **kwargs: Any ) -> list[ Restaurant ]:
      self.calls.append( ( 'get_restaurants', kwargs ) )
      return [ Restaurant( name=RESTAURANT_NAME, location='Africa', sub_location=None ) ]


   def get_restrooms( self, **kwargs: Any ) -> list[ Restroom ]:
      self.calls.append( ( 'get_restrooms', kwargs ) )
      return [ Restroom( title=RESTROOM_NAME ) ]


   def get_gift_shops( self, **kwargs: Any ) -> list[ GiftShop ]:
      self.calls.append( ( 'get_gift_shops', kwargs ) )
      return [ GiftShop( name=GIFT_SHOP_NAME, location='Learning & Engagement Centre' ) ]


   def get_attractions( self, **kwargs: Any ) -> list[ Attraction ]:
      self.calls.append( ( 'get_attractions', kwargs ) )
      return [ Attraction( name=ATTRACTION_NAME, free_with_admission=0 ) ]


   def get_zoomobile_route( self, **kwargs: Any ) -> ZoomobileRoute:
      self.calls.append( ( 'get_zoomobile_route', kwargs ) )
      return ZoomobileRoute(
         route='summer',
         route_source='manual',
         zoomobile_stations=( ZoomobileStation( name=ZOOMOBILE_STATION_NAME ), ),
      )


   def get_guardians_talk_schedule( self, **kwargs: Any ) -> list[ GuardiansTalk ]:
      self.calls.append( ( 'get_guardians_talk_schedule', kwargs ) )
      return [ GuardiansTalk( name=GUARDIANS_TALK_NAME, location=GUARDIANS_TALK_LOCATION, x_coord=51.138, y_coord=41.279 ) ]


   def get_available_wild_encounters( self, **kwargs: Any ) -> list[ WildEncounter ]:
      self.calls.append( ( 'get_available_wild_encounters', kwargs ) )
      return [
         WildEncounter(
            name=WILD_ENCOUNTER_NAME,
            meeting_spot=WILD_ENCOUNTER_MEETING_SPOT,
            link=WILD_ENCOUNTER_LINK )
      ]


   def get_drinking_fountains( self, **kwargs: Any ) -> list[ DrinkingFountain ]:
      self.calls.append( ( 'get_drinking_fountains', kwargs ) )
      return [
         DrinkingFountain(
            x_coord=DRINKING_FOUNTAIN_X_COORD,
            y_coord=DRINKING_FOUNTAIN_Y_COORD )
      ]


   def get_defibrillators( self ) -> list[ Defibrillator ]:
      self.calls.append( ( 'get_defibrillators', {} ) )
      return [ Defibrillator( x_coord=12.345, y_coord=67.890 ) ]


   def get_emergency_intercoms( self ) -> list[ EmergencyIntercom ]:
      self.calls.append( ( 'get_emergency_intercoms', {} ) )
      return [ EmergencyIntercom( x_coord=23.456, y_coord=78.901 ) ]


   def get_guest_services( self ) -> list[ GuestService ]:
      self.calls.append( ( 'get_guest_services', {} ) )
      return [
         GuestService(
            service_type='Information',
            x_coord=34.567,
            y_coord=89.012 )
      ]


   def get_picnic_sites( self ) -> list[ PicnicSite ]:
      self.calls.append( ( 'get_picnic_sites', {} ) )
      return [
         PicnicSite(
            x_coord=45.678,
            y_coord=90.123 )
      ]


   def get_event_sites( self ) -> list[ EventSite ]:
      self.calls.append( ( 'get_event_sites', {} ) )
      return [
         EventSite(
            name='Special Events Center',
            x_coord=56.789,
            y_coord=12.345 )
      ]


   def get_updates_for_visit_date( self, **kwargs: Any ) -> list[ Update ]:
      self.calls.append( ( 'get_updates_for_visit_date', kwargs ) )
      return [
         Update(
            title=UPDATE_TITLE,
            description='Come meet the new calf.',
            update_type='New Arrival',
            start_date='2026-06-01',
            end_date='2026-06-30' )
      ]


   def get_closed_exhibits( self, **kwargs: Any ) -> list[ str ]:
      self.calls.append( ( 'get_closed_exhibits', kwargs ) )
      return [ ANIMAL_EXHIBIT ]


   def get_closed_exhibits_for_visit_date( self, **kwargs: Any ) -> list[ str ]:
      return self.get_closed_exhibits( **kwargs )


   def get_animals_matching_query( self, **kwargs: Any ) -> list[ Animal ]:
      self.calls.append( ( 'get_animals_matching_query', kwargs ) )
      return [ Animal( species=ANIMAL_NAME, exhibit=ANIMAL_EXHIBIT, likelihood=100 ) ]


   def get_pavilions_matching_query( self, query: str ) -> list[ Pavilion ]:
      self.calls.append( ( 'get_pavilions_matching_query', { 'query': query } ) )
      return [ Pavilion( name=PAVILION_NAME, region='Africa' ) ]


   def get_restaurants_matching_query( self, **kwargs: Any ) -> list[ Restaurant ]:
      self.calls.append( ( 'get_restaurants_matching_query', kwargs ) )
      return [ Restaurant( name=RESTAURANT_NAME, location='Africa', sub_location=None ) ]


   def get_restrooms_matching_query( self, **kwargs: Any ) -> list[ Restroom ]:
      self.calls.append( ( 'get_restrooms_matching_query', kwargs ) )
      return [ Restroom( title=RESTROOM_NAME ) ]


   def get_gift_shops_matching_query( self, **kwargs: Any ) -> list[ GiftShop ]:
      self.calls.append( ( 'get_gift_shops_matching_query', kwargs ) )
      return [ GiftShop( name=GIFT_SHOP_NAME, location='Learning & Engagement Centre' ) ]


   def get_attractions_matching_query( self, **kwargs: Any ) -> list[ Attraction ]:
      self.calls.append( ( 'get_attractions_matching_query', kwargs ) )
      return [ Attraction( name=ATTRACTION_NAME, free_with_admission=0 ) ]


   def get_zoomobile_stations_matching_query( self, **kwargs: Any ) -> list[ ZoomobileStation ]:
      self.calls.append( ( 'get_zoomobile_stations_matching_query', kwargs ) )
      return [ ZoomobileStation( name=ZOOMOBILE_STATION_NAME ) ]


   def get_guardians_talks_matching_query( self, **kwargs: Any ) -> list[ GuardiansTalk ]:
      self.calls.append( ( 'get_guardians_talks_matching_query', kwargs ) )
      return [ GuardiansTalk( name=GUARDIANS_TALK_NAME, location=GUARDIANS_TALK_LOCATION, x_coord=51.138, y_coord=41.279 ) ]


   def get_wild_encounters_matching_query( self, **kwargs: Any ) -> list[ WildEncounter ]:
      self.calls.append( ( 'get_wild_encounters_matching_query', kwargs ) )
      return [
         WildEncounter(
            name=WILD_ENCOUNTER_NAME,
            meeting_spot=WILD_ENCOUNTER_MEETING_SPOT,
            link=WILD_ENCOUNTER_LINK )
      ]


   def set_itinerary( self, **kwargs: Any ) -> ItinerarySaveResult:
      self.calls.append( ( 'set_itinerary', kwargs ) )
      return ItinerarySaveResult( itinerary=Itinerary( date='2026-06-15' ) )


   def schedule_itinerary_item( self, **kwargs: Any ) -> ItinerarySaveResult:
      self.calls.append( ( 'schedule_itinerary_item', kwargs ) )
      return ItinerarySaveResult( itinerary=Itinerary( date='2026-06-15' ) )


   def bulk_schedule_animals( self, **kwargs: Any ) -> ItinerarySaveResult:
      self.calls.append( ( 'bulk_schedule_animals', kwargs ) )
      return ItinerarySaveResult( itinerary=Itinerary( date='2026-06-15' ) )


   def get_itinerary_date( self ) -> str:
      self.calls.append( ( 'get_itinerary_date', {} ) )
      return '2026-06-15'


   def get_itinerary( self, **kwargs: Any ) -> Itinerary:
      self.calls.append( ( 'get_itinerary', kwargs ) )
      return Itinerary( date='2026-06-15' )


   def set_arrival_time( self, **kwargs: Any ) -> ItineraryTimeSetResult:
      self.calls.append( ( 'set_arrival_time', kwargs ) )
      return ItineraryTimeSetResult()


   def set_departure_time( self, **kwargs: Any ) -> ItineraryTimeSetResult:
      self.calls.append( ( 'set_departure_time', kwargs ) )
      return ItineraryTimeSetResult()


   def unschedule_itinerary_item( self, **kwargs: Any ) -> ItinerarySaveResult:
      self.calls.append( ( 'unschedule_itinerary_item', kwargs ) )
      return ItinerarySaveResult( itinerary=Itinerary( date='2026-06-15' ) )


   def remove_itinerary_item( self, **kwargs: Any ) -> ItinerarySaveResult:
      self.calls.append( ( 'remove_itinerary_item', kwargs ) )
      return ItinerarySaveResult( itinerary=Itinerary( date='2026-06-15' ) )


   def suppress_itinerary_warning(
         self,
         **kwargs: Any ) -> SuppressItineraryWarningResult:
      self.calls.append( ( 'suppress_itinerary_warning', kwargs ) )
      return SuppressItineraryWarningResult()


   def accept_itinerary( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'accept_itinerary', kwargs ) )
      return True


   def get_zoo_hours( self, day: int, month: str, year: int ) -> ZooHours:
      self.calls.append(
         ( 'get_zoo_hours', { 'day': day, 'month': month, 'year': year } ) )

      return ZooHours(
         date='2026-06-20',
         early_admission_time='09:00',
         open_time='09:30',
         last_admission_time='18:00',
         close_time='19:00' )


   def clear_itinerary( self ) -> bool:
      self.calls.append( ( 'clear_itinerary', {} ) )
      return True


   def get_animal_species_names( self ) -> list[ str ]:
      self.calls.append( ( 'get_animal_species_names', {} ) )
      return [ ANIMAL_NAME, 'Amur Tiger' ]


   def get_exhibits( self ) -> list[ str ]:
      self.calls.append( ( 'get_exhibits', {} ) )
      return [ ANIMAL_EXHIBIT, 'Eurasia Wilds' ]


   def get_regions_with_exhibits( self, **kwargs: Any ) -> list[ RegionWithExhibits ]:
      self.calls.append( ( 'get_regions_with_exhibits', kwargs ) )
      return [
         RegionWithExhibits(
            name='Africa',
            exhibits=[ ANIMAL_EXHIBIT ] )
      ]


   def get_restaurant_names( self ) -> list[ str ]:
      self.calls.append( ( 'get_restaurant_names', {} ) )
      return [ RESTAURANT_NAME ]


   def get_restroom_names( self ) -> list[ str ]:
      self.calls.append( ( 'get_restroom_names', {} ) )
      return [ RESTROOM_NAME ]


   def get_gift_shop_names( self ) -> list[ str ]:
      self.calls.append( ( 'get_gift_shop_names', {} ) )
      return [ GIFT_SHOP_NAME ]


   def get_attraction_names( self ) -> list[ str ]:
      self.calls.append( ( 'get_attraction_names', {} ) )
      return [ ATTRACTION_NAME ]


   def get_zoomobile_station_names( self ) -> list[ str ]:
      self.calls.append( ( 'get_zoomobile_station_names', {} ) )
      return [ ZOOMOBILE_STATION_NAME ]


   def get_guardians_talk_locations( self ) -> list[ str ]:
      self.calls.append( ( 'get_guardians_talk_locations', {} ) )
      return [ GUARDIANS_TALK_LOCATION ]


   def get_guardians_talk_names( self ) -> list[ str ]:
      self.calls.append( ( 'get_guardians_talk_names', {} ) )
      return [ GUARDIANS_TALK_NAME ]


   def get_guardians_talk_names_at_location( self, location: str ) -> list[ str ]:
      self.calls.append( ( 'get_guardians_talk_names_at_location', { 'location': location } ) )
      return [ GUARDIANS_TALK_NAME ]


   def get_guardians_talk_occurrences( self, **kwargs: Any ) -> list[ ScheduledOccurrence ]:
      self.calls.append( ( 'get_guardians_talk_occurrences', kwargs ) )
      return [
         ScheduledOccurrence(
            date='2026-06-15',
            time='10:00' )
      ]


   def get_wild_encounter_names( self ) -> list[ str ]:
      self.calls.append( ( 'get_wild_encounter_names', {} ) )
      return [ WILD_ENCOUNTER_NAME ]


   def get_wild_encounter_occurrences( self, **kwargs: Any ) -> list[ ScheduledOccurrence ]:
      self.calls.append( ( 'get_wild_encounter_occurrences', kwargs ) )
      return [
         ScheduledOccurrence(
            date='2026-06-15',
            time='14:00' )
      ]


   def get_unexpired_updates( self ) -> list[ Update ]:
      self.calls.append( ( 'get_unexpired_updates', {} ) )
      return [
         Update(
            title=UPDATE_TITLE,
            description='Come meet the new calf.',
            update_type='New Arrival',
            start_date='2026-06-01',
            end_date='2026-06-30' )
      ]


   def __getattr__( self, name: str ) -> Callable[ ..., bool ]:
      mutation_prefixes = (
         'create_',
         'set_',
         'remove_',
         'end_',
         'edit_',
         'cancel_',
         'replace_',
         'trim_'
      )

      if not name.startswith( mutation_prefixes ):
         raise AttributeError( name )

      def mutation_stub( **kwargs: Any ) -> bool:
         self.calls.append( ( name, kwargs ) )
         return StubZooControllers.default_success

      return mutation_stub


def _patch_controller_with_stub(
      monkeypatch: pytest.MonkeyPatch,
      controller_class: type,
      stub: StubZooControllers ) -> None:
   for method_name in dir( controller_class ):
      if method_name.startswith( '_' ) or not hasattr( stub, method_name ):
         continue

      stub_method = getattr( stub, method_name )

      if not callable( stub_method ):
         continue

      @classmethod
      def patched( cls: type, *args: Any, _stub_method: Callable[ ..., Any ] = stub_method, **kwargs: Any ) -> Any:
         return _stub_method( *args, **kwargs )

      monkeypatch.setattr( controller_class, method_name, patched )


@pytest.fixture
def stub_controllers( monkeypatch: pytest.MonkeyPatch ) -> type[ StubZooControllers ]:
   from api import connection
   from api.animals.coordinators.animal_coordinator import AnimalCoordinator
   from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
   from api.defibrillators.coordinators.defibrillator_coordinator import DefibrillatorCoordinator
   from api.drinking_fountains.coordinators.drinking_fountain_coordinator import DrinkingFountainCoordinator
   from api.emergency_intercoms.coordinators.emergency_intercom_coordinator import EmergencyIntercomCoordinator
   from api.event_sites.coordinators.event_site_coordinator import EventSiteCoordinator
   from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator
   from api.giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
   from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
   from api.guest_services.coordinators.guest_service_coordinator import GuestServiceCoordinator
   from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
   from api.pavilions.coordinators.pavilion_coordinator import PavilionCoordinator
   from api.picnic_sites.coordinators.picnic_site_coordinator import PicnicSiteCoordinator
   import api.request_connection as request_connection
   from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
   from api.restrooms.coordinators.restroom_coordinator import RestroomCoordinator
   from api.updates.coordinators.update_coordinator import UpdateCoordinator
   from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
   from api.zoo_hours.coordinators.zoo_hours_coordinator import ZooHoursCoordinator
   from api.zoomobile.coordinators.zoomobile_coordinator import ZoomobileCoordinator

   StubZooControllers.instances = []
   StubZooControllers.default_success = True
   stub = StubZooControllers( None )

   monkeypatch.setattr( connection, 'open_connection', lambda db_path='animals.db': None )

   def stub_set_connection( conn: Connection | None ) -> None:
      StubZooControllers._active = stub

   def stub_clear_connection() -> None:
      if StubZooControllers.instances:
         StubZooControllers.instances[ -1 ].closed = True

   monkeypatch.setattr( request_connection, 'set_connection', stub_set_connection )
   monkeypatch.setattr( request_connection, 'clear_connection', stub_clear_connection )

   controller_classes = [
      AnimalCoordinator,
      ExhibitCoordinator,
      PavilionCoordinator,
      RestaurantCoordinator,
      RestroomCoordinator,
      GiftShopCoordinator,
      AttractionCoordinator,
      ZoomobileCoordinator,
      GuardiansCoordinator,
      WildEncounterCoordinator,
      DrinkingFountainCoordinator,
      DefibrillatorCoordinator,
      EmergencyIntercomCoordinator,
      GuestServiceCoordinator,
      PicnicSiteCoordinator,
      EventSiteCoordinator,
      UpdateCoordinator,
      ItineraryCoordinator,
      ZooHoursCoordinator,
   ]

   for controller_class in controller_classes:
      _patch_controller_with_stub( monkeypatch, controller_class, stub )

   return StubZooControllers


@pytest.fixture
def stub_database( stub_controllers: type[ StubZooControllers ] ) -> type[ StubZooControllers ]:
   return stub_controllers

