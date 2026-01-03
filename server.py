from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
from urllib.parse import urlparse


class MyHandler( BaseHTTPRequestHandler ):    
   def do_GET( self ):
      parsed = urlparse( self.path )

      if parsed.path in ['/home.html']:
         fp = open( './pages/home.html' )
         content = fp.read()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'text/html' )
         self.send_header( 'Content-length', len( content ) )
         self.end_headers()
         self.wfile.write( bytes( content, 'utf-8' ) )


if __name__ == '__main__':
   httpd = HTTPServer( ( 'localhost', int( sys.argv[1] ) ), MyHandler )
   print( 'Server listing in port:  ', int( sys.argv[1] ) )
   httpd.serve_forever()