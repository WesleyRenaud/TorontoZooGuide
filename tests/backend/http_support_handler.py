from __future__ import annotations

from io import BytesIO
import json
from typing import Any

import api.server as server

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
