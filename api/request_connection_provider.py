from __future__ import annotations

from collections.abc import Callable
import contextvars
from functools import wraps
from typing import Any
from typing import ClassVar

from .database_connection_provider import DatabaseConnectionProvider
from .types import Types


class RequestConnectionProvider():
   _connection: ClassVar[ contextvars.ContextVar[ Types.Connection | None ] ] = (
      contextvars.ContextVar( 'connection', default=None ) )


   @classmethod
   def set( cls, conn: Types.Connection | None ) -> None:
      cls._connection.set( conn )


   @classmethod
   def get( cls ) -> Types.Connection | None:
      return cls._connection.get()


   @classmethod
   def clear( cls ) -> None:
      cls._connection.set( None )


   @classmethod
   def with_db_connection(
         cls,
         handler: Callable[ ..., Any ] ) -> Callable[ ..., Any ]:
      @wraps( handler )
      def wrapped( self: Any, *args: Any, **kwargs: Any ) -> Any:
         conn = DatabaseConnectionProvider.open()

         try:
            cls.set( conn )
            return handler( self, *args, **kwargs )
         finally:
            DatabaseConnectionProvider.close( conn )
            cls.clear()

      return wrapped
