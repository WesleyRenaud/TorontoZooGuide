from __future__ import annotations

from collections.abc import Callable
from functools import wraps
import html
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import mimetypes
import os
import re
import subprocess
import sys
from typing import Any
from urllib.parse import unquote, urlparse

from . import connection
from .animals.controllers.animal_controller import AnimalController
from .attractions.controllers.attraction_controller import AttractionController
from .defibrillators.controllers.defibrillator_controller import DefibrillatorController
from .drinking_fountains.controllers.drinking_fountain_controller import DrinkingFountainController
from .emergency_intercoms.controllers.emergency_intercom_controller import EmergencyIntercomController
from .event_sites.controllers.event_site_controller import EventSiteController
from .exhibits.controllers.exhibit_controller import ExhibitController
from .giftshops.controllers.gift_shop_controller import GiftShopController
from .guardians.controllers.guardians_controller import GuardiansController
from .guest_services.controllers.guest_service_controller import GuestServiceController
from .itinerary.controllers.itinerary_controller import ItineraryController
from .pavilions.controllers.pavilion_controller import PavilionController
from .picnic_sites.controllers.picnic_site_controller import PicnicSiteController
from .request_connection import clear_connection
from .request_connection import get_connection
from .request_connection import set_connection
from .restaurants.controllers.restaurant_controller import RestaurantController
from .restrooms.controllers.restroom_controller import RestroomController
from .shared.constants import itinerary_config_to_dict
from .shared.enums import AnimalViewingScope
from .updates.controllers.update_controller import UpdateController
from .wild_encounters.controllers.wild_encounter_controller import WildEncounterController
from .zoo_hours.controllers.zoo_hours_controller import ZooHoursController
from .zoomobile.controllers.zoomobile_controller import ZoomobileController


DEFAULT_PORT = 8000
STRING_EXPORT_SCRIPT = './tools/exportStringValues.mjs'
HTML_STRING_TOKEN_RE = re.compile( r'\{\{\s*([a-zA-Z0-9_.]+)\s*\}\}' )


def _flatten_string_values(
      values: dict[ str, Any ],
      prefix: str = '' ) -> dict[ str, str ]:
   flattened = {}

   for key, value in values.items():
      path = '{}.{}'.format( prefix, key ) if prefix else key

      if isinstance( value, dict ):
         flattened.update( _flatten_string_values( value, path ) )
      else:
         flattened[ path ] = str( value )

   return flattened


def get_html_string_values() -> dict[ str, str ]:
   result = subprocess.run(
      [ 'node', STRING_EXPORT_SCRIPT ],
      check=True,
      capture_output=True,
      text=True
   )

   return _flatten_string_values( json.loads( result.stdout ) )


def render_html_strings( content: str ) -> str:
   string_values = get_html_string_values()

   def replace_token( match: re.Match[ str ] ) -> str:
      key = match.group( 1 )
      value = string_values.get( key )

      if value is None:
         return match.group( 0 )

      return html.escape( value, quote=True )

   return HTML_STRING_TOKEN_RE.sub( replace_token, content )


def with_controllers(
      handler: Callable[ ..., Any ] ) -> Callable[ ..., Any ]:
   @wraps( handler )
   def wrapped( self: MyHandler, *args: Any, **kwargs: Any ) -> Any:
      conn = connection.open_connection()

      try:
         set_connection( conn )
         return handler( self, *args, **kwargs )
      finally:
         connection.close_connection( conn )
         clear_connection()

   return wrapped


