from __future__ import annotations

from dataclasses import replace

from ..data_access.itinerary_provider import ItineraryProvider
from ..data_access.itinerary_save_input import ItinerarySaveInput
from ..data_access.saved_itinerary import SavedItinerary
from ..domain.itinerary_adjustment import ItineraryAdjustment
from ..domain.itinerary_adjustment_reason import ItineraryAdjustmentReason
from ..domain.itinerary_adjustment_type import ItineraryAdjustmentType
from ...shared.calendar_dates import DateValues
from ...types import Connection
from ..validation.itinerary_arrival_time_validator import ItineraryArrivalTimeValidator
from ...zoo_hours.data_access.zoo_hours_provider import ZooHoursProvider
from ...zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


class ItinerarySaveRestrictiveHoursAdjuster():
   @classmethod
   def adjust(
         cls,
         conn: Connection,
         save_input: ItinerarySaveInput,
         *,
         old_visit_date: str | None ) -> tuple[
            ItinerarySaveInput,
            list[ ItineraryAdjustment ],
         ]:
      if old_visit_date == save_input.date.isoformat():
         return ( save_input, [] )

      zoo_hours_record = ZooHoursProvider.fetch_zoo_hours_record(
         conn,
         save_input.date.isoformat() )
      saved_itinerary = (
         ItineraryProvider.fetch_saved_itinerary( conn )
         if old_visit_date is not None
         else None )
      adjustments: list[ ItineraryAdjustment ] = []
      updated_input = save_input

      arrival_adjustment = cls._arrival_adjustment(
         updated_input,
         saved_itinerary,
         zoo_hours_record )

      if arrival_adjustment is not None:
         adjustments.append( arrival_adjustment )
         updated_input = replace(
            updated_input,
            arrival_time=arrival_adjustment.value )

      departure_adjustment = cls._departure_adjustment(
         updated_input,
         saved_itinerary,
         zoo_hours_record )

      if departure_adjustment is not None:
         adjustments.append( departure_adjustment )
         updated_input = replace(
            updated_input,
            departure_time=departure_adjustment.value )

      return ( updated_input, adjustments )


   @classmethod
   def _arrival_adjustment(
         cls,
         save_input: ItinerarySaveInput,
         saved_itinerary: SavedItinerary | None,
         zoo_hours_record: ZooHoursRecord ) -> ItineraryAdjustment | None:
      if (
            save_input.arrival_time is None
            or saved_itinerary is None
            or saved_itinerary.arrival_time != save_input.arrival_time
      ):
         return None

      arrival_minutes = DateValues.time_value_in_minutes( save_input.arrival_time )
      earliest_time = ItineraryArrivalTimeValidator.earliest_arrival_time(
         zoo_hours_record )
      earliest_minutes = DateValues.time_value_in_minutes( earliest_time )
      last_admission_minutes = DateValues.time_value_in_minutes(
         zoo_hours_record.last_admission_time )

      adjusted_arrival_time: str | None = None

      if arrival_minutes < earliest_minutes:
         adjusted_arrival_time = earliest_time
      elif arrival_minutes > last_admission_minutes:
         adjusted_arrival_time = zoo_hours_record.last_admission_time

      if (
            adjusted_arrival_time is None
            or adjusted_arrival_time == save_input.arrival_time ):
         return None

      return ItineraryAdjustment(
         type=ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED,
         field='arrivalTime',
         previous_value=save_input.arrival_time,
         value=adjusted_arrival_time,
         reason=ItineraryAdjustmentReason.ARRIVAL_OUTSIDE_ADMISSION_HOURS )


   @classmethod
   def _departure_adjustment(
         cls,
         save_input: ItinerarySaveInput,
         saved_itinerary: SavedItinerary | None,
         zoo_hours_record: ZooHoursRecord ) -> ItineraryAdjustment | None:
      if (
            save_input.departure_time is None
            or saved_itinerary is None
            or saved_itinerary.departure_time != save_input.departure_time
      ):
         return None

      departure_minutes = DateValues.time_value_in_minutes(
         save_input.departure_time )
      open_minutes = DateValues.time_value_in_minutes( zoo_hours_record.open_time )
      close_minutes = DateValues.time_value_in_minutes( zoo_hours_record.close_time )

      adjusted_departure_time: str | None = None

      if departure_minutes < open_minutes:
         adjusted_departure_time = zoo_hours_record.open_time
      elif departure_minutes > close_minutes:
         adjusted_departure_time = zoo_hours_record.close_time

      if (
            adjusted_departure_time is None
            or adjusted_departure_time == save_input.departure_time ):
         return None

      return ItineraryAdjustment(
         type=ItineraryAdjustmentType.DEPARTURE_TIME_ADJUSTED,
         field='departureTime',
         previous_value=save_input.departure_time,
         value=adjusted_departure_time,
         reason=ItineraryAdjustmentReason.DEPARTURE_OUTSIDE_OPERATING_HOURS )
