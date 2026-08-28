from __future__ import annotations

from .bulk_schedule_stop_selector import BulkScheduleStopSelector
from .bulk_schedule_window_prep import BulkScheduleWindowPrep
from ..core.guest_item_schedule_status_checker import GuestItemScheduleStatusChecker
from ...data_access.itinerary_provider import ItineraryProvider
from .transportation_transit_ride_applier import TransportationTransitRideApplier
from ....types import Types


class BulkScheduleTransitLegsBuilder():
   @classmethod
   def apply(
         cls,
         conn: Types.Connection,
         *,
         prep: BulkScheduleWindowPrep ) -> None:
      saved_after_pack = ItineraryProvider.fetch_saved_itinerary( conn )
      TransportationTransitRideApplier.apply(
         conn,
         transit_rows=BulkScheduleStopSelector.transit_transportations(
            saved_after_pack ),
         scheduled_animals=[
            animal_row
            for animal_row in saved_after_pack.animal_rows
            if GuestItemScheduleStatusChecker.has_schedule_times(
               animal_row.start_time,
               animal_row.end_time )
         ],
         visit_date=prep.visit_date,
         schedule_anchor_seconds=prep.start_state.schedule_anchor_seconds,
         zoo_operating_hours=prep.zoo_operating_hours )
