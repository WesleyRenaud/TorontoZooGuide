from ..data_access.restroom import fetch_restroom_records
from ..logic.restroom import build_restrooms
from ..logic.restroom import resolve_restroom_context


class RestroomController():
   def __init__( self, conn ):
      self._conn = conn


   def get_restrooms(
         self,
         month=None,
         day=None,
         include_closed_restrooms=False ):

      return build_restrooms(
         restroom_records=fetch_restroom_records( self._conn ),
         context=resolve_restroom_context(
            month=month,
            day=day ),
         include_closed_restrooms=include_closed_restrooms )
