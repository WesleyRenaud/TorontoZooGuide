from ... import zoo
from .update_edit_input import UpdateEditInput
from .update_type import normalize_update_type


def build_update_edit_input(
      title,
      start_date,
      description,
      update_type,
      end_date ):
   normalized_end_date = None

   if end_date != None:
      normalized_end_date = zoo.ZooUtil.normalize_date_key( end_date )

   return UpdateEditInput(
      title=title,
      start_date=start_date,
      description=description,
      update_type=normalize_update_type( update_type ),
      end_date=normalized_end_date )
