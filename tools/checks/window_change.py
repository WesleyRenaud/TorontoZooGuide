from __future__ import annotations

from enum import Enum


class WindowChange( str, Enum ):
   EXTENDED = 'extended'
   SET = 'set'
   TRIMMED = 'trimmed'
