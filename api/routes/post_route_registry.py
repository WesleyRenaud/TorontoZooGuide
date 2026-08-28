from __future__ import annotations

from typing import ClassVar

from ..json_request_handler import PostRouteHandler

class PostRouteRegistry():
   ROUTES: ClassVar[ dict[ str, PostRouteHandler ] ] = {}

   @classmethod
   def register( cls, routes: dict[ str, PostRouteHandler ] ) -> None:
      cls.ROUTES.update( routes )
