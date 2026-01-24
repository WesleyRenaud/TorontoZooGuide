from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
from urllib.parse import urlparse

import database


class MyHandler( BaseHTTPRequestHandler ):
   database = database.Database()

   def do_GET( self ):
      parsed = urlparse( self.path )

      if parsed.path in ['/home.html']:
         self.send_response( 200 )
         self.send_header( 'Content-type', 'text/html' )
         self.end_headers()
         with open( './pages/home.html', 'rb' ) as fp:
            while True:
               chunk = fp.read( 8192 )
               if not chunk:
                  break
               self.wfile.write( chunk )

      elif parsed.path == '/styles/styles.css':
         self.send_response( 200 )
         self.send_header( 'Content-type', 'text/css' )
         self.end_headers()
         with open( './styles/styles.css', 'rb' ) as fp:
            while True:
               chunk = fp.read( 8192 )
               if not chunk:
                  break
               self.wfile.write( chunk )

      elif parsed.path == '/scripts/scripts.js':
         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/javascript' )
         self.end_headers()
         with open('./scripts/scripts.js', 'rb') as fp:
            while True:
               chunk = fp.read( 8192 )
               if not chunk:
                  break
               self.wfile.write( chunk )

      elif 'png' in parsed.path:
         image_path = parsed.path.replace( '%20', ' ' )
         image_path = image_path[1:]

         self.send_response( 200 )
         self.send_header( 'Content-type', 'image/png' )
         self.end_headers()
         with open(image_path, 'rb') as fp:
            while True:
               chunk = fp.read( 8192 )
               if not chunk:
                  break
               self.wfile.write( chunk )


   def do_POST( self ):
      if self.path == '/get-visible-animals':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         temp = data.get( 'temp' )

         animals = self.database.get_animals_viewable_on_day( month, day, temp )
         
         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"animals": [animal.to_dict() for animal in animals]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


if __name__ == '__main__':
   httpd = HTTPServer( ( 'localhost', int( sys.argv[1] ) ), MyHandler )
   print( 'Server listing in port:  ', int( sys.argv[1] ) )
   httpd.serve_forever()
