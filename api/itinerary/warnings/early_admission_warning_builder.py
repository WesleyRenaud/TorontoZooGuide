from __future__ import annotations

from ..data_access.itinerary_status_provider import ItineraryStatusProvider
from .itinerary_suppressed_warnings_builder import ItinerarySuppressedWarningsBuilder
from ...shared.calendar_dates import DateValues
from ...shared.enums import ItineraryErrorType
from ...types import Connection, ScheduleTimeKey
from ...zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


class EarlyAdmissionWarningBuilder():
   @classmethod
   def arrival_is_during_early_admission(
         cls,
         arrival_time: ScheduleTimeKey,
         zoo_hours_record: ZooHoursRecord | None ) -> bool:
      if zoo_hours_record is None or zoo_hours_record.early_admission_time is None:
         return False

      arrival_seconds = DateValues.time_value_in_seconds( arrival_time )
      early_admission_seconds = DateValues.time_value_in_seconds(
         zoo_hours_record.early_admission_time )
      open_seconds = DateValues.time_value_in_seconds( zoo_hours_record.open_time )

      if (
            arrival_seconds is None
            or early_admission_seconds is None
            or open_seconds is None ):
         return False

      return early_admission_seconds <= arrival_seconds < open_seconds


   @classmethod
   def is_required(
         cls,
         conn: Connection,
         arrival_time: ScheduleTimeKey,
         zoo_hours_record: ZooHoursRecord | None,
         *,
         confirming_early_admission: bool,
         suppressed_warnings: list[ ItineraryErrorType ] | None = None ) -> bool:
      if confirming_early_admission:
         return False

      if ItineraryStatusProvider.is_itinerary_error_suppressed(
            conn,
            ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP ):
         if suppressed_warnings is not None:
            ItinerarySuppressedWarningsBuilder.append_suppressed_warning(
               suppressed_warnings,
               ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP )

         return False

      return cls.arrival_is_during_early_admission(
         arrival_time,
         zoo_hours_record )
