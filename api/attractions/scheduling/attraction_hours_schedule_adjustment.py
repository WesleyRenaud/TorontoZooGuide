from __future__ import annotations

from enum import Enum


class AttractionHoursScheduleAdjustment( str, Enum ):
   BEFORE_OPEN = 'beforeOpen'
   AFTER_CLOSE = 'afterClose'
