from http.server import HTTPServer, BaseHTTPRequestHandler
from functools import wraps
import json
import mimetypes
import os
import sys
from urllib.parse import unquote, urlparse

import database


DEFAULT_PORT = 8000


def with_database( handler ):
   @wraps( handler )
   def wrapped( self, *args, **kwargs ):
      db = database.Database()

      try:
         self.database = db
         return handler( self, *args, **kwargs )
      finally:
         self.database = None
         db.close()

   return wrapped


class MyHandler( BaseHTTPRequestHandler ):
   database = None

   def _send_file( self, filepath, content_type=None ):
      if not os.path.isfile( filepath ):
         self.send_error( 404, "Not Found" )
         return

      self.send_response( 200 )
      if not content_type:
         content_type, _ = mimetypes.guess_type( filepath )
      self.send_header( "Content-type", content_type or "application/octet-stream" )
      self.end_headers()

      with open( filepath, "rb" ) as fp:
         while True:
               chunk = fp.read( 8192 )
               if not chunk:
                  break
               self.wfile.write( chunk )


   def do_GET( self ):
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


   @with_database
   def do_POST( self ):
      if self.path == '/get-visible-animals':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         temp = data.get( 'temp' )
         include_off_display_animals = data.get( 'includeOffDisplayAnimals' ) or False

         animals = self.database.get_animals_viewable_on_day(
            month=month,
            day=day,
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

         exhibits = self.database.get_exhibits_in_region( region=region )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "exhibits": exhibits }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-regions':
         regions = self.database.get_regions()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { 'regions': regions }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-animal-names-by-exhibit':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         exhibit = data.get( 'exhibit' )

         animals = self.database.get_animals_in_exhibit( exhibit=exhibit )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "animals": animals }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-animal-information':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         species = data.get( 'species' )

         animal_info = self.database.get_animal_information( species=species )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "information": [ animal_info.to_dict() ] }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-animals-by-exhibit':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         temp = data.get( 'temp' )
         exhibits_to_include = data.get( 'exhibitsToInclude' ) or []

         animals = self.database.get_animals_viewable_on_day(
            month=month,
            day=day,
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
         pavilions = self.database.get_pavilions()

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
         include_closed_restaurants = data.get( 'includeClosedRestaurants' )
         restaurants_to_include = data.get( 'restaurantsToInclude' )

         restaurants = self.database.get_restaurants(
            month=month,
            day=day,
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
         include_closed_restrooms = data.get( 'includeClosedRestrooms' ) or False

         restrooms = self.database.get_restrooms(
            month=month,
            day=day,
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
         include_closed_gift_shops = data.get( 'includeClosedGiftShops' )
         gift_shops_to_include = data.get( 'giftShopsToInclude' )

         gift_shops = self.database.get_gift_shops(
            month=month,
            day=day,
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
         include_closed_attractions = data.get( 'includeClosedAttractions' ) or False

         attractions = self.database.get_attractions(
            month=month,
            day=day,
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
         zoomobile_stations_to_include = data.get( 'zoomobileStationsToInclude' ) or []

         zoomobile_route = self.database.get_zoomobile_route(
            route=route,
            month=month,
            day=day,
            zoomobile_stations_to_include=zoomobile_stations_to_include )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'route': zoomobile_route[ 'route' ],
            'route_source': zoomobile_route[ 'route_source' ],
            'zoomobile_stations': [ station.to_dict() for station in zoomobile_route[ 'zoomobile_stations' ] ]
         }

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-guardians-talks':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )

         guardians_talks = self.database.get_guardians_talks( month=month, day=day )

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

         wild_encounters = self.database.get_available_wild_encounters(
            month=month,
            day=day )

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

         drinking_fountains = self.database.get_drinking_fountains( month=month, day=day )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "drinking_fountains": [ drinking_fountain.to_dict() for drinking_fountain in drinking_fountains ] }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-defibrillators':
         defibrillators = self.database.get_defibrillators()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "defibrillators": [ defibrillator.to_dict() for defibrillator in defibrillators ] }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-emergency-intercoms':
         emergency_intercoms = self.database.get_emergency_intercoms()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "emergency_intercoms": [ emergency_intercom.to_dict() for emergency_intercom in emergency_intercoms ] }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-closed-exhibits':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )

         closed_exhibits = self.database.get_closed_exhibits(
            month=month,
            day=day
         )

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
            animals = self.database.get_animals_matching_query(
               query=query,
               month=month,
               day=day,
               temp=temp,
               include_off_display_animals=include_off_display_animals ) or []
            for animal in animals:
                  d = animal.to_dict()
                  d[ 'type' ] = d.get( 'type', 'animal' )
                  animals_json.append( d )

         if include_pavilions:
            pavilions = self.database.get_pavilions_matching_query( query=query ) or []
            for pavilion in pavilions:
                  d = pavilion.to_dict()
                  d[ 'type' ] = d.get( 'type', 'pavilion' )
                  pavilions_json.append( d )

         if include_restaurants:
            restaurants = self.database.get_restaurants_matching_query(
               query=query,
               month=month,
               day=day,
               include_closed_restaurants=include_closed_restaurants ) or []
            for restaurant in restaurants:
                  d = restaurant.to_dict()
                  d[ 'type' ] = d.get( 'type', 'restaurant' )
                  restaurants_json.append( d )

         if include_restrooms:
            restrooms = self.database.get_restrooms_matching_query(
               query=query,
               month=month,
               day=day,
               include_closed_restrooms=include_closed_restrooms ) or []
            for restroom in restrooms:
                  d = restroom.to_dict()
                  d[ 'type' ] = d.get( 'type', 'restroom' )
                  restrooms_json.append( d )

         if include_gift_shops:
            gift_shops = self.database.get_gift_shops_matching_query( query=query, month=month, day=day ) or []
            for gift_shop in gift_shops:
                  d = gift_shop.to_dict()
                  d[ 'type' ] = d.get( 'type', 'giftShop' )
                  gift_shops_json.append( d )

         if include_attractions:
            attractions = self.database.get_attractions_matching_query(
               query=query,
               month=month,
               day=day,
               include_closed_attractions=include_closed_attractions ) or []
            for attraction in attractions:
                  d = attraction.to_dict()
                  d[ 'type' ] = d.get( 'type', 'attraction' )
                  attractions_json.append( d )

         if include_zoomobile_stations:
            zoomobile_stations = self.database.get_zoomobile_stations_matching_query(
               query=query,
               route=zoomobile_route,
               month=month,
               day=day ) or []
            for zoomobile_station in zoomobile_stations:
                  d = zoomobile_station.to_dict()
                  d[ 'type' ] = d.get( 'type', 'zoomobileStation' )
                  zoomobile_stations_json.append( d )

         if include_guardians_talks:
            guardians_talks = self.database.get_guardians_talks_matching_query( query=query, month=month, day=day ) or []
            for guardians_talk in guardians_talks:
                  d = guardians_talk.to_dict()
                  d[ 'type' ] = d.get( 'type', 'guardiansTalk' )
                  guardians_talks_json.append( d )

         if include_wild_encounters:
            wild_encounters = self.database.get_wild_encounters_matching_query( query=query, month=month, day=day ) or []
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
         animals = data.get( 'animals' )
         attractions = data.get( 'attractions' )
         guardians_talks = data.get( 'guardiansTalks' )
         wild_encounters = data.get( 'wildEncounters' )
         is_active = data.get( 'isActive' )

         success = self.database.set_itinerary(
            date=date,
            animals=animals,
            attractions=attractions,
            guardians_talks=guardians_talks,
            wild_encounters=wild_encounters,
            is_active=is_active )

         itinerary = self.database.get_itinerary() if success else None

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'itinerary': itinerary.to_dict() if itinerary != None else None
         }

         if not success:
            response[ 'error' ] = 'Could not save itinerary.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-itinerary':
         itinerary = self.database.get_itinerary()

         response = { 'itinerary': itinerary.to_dict() }

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/clear-itinerary':
         success = self.database.clear_itinerary()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success
         }

         if not success:
            response[ 'error' ] = 'Could not clear itinerary.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/validate-itinerary':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         date = data.get( 'date' )
         temp = data.get( 'temp' )
         animals_to_include = data.get( 'animals' ) or []
         attractions_to_include = data.get( 'attractions' ) or []
         guardians_talks_to_include = data.get( 'guardiansTalks' ) or []
         wild_encounters_to_include = data.get( 'wildEncounters' ) or []

         previous_itinerary = self.database.get_itinerary()

         previous_animals_json = []
         previous_attractions_json = []
         previous_guardians_talks_json = []
         previous_wild_encounters_json = []

         if previous_itinerary != None:
            for animal in previous_itinerary.animals:
               d = animal.to_dict()
               d[ 'type' ] = d.get( 'type', 'animal' )
               previous_animals_json.append( d )

            for attraction in previous_itinerary.attractions:
               d = attraction.to_dict()
               d[ 'type' ] = d.get( 'type', 'attraction' )
               previous_attractions_json.append( d )

            for guardians_talk in previous_itinerary.guardians_talks:
               d = guardians_talk.to_dict()
               d[ 'type' ] = d.get( 'type', 'guardiansTalk' )
               previous_guardians_talks_json.append( d )

            for wild_encounter in previous_itinerary.wild_encounters:
               d = wild_encounter.to_dict()
               d[ 'type' ] = d.get( 'type', 'wildEncounter' )
               previous_wild_encounters_json.append( d )

         animal_validation = self.database.validate_animals(
            month=month,
            day=day,
            temp=temp,
            animals_to_include=animals_to_include )

         animals = animal_validation[ 'valid_animals' ]
         removed_animals = animal_validation[ 'removed_animals' ]

         attraction_validation = self.database.validate_attractions(
            month=month,
            day=day,
            attractions_to_include=attractions_to_include )

         attractions = attraction_validation[ 'valid_attractions' ]
         removed_attractions = attraction_validation[ 'removed_attractions' ]

         guardians_talk_validation = self.database.validate_guardians_talks(
            month=month,
            day=day,
            guardians_talks_to_include=guardians_talks_to_include )

         guardians_talks = guardians_talk_validation[ 'valid_guardians_talks' ]
         removed_guardians_talks = guardians_talk_validation[ 'removed_guardians_talks' ]

         wild_encounter_validation = self.database.validate_wild_encounters(
            month=month,
            day=day,
            wild_encounters_to_include=wild_encounters_to_include )

         wild_encounters = wild_encounter_validation[ 'valid_wild_encounters' ]
         removed_wild_encounters = wild_encounter_validation[ 'removed_wild_encounters' ]

         animals_json = []
         removed_animals_json = []
         attractions_json = []
         removed_attractions_json = []
         guardians_talks_json = []
         removed_guardians_talks_json = []
         wild_encounters_json = []
         removed_wild_encounters_json = []

         for animal in animals:
            d = animal.to_dict()
            d[ 'type' ] = d.get( 'type', 'animal' )
            animals_json.append( d )

         for animal in removed_animals:
            d = animal.to_dict()
            d[ 'type' ] = d.get( 'type', 'animal' )
            d[ 'removalReason' ] = animal.off_display_message
            removed_animals_json.append( d )

         for attraction in attractions:
            d = attraction.to_dict()
            d[ 'type' ] = d.get( 'type', 'attraction' )
            attractions_json.append( d )

         for attraction in removed_attractions:
            d = attraction.to_dict()
            d[ 'type' ] = d.get( 'type', 'attraction' )
            d[ 'removalReason' ] = attraction.closed_message
            removed_attractions_json.append( d )

         for guardians_talk in guardians_talks:
            d = guardians_talk.to_dict()
            d[ 'type' ] = d.get( 'type', 'guardiansTalk' )
            guardians_talks_json.append( d )

         for guardians_talk in removed_guardians_talks:
            d = guardians_talk.to_dict()
            d[ 'type' ] = d.get( 'type', 'guardiansTalk' )
            d[ 'removalReason' ] = guardians_talk.unavailable_message
            removed_guardians_talks_json.append( d )

         for wild_encounter in wild_encounters:
            d = wild_encounter.to_dict()
            d[ 'type' ] = d.get( 'type', 'wildEncounter' )
            wild_encounters_json.append( d )

         for wild_encounter in removed_wild_encounters:
            d = wild_encounter.to_dict()
            d[ 'type' ] = d.get( 'type', 'wildEncounter' )
            d[ 'removalReason' ] = wild_encounter.unavailable_message
            removed_wild_encounters_json.append( d )

         clear_success = self.database.clear_itinerary()

         set_success = False

         if clear_success:
            set_success = self.database.set_itinerary(
               date=date,
               animals=animals_json,
               attractions=attractions_json,
               guardians_talks=guardians_talks_json,
               wild_encounters=wild_encounters_json,
               is_active=True )

         response = {
            'success': clear_success and set_success,
            'previous': {
               'animals': previous_animals_json,
               'attractions': previous_attractions_json,
               'guardiansTalks': previous_guardians_talks_json,
               'wildEncounters': previous_wild_encounters_json,
            },
            'validated': {
               'animals': animals_json,
               'attractions': attractions_json,
               'guardiansTalks': guardians_talks_json,
               'wildEncounters': wild_encounters_json,
            },
            'removed': {
               'animals': removed_animals_json,
               'attractions': removed_attractions_json,
               'guardiansTalks': removed_guardians_talks_json,
               'wildEncounters': removed_wild_encounters_json,
            },
         }

         if not clear_success:
            response[ 'error' ] = 'Could not clear itinerary.'
         elif not set_success:
            response[ 'error' ] = 'Could not save validated itinerary.'

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-species':
         species = self.database.get_species()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "species": species }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-restaurant-names':
         restaurants = self.database.get_restaurant_names()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "restaurants": restaurants }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-restroom-names':
         restrooms = self.database.get_restroom_names()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "restrooms": restrooms }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-gift-shop-names':
         gift_shops = self.database.get_gift_shop_names()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "gift_shops": gift_shops }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-attraction-names':
         attractions = self.database.get_attraction_names()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "attractions": attractions }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-zoomobile-station-names':
         zoomobile_stations = self.database.get_zoomobile_station_names()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "zoomobile_stations": zoomobile_stations }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-guardians-talk-locations':
         guardians_talk_locations = self.database.get_guardians_talk_locations()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "guardians_talk_locations": guardians_talk_locations }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-guardians-talk-names':
         guardians_talks = self.database.get_guardians_talk_names()

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

         guardians_talks = self.database.get_guardians_talk_names_at_location( location=location )

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

         occurrences = self.database.get_guardians_talk_occurrences( talk=talk, location=location )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'occurrences': occurrences,
            'talk': talk,
            'location': location
         }

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-wild-encounter-names':
         wild_encounters = self.database.get_wild_encounter_names()

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

         occurrences = self.database.get_wild_encounter_occurrences( wild_encounter=wild_encounter )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'occurrences': occurrences,
            'wildEncounter': wild_encounter
         }

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-exhibits-by-region':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )

         regions = self.database.get_regions_with_exhibits(
            month=month,
            day=day )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = { "regions": regions }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-exhibits':
         exhibits = self.database.get_exhibits()

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

         success = self.database.set_animal_as_off_display(
            species=species,
            exhibit=exhibit,
            start_date=start_date,
            end_date=end_date,
            message=message )

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

         success = self.database.set_animal_as_on_display(
            species=species,
            exhibit=exhibit )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'species': species,
            'exhibit': exhibit,
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

         success = self.database.set_animal_limited_viewing_schedule(
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

         success = self.database.remove_animal_visibility_schedule( species=species, exhibit=exhibit )

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

         success = self.database.set_animal_viewing_alert(
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

         success = self.database.remove_animal_viewing_alert( species=species, exhibit=exhibit )

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

         success = self.database.set_exhibit_as_closed( exhibit=exhibit, start_date=start_date, end_date=end_date, message=message )

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

         success = self.database.set_exhibit_as_open(
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

         success = self.database.set_restroom_as_closed(
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

         success = self.database.set_restroom_as_open(
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

         success = self.database.set_restroom_alert(
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

         success = self.database.remove_restroom_alert(
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


      elif self.path == '/set-restaurant-closed':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         restaurant = data.get( 'restaurant' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )
         message = data.get( 'message' )

         success = self.database.set_restaurant_as_closed(
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

         success = self.database.set_restaurant_opening_schedule(
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

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-gift-shop-closed':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         gift_shop = data.get( 'giftShop' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )
         message = data.get( 'message' )

         success = self.database.set_gift_shop_as_closed(
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

         success = self.database.set_gift_shop_opening_schedule(
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

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-attraction-closed':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         attraction = data.get( 'attraction' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )
         message = data.get( 'message' )

         success = self.database.set_attraction_as_closed(
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

         success = self.database.set_attraction_opening_schedule(
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

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-zoomobile-station-closed':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         zoomobile_station = data.get( 'zoomobileStation' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )
         message = data.get( 'message' )

         success = self.database.set_zoomobile_station_as_closed(
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

         success = self.database.set_zoomobile_station_as_open( zoomobile_station=zoomobile_station )

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
            success = self.database.set_current_zoomobile_route(
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
         talk_time = data.get( 'time' )

         monday = data.get( 'monday' )
         tuesday = data.get( 'tuesday' )
         wednesday = data.get( 'wednesday' )
         thursday = data.get( 'thursday' )
         friday = data.get( 'friday' )
         saturday = data.get( 'saturday' )
         sunday = data.get( 'sunday' )

         message = data.get( 'message' )

         success = self.database.set_guardians_talk_schedule(
            talk=talk,
            location=location,
            start_date=schedule_start_date,
            end_date=schedule_end_date,
            talk_time=talk_time,
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
            'talk': talk,
            'location': location,
            'startDate': schedule_start_date,
            'endDate': schedule_end_date,
            'time': talk_time,
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
            response[ 'error' ] = f'Could not set schedule for "{ talk }" at "{ location }".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/end-guardians-talk-schedule':
         content_length = int( self.headers[ 'Content-Length' ] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         talk = data.get( 'talk' )
         location = data.get( 'location' )
         schedule_end_date = data.get( 'endDate' )

         success = self.database.end_guardians_talk_schedule(
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

         success = self.database.cancel_guardians_talk_occurrence(
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

         success = self.database.set_wild_encounter_schedule(
            wild_encounter=wild_encounter,
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

         success = self.database.end_wild_encounter_schedule(
            wild_encounter=wild_encounter,
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

         success = self.database.cancel_wild_encounter_occurrence(
            wild_encounter=wild_encounter,
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

         success = self.database.set_drinking_fountains_as_closed(
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

         success = self.database.set_drinking_fountains_as_open(
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
