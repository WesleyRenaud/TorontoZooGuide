from __future__ import annotations

import sys

from .server_runner import ServerRunner


if __name__ == '__main__':
   port = int( sys.argv[ 1 ] ) if len( sys.argv ) > 1 else ServerRunner.DEFAULT_PORT
   ServerRunner.run( port )
