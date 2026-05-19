from ... import zoo


def map_emergency_intercom_record( row ):
   return zoo.EmergencyIntercom(
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ] )



def map_emergency_intercom_records( rows ):
   return [
      map_emergency_intercom_record( row )
      for row in rows
   ]
