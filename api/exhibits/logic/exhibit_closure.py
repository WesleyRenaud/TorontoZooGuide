from ... import zoo


def is_exhibit_closure_active_on_visit_date(
      is_closed,
      closed_start,
      closed_end,
      target_date ):
   if not is_closed or target_date is None:
      return False

   return zoo.ZooUtil.is_date_in_range(
      target_date=target_date,
      start_date_value=closed_start,
      end_date_value=closed_end )


def exhibit_names_closed_on_visit_date( closure_records, target_date ):
   return [
      record.exhibit
      for record in closure_records
      if is_exhibit_closure_active_on_visit_date(
         True,
         record.closed_start,
         record.closed_end,
         target_date )
   ]
