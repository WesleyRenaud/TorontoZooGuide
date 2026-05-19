from ... import zoo


def drinking_fountain_status_applies_to_date( status_record, target_date ):
   if status_record is None:
      return False

   return zoo.ZooUtil.is_date_in_range(
      target_date=target_date,
      start_date_value=status_record.start_date,
      end_date_value=status_record.end_date )



def build_drinking_fountain_status( status_record ):
   closed_message = status_record.closed_message
   likelihood = 0.0 if status_record.is_closed else 1.0

   return status_record.is_closed, closed_message, likelihood



def build_drinking_fountain_seasonal_status( likelihood ):
   is_closed = likelihood <= 0

   return is_closed, None, likelihood
