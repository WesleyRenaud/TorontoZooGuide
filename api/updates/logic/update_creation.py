from ... import zoo
from .update_create_input import UpdateCreateInput
from .update_type import normalize_update_type


def build_update_create_input(
      title,
      description,
      update_type,
      start_date,
      end_date ):
   normalized_update_type = normalize_update_type( update_type )
   date_range = zoo.ZooUtil.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not zoo.ZooUtil.is_date_range_ordered(
         start_date_value=date_range.start_date,
         end_date_value=date_range.end_date ):
      return None

   return UpdateCreateInput(
      title=title,
      description=description,
      update_type=normalized_update_type,
      start_date=date_range.start_date,
      end_date=date_range.end_date )
