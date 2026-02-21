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

         animals = self.database.get_animals_viewable_on_day( month, day, temp, include_off_display_animals, species_to_include )
         
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

         restaurants = self.database.get_restaurants()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"restaurants": [restaurant.to_dict() for restaurant in restaurants]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/search':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         query = ( data.get( 'query' ) or '' ).strip()
         include_animals = bool( data.get( 'includeAnimals' ) )
         include_pavilions = bool( data.get( 'includePavilions' ) )
         include_restaurants = bool( data.get( 'includeRestaurants') )

         animals_json = []
         pavilions_json = []
         restaurants_json = []

         if include_animals and query:
            animals = self.database.get_animals_matching_query( query ) or []
            for animal in animals:
                  d = animal.to_dict()
                  d['type'] = d.get( 'type', 'animal' )
                  animals_json.append( d )

         if include_pavilions and query:
            pavilions = self.database.get_pavilions_matching_query( query ) or []
            for pavilion in pavilions:
                  d = pavilion.to_dict()
                  d['type'] = d.get( 'type', 'pavilion' )
                  pavilions_json.append( d )

         if include_restaurants and query:
            restaurants = self.database.get_restaurants_matching_query( query ) or []
            for restaurant in restaurants:
                  d = restaurant.to_dict()
                  d['type'] = d.get( 'type', 'restaurant' )
                  restaurants_json.append( d )

         response = {
            'animals': animals_json,
            'pavilions': pavilions_json,
            'restaurants': restaurants_json
         }

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


if __name__ == '__main__':
   httpd = HTTPServer( ( 'localhost', int( sys.argv[1] ) ), MyHandler )
   print( 'Server listing in port:  ', int( sys.argv[1] ) )
   httpd.serve_forever()
