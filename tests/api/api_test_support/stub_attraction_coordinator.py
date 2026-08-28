from __future__ import annotations

from typing import Any

from api.attractions.scheduling.attraction_hours_schedule_time_bounds import AttractionHoursScheduleTimeBounds
from api.models.attraction import Attraction


class StubAttractionCoordinator():
   instances: list[ StubAttractionCoordinator ] = []
   default_success: bool = True
   raise_time_bounds_error: bool = False
   raise_hours_schedule_error: bool = False


   def __init__(
         self,
         *,
         attraction_names: list[ str ],
         attractions: list[ Attraction ],
         hours_time_bounds: AttractionHoursScheduleTimeBounds | None ) -> None:
      self.attraction_names = attraction_names
      self.attractions = attractions
      self.hours_time_bounds = hours_time_bounds
      self.calls: list[ tuple[ str, dict[ str, Any ] ] ] = []
      self.closed = False
      StubAttractionCoordinator.instances.append( self )


   def close( self ) -> None:
      self.closed = True


   def get_attraction_names( self ) -> list[ str ]:
      self.calls.append( ( 'get_attraction_names', {} ) )
      return list( self.attraction_names )


   def get_attractions(
         self,
         *,
         day: int,
         month: str,
         year: int,
         include_closed_attractions: bool = False ) -> list[ Attraction ]:
      self.calls.append(
         (
            'get_attractions',
            {
               'day': day,
               'month': month,
               'year': year,
               'include_closed_attractions': include_closed_attractions,
            }
         )
      )
      return list( self.attractions )


   def set_attraction_as_closed( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_attraction_as_closed', kwargs ) )
      return StubAttractionCoordinator.default_success


   def set_attraction_closure_override( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_attraction_closure_override', kwargs ) )
      return StubAttractionCoordinator.default_success


   def set_attraction_opening_schedule( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_attraction_opening_schedule', kwargs ) )
      return StubAttractionCoordinator.default_success


   def replace_attraction_opening_schedule_overlaps( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'replace_attraction_opening_schedule_overlaps', kwargs ) )
      return StubAttractionCoordinator.default_success


   def trim_attraction_opening_schedule_overlaps( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'trim_attraction_opening_schedule_overlaps', kwargs ) )
      return StubAttractionCoordinator.default_success


   def get_attraction_hours_schedule_time_bounds(
         self,
         *,
         start_date: str | None = None,
         end_date: str | None = None ) -> AttractionHoursScheduleTimeBounds:
      self.calls.append(
         (
            'get_attraction_hours_schedule_time_bounds',
            {
               'start_date': start_date,
               'end_date': end_date,
            }
         )
      )
      if StubAttractionCoordinator.raise_time_bounds_error:
         raise ValueError( 'No zoo hours found for the selected date range.' )

      assert self.hours_time_bounds is not None
      return self.hours_time_bounds


   def set_attraction_hours_schedule( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_attraction_hours_schedule', kwargs ) )
      if StubAttractionCoordinator.raise_hours_schedule_error:
         raise ValueError( 'Attraction hours must fall within regular zoo hours.' )
      return StubAttractionCoordinator.default_success


   def replace_attraction_hours_schedule_overlaps( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'replace_attraction_hours_schedule_overlaps', kwargs ) )
      if StubAttractionCoordinator.raise_hours_schedule_error:
         raise ValueError( 'Attraction hours must fall within regular zoo hours.' )
      return StubAttractionCoordinator.default_success


   def trim_attraction_hours_schedule_overlaps( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'trim_attraction_hours_schedule_overlaps', kwargs ) )
      if StubAttractionCoordinator.raise_hours_schedule_error:
         raise ValueError( 'Attraction hours must fall within regular zoo hours.' )
      return StubAttractionCoordinator.default_success
