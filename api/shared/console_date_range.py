from .. import database as database_module
from ..zoo_util import ZooUtil
from .date_range import DateRange


def resolve_open_ended_console_date_range( start_date, end_date ):
   if not start_date:
      start_date = database_module.datetime.now().date().isoformat()

   return DateRange(
      start_date=ZooUtil.normalize_date_key( start_date ),
      end_date=ZooUtil.normalize_date_key( end_date ) )
