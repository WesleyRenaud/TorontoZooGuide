import contextvars


_connection = contextvars.ContextVar( 'connection', default=None )


def set_connection( conn ):
   _connection.set( conn )


def get_connection():
   return _connection.get()


def clear_connection():
   _connection.set( None )
