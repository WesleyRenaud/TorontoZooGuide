from __future__ import annotations

from enum import Enum


class ItineraryAdjustmentReason( str, Enum ):
   ARRIVAL_OUTSIDE_ADMISSION_HOURS = 'arrivalOutsideAdmissionHours'
   DEPARTURE_OUTSIDE_OPERATING_HOURS = 'departureOutsideOperatingHours'
   BULK_SCHEDULE_CONSECUTIVE_PACKING = 'bulkScheduleConsecutivePacking'
