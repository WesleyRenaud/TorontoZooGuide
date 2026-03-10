from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import mimetypes
import os
import sys
from urllib.parse import unquote, urlparse

import database


class MyHandler( BaseHTTPRequestHandler ):
   database = database.Database()

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
         return self._send_file("." + path )   # serves ALL modules
      if path.startswith( "/images/" ):
         return self._send_file( "." + path )

      # Otherwise
      self.send_error( 404, "Not Found" )


   def do_POST( self ):
      if self.path == '/get-visible-animals':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         temp = data.get( 'temp' )
         include_off_display_animals = data.get( 'includeOffDisplayAnimals' )
         species_to_include = data.get( 'speciesToInclude' )

         animals = self.database.get_animals_viewable_on_day( month=month, day=day, temp=temp,
                                                              include_off_display_animals=include_off_display_animals,
                                                              species_to_include=species_to_include )
         
         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"animals": [animal.to_dict() for animal in animals]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-exhibits-in-region':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         region = data.get( 'region' )

         exhibits = self.database.get_exhibits_in_region( region )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"exhibits": exhibits}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-animals-in-exhibit':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         exhibit = data.get( 'exhibit' )

         animals = self.database.get_animals_in_exhibit( exhibit )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"animals": animals}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-animal-information':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         species = data.get( 'species' )

         animal_info = self.database.get_animal_information( species )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"information": [animal_info.to_dict()]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-pavilions':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         pavilions = self.database.get_pavilions()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"pavilions": [pavilion.to_dict() for pavilion in pavilions]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-restaurants':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         include_seasonal_restaurants = data.get( 'includeSeasonalRestaurants' )
         restaurants_to_include = data.get( 'restaurantsToInclude' )

         restaurants = self.database.get_restaurants( month, include_seasonal_restaurants, restaurants_to_include )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"restaurants": [restaurant.to_dict() for restaurant in restaurants]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-restrooms':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         restrooms = self.database.get_restrooms()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"restrooms": [restroom.to_dict() for restroom in restrooms]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-gift-shops':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         include_seasonal_gift_shops = data.get( 'includeSeasonalGiftShops' )
         gift_shops_to_include = data.get( 'giftShopsToInclude' )

         gift_shops = self.database.get_gift_shops( month, include_seasonal_gift_shops, gift_shops_to_include )
         
         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"gift_shops": [gift_shop.to_dict() for gift_shop in gift_shops]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-attractions':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         include_seasonal_attractions = data.get( 'includeSeasonalAttractions' )
         attractions_to_include = data.get( 'attractionsToInclude' )

         attractions = self.database.get_attractions( month, include_seasonal_attractions, attractions_to_include )
         
         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"attractions": [attraction.to_dict() for attraction in attractions]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-zoomobile-route':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         route_type = data.get( 'zoomobileRouteType' )
         zoomobile_stations_to_include = data.get( 'zoomobileStationsToInclude' )

         zoomobile_route = self.database.get_zoomobile_route( route_type, zoomobile_stations_to_include )
         
         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {
            "zoomobile_stations": [station.to_dict() for station in zoomobile_route[0]],
            "zoomobile_route_markers": [marker.to_dict() for marker in zoomobile_route[1]]
         }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-meet-the-guardians-talks':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         meet_the_guardians_talks = self.database.get_meet_the_guardians_talks()
         
         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"meet_the_guardians_talks": [meet_the_guardians_talk.to_dict() for meet_the_guardians_talk in meet_the_guardians_talks]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-wild-encounter-meeting-spots':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         wild_encounter_meeting_spots = self.database.get_wild_encounter_meeting_spots()
         
         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"wild_encounter_meeting_spots": [wild_encounter_meeting_spot.to_dict() for wild_encounter_meeting_spot in wild_encounter_meeting_spots]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/search':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         query = ( data.get( 'query' ) or '' ).strip()
         include_animals = bool( data.get( 'includeAnimals' ) )
         include_pavilions = bool( data.get( 'includePavilions' ) )
         include_restaurants = bool( data.get( 'includeRestaurants') )
         include_restrooms = bool( data.get( 'includeRestrooms' ) )
         include_gift_shops = bool( data.get( 'includeGiftShops' ) )
         include_attractions = bool( data.get( 'includeAttractions' ) )
         include_zoomobile_stations = bool( data.get( 'includeZoomobileStations' ) )
         include_wild_encounter_meeting_spots = bool( data.get( 'includeWildEncounterMeetingSpots' ) )
         include_wild_encounters = bool( data.get( 'includeWildEncounters' ) )
         include_meet_the_guardians_talks = bool( data.get( 'includeMeetTheGuardiansTalks' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         temp = data.get( 'temp' )
         day_of_week = data.get( 'dayOfWeek' )

         include_off_display_animals = bool( data.get( 'includeOffDisplayAnimals' ) )
         include_season_attractions = bool( data.get( 'includeSeasonalAttractions' ) )

         animals_json = []
         pavilions_json = []
         restaurants_json = []
         restrooms_json = []
         gift_shops_json = []
         attractions_json = []
         zoomobile_stations_json = []
         wild_encounter_meeting_spots_json = []
         wild_encounters_json = []
         meet_the_guardians_talks_json = []

         if include_animals:
            animals = self.database.get_animals_matching_query( query, month, day, temp, include_off_display_animals ) or []
            for animal in animals:
                  d = animal.to_dict()
                  d['type'] = d.get( 'type', 'animal' )
                  animals_json.append( d )

         if include_pavilions:
            pavilions = self.database.get_pavilions_matching_query( query ) or []
            for pavilion in pavilions:
                  d = pavilion.to_dict()
                  d['type'] = d.get( 'type', 'pavilion' )
                  pavilions_json.append( d )

         if include_restaurants:
            restaurants = self.database.get_restaurants_matching_query( query, month ) or []
            for restaurant in restaurants:
                  d = restaurant.to_dict()
                  d['type'] = d.get( 'type', 'restaurant' )
                  restaurants_json.append( d )

         if include_restrooms:
            restrooms = self.database.get_restrooms_matching_query( query ) or []
            for restroom in restrooms:
                  d = restroom.to_dict()
                  d['type'] = d.get( 'type', 'restroom' )
                  restrooms_json.append( d )

         if include_gift_shops:
            gift_shops = self.database.get_gift_shops_matching_query( query, month ) or []
            for gift_shop in gift_shops:
                  d = gift_shop.to_dict()
                  d['type'] = d.get( 'type', 'giftShop' )
                  gift_shops_json.append( d )

         if include_attractions:
            attractions = self.database.get_attractions_matching_query( query, month, include_season_attractions ) or []
            for attraction in attractions:
                  d = attraction.to_dict()
                  d['type'] = d.get( 'type', 'attraction' )
                  attractions_json.append( d )

         if include_zoomobile_stations:
            zoomobile_stations = self.database.get_zoomobile_stations_matching_query( query ) or []
            for zoomobile_station in zoomobile_stations:
                  d = zoomobile_station.to_dict()
                  d['type'] = d.get( 'type', 'zoomobileStation' )
                  zoomobile_stations_json.append( d )

         if include_wild_encounter_meeting_spots:
            wild_encounter_meeting_spots = self.database.get_wild_encounter_meeting_spots_matching_query( query ) or []
            for wild_encounter_meeting_spot in wild_encounter_meeting_spots:
                  d = wild_encounter_meeting_spot.to_dict()
                  d['type'] = d.get( 'type', 'wildEncounterMeetingSpot' )
                  wild_encounter_meeting_spots_json.append( d )

         if include_meet_the_guardians_talks:
            meet_the_guardians_talks = self.database.get_meet_the_guardians_talks_with_date_times_matching_query( query, day_of_week ) or []
            for meet_the_guardians_talk in meet_the_guardians_talks:
                  d = meet_the_guardians_talk.to_dict()
                  d['type'] = d.get( 'type', 'meetTheGuardiansTalk' )
                  meet_the_guardians_talks_json.append( d )

         if include_wild_encounters:
            wild_encounters = self.database.get_wild_encounters_matching_query( query, day_of_week ) or []
            for wild_encounter in wild_encounters:
                  d = wild_encounter.to_dict()
                  d['type'] = d.get( 'type', 'wildEncounter' )
                  wild_encounters_json.append( d )

         response = {
            'animals': animals_json,
            'pavilions': pavilions_json,
            'restaurants': restaurants_json,
            'restrooms': restrooms_json,
            'gift_shops': gift_shops_json,
            'attractions': attractions_json,
            'zoomobile_stations': zoomobile_stations_json,
            'wild_encounter_meeting_spots': wild_encounter_meeting_spots_json,
            'wild_encounters': wild_encounters_json,
            'meet_the_guardians_talks': meet_the_guardians_talks_json
         }

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )

   
      elif self.path == '/build-itinerary':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         temp = data.get( 'temp' )
         animals_to_include = data.get( 'animals' )
         attractions_to_include = data.get( 'attractions' )
         meet_the_guardians_talks_to_include = data.get( 'meetTheGuardiansTalks' )
         wild_encounters_to_include = data.get( 'wildEncounters' )

         animals_json = []
         attractions_json = []
         meet_the_guardians_talks_json = []
         wild_encounters_json = []

         if animals_to_include:
            animals = self.database.get_animals_viewable_on_day( month=month,
                                                                 day=day,
                                                                 temp=temp,
                                                                 species_to_include=animals_to_include,
                                                                 itinerary_mode=True )
            for animal in animals:
               d = animal.to_dict()
               d['type'] = d.get( 'type', 'animal' )
               animals_json.append( d )

         if attractions_to_include:
            attractions = self.database.get_attractions( month=month,
                                                         attractions_to_include=attractions_to_include,
                                                         itinerary_mode=True )
            for attraction in attractions:
                  d = attraction.to_dict()
                  d['type'] = d.get( 'type', 'attraction' )
                  attractions_json.append( d )
               
         if meet_the_guardians_talks_to_include:
            meet_the_guardians_talks = self.database.get_meet_the_guardians_talks_with_date_times( meet_the_guardians_talks_to_include=
                                                                                                   meet_the_guardians_talks_to_include,
                                                                                                   itinerary_mode=True )
            for meet_the_guardians_talk in meet_the_guardians_talks:
                  d = meet_the_guardians_talk.to_dict()
                  d['type'] = d.get( 'type', 'meetTheGuardiansTalk' )
                  meet_the_guardians_talks_json.append( d )

         if wild_encounters_to_include:
            wild_encounters = self.database.get_wild_encounter_meeting_spots_for_wild_encounters( wild_encounters_to_include=wild_encounters_to_include )
            for wild_encounter in wild_encounters:
                  d = wild_encounter.to_dict()
                  d['type'] = d.get( 'type', 'wildEncounter' )
                  wild_encounters_json.append( d )

         response = {
            'animals': animals_json,
            'attractions': attractions_json,
            'meet_the_guardians_talks': meet_the_guardians_talks_json,
            'wild_encounters': wild_encounters_json
         }

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      if self.path == '/get-species':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         species = self.database.get_species()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"species": species}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      if self.path == '/get-exhibits':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         exhibits = self.database.get_exhibits()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"exhibits": exhibits}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-animal-off-display':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         species = data.get( 'species' )
         exhibit = data.get( 'exhibit' )
         message = data.get( 'message' )

         success = self.database.set_animal_as_off_display( species, exhibit, message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'species': species,
            'exhibit': exhibit,
            'message': message,
         }

         if not success:
            response[ 'error' ] = f'No animal found with species "{species}".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-animal-on-display':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         species = data.get( 'species' )
         exhibit = data.get( 'exhibit' )

         success = self.database.set_animal_as_on_display( species, exhibit )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'species': species,
            'exhibit': exhibit,
         }

         if not success:
            response['error'] = f'No off-display entry found for "{species}" in "{exhibit}".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


if __name__ == '__main__':
   httpd = HTTPServer( ( 'localhost', int( sys.argv[1] ) ), MyHandler )
   print( 'Server listing in port:  ', int( sys.argv[1] ) )
   httpd.serve_forever()