class MyHandler( BaseHTTPRequestHandler ):
   pass

   def _send_file(
         self,
         filepath: str,
         content_type: str | None = None ) -> None:
      if not os.path.isfile( filepath ):
         self.send_error( 404, "Not Found" )
         return

      self.send_response( 200 )
      if not content_type:
         content_type, _ = mimetypes.guess_type( filepath )
      self.send_header( "Content-type", content_type or "application/octet-stream" )
      self.end_headers()

      if content_type == "text/html":
         with open( filepath, encoding='utf-8' ) as fp:
            self.wfile.write( render_html_strings( fp.read() ).encode( 'utf-8' ) )
         return

      with open( filepath, "rb" ) as fp:
         while True:
               chunk = fp.read( 8192 )
               if not chunk:
                  break
               self.wfile.write( chunk )


   def do_GET( self ) -> None:
      parsed = urlparse( self.path )
      path = unquote( parsed.path )  # handles %20 etc

      # Pages
      if path == "/map.html":
         return self._send_file( "./pages/map.html", "text/html" )
      if path == "/animals.html":
         return self._send_file( "./pages/animals.html", "text/html" )
      if path == "/itinerary.html":
         return self._send_file( "./pages/itinerary.html", "text/html" )
      if path == "/console-operations.html":
         return self._send_file( "./pages/console-operations.html", "text/html" )

      # Static folders (serve anything inside)
      if path.startswith( "/styles/" ):
         return self._send_file( "." + path )
      if path.startswith( "/scripts/" ):
         return self._send_file( "." + path )   # serves ALL modules
      if path.startswith( "/images/" ):
         return self._send_file( "." + path )

      # Otherwise
      self.send_error( 404, "Not Found" )


   @with_controllers
   def do_POST( self ) -> None:
      if self.path == '/get-visible-animals':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         day = data.get( 'day' )
         month = data.get( 'month' )
         year = data.get( 'year' )
         temp = data.get( 'temp' )
         include_off_display_animals = data.get( 'includeOffDisplayAnimals' ) or False

         animals = AnimalController.get_animals_viewable_on_day(
            day=day,
            month=month,
            year=year,
            temp=temp,
            include_off_display_animals=include_off_display_animals,
            threshold=0 )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = { "animals": [ animal.to_dict() for animal in animals ] }

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-exhibits-in-region':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         region = data.get( 'region' )

         exhibits = ExhibitController.get_exhibits_in_region( region=region )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "exhibits": exhibits }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-regions':
         regions = ExhibitController.get_regions()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { 'regions': [ region.to_dict() for region in regions ] }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-animal-names-by-exhibit':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         exhibit = data.get( 'exhibit' )

         animals = ExhibitController.get_names_of_animals_in_exhibit( exhibit=exhibit )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "animals": animals }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-animal-viewing-scopes':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         species = data.get( 'species' )
         exhibit = data.get( 'exhibit' )

         viewing_scopes = AnimalController.get_animal_viewing_scopes(
            species=species,
            exhibit=exhibit )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {
            'viewingScopes': [
               viewing_scope.value for viewing_scope in viewing_scopes
            ]
         }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-animal-information':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         species = data.get( 'species' )

         animal_info = AnimalController.get_animal_information( species=species )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "information": [ animal_info.to_dict() ] }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-animals-by-exhibit':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         day = data.get( 'day' )
         month = data.get( 'month' )
         year = data.get( 'year' )
         temp = data.get( 'temp' )
         exhibits_to_include = data.get( 'exhibitsToInclude' ) or []

         animals = AnimalController.get_animals_viewable_on_day(
            day=day,
            month=month,
            year=year,
            temp=temp,
            include_off_display_animals=False,
            threshold=0,
            exhibits_to_include=exhibits_to_include )

         animals_json = []

         for animal in animals:
            d = animal.to_dict()
            d[ 'type' ] = d.get( 'type', 'animal' )
            animals_json.append( d )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'animals': animals_json
         }

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-pavilions':
         pavilions = PavilionController.get_pavilions()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "pavilions": [ pavilion.to_dict() for pavilion in pavilions ] }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-restaurants':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         year = data.get( 'year' )
         include_closed_restaurants = data.get( 'includeClosedRestaurants' )
         restaurants_to_include = data.get( 'restaurantsToInclude' )

         restaurants = RestaurantController.get_restaurants(
            day=day,
            month=month,
            year=year,
            include_closed_restaurants=include_closed_restaurants,
            restaurants_to_include=restaurants_to_include )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "restaurants": [ restaurant.to_dict() for restaurant in restaurants ] }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-restrooms':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         year = data.get( 'year' )
         include_closed_restrooms = data.get( 'includeClosedRestrooms' ) or False

         restrooms = RestroomController.get_restrooms(
            day=day,
            month=month,
            year=year,
            include_closed_restrooms=include_closed_restrooms )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "restrooms": [ restroom.to_dict() for restroom in restrooms ] }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-gift-shops':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         year = data.get( 'year' )
         include_closed_gift_shops = data.get( 'includeClosedGiftShops' )
         gift_shops_to_include = data.get( 'giftShopsToInclude' )

         gift_shops = GiftShopController.get_gift_shops(
            day=day,
            month=month,
            year=year,
            include_closed_gift_shops=include_closed_gift_shops,
            gift_shops_to_include=gift_shops_to_include )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "gift_shops": [ gift_shop.to_dict() for gift_shop in gift_shops ] }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-attractions':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         year = data.get( 'year' )
         include_closed_attractions = data.get( 'includeClosedAttractions' ) or False

         attractions = AttractionController.get_attractions(
            day=day,
            month=month,
            year=year,
            include_closed_attractions=include_closed_attractions )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = { "attractions": [ attraction.to_dict() for attraction in attractions ] }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-zoomobile-route':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         route = data.get( 'zoomobileRoute' )
         month = data.get( 'month' )
         day = data.get( 'day' )
         year = data.get( 'year' )
         zoomobile_stations_to_include = data.get( 'zoomobileStationsToInclude' ) or []

         zoomobile_route = ZoomobileController.get_zoomobile_route(
            route=route,
            day=day,
            month=month,
            year=year,
            zoomobile_stations_to_include=zoomobile_stations_to_include )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = zoomobile_route.to_dict()

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-guardians-talks':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         year = data.get( 'year' )

         guardians_talks = GuardiansController.get_guardians_talk_schedule(
            month=month,
            day=day,
            year=year )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = { "guardians_talks": [ guardians_talk.to_dict() for guardians_talk in guardians_talks ] }

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-wild-encounters':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         year = data.get( 'year' )

         wild_encounters = WildEncounterController.get_available_wild_encounters(
            month=month,
            day=day,
            year=year )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "wild_encounters": [ wild_encounter.to_dict() for wild_encounter in wild_encounters ] }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-drinking-fountains':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         year = data.get( 'year' )

         drinking_fountains = DrinkingFountainController.get_drinking_fountains(
            day=day,
            month=month,
            year=year )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "drinking_fountains": [ drinking_fountain.to_dict() for drinking_fountain in drinking_fountains ] }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-defibrillators':
         defibrillators = DefibrillatorController.get_defibrillators()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "defibrillators": [ defibrillator.to_dict() for defibrillator in defibrillators ] }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-emergency-intercoms':
         emergency_intercoms = EmergencyIntercomController.get_emergency_intercoms()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "emergency_intercoms": [ emergency_intercom.to_dict() for emergency_intercom in emergency_intercoms ] }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-guest-services':
         guest_services = GuestServiceController.get_guest_services()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "guest_services": [ guest_service.to_dict() for guest_service in guest_services ] }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-picnic-sites':
         picnic_sites = PicnicSiteController.get_picnic_sites()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "picnic_sites": [ picnic_site.to_dict() for picnic_site in picnic_sites ] }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-event-sites':
         event_sites = EventSiteController.get_event_sites()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "event_sites": [ event_site.to_dict() for event_site in event_sites ] }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-updates':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         year = data.get( 'year' )

         updates = UpdateController.get_updates_for_visit_date(
            month=month,
            day=day,
            year=year )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "updates": [ update.to_dict() for update in updates ] }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-closed-exhibits':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         year = data.get( 'year' )

         closed_exhibits = ExhibitController.get_closed_exhibits_for_visit_date(
            month=month,
            day=day,
            year=year )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = { "closed_exhibits": closed_exhibits }

         self.wfile.write(
            json.dumps( response ).encode( 'utf-8' )
         )


      elif self.path == '/search':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         query = ( data.get( 'query' ) or '' ).strip()
         include_animals = bool( data.get( 'includeAnimals' ) )
         include_pavilions = bool( data.get( 'includePavilions' ) )
         include_restaurants = bool( data.get( 'includeRestaurants' ) )
         include_restrooms = bool( data.get( 'includeRestrooms' ) )
         include_gift_shops = bool( data.get( 'includeGiftShops' ) )
         include_attractions = bool( data.get( 'includeAttractions' ) )
         include_zoomobile_stations = bool( data.get( 'includeZoomobileStations' ) )
         include_guardians_talks = bool( data.get( 'includeGuardiansTalks' ) )
         include_wild_encounters = bool( data.get( 'includeWildEncounters' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         year = data.get( 'year' )
         temp = data.get( 'temp' )

         include_off_display_animals = bool( data.get( 'includeOffDisplayAnimals' ) )
         include_closed_restaurants = bool( data.get( 'includeClosedRestaurants' ) )
         include_closed_restrooms = bool( data.get( 'includeClosedRestrooms' ) )
         include_closed_attractions = bool( data.get( 'includeClosedAttractions' ) )
         zoomobile_route = data.get( 'zoomobileRoute' )

         animals_json = []
         pavilions_json = []
         restaurants_json = []
         restrooms_json = []
         gift_shops_json = []
         attractions_json = []
         zoomobile_stations_json = []
         wild_encounters_json = []
         guardians_talks_json = []

         if include_animals:
            animals = AnimalController.get_animals_matching_query(
               query=query,
               day=day,
               month=month,
               year=year,
               temp=temp,
               include_off_display_animals=include_off_display_animals ) or []
            for animal in animals:
                  d = animal.to_dict()
                  d[ 'type' ] = d.get( 'type', 'animal' )
                  animals_json.append( d )

         if include_pavilions:
            pavilions = PavilionController.get_pavilions_matching_query( query=query ) or []
            for pavilion in pavilions:
                  d = pavilion.to_dict()
                  d[ 'type' ] = d.get( 'type', 'pavilion' )
                  pavilions_json.append( d )

         if include_restaurants:
            restaurants = RestaurantController.get_restaurants_matching_query(
               query=query,
               day=day,
               month=month,
               year=year,
               include_closed_restaurants=include_closed_restaurants ) or []
            for restaurant in restaurants:
                  d = restaurant.to_dict()
                  d[ 'type' ] = d.get( 'type', 'restaurant' )
                  restaurants_json.append( d )

         if include_restrooms:
            restrooms = RestroomController.get_restrooms_matching_query(
               query=query,
               day=day,
               month=month,
               year=year,
               include_closed_restrooms=include_closed_restrooms ) or []
            for restroom in restrooms:
                  d = restroom.to_dict()
                  d[ 'type' ] = d.get( 'type', 'restroom' )
                  restrooms_json.append( d )

         if include_gift_shops:
            gift_shops = GiftShopController.get_gift_shops_matching_query(
               query=query,
               day=day,
               month=month,
               year=year ) or []
            for gift_shop in gift_shops:
                  d = gift_shop.to_dict()
                  d[ 'type' ] = d.get( 'type', 'giftShop' )
                  gift_shops_json.append( d )

         if include_attractions:
            attractions = AttractionController.get_attractions_matching_query(
               query=query,
               day=day,
               month=month,
               year=year,
               include_closed_attractions=include_closed_attractions ) or []
            for attraction in attractions:
                  d = attraction.to_dict()
                  d[ 'type' ] = d.get( 'type', 'attraction' )
                  attractions_json.append( d )

         if include_zoomobile_stations:
            zoomobile_stations = ZoomobileController.get_zoomobile_stations_matching_query(
               query=query,
               route=zoomobile_route,
               day=day,
               month=month,
               year=year ) or []
            for zoomobile_station in zoomobile_stations:
                  d = zoomobile_station.to_dict()
                  d[ 'type' ] = d.get( 'type', 'zoomobileStation' )
                  zoomobile_stations_json.append( d )

         if include_guardians_talks:
            guardians_talks = GuardiansController.get_guardians_talks_matching_query(
               query=query,
               month=month,
               day=day,
               year=year ) or []
            for guardians_talk in guardians_talks:
                  d = guardians_talk.to_dict()
                  d[ 'type' ] = d.get( 'type', 'guardiansTalk' )
                  guardians_talks_json.append( d )

         if include_wild_encounters:
            wild_encounters = WildEncounterController.get_wild_encounters_matching_query(
               query=query,
               month=month,
               day=day,
               year=year ) or []
            for wild_encounter in wild_encounters:
                  d = wild_encounter.to_dict()
                  d[ 'type' ] = d.get( 'type', 'wildEncounter' )
                  wild_encounters_json.append( d )

         response = {
            'animals': animals_json,
            'pavilions': pavilions_json,
            'restaurants': restaurants_json,
            'restrooms': restrooms_json,
            'gift_shops': gift_shops_json,
            'attractions': attractions_json,
            'zoomobile_stations': zoomobile_stations_json,
            'wild_encounters': wild_encounters_json,
            'guardians_talks': guardians_talks_json
         }

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-itinerary':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         date = data.get( 'date' )
         arrival_time = data.get( 'arrivalTime' )
         departure_time = data.get( 'departureTime' )
         animals = data.get( 'animals' )
         attractions = data.get( 'attractions' )
         guardians_talks = data.get( 'guardiansTalks' )
         wild_encounters = data.get( 'wildEncounters' )
         selected_exhibits = data.get( 'selectedExhibits' )
         temp = data.get( 'temp' )
         overriding_conflicting_guardians_talks = bool(
            data.get( 'overridingConflictingGuardiansTalks' ) )
         confirming_short_visit = bool( data.get( 'confirmingShortVisit' ) )
         suppress_short_visit_warning = bool(
            data.get( 'suppressShortVisitWarning' ) )

         save_result = ItineraryController.set_itinerary(
            date=date,
            arrival_time=arrival_time,
            departure_time=departure_time,
            animals=animals,
            attractions=attractions,
            guardians_talks=guardians_talks,
            wild_encounters=wild_encounters,
            selected_exhibits=selected_exhibits,
            visit_date_temp=temp,
            overriding_conflicting_guardians_talks=(
               overriding_conflicting_guardians_talks ),
            confirming_short_visit=confirming_short_visit,
            suppress_short_visit_warning=suppress_short_visit_warning )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'errorType': save_result.error_type.value,
            'itinerary': save_result.itinerary.to_dict(),
            'itinerary_config': itinerary_config_to_dict( get_connection() ),
            'issues': [
               issue.to_dict() for issue in save_result.issues
            ],
         }

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-itinerary-date':
         date = ItineraryController.get_itinerary_date()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = { 'date': date }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/schedule-itinerary-item':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         item_type = data.get( 'itemType' )
         key = data.get( 'key' )
         start_time = data.get( 'startTime' )
         duration_minutes = data.get( 'durationMinutes' )
         confirming_schedule_item_not_on_itinerary = bool(
            data.get( 'confirmingScheduleItemNotOnItinerary' ) )
         suppress_schedule_item_not_on_itinerary_warning = bool(
            data.get( 'suppressScheduleItemNotOnItineraryWarning' ) )

         save_result = ItineraryController.schedule_itinerary_item(
            item_type=item_type,
            key=key,
            start_time=start_time,
            duration_minutes=duration_minutes,
            confirming_schedule_item_not_on_itinerary=(
               confirming_schedule_item_not_on_itinerary
            ),
            suppress_schedule_item_not_on_itinerary_warning=(
               suppress_schedule_item_not_on_itinerary_warning
            ) )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'errorType': save_result.error_type.value,
         }

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/unschedule-itinerary-item':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         item_type = data.get( 'itemType' )
         key = data.get( 'key' )

         save_result = ItineraryController.unschedule_itinerary_item(
            item_type=item_type,
            key=key )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'errorType': save_result.error_type.value,
         }

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-itinerary-arrival-time':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         arrival_time = data.get( 'arrivalTime' )
         confirming_short_visit = bool( data.get( 'confirmingShortVisit' ) )
         suppress_short_visit_warning = bool(
            data.get( 'suppressShortVisitWarning' ) )

         save_result = ItineraryController.set_arrival_time(
            arrival_time=arrival_time,
            confirming_short_visit=confirming_short_visit,
            suppress_short_visit_warning=suppress_short_visit_warning )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'errorType': save_result.error_type.value,
            'arrivalTime': arrival_time,
            'itinerary_config': itinerary_config_to_dict( get_connection() ),
         }

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-itinerary-departure-time':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         departure_time = data.get( 'departureTime' )
         confirming_short_visit = bool( data.get( 'confirmingShortVisit' ) )
         suppress_short_visit_warning = bool(
            data.get( 'suppressShortVisitWarning' ) )

         save_result = ItineraryController.set_departure_time(
            departure_time=departure_time,
            confirming_short_visit=confirming_short_visit,
            suppress_short_visit_warning=suppress_short_visit_warning )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'errorType': save_result.error_type.value,
            'departureTime': departure_time,
            'itinerary_config': itinerary_config_to_dict( get_connection() ),
         }

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-itinerary':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )
         temp = data.get( 'temp' )

         itinerary = ItineraryController.get_itinerary( visit_date_temp=temp )

         response = {
            'itinerary': itinerary.to_dict(),
            'itinerary_config': itinerary_config_to_dict( get_connection() ),
         }

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-zoo-hours':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         day = data.get( 'day' )
         month = data.get( 'month' )
         year = data.get( 'year' )
         hours = ZooHoursController.get_zoo_hours(
            day=day,
            month=month,
            year=year )

         response = {
            'hours': hours.to_dict() if hours is not None else None,
         }

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/clear-itinerary':
         success = ItineraryController.clear_itinerary()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success
         }

         if not success:
            response[ 'error' ] = 'Could not clear itinerary.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/accept-itinerary':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )
         temp = data.get( 'temp' )
         animals_to_keep = data.get( 'animalsToKeep' )
         attractions_to_keep = data.get( 'attractionsToKeep' )

         success = ItineraryController.accept_itinerary(
            animals_to_keep=animals_to_keep,
            attractions_to_keep=attractions_to_keep )
         itinerary = (
            ItineraryController.get_itinerary( visit_date_temp=temp )
            if success
            else None
         )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'itinerary': itinerary.to_dict() if itinerary != None else None,
            'itinerary_config': itinerary_config_to_dict( get_connection() ),
         }

         if not success:
            response[ 'error' ] = 'Could not accept itinerary changes.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-animal-species-names':
         species = AnimalController.get_animal_species_names()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "species": species }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-restaurant-names':
         restaurants = RestaurantController.get_restaurant_names()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "restaurants": restaurants }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-restroom-names':
         restrooms = RestroomController.get_restroom_names()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "restrooms": restrooms }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-gift-shop-names':
         gift_shops = GiftShopController.get_gift_shop_names()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "gift_shops": gift_shops }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-attraction-names':
         attractions = AttractionController.get_attraction_names()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "attractions": attractions }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-zoomobile-station-names':
         zoomobile_stations = ZoomobileController.get_zoomobile_station_names()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "zoomobile_stations": zoomobile_stations }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-guardians-talk-locations':
         guardians_talk_locations = GuardiansController.get_guardians_talk_locations()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "guardians_talk_locations": guardians_talk_locations }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-guardians-talk-names':
         guardians_talks = GuardiansController.get_guardians_talk_names()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "guardians_talks": guardians_talks }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-guardians-talk-names-at-location':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         location = data.get( 'location' )

         guardians_talks = GuardiansController.get_guardians_talk_names_at_location( location=location )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "guardians_talks": guardians_talks }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-guardians-talk-occurrences':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         talk = data.get( 'talk' )
         location = data.get( 'location' )

         occurrences = GuardiansController.get_guardians_talk_occurrences( talk=talk, location=location )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'occurrences': [ occurrence.to_dict() for occurrence in occurrences ],
            'talk': talk,
            'location': location
         }

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-wild-encounter-names':
         wild_encounters = WildEncounterController.get_wild_encounter_names()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "wild_encounters": wild_encounters }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-wild-encounter-occurrences':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         wild_encounter = data.get( 'wildEncounter' )

         occurrences = WildEncounterController.get_wild_encounter_occurrences(
            wild_encounter_name=wild_encounter )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'occurrences': [ occurrence.to_dict() for occurrence in occurrences ],
            'wildEncounter': wild_encounter
         }

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-active-update-options':
         updates = UpdateController.get_unexpired_updates()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { 'updates': [ update.to_dict() for update in updates ] }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-exhibits-by-region':
         regions = ExhibitController.get_regions_with_exhibits()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "regions": [ region.to_dict() for region in regions ] }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-exhibits':
         exhibits = ExhibitController.get_exhibits()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "exhibits": exhibits }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-animal-off-display':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         species = data.get( 'species' )
         exhibit = data.get( 'exhibit' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )
         message = data.get( 'message' )
         viewing_scope = AnimalViewingScope.normalize( data.get( 'viewingScope' ) )

         success = AnimalController.set_animal_as_off_display(
            species=species,
            exhibit=exhibit,
            start_date=start_date,
            end_date=end_date,
            message=message,
            viewing_scope=viewing_scope )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'species': species,
            'exhibit': exhibit,
            'startDate': start_date,
            'endDate': end_date,
            'message': message,
            'viewingScope': viewing_scope.value,
         }

         if not success:
            response[ 'error' ] = f'No animal found with species "{ species }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-animal-on-display':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         species = data.get( 'species' )
         exhibit = data.get( 'exhibit' )
         viewing_scope = AnimalViewingScope.normalize( data.get( 'viewingScope' ) )

         success = AnimalController.set_animal_as_on_display(
            species=species,
            exhibit=exhibit,
            viewing_scope=viewing_scope )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'species': species,
            'exhibit': exhibit,
            'viewingScope': viewing_scope.value,
         }

         if not success:
            response[ 'error' ] = f'No off-display entry found for "{ species }" in "{ exhibit }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-animal-visibility-schedule':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         species = data.get( 'species' )
         exhibit = data.get( 'exhibit' )
         schedule_start_date = data.get( 'scheduleStartDate' )
         schedule_end_date = data.get( 'scheduleEndDate' )
         daily_start_time = data.get( 'dailyStartTime' )
         daily_end_time = data.get( 'dailyEndTime' )
         message = data.get( 'message' )

         success = AnimalController.set_animal_limited_viewing_schedule(
            species=species,
            exhibit=exhibit,
            start_date=schedule_start_date,
            end_date=schedule_end_date,
            daily_start_time=daily_start_time,
            daily_end_time=daily_end_time,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'species': species,
            'exhibit': exhibit,
            'scheduleStartDate': schedule_start_date,
            'scheduleEndDate': schedule_end_date,
            'dailyStartTime': daily_start_time,
            'dailyEndTime': daily_end_time,
            'message': message,
         }

         if not success:
            response[ 'error' ] = f'Could not set limited viewing schedule for "{ species }" in "{ exhibit }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/remove-animal-visibility-schedule':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         species = data.get( 'species' )
         exhibit = data.get( 'exhibit' )

         success = AnimalController.remove_animal_visibility_schedule( species=species, exhibit=exhibit )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'species': species,
            'exhibit': exhibit,
         }

         if not success:
            response[ 'error' ] = f'Could not remove visibility schedule for "{ species }" in "{ exhibit }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-animal-viewing-alert':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         species = data.get( 'species' )
         exhibit = data.get( 'exhibit' )
         alert_start_date = data.get( 'alertStartDate' )
         alert_end_date = data.get( 'alertEndDate' )
         message = data.get( 'message' )

         success = AnimalController.set_animal_viewing_alert(
            species=species,
            exhibit=exhibit,
            alert_start_date=alert_start_date,
            alert_end_date=alert_end_date,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'species': species,
            'exhibit': exhibit,
            'alertStartDate': alert_start_date,
            'alertEndDate': alert_end_date,
            'message': message,
         }

         if not success:
            response[ 'error' ] = f'Could not set viewing alert for "{ species }" in "{ exhibit }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/remove-animal-viewing-alert':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         species = data.get( 'species' )
         exhibit = data.get( 'exhibit' )

         success = AnimalController.remove_animal_viewing_alert( species=species, exhibit=exhibit )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'species': species,
            'exhibit': exhibit
         }

         if not success:
            response[ 'error' ] = f'Could not remove viewing alert for "{ species }" in "{ exhibit }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-exhibit-closed':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         exhibit = data.get( 'exhibit' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )
         message = data.get( 'message' )

         success = ExhibitController.set_exhibit_as_closed( exhibit=exhibit, start_date=start_date, end_date=end_date, message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'exhibit': exhibit,
            'startDate': start_date,
            'endDate': end_date,
            'message': message
         }

         if not success:
            response[ 'error' ] = f'Could not set "{ exhibit }" as closed.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-exhibit-open':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         exhibit = data.get( 'exhibit' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )

         success = ExhibitController.set_exhibit_as_open(
            exhibit=exhibit,
            start_date=start_date,
            end_date=end_date )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'exhibit': exhibit,
            'startDate': start_date,
            'endDate': end_date
         }

         if not success:
            response[ 'error' ] = f'Could not set "{ exhibit }" as open.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-restroom-closed':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         restroom = data.get( 'restroom' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )
         message = data.get( 'message' )

         success = RestroomController.set_restroom_as_closed(
            restroom=restroom,
            start_date=start_date,
            end_date=end_date,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'restroom': restroom,
            'startDate': start_date,
            'endDate': end_date,
            'message': message
         }

         if not success:
            response[ 'error' ] = f'Could not set "{ restroom }" as closed.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-restroom-open':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         restroom = data.get( 'restroom' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )

         success = RestroomController.set_restroom_as_open(
            restroom=restroom,
            start_date=start_date,
            end_date=end_date )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'restroom': restroom,
            'startDate': start_date,
            'endDate': end_date
         }

         if not success:
            response[ 'error' ] = f'Could not set "{ restroom }" as open.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-restroom-alert':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         restroom = data.get( 'restroom' )
         alert_start_date = data.get( 'alertStartDate' )
         alert_end_date = data.get( 'alertEndDate' )
         message = data.get( 'message' )

         success = RestroomController.set_restroom_alert(
            restroom=restroom,
            alert_start_date=alert_start_date,
            alert_end_date=alert_end_date,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'restroom': restroom,
            'alertStartDate': alert_start_date,
            'alertEndDate': alert_end_date,
            'message': message
         }

         if not success:
            response[ 'error' ] = f'Could not set alert for "{ restroom }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/remove-restroom-alert':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         restroom = data.get( 'restroom' )

         success = RestroomController.remove_restroom_alert(
            restroom=restroom )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'restroom': restroom
         }

         if not success:
            response[ 'error' ] = f'Could not remove alert for "{ restroom }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/create-update':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         title = data.get( 'title' )
         description = data.get( 'description' )
         update_type = data.get( 'type' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )

         success = UpdateController.create_update(
            title=title,
            description=description,
            update_type=update_type,
            start_date=start_date,
            end_date=end_date )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'title': title,
            'description': description,
            'type': update_type,
            'startDate': start_date,
            'endDate': end_date
         }

         if not success:
            response[ 'error' ] = 'Could not create update.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/end-update':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         title = data.get( 'title' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )

         success = UpdateController.end_update(
            title=title,
            start_date=start_date,
            end_date=end_date )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'title': title,
            'startDate': start_date,
            'endDate': end_date
         }

         if not success:
            response[ 'error' ] = 'Could not end update.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/edit-update':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         title = data.get( 'title' )
         start_date = data.get( 'startDate' )
         description = data.get( 'description' )
         update_type = data.get( 'type' )
         end_date = data.get( 'endDate' )

         success = UpdateController.edit_update(
            title=title,
            start_date=start_date,
            description=description,
            update_type=update_type,
            end_date=end_date )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'title': title,
            'startDate': start_date,
            'description': description,
            'type': update_type,
            'endDate': end_date
         }

         if not success:
            response[ 'error' ] = 'Could not edit update.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-restaurant-closed':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         restaurant = data.get( 'restaurant' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )
         message = data.get( 'message' )

         success = RestaurantController.set_restaurant_as_closed(
            restaurant=restaurant,
            start_date=start_date,
            end_date=end_date,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'restaurant': restaurant,
            'startDate': start_date,
            'endDate': end_date,
            'message': message
         }

         if not success:
            response[ 'error' ] = f'Could not set "{ restaurant }" as closed.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-restaurant-closure-override':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         restaurant = data.get( 'restaurant' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )
         message = data.get( 'message' )

         success = RestaurantController.set_restaurant_closure_override(
            restaurant=restaurant,
            start_date=start_date,
            end_date=end_date,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'restaurant': restaurant,
            'startDate': start_date,
            'endDate': end_date,
            'message': message
         }

         if not success:
            response[ 'error' ] = f'Could not create closure override for "{ restaurant }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-restaurant-opening-schedule':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         restaurant = data.get( 'restaurant' )
         schedule_start_date = data.get( 'scheduleStartDate' )
         schedule_end_date = data.get( 'scheduleEndDate' )

         monday = data.get( 'monday' )
         tuesday = data.get( 'tuesday' )
         wednesday = data.get( 'wednesday' )
         thursday = data.get( 'thursday' )
         friday = data.get( 'friday' )
         saturday = data.get( 'saturday' )
         sunday = data.get( 'sunday' )
         holidays_only = data.get( 'holidaysOnly' )

         message = data.get( 'message' )

         success = RestaurantController.set_restaurant_opening_schedule(
            restaurant=restaurant,
            start_date=schedule_start_date,
            end_date=schedule_end_date,
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
            thursday=thursday,
            friday=friday,
            saturday=saturday,
            sunday=sunday,
            holidays_only=holidays_only,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'restaurant': restaurant,
            'scheduleStartDate': schedule_start_date,
            'scheduleEndDate': schedule_end_date,
            'monday': monday,
            'tuesday': tuesday,
            'wednesday': wednesday,
            'thursday': thursday,
            'friday': friday,
            'saturday': saturday,
            'sunday': sunday,
            'holidaysOnly': holidays_only,
            'message': message
         }

         if not success:
            response[ 'error' ] = f'Could not set opening schedule for "{ restaurant }".'
            response[ 'errorType' ] = 'overlappingSchedule'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/replace-restaurant-opening-schedule-overlaps':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         restaurant = data.get( 'restaurant' )
         schedule_start_date = data.get( 'scheduleStartDate' )
         schedule_end_date = data.get( 'scheduleEndDate' )

         monday = data.get( 'monday' )
         tuesday = data.get( 'tuesday' )
         wednesday = data.get( 'wednesday' )
         thursday = data.get( 'thursday' )
         friday = data.get( 'friday' )
         saturday = data.get( 'saturday' )
         sunday = data.get( 'sunday' )
         holidays_only = data.get( 'holidaysOnly' )

         message = data.get( 'message' )

         success = RestaurantController.replace_restaurant_opening_schedule_overlaps(
            restaurant=restaurant,
            start_date=schedule_start_date,
            end_date=schedule_end_date,
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
            thursday=thursday,
            friday=friday,
            saturday=saturday,
            sunday=sunday,
            holidays_only=holidays_only,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'restaurant': restaurant,
            'scheduleStartDate': schedule_start_date,
            'scheduleEndDate': schedule_end_date,
            'monday': monday,
            'tuesday': tuesday,
            'wednesday': wednesday,
            'thursday': thursday,
            'friday': friday,
            'saturday': saturday,
            'sunday': sunday,
            'holidaysOnly': holidays_only,
            'message': message
         }

         if not success:
            response[ 'error' ] = f'Could not replace opening schedule overlaps for "{ restaurant }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/trim-restaurant-opening-schedule-overlaps':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         restaurant = data.get( 'restaurant' )
         schedule_start_date = data.get( 'scheduleStartDate' )
         schedule_end_date = data.get( 'scheduleEndDate' )

         monday = data.get( 'monday' )
         tuesday = data.get( 'tuesday' )
         wednesday = data.get( 'wednesday' )
         thursday = data.get( 'thursday' )
         friday = data.get( 'friday' )
         saturday = data.get( 'saturday' )
         sunday = data.get( 'sunday' )
         holidays_only = data.get( 'holidaysOnly' )

         message = data.get( 'message' )

         success = RestaurantController.trim_restaurant_opening_schedule_overlaps(
            restaurant=restaurant,
            start_date=schedule_start_date,
            end_date=schedule_end_date,
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
            thursday=thursday,
            friday=friday,
            saturday=saturday,
            sunday=sunday,
            holidays_only=holidays_only,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'restaurant': restaurant,
            'scheduleStartDate': schedule_start_date,
            'scheduleEndDate': schedule_end_date,
            'monday': monday,
            'tuesday': tuesday,
            'wednesday': wednesday,
            'thursday': thursday,
            'friday': friday,
            'saturday': saturday,
            'sunday': sunday,
            'holidaysOnly': holidays_only,
            'message': message
         }

         if not success:
            response[ 'error' ] = f'Could not trim opening schedule overlaps for "{ restaurant }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-gift-shop-closed':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         gift_shop = data.get( 'giftShop' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )
         message = data.get( 'message' )

         success = GiftShopController.set_gift_shop_as_closed(
            gift_shop=gift_shop,
            start_date=start_date,
            end_date=end_date,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'gift_shop': gift_shop,
            'startDate': start_date,
            'endDate': end_date,
            'message': message
         }

         if not success:
            response[ 'error' ] = f'Could not set "{ gift_shop }" as closed.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-gift-shop-opening-schedule':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         gift_shop = data.get( 'giftShop' )
         schedule_start_date = data.get( 'scheduleStartDate' )
         schedule_end_date = data.get( 'scheduleEndDate' )

         monday = data.get( 'monday' )
         tuesday = data.get( 'tuesday' )
         wednesday = data.get( 'wednesday' )
         thursday = data.get( 'thursday' )
         friday = data.get( 'friday' )
         saturday = data.get( 'saturday' )
         sunday = data.get( 'sunday' )
         holidays_only = data.get( 'holidaysOnly' )

         message = data.get( 'message' )

         success = GiftShopController.set_gift_shop_opening_schedule(
            gift_shop=gift_shop,
            start_date=schedule_start_date,
            end_date=schedule_end_date,
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
            thursday=thursday,
            friday=friday,
            saturday=saturday,
            sunday=sunday,
            holidays_only=holidays_only,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'gift_shop': gift_shop,
            'scheduleStartDate': schedule_start_date,
            'scheduleEndDate': schedule_end_date,
            'monday': monday,
            'tuesday': tuesday,
            'wednesday': wednesday,
            'thursday': thursday,
            'friday': friday,
            'saturday': saturday,
            'sunday': sunday,
            'holidaysOnly': holidays_only,
            'message': message
         }

         if not success:
            response[ 'error' ] = f'Could not set opening schedule for "{ gift_shop }".'
            response[ 'errorType' ] = 'overlappingSchedule'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/replace-gift-shop-opening-schedule-overlaps':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         gift_shop = data.get( 'giftShop' )
         schedule_start_date = data.get( 'scheduleStartDate' )
         schedule_end_date = data.get( 'scheduleEndDate' )

         monday = data.get( 'monday' )
         tuesday = data.get( 'tuesday' )
         wednesday = data.get( 'wednesday' )
         thursday = data.get( 'thursday' )
         friday = data.get( 'friday' )
         saturday = data.get( 'saturday' )
         sunday = data.get( 'sunday' )
         holidays_only = data.get( 'holidaysOnly' )

         message = data.get( 'message' )

         success = GiftShopController.replace_gift_shop_opening_schedule_overlaps(
            gift_shop=gift_shop,
            start_date=schedule_start_date,
            end_date=schedule_end_date,
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
            thursday=thursday,
            friday=friday,
            saturday=saturday,
            sunday=sunday,
            holidays_only=holidays_only,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'gift_shop': gift_shop,
            'scheduleStartDate': schedule_start_date,
            'scheduleEndDate': schedule_end_date,
            'monday': monday,
            'tuesday': tuesday,
            'wednesday': wednesday,
            'thursday': thursday,
            'friday': friday,
            'saturday': saturday,
            'sunday': sunday,
            'holidaysOnly': holidays_only,
            'message': message
         }

         if not success:
            response[ 'error' ] = f'Could not replace opening schedule overlaps for "{ gift_shop }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/trim-gift-shop-opening-schedule-overlaps':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         gift_shop = data.get( 'giftShop' )
         schedule_start_date = data.get( 'scheduleStartDate' )
         schedule_end_date = data.get( 'scheduleEndDate' )

         monday = data.get( 'monday' )
         tuesday = data.get( 'tuesday' )
         wednesday = data.get( 'wednesday' )
         thursday = data.get( 'thursday' )
         friday = data.get( 'friday' )
         saturday = data.get( 'saturday' )
         sunday = data.get( 'sunday' )
         holidays_only = data.get( 'holidaysOnly' )

         message = data.get( 'message' )

         success = GiftShopController.trim_gift_shop_opening_schedule_overlaps(
            gift_shop=gift_shop,
            start_date=schedule_start_date,
            end_date=schedule_end_date,
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
            thursday=thursday,
            friday=friday,
            saturday=saturday,
            sunday=sunday,
            holidays_only=holidays_only,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'gift_shop': gift_shop,
            'scheduleStartDate': schedule_start_date,
            'scheduleEndDate': schedule_end_date,
            'monday': monday,
            'tuesday': tuesday,
            'wednesday': wednesday,
            'thursday': thursday,
            'friday': friday,
            'saturday': saturday,
            'sunday': sunday,
            'holidaysOnly': holidays_only,
            'message': message
         }

         if not success:
            response[ 'error' ] = f'Could not trim opening schedule overlaps for "{ gift_shop }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-gift-shop-closure-override':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         gift_shop = data.get( 'giftShop' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )
         message = data.get( 'message' )

         success = GiftShopController.set_gift_shop_closure_override(
            gift_shop=gift_shop,
            start_date=start_date,
            end_date=end_date,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'gift_shop': gift_shop,
            'startDate': start_date,
            'endDate': end_date,
            'message': message
         }

         if not success:
            response[ 'error' ] = f'Could not create closure override for "{ gift_shop }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-attraction-closed':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         attraction = data.get( 'attraction' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )
         message = data.get( 'message' )

         success = AttractionController.set_attraction_as_closed(
            attraction=attraction,
            start_date=start_date,
            end_date=end_date,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'attraction': attraction,
            'startDate': start_date,
            'endDate': end_date,
            'message': message
         }

         if not success:
            response[ 'error' ] = f'Could not set "{ attraction }" as closed.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-attraction-closure-override':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         attraction = data.get( 'attraction' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )
         message = data.get( 'message' )

         success = AttractionController.set_attraction_closure_override(
            attraction=attraction,
            start_date=start_date,
            end_date=end_date,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'attraction': attraction,
            'startDate': start_date,
            'endDate': end_date,
            'message': message
         }

         if not success:
            response[ 'error' ] = f'Could not create closure override for "{ attraction }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-attraction-opening-schedule':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         attraction = data.get( 'attraction' )
         schedule_start_date = data.get( 'scheduleStartDate' )
         schedule_end_date = data.get( 'scheduleEndDate' )

         monday = data.get( 'monday' )
         tuesday = data.get( 'tuesday' )
         wednesday = data.get( 'wednesday' )
         thursday = data.get( 'thursday' )
         friday = data.get( 'friday' )
         saturday = data.get( 'saturday' )
         sunday = data.get( 'sunday' )
         holidays_only = data.get( 'holidaysOnly' )

         message = data.get( 'message' )

         success = AttractionController.set_attraction_opening_schedule(
            attraction=attraction,
            start_date=schedule_start_date,
            end_date=schedule_end_date,
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
            thursday=thursday,
            friday=friday,
            saturday=saturday,
            sunday=sunday,
            holidays_only=holidays_only,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'attraction': attraction,
            'scheduleStartDate': schedule_start_date,
            'scheduleEndDate': schedule_end_date,
            'monday': monday,
            'tuesday': tuesday,
            'wednesday': wednesday,
            'thursday': thursday,
            'friday': friday,
            'saturday': saturday,
            'sunday': sunday,
            'holidaysOnly': holidays_only,
            'message': message
         }

         if not success:
            response[ 'error' ] = f'Could not set opening schedule for "{ attraction }".'
            response[ 'errorType' ] = 'overlappingSchedule'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/replace-attraction-opening-schedule-overlaps':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         attraction = data.get( 'attraction' )
         schedule_start_date = data.get( 'scheduleStartDate' )
         schedule_end_date = data.get( 'scheduleEndDate' )

         monday = data.get( 'monday' )
         tuesday = data.get( 'tuesday' )
         wednesday = data.get( 'wednesday' )
         thursday = data.get( 'thursday' )
         friday = data.get( 'friday' )
         saturday = data.get( 'saturday' )
         sunday = data.get( 'sunday' )
         holidays_only = data.get( 'holidaysOnly' )

         message = data.get( 'message' )

         success = AttractionController.replace_attraction_opening_schedule_overlaps(
            attraction=attraction,
            start_date=schedule_start_date,
            end_date=schedule_end_date,
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
            thursday=thursday,
            friday=friday,
            saturday=saturday,
            sunday=sunday,
            holidays_only=holidays_only,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'attraction': attraction,
            'scheduleStartDate': schedule_start_date,
            'scheduleEndDate': schedule_end_date,
            'monday': monday,
            'tuesday': tuesday,
            'wednesday': wednesday,
            'thursday': thursday,
            'friday': friday,
            'saturday': saturday,
            'sunday': sunday,
            'holidaysOnly': holidays_only,
            'message': message
         }

         if not success:
            response[ 'error' ] = f'Could not replace opening schedule overlaps for "{ attraction }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/trim-attraction-opening-schedule-overlaps':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         attraction = data.get( 'attraction' )
         schedule_start_date = data.get( 'scheduleStartDate' )
         schedule_end_date = data.get( 'scheduleEndDate' )

         monday = data.get( 'monday' )
         tuesday = data.get( 'tuesday' )
         wednesday = data.get( 'wednesday' )
         thursday = data.get( 'thursday' )
         friday = data.get( 'friday' )
         saturday = data.get( 'saturday' )
         sunday = data.get( 'sunday' )
         holidays_only = data.get( 'holidaysOnly' )

         message = data.get( 'message' )

         success = AttractionController.trim_attraction_opening_schedule_overlaps(
            attraction=attraction,
            start_date=schedule_start_date,
            end_date=schedule_end_date,
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
            thursday=thursday,
            friday=friday,
            saturday=saturday,
            sunday=sunday,
            holidays_only=holidays_only,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'attraction': attraction,
            'scheduleStartDate': schedule_start_date,
            'scheduleEndDate': schedule_end_date,
            'monday': monday,
            'tuesday': tuesday,
            'wednesday': wednesday,
            'thursday': thursday,
            'friday': friday,
            'saturday': saturday,
            'sunday': sunday,
            'holidaysOnly': holidays_only,
            'message': message
         }

         if not success:
            response[ 'error' ] = f'Could not trim opening schedule overlaps for "{ attraction }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-zoomobile-station-closed':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         zoomobile_station = data.get( 'zoomobileStation' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )
         message = data.get( 'message' )

         success = ZoomobileController.set_zoomobile_station_as_closed(
            zoomobile_station=zoomobile_station,
            start_date=start_date,
            end_date=end_date,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'zoomobile_station': zoomobile_station,
            'startDate': start_date,
            'endDate': end_date,
            'message': message
         }

         if not success:
            response[ 'error' ] = f'Could not set "{ zoomobile_station }" as closed.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-zoomobile-station-open':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         zoomobile_station = data.get( 'zoomobileStation' )

         success = ZoomobileController.set_zoomobile_station_as_open( zoomobile_station=zoomobile_station )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'zoomobile_station': zoomobile_station
         }

         if not success:
            response[ 'error' ] = f'Could not set "{ zoomobile_station }" as open.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-current-zoomobile-route':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         route = data.get( 'route' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )

         success = False

         if route in ( 'summer', 'winter' ):
            success = ZoomobileController.set_current_zoomobile_route(
               route=route,
               start_date=start_date,
               end_date=end_date )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'route': route,
            'startDate': start_date,
            'endDate': end_date
         }

         if not success:
            response[ 'error' ] = f'Could not set Zoomobile route to "{ route }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-guardians-talk-schedule':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         talk = data.get( 'talk' )
         location = data.get( 'location' )
         schedule_start_date = data.get( 'startDate' )
         schedule_end_date = data.get( 'endDate' )
         monday_time = data.get( 'mondayTime' )
         tuesday_time = data.get( 'tuesdayTime' )
         wednesday_time = data.get( 'wednesdayTime' )
         thursday_time = data.get( 'thursdayTime' )
         friday_time = data.get( 'fridayTime' )
         saturday_time = data.get( 'saturdayTime' )
         sunday_time = data.get( 'sundayTime' )

         message = data.get( 'message' )

         success = GuardiansController.set_guardians_talk_schedule(
            talk=talk,
            location=location,
            start_date=schedule_start_date,
            end_date=schedule_end_date,
            monday_time=monday_time,
            tuesday_time=tuesday_time,
            wednesday_time=wednesday_time,
            thursday_time=thursday_time,
            friday_time=friday_time,
            saturday_time=saturday_time,
            sunday_time=sunday_time,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'talk': talk,
            'location': location,
            'startDate': schedule_start_date,
            'endDate': schedule_end_date,
            'mondayTime': monday_time,
            'tuesdayTime': tuesday_time,
            'wednesdayTime': wednesday_time,
            'thursdayTime': thursday_time,
            'fridayTime': friday_time,
            'saturdayTime': saturday_time,
            'sundayTime': sunday_time,
            'message': message
         }

         if not success:
            response[ 'error' ] = f'Could not set schedule for "{ talk }" at "{ location }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/end-guardians-talk-schedule':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         talk = data.get( 'talk' )
         location = data.get( 'location' )
         schedule_end_date = data.get( 'endDate' )

         success = GuardiansController.end_guardians_talk_schedule(
            talk=talk,
            location=location,
            schedule_end_date=schedule_end_date )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'talk': talk,
            'location': location,
            'endDate': schedule_end_date
         }

         if not success:
            response[ 'error' ] = f'Could not end schedule for "{ talk }" at "{ location }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/cancel-guardians-talk-occurrence':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         talk = data.get( 'talk' )
         location = data.get( 'location' )
         date = data.get( 'date' )
         time = data.get( 'time' )

         success = GuardiansController.cancel_guardians_talk_occurrence(
            talk=talk,
            location=location,
            date=date,
            time=time )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'talk': talk,
            'location': location,
            'date': date,
            'time': time
         }

         if not success:
            response[ 'error' ] = f'Could not cancel "{ talk }" at "{ location }" on { date } at { time }.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-wild-encounter-schedule':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         wild_encounter = data.get( 'wildEncounter' )
         schedule_start_date = data.get( 'startDate' )
         schedule_end_date = data.get( 'endDate' )
         encounter_time = data.get( 'time' )

         monday = data.get( 'monday' )
         tuesday = data.get( 'tuesday' )
         wednesday = data.get( 'wednesday' )
         thursday = data.get( 'thursday' )
         friday = data.get( 'friday' )
         saturday = data.get( 'saturday' )
         sunday = data.get( 'sunday' )

         message = data.get( 'message' )

         success = WildEncounterController.set_wild_encounter_schedule(
            wild_encounter_name=wild_encounter,
            start_date=schedule_start_date,
            end_date=schedule_end_date,
            encounter_time=encounter_time,
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
            thursday=thursday,
            friday=friday,
            saturday=saturday,
            sunday=sunday,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'wildEncounter': wild_encounter,
            'startDate': schedule_start_date,
            'endDate': schedule_end_date,
            'time': encounter_time,
            'monday': monday,
            'tuesday': tuesday,
            'wednesday': wednesday,
            'thursday': thursday,
            'friday': friday,
            'saturday': saturday,
            'sunday': sunday,
            'message': message
         }

         if not success:
            response[ 'error' ] = f'Could not set schedule for "{ wild_encounter }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/end-wild-encounter-schedule':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         wild_encounter = data.get( 'wildEncounter' )
         schedule_end_date = data.get( 'endDate' )

         success = WildEncounterController.end_wild_encounter_schedule(
            wild_encounter_name=wild_encounter,
            schedule_end_date=schedule_end_date )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'wildEncounter': wild_encounter,
            'endDate': schedule_end_date
         }

         if not success:
            response[ 'error' ] = f'Could not end schedule for "{ wild_encounter }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/cancel-wild-encounter-occurrence':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         wild_encounter = data.get( 'wildEncounter' )
         date = data.get( 'date' )
         time = data.get( 'time' )

         success = WildEncounterController.cancel_wild_encounter_occurrence(
            wild_encounter_name=wild_encounter,
            date=date,
            time=time )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'wildEncounter': wild_encounter,
            'date': date,
            'time': time
         }

         if not success:
            response[ 'error' ] = f'Could not cancel "{ wild_encounter }" on { date } at { time }.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-drinking-fountains-closed':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )
         message = data.get( 'message' )

         success = DrinkingFountainController.set_drinking_fountains_as_closed(
            start_date=start_date,
            end_date=end_date,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'startDate': start_date,
            'endDate': end_date,
            'message': message
         }

         if not success:
            response[ 'error' ] = 'Could not set drinking fountains as closed.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-drinking-fountains-open':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )

         success = DrinkingFountainController.set_drinking_fountains_as_open(
            start_date=start_date,
            end_date=end_date )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'startDate': start_date,
            'endDate': end_date
         }

         if not success:
            response[ 'error' ] = 'Could not set drinking fountains as open.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


if __name__ == '__main__':
   port = int( sys.argv[ 1 ] ) if len( sys.argv ) > 1 else DEFAULT_PORT
   httpd = HTTPServer( ( 'localhost', port ), MyHandler )
   print( 'Server listening on port: ', port )
   httpd.serve_forever()
