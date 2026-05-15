from .restroom_record import RestroomRecord


def map_restroom_record( row ):
   return RestroomRecord(
      title=row[ 'TITLE' ],
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ],
      is_closed=row[ 'IS_CLOSED' ],
      closed_message=row[ 'CLOSED_MESSAGE' ],
      closed_start=row[ 'CLOSED_START' ],
      closed_end=row[ 'CLOSED_END' ],
      alert_message=row[ 'ALERT_MESSAGE' ],
      alert_start_date=row[ 'ALERT_START_DATE' ],
      alert_end_date=row[ 'ALERT_END_DATE' ] )


def map_restroom_records( rows ):
   return [
      map_restroom_record( row )
      for row in rows
   ]
