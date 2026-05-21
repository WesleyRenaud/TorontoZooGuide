from ... import zoo
from .update_end_input import UpdateEndInput


def build_update_end_input( title, start_date, end_date ):
   if not end_date:
      end_date = zoo.ZooUtil.today_date_key()

   return UpdateEndInput(
      title=title,
      start_date=start_date,
      end_date=end_date )
