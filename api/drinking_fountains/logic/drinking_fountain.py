from ... import zoo


def drinking_fountain_record_to_model( record, is_closed, closed_message, likelihood ):
   return zoo.DrinkingFountain(
      x_coord=record.x_coord,
      y_coord=record.y_coord,
      is_closed=is_closed,
      closed_message=closed_message if is_closed else None,
      likelihood=likelihood )



def build_drinking_fountains( fountain_records, is_closed, closed_message, likelihood ):
   return [
      drinking_fountain_record_to_model(
         record,
         is_closed,
         closed_message,
         likelihood )
      for record in fountain_records
   ]
