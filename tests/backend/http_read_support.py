from __future__ import annotations

from typing import Any

from http_support import make_handler
from http_support import response_json

import api.server as server


def assert_read_endpoint_returns_json_key(
      path: str,
      body: dict[ str, Any ],
      response_key: str ) -> None:
   handler = make_handler( path, body )

   server.MyHandler.do_POST( handler )

   assert handler.statuses == [ 200 ]
   assert response_key in response_json( handler )
