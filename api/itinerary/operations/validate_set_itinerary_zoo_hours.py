from __future__ import annotations

from typing import Any

from ..data_access.itinerary_provider import ItineraryProvider
from ..data_access.itinerary_save_input import ItinerarySaveInput
from ..results.itinerary_save_result import ItinerarySaveResult
from .set_itinerary_context import build_set_itinerary_error_result
from ...shared.enums import ItineraryErrorType
from ...types import Connection
from ..validation.fixed_zoo_schedule_start_times import fixed_zoo_schedule_start_times_from_save_input
from ..validation.fixed_zoo_schedule_start_times import fixed_zoo_schedule_start_times_from_saved_itinerary
from ..validation.fixed_zoo_schedule_start_times import merge_fixed_zoo_schedule_start_times
from ..validation.itinerary_arrival_time_validation import arrival_time_is_valid_for_zoo_hours
from ..validation.itinerary_departure_time_validation import departure_time_is_valid_for_zoo_hours
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
   fixed_zoo_start_times = merge_fixed_zoo_schedule_start_times(
      fixed_zoo_schedule_start_times_from_save_input( save_input ),
      fixed_zoo_schedule_start_times_from_saved_itinerary(
         ItineraryProvider.fetch_saved_itinerary( conn ) ) )

   arrival_time_error = arrival_time_is_valid_for_zoo_hours(
      save_input.arrival_time,
      zoo_hours_record,
      departure_time=save_input.departure_time,
      fixed_zoo_start_times=fixed_zoo_start_times )

   if arrival_time_error != ItineraryErrorType.SUCCESS:
      return build_set_itinerary_error_result(
         conn,
         arrival_time_error,
         itinerary_controller_kwargs )

   departure_time_error = departure_time_is_valid_for_zoo_hours(
      save_input.departure_time,
      zoo_hours_record,
      arrival_time=save_input.arrival_time )

   if departure_time_error != ItineraryErrorType.SUCCESS:
      return build_set_itinerary_error_result(
         conn,
         departure_time_error,
         itinerary_controller_kwargs )

   return None
