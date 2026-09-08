from __future__ import annotations

import sys

from .server_runner import ServerRunner
from .shared.enums.position import Position


if __name__ == '__main__':
   port = int( sys.argv[ Position.SECOND ] ) if len( sys.argv ) > 1 else ServerRunner.DEFAULT_PORT
   ServerRunner.run( port )
