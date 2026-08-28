from __future__ import annotations

from typing import ClassVar

from ..static_request_handler import GetRouteHandler

class GetRouteRegistry():
   ROUTES: ClassVar[ dict[ str, GetRouteHandler ] ] = {}

   @classmethod
   def register( cls, routes: dict[ str, GetRouteHandler ] ) -> None:
      cls.ROUTES.update( routes )
