from ..data_access.restroom import fetch_restroom_records
from ..logic.restroom import build_restrooms
from ..logic.restroom import resolve_restroom_context
from ..logic.restrooms_matching_query import build_restrooms_matching_query


class RestroomController():
   def __init__( self, conn ):
      self._conn = conn


   def get_restrooms(
         self,
         day,
         month,
         year,
         include_closed_restrooms=False ):

      return build_restrooms(
         restroom_records=fetch_restroom_records( self._conn ),
         context=resolve_restroom_context(
            day=day,
            month=month,
            year=year ),
         include_closed_restrooms=include_closed_restrooms )


   def get_restrooms_matching_query(
         self,
         query,
         day,
         month,
         year,
         include_closed_restrooms ):

      restrooms = self.get_restrooms(
         day=day,
         month=month,
         year=year,
         include_closed_restrooms=include_closed_restrooms )

      return build_restrooms_matching_query(
         restrooms,
         query )
