from ... import zoo
from ..data_access.exhibit import fetch_animal_names_in_exhibit
from ..data_access.exhibit import fetch_exhibit_names_in_region
from ..data_access.exhibit import fetch_region_exhibit_rows
from ..data_access.exhibit_closure import fetch_exhibit_closure_records
from ..logic.exhibit import build_region_options
from ..logic.exhibit_closure import exhibit_names_closed_on_visit_date


class ExhibitController():
   def __init__( self, conn ):
      self._conn = conn


   def get_exhibits_in_region( self, region ):
      return fetch_exhibit_names_in_region(
         self._conn,
         region=region )


   def get_regions( self ):
      return build_region_options(
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
