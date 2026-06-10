from __future__ import annotations

from collections.abc import Callable
import contextvars
from functools import wraps
from typing import Any

from . import connection
from .types import Connection


_connection = contextvars.ContextVar( 'connection', default=None )


def set_connection( conn: Connection | None ) -> None:
   _connection.set( conn )


def get_connection() -> Connection | None:
   return _connection.get()


def clear_connection() -> None:
   _connection.set( None )


def with_db_connection(
      handler: Callable[ ..., Any ] ) -> Callable[ ..., Any ]:
   @wraps( handler )
   def wrapped( self: Any, *args: Any, **kwargs: Any ) -> Any:
      conn = connection.open_connection()

      try:
         set_connection( conn )
         return handler( self, *args, **kwargs )
      finally:
         connection.close_connection( conn )
         clear_connection()

   return wrapped
