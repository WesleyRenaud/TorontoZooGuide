from __future__ import annotations

from typing import Any

from ..data_access.itinerary_provider import ItineraryProvider
from ..data_access.itinerary_save_input import ItinerarySaveInput
from ..results.itinerary_save_result import ItinerarySaveResult
from .set_itinerary_context import build_set_itinerary_error_result
from ...shared.enums import ItineraryErrorType
from ...types import Connection
from ..validation.fixed_zoo_schedule_start_times_builder import FixedZooScheduleStartTimesBuilder
from ..validation.itinerary_arrival_time_validator import ItineraryArrivalTimeValidator
from ..validation.itinerary_departure_time_validator import ItineraryDepartureTimeValidator
from ...zoo_hours.data_access.zoo_hours_provider import ZooHoursProvider


def validate_set_itinerary_zoo_hours(
      conn: Connection,
      save_input: ItinerarySaveInput,
      itinerary_controller_kwargs: dict[ str, Any ] ) -> ItinerarySaveResult | None:
   if (
         save_input.arrival_time is None
         or save_input.departure_time is None
   ):
      return None

   zoo_hours_record = ZooHoursProvider.fetch_zoo_hours_record(
      conn,
      save_input.date.isoformat() )
   fixed_zoo_start_times = FixedZooScheduleStartTimesBuilder.merge(
      FixedZooScheduleStartTimesBuilder.from_save_input( save_input ),
      FixedZooScheduleStartTimesBuilder.from_saved_itinerary(
         ItineraryProvider.fetch_saved_itinerary( conn ) ) )

   arrival_time_error = ItineraryArrivalTimeValidator.validate_for_zoo_hours(
      save_input.arrival_time,
      zoo_hours_record,
      departure_time=save_input.departure_time,
      fixed_zoo_start_times=fixed_zoo_start_times )

   if arrival_time_error != ItineraryErrorType.SUCCESS:
      return build_set_itinerary_error_result(
         conn,
         arrival_time_error,
         itinerary_controller_kwargs )

   departure_time_error = ItineraryDepartureTimeValidator.validate_for_zoo_hours(
      save_input.departure_time,
      zoo_hours_record,
      arrival_time=save_input.arrival_time )

   if departure_time_error != ItineraryErrorType.SUCCESS:
      return build_set_itinerary_error_result(
         conn,
         departure_time_error,
         itinerary_controller_kwargs )

   return None
