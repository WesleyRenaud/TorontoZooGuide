import contextvars

from .types import Connection


_connection = contextvars.ContextVar( 'connection', default=None )


def set_connection( conn: Connection | None ) -> None:
   _connection.set( conn )


def get_connection() -> Connection | None:
   return _connection.get()


def clear_connection() -> None:
   _connection.set( None )
