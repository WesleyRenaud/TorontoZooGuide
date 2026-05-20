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

   if not zoo.ZooUtil.is_date_range_ordered(
         start_date_value=start_date,
         end_date_value=end_date ):
      return None

   return UpdateCreateInput(
      title=title,
      description=description,
      update_type=normalized_update_type,
      start_date=start_date,
      end_date=end_date )
