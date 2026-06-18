from __future__ import annotations

from typing import Any

from http_support_handler import make_handler
from http_support_handler import response_json

import api.server as server


def post_itinerary_route(
      path: str,
      body: dict[ str, Any ] | None = None,
) -> tuple[ int, dict[ str, Any ] ]:
   handler = make_handler( path, body )
   server.MyHandler.do_POST( handler )
   status = handler.statuses[ -1 ] if handler.statuses else 500
   return status, response_json( handler )
