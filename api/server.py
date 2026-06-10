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
from .animals.coordinators.animal_coordinator import AnimalCoordinator
from .attractions.coordinators.attraction_coordinator import AttractionCoordinator
from .giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
from .guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from .itinerary.controllers.itinerary_controller import ItineraryController
from .itinerary.logic.itinerary_result_response import itinerary_result_to_dict
from .itinerary.logic.itinerary_result_response import itinerary_time_set_result_to_dict
from .itinerary.logic.itinerary_result_response import suppress_itinerary_warning_result_to_dict
from .pavilions.coordinators.pavilion_coordinator import PavilionCoordinator
from .request_connection import clear_connection
from .request_connection import get_connection
from .request_connection import set_connection
from .restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from .restrooms.coordinators.restroom_coordinator import RestroomCoordinator
from .routes import POST_ROUTES
from .shared.constants import itinerary_config_to_dict
from .shared.typed_dict import to_dict_with_type
from .wild_encounters.controllers.wild_encounter_controller import WildEncounterController
from .zoo_hours.controllers.zoo_hours_controller import ZooHoursController
from .zoomobile.coordinators.zoomobile_coordinator import ZoomobileCoordinator


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
   def _read_json_body( self ) -> dict[ str, Any ]:
      content_length = int( self.headers[ 'Content-Length' ] )
      post_data = self.rfile.read( content_length )
      return json.loads( post_data.decode( 'utf-8' ) )


   def _write_json( self, payload: Any, status: int = 200 ) -> None:
      self.send_response( status )
      self.send_header( 'Content-type', 'application/json' )
      self.end_headers()
      self.wfile.write( json.dumps( payload ).encode( 'utf-8' ) )


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
      route = POST_ROUTES.get( self.path )

      if route is not None:
         route( self )
         return

      if self.path == '/get-wild-encounters':
         data = self._read_json_body()

         month = data.get( 'month' )
         day = data.get( 'day' )
         year = data.get( 'year' )

         wild_encounters = WildEncounterController.get_available_wild_encounters(
            month=month,
            day=day,
            year=year )

         response = { "wild_encounters": [ wild_encounter.to_dict() for wild_encounter in wild_encounters ] }
         self._write_json( response )


      elif self.path == '/search':
         data = self._read_json_body()

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
            animals_json = [
               to_dict_with_type( animal, 'animal' )
               for animal in (
                  AnimalCoordinator.get_animals_matching_query(
                     query=query,
                     day=day,
                     month=month,
                     year=year,
                     temp=temp,
                     include_off_display_animals=include_off_display_animals ) or []
               )
            ]

         if include_pavilions:
            pavilions_json = [
               to_dict_with_type( pavilion, 'pavilion' )
               for pavilion in (
                  PavilionCoordinator.get_pavilions_matching_query( query=query ) or []
               )
            ]

         if include_restaurants:
            restaurants_json = [
               to_dict_with_type( restaurant, 'restaurant' )
               for restaurant in (
                  RestaurantCoordinator.get_restaurants_matching_query(
                     query=query,
                     day=day,
                     month=month,
                     year=year,
                     include_closed_restaurants=include_closed_restaurants ) or []
               )
            ]

         if include_restrooms:
            restrooms_json = [
               to_dict_with_type( restroom, 'restroom' )
               for restroom in (
                  RestroomCoordinator.get_restrooms_matching_query(
                     query=query,
                     day=day,
                     month=month,
                     year=year,
                     include_closed_restrooms=include_closed_restrooms ) or []
               )
            ]

         if include_gift_shops:
            gift_shops_json = [
               to_dict_with_type( gift_shop, 'giftShop' )
               for gift_shop in (
                  GiftShopCoordinator.get_gift_shops_matching_query(
                     query=query,
                     day=day,
                     month=month,
                     year=year ) or []
               )
            ]

         if include_attractions:
            attractions_json = [
               to_dict_with_type( attraction, 'attraction' )
               for attraction in (
                  AttractionCoordinator.get_attractions_matching_query(
                     query=query,
                     day=day,
                     month=month,
                     year=year,
                     include_closed_attractions=include_closed_attractions ) or []
               )
            ]

         if include_zoomobile_stations:
            zoomobile_stations_json = [
               to_dict_with_type( zoomobile_station, 'zoomobileStation' )
               for zoomobile_station in (
                  ZoomobileCoordinator.get_zoomobile_stations_matching_query(
                     query=query,
                     route=zoomobile_route,
                     day=day,
                     month=month,
                     year=year ) or []
               )
            ]

         if include_guardians_talks:
            guardians_talks_json = [
               to_dict_with_type( guardians_talk, 'guardiansTalk' )
               for guardians_talk in (
                  GuardiansCoordinator.get_guardians_talks_matching_query(
                     query=query,
                     month=month,
                     day=day,
                     year=year ) or []
               )
            ]

         if include_wild_encounters:
            wild_encounters_json = [
               to_dict_with_type( wild_encounter, 'wildEncounter' )
               for wild_encounter in (
                  WildEncounterController.get_wild_encounters_matching_query(
                     query=query,
                     month=month,
                     day=day,
                     year=year ) or []
               )
            ]

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

         self._write_json( response )


      elif self.path == '/set-itinerary':
         data = self._read_json_body()

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
         confirming_early_admission = bool(
            data.get( 'confirmingEarlyAdmission' ) )
         confirming_guardians_talk_unschedule = bool(
            data.get( 'confirmingGuardiansTalkUnschedule' ) )
         confirming_wild_encounter_unschedule = bool(
            data.get( 'confirmingWildEncounterUnschedule' ) )

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
            confirming_early_admission=confirming_early_admission,
            confirming_guardians_talk_unschedule=(
               confirming_guardians_talk_unschedule ),
            confirming_wild_encounter_unschedule=(
               confirming_wild_encounter_unschedule ) )

         response = itinerary_result_to_dict(
            save_result,
            conn=get_connection(),
            include_config=True )

         self._write_json( response )


      elif self.path == '/get-itinerary-date':
         date = ItineraryController.get_itinerary_date()

         response = { 'date': date }
         self._write_json( response )


      elif self.path == '/schedule-itinerary-item':
         data = self._read_json_body()

         item_type = data.get( 'itemType' )
         key = data.get( 'key' )
         start_time = data.get( 'startTime' )
         duration_minutes = data.get( 'durationMinutes' )
         confirming_schedule_item_not_on_itinerary = bool(
            data.get( 'confirmingScheduleItemNotOnItinerary' ) )
         confirming_guardians_talk_unschedule = bool(
            data.get( 'confirmingGuardiansTalkUnschedule' ) )
         confirming_wild_encounter_unschedule = bool(
            data.get( 'confirmingWildEncounterUnschedule' ) )

         save_result = ItineraryController.schedule_itinerary_item(
            item_type=item_type,
            key=key,
            start_time=start_time,
            duration_minutes=duration_minutes,
            confirming_schedule_item_not_on_itinerary=(
               confirming_schedule_item_not_on_itinerary
            ),
            confirming_guardians_talk_unschedule=(
               confirming_guardians_talk_unschedule ),
            confirming_wild_encounter_unschedule=(
               confirming_wild_encounter_unschedule ) )

         response = itinerary_result_to_dict(
            save_result,
            conn=get_connection(),
            include_config=True )

         self._write_json( response )


      elif self.path == '/bulk-schedule-animals':
         data = self._read_json_body()

         temp = data.get( 'temp' )

         save_result = ItineraryController.bulk_schedule_animals(
            visit_date_temp=temp )

         response = itinerary_result_to_dict(
            save_result,
            conn=get_connection(),
            include_config=True )

         self._write_json( response )


      elif self.path == '/unschedule-itinerary-item':
         data = self._read_json_body()

         item_type = data.get( 'itemType' )
         key = data.get( 'key' )

         save_result = ItineraryController.unschedule_itinerary_item(
            item_type=item_type,
            key=key )

         response = itinerary_result_to_dict(
            save_result,
            conn=get_connection() )

         self._write_json( response )


      elif self.path == '/remove-item-from-itinerary':
         data = self._read_json_body()

         item_type = data.get( 'itemType' )
         key = data.get( 'key' )

         save_result = ItineraryController.remove_itinerary_item(
            item_type=item_type,
            key=key )

         response = itinerary_result_to_dict(
            save_result,
            conn=get_connection() )

         self._write_json( response )


      elif self.path == '/set-itinerary-arrival-time':
         data = self._read_json_body()

         arrival_time = data.get( 'arrivalTime' )
         confirming_short_visit = bool( data.get( 'confirmingShortVisit' ) )
         confirming_early_admission = bool(
            data.get( 'confirmingEarlyAdmission' ) )

         save_result = ItineraryController.set_arrival_time(
            arrival_time=arrival_time,
            confirming_short_visit=confirming_short_visit,
            confirming_early_admission=confirming_early_admission )

         response = itinerary_time_set_result_to_dict(
            save_result,
            conn=get_connection(),
            extra={ 'arrivalTime': arrival_time } )

         self._write_json( response )


      elif self.path == '/set-itinerary-departure-time':
         data = self._read_json_body()

         departure_time = data.get( 'departureTime' )
         confirming_short_visit = bool( data.get( 'confirmingShortVisit' ) )

         save_result = ItineraryController.set_departure_time(
            departure_time=departure_time,
            confirming_short_visit=confirming_short_visit )

         response = itinerary_time_set_result_to_dict(
            save_result,
            conn=get_connection(),
            extra={ 'departureTime': departure_time } )

         self._write_json( response )


      elif self.path == '/suppress-itinerary-warning':
         data = self._read_json_body()

         warning_type = data.get( 'warningType' )

         result = ItineraryController.suppress_itinerary_warning(
            warning_type=warning_type )

         response = suppress_itinerary_warning_result_to_dict(
            result,
            conn=get_connection() )

         self._write_json( response )


      elif self.path == '/get-itinerary':
         data = self._read_json_body()
         temp = data.get( 'temp' )

         itinerary = ItineraryController.get_itinerary( visit_date_temp=temp )

         response = {
            'itinerary': itinerary.to_dict(),
            'itinerary_config': itinerary_config_to_dict( get_connection() ),
         }

         self._write_json( response )


      elif self.path == '/get-zoo-hours':
         data = self._read_json_body()

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

         self._write_json( response )


      elif self.path == '/clear-itinerary':
         success = ItineraryController.clear_itinerary()

         response = {
            'success': success
         }

         if not success:
            response[ 'error' ] = 'Could not clear itinerary.'

         self._write_json( response )


      elif self.path == '/accept-itinerary':
         data = self._read_json_body()
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

         response = {
            'success': success,
            'itinerary': itinerary.to_dict() if itinerary != None else None,
            'itinerary_config': itinerary_config_to_dict( get_connection() ),
         }

         if not success:
            response[ 'error' ] = 'Could not accept itinerary changes.'

         self._write_json( response )


      elif self.path == '/get-wild-encounter-names':
         wild_encounters = WildEncounterController.get_wild_encounter_names()

         response = { "wild_encounters": wild_encounters }
         self._write_json( response )


      elif self.path == '/get-wild-encounter-occurrences':
         data = self._read_json_body()

         wild_encounter = data.get( 'wildEncounter' )

         occurrences = WildEncounterController.get_wild_encounter_occurrences(
            wild_encounter_name=wild_encounter )

         response = {
            'occurrences': [ occurrence.to_dict() for occurrence in occurrences ],
            'wildEncounter': wild_encounter
         }

         self._write_json( response )


      elif self.path == '/set-wild-encounter-schedule':
         data = self._read_json_body()

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

         self._write_json( response )


      elif self.path == '/end-wild-encounter-schedule':
         data = self._read_json_body()

         wild_encounter = data.get( 'wildEncounter' )
         schedule_end_date = data.get( 'endDate' )

         success = WildEncounterController.end_wild_encounter_schedule(
            wild_encounter_name=wild_encounter,
            schedule_end_date=schedule_end_date )

         response = {
            'success': success,
            'wildEncounter': wild_encounter,
            'endDate': schedule_end_date
         }

         if not success:
            response[ 'error' ] = f'Could not end schedule for "{ wild_encounter }".'

         self._write_json( response )


      elif self.path == '/cancel-wild-encounter-occurrence':
         data = self._read_json_body()

         wild_encounter = data.get( 'wildEncounter' )
         date = data.get( 'date' )
         time = data.get( 'time' )

         success = WildEncounterController.cancel_wild_encounter_occurrence(
            wild_encounter_name=wild_encounter,
            date=date,
            time=time )

         response = {
            'success': success,
            'wildEncounter': wild_encounter,
            'date': date,
            'time': time
         }

         if not success:
            response[ 'error' ] = f'Could not cancel "{ wild_encounter }" on { date } at { time }.'

         self._write_json( response )


if __name__ == '__main__':
   port = int( sys.argv[ 1 ] ) if len( sys.argv ) > 1 else DEFAULT_PORT
   httpd = HTTPServer( ( 'localhost', port ), MyHandler )
   print( 'Server listening on port: ', port )
   httpd.serve_forever()
