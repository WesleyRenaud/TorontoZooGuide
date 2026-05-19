from .drinking_fountain_record import DrinkingFountainRecord


def map_drinking_fountain_record( row ):
   return DrinkingFountainRecord(
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ] )



def map_drinking_fountain_records( rows ):
   return [
      map_drinking_fountain_record( row )
      for row in rows
   ]
