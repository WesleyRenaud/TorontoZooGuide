from ... import zoo
from ..data_access.exhibit import fetch_animal_names_in_exhibit
from ..data_access.exhibit import fetch_exhibit_names
from ..data_access.exhibit import fetch_exhibit_names_in_region
from ..data_access.exhibit import fetch_region_exhibit_rows
from ..data_access.exhibit_closure import fetch_exhibit_closure_records
from ..data_access.exhibit_closure import save_exhibit_closed_status
from ..data_access.exhibit_closure import save_exhibit_open_status
from ..logic.exhibit import build_region_options
from ..logic.exhibit_closure import exhibit_names_closed_on_visit_date
from ..logic.exhibit_status import build_exhibit_closed_status
from ..logic.regions_with_exhibits import build_regions_with_exhibits
from ...shared.console_date_range import resolve_open_ended_console_date_range


class ExhibitController():
   def __init__( self, conn ):
      self._conn = conn


   def get_exhibits_in_region( self, region ):
      return fetch_exhibit_names_in_region(
         self._conn,
         region=region )


   def get_exhibits( self ):
      return fetch_exhibit_names( self._conn )


   def get_regions( self ):
      return build_region_options(
         fetch_region_exhibit_rows( self._conn ) )


   def get_regions_with_exhibits( self ):
      return build_regions_with_exhibits(
         fetch_region_exhibit_rows( self._conn ) )


   def get_names_of_animals_in_exhibit( self, exhibit ):
      return fetch_animal_names_in_exhibit(
         self._conn,
         exhibit=exhibit )


   def get_closed_exhibits_for_visit_date( self, month, day, year ):
      target_date = zoo.ZooUtil.visit_target_date(
         month=month,
         day=day,
         year=year )

      return exhibit_names_closed_on_visit_date(
         fetch_exhibit_closure_records( self._conn ),
         target_date )


   def set_exhibit_as_closed( self, exhibit, start_date, end_date, message ):
      status = build_exhibit_closed_status(
         exhibit=exhibit,
         start_date=start_date,
         end_date=end_date,
         message=message )

      return save_exhibit_closed_status(
         self._conn,
         exhibit=status.exhibit,
         start_date=status.start_date,
         end_date=status.end_date,
         message=status.message )


   def set_exhibit_as_open( self, exhibit, start_date, end_date ):
      date_range = resolve_open_ended_console_date_range(
         start_date=start_date,
         end_date=end_date )

      return save_exhibit_open_status(
         self._conn,
         exhibit=exhibit,
         start_date=date_range.start_date,
         end_date=date_range.end_date )
