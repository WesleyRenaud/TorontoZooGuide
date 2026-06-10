from __future__ import annotations

import sys

from .server import DEFAULT_PORT
from .server import run_server


if __name__ == '__main__':
   port = int( sys.argv[ 1 ] ) if len( sys.argv ) > 1 else DEFAULT_PORT
   run_server( port )
