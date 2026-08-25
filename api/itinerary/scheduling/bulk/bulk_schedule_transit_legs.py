from __future__ import annotations

from .animals_for_bulk_schedule import transit_transportations_for_bulk_schedule
from .bulk_schedule_window_prep import BulkScheduleWindowPrep
from ..core.guest_item_schedule_status import has_itinerary_schedule_times
from ...data_access.itinerary import fetch_saved_itinerary
from .transportation_transit_rides import apply_transportation_transit_rides
from ....types import Connection


def apply_bulk_schedule_transit_legs(
      conn: Connection,
      *,
      prep: BulkScheduleWindowPrep ) -> None:
   saved_after_pack = fetch_saved_itinerary( conn )
   apply_transportation_transit_rides(
      conn,
      transit_rows=transit_transportations_for_bulk_schedule( saved_after_pack ),
      scheduled_animals=[
         animal_row
         for animal_row in saved_after_pack.animal_rows
         if has_itinerary_schedule_times(
            animal_row.start_time,
            animal_row.end_time )
      ],
      visit_date=prep.visit_date,
      schedule_anchor_seconds=prep.start_state.schedule_anchor_seconds,
      zoo_operating_hours=prep.zoo_operating_hours )
