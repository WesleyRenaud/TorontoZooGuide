from __future__ import annotations

from enum import IntEnum


class CheckExitCode( IntEnum ):
   CLEAR = 0
   DIFFERENCES = 1
   COULD_NOT_FINISH = 2
