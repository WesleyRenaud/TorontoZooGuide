from ... import zoo


def map_defibrillator_record( row ):
   return zoo.Defibrillator(
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ] )



def map_defibrillator_records( rows ):
   return [
      map_defibrillator_record( row )
      for row in rows
   ]
