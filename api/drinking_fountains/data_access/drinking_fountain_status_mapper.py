from .drinking_fountain_status_record import DrinkingFountainStatusRecord


def map_drinking_fountain_status_record( row ):
   return DrinkingFountainStatusRecord(
      is_closed=row[ 'IS_CLOSED' ],
      start_date=row[ 'START_DATE' ],
      end_date=row[ 'END_DATE' ],
      closed_message=row[ 'CLOSED_MESSAGE' ] )
