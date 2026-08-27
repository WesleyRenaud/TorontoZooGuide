from __future__ import annotations

from typing import Any

from ..core.scheduling_anchor import scheduling_anchor_seconds_covering_fixed_zoo_starts
from ..core.scheduling_anchor import scheduling_day_end_seconds
from ...data_access.itinerary_provider import ItineraryProvider
from ...data_access.itinerary_status_provider import ItineraryStatusProvider
from ...data_access.saved_itinerary import SavedItinerary
from .itinerary_save_result_builder import ItinerarySaveResultBuilder
from .prepared_schedule_window import PreparedScheduleWindow
from ...results.itinerary_save_result import ItinerarySaveResult
from ....shared.calendar_dates import DateValues
from ....shared.enums import ItineraryErrorType
from ....types import Connection
from ....types import ScheduleTimeKey
from ...validation.fixed_zoo_schedule_start_times_builder import FixedZooScheduleStartTimesBuilder
from ....zoo_hours.data_access.zoo_hours_provider import ZooHoursProvider
from ....zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


class ScheduleWindowPreparer():
   @classmethod
   def prepare(
         cls,
         conn: Connection,
         saved_itinerary: SavedItinerary,
         **itinerary_context: Any ) -> PreparedScheduleWindow | ItinerarySaveResult:
      visit_date = ItineraryProvider.fetch_itinerary_date( conn )

      if visit_date is None:
         return ItinerarySaveResultBuilder.save_result(
            conn,
            ItineraryErrorType.ITINERARY_DATE_NOT_SET,
            **itinerary_context )

      parsed_visit_date = DateValues.parse_date_value( visit_date )

      if parsed_visit_date is None:
         return ItinerarySaveResultBuilder.save_result(
            conn,
            ItineraryErrorType.ITINERARY_DATE_NOT_SET,
            **itinerary_context )

      zoo_hours_record = ZooHoursProvider.fetch_zoo_hours_record( conn, visit_date )
      zoo_operating_hours_value = (
         None
         if zoo_hours_record is None
         else zoo_hours_record.operating_hours() )
      allow_early_admission = cls._early_admission_allowed( conn )

      fixed_zoo_start_times = FixedZooScheduleStartTimesBuilder.from_saved_itinerary(
         saved_itinerary )
      anchor_seconds = scheduling_anchor_seconds_covering_fixed_zoo_starts(
         zoo_hours_record,
         saved_itinerary.arrival_time,
         fixed_zoo_start_times,
         allow_early_admission=allow_early_admission )
      day_end_seconds = scheduling_day_end_seconds(
         zoo_hours_record,
         saved_itinerary.departure_time )

      if anchor_seconds is None or day_end_seconds is None:
         return ItinerarySaveResultBuilder.save_result(
            conn,
            ItineraryErrorType.SCHEDULE_WINDOW_UNAVAILABLE,
            **itinerary_context )

      return PreparedScheduleWindow(
         saved_itinerary=saved_itinerary,
         window=( anchor_seconds, day_end_seconds ),
         visit_date=parsed_visit_date,
         zoo_operating_hours=zoo_operating_hours_value )


   @classmethod
   def prepare_zoo_hours(
         cls,
         conn: Connection,
         saved_itinerary: SavedItinerary,
         **itinerary_context: Any ) -> PreparedScheduleWindow | ItinerarySaveResult:
      visit_date = ItineraryProvider.fetch_itinerary_date( conn )

      if visit_date is None:
         return ItinerarySaveResultBuilder.save_result(
            conn,
            ItineraryErrorType.ITINERARY_DATE_NOT_SET,
            **itinerary_context )

      parsed_visit_date = DateValues.parse_date_value( visit_date )

      if parsed_visit_date is None:
         return ItinerarySaveResultBuilder.save_result(
            conn,
            ItineraryErrorType.ITINERARY_DATE_NOT_SET,
            **itinerary_context )

      zoo_hours_record = ZooHoursProvider.fetch_zoo_hours_record( conn, visit_date )
      zoo_operating_hours_value = (
         None
         if zoo_hours_record is None
         else zoo_hours_record.operating_hours() )
      allow_early_admission = cls._early_admission_allowed( conn )

      window = cls.zoo_hours_window_seconds(
         zoo_hours_record,
         fixed_zoo_start_times=(
            FixedZooScheduleStartTimesBuilder.from_saved_itinerary( saved_itinerary ) ),
         allow_early_admission=allow_early_admission )

      if window is None:
         return ItinerarySaveResultBuilder.save_result(
            conn,
            ItineraryErrorType.SCHEDULE_WINDOW_UNAVAILABLE,
            **itinerary_context )

      return PreparedScheduleWindow(
         saved_itinerary=saved_itinerary,
         window=window,
         visit_date=parsed_visit_date,
         zoo_operating_hours=zoo_operating_hours_value )


   @classmethod
   def zoo_hours_window_seconds(
         cls,
         zoo_hours_record: ZooHoursRecord | None,
         *,
         fixed_zoo_start_times: list[ ScheduleTimeKey ] | None = None,
         allow_early_admission: bool = False ) -> tuple[ int, int ] | None:
      anchor_seconds = scheduling_anchor_seconds_covering_fixed_zoo_starts(
         zoo_hours_record,
         None,
         fixed_zoo_start_times,
         allow_early_admission=allow_early_admission )
      day_end_seconds = scheduling_day_end_seconds( zoo_hours_record, None )

      if anchor_seconds is None or day_end_seconds is None:
         return None

      return ( anchor_seconds, day_end_seconds )


   @classmethod
   def _early_admission_allowed( cls, conn: Connection ) -> bool:
      return ItineraryStatusProvider.is_itinerary_error_suppressed(
         conn,
         ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP )
