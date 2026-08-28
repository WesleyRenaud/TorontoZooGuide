from __future__ import annotations

from typing import Any

from http_support_handler import make_handler
from http_support_handler import response_json

import api.http_request_handler as server


def post_route(
      path: str,
      body: dict[ str, Any ] | None = None,
) -> tuple[ int, dict[ str, Any ] ]:
   handler = make_handler( path, body )
   server.HttpRequestHandler.do_POST( handler )
   status = handler.statuses[ -1 ] if handler.statuses else 500
   return status, response_json( handler )
