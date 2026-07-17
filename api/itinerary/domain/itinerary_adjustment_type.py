from __future__ import annotations

from enum import Enum


class ItineraryAdjustmentType( str, Enum ):
   ARRIVAL_TIME_ADJUSTED = 'arrivalTimeAdjusted'
   DEPARTURE_TIME_ADJUSTED = 'departureTimeAdjusted'
