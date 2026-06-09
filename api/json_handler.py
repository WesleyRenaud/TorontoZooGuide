from __future__ import annotations

from collections.abc import Callable
from typing import Any, Protocol


class JsonRequestHandler( Protocol ):
   def _read_json_body( self ) -> dict[ str, Any ]:
      ...


   def _write_json( self, payload: Any, status: int = 200 ) -> None:
      ...


PostRouteHandler = Callable[ [ JsonRequestHandler ], None ]
