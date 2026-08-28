from __future__ import annotations

from collections.abc import Callable
from typing import Protocol


class StaticRequestHandler( Protocol ):
   path: str


   def _send_file(
         self,
         filepath: str,
         content_type: str | None = None ) -> None:
      ...


   def send_error( self, code: int, message: str | None = None ) -> None:
      ...


GetRouteHandler = Callable[ [ StaticRequestHandler ], None ]
