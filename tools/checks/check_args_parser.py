from __future__ import annotations

import argparse
from pathlib import Path

from .paths import Paths


class CheckArgsParser():
   @classmethod
   def parse( cls, description: str ) -> argparse.Namespace:
      parser = argparse.ArgumentParser( description=description )
      parser.add_argument(
         '--database',
         type=Path,
         default=Paths.DATABASE,
         help='Path to animals.db. The file is opened read-only.',
      )
      return parser.parse_args()
